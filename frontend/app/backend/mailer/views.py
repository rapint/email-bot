from django.shortcuts import render
from django.core.mail import EmailMessage, get_connection
from .models import EmailAccount
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import datetime
from gspread_formatting import CellFormat, color, format_cell_range
import threading
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__), "fresh-lens-485918-g4-2d37947e9238.json"
)

# Global log store (keeps only latest 5 logs)
GLOBAL_LOGS = []

@login_required
def get_logs(request):
    """Return last 5 logs as JSON"""
    return JsonResponse({"logs": GLOBAL_LOGS})

def add_log(msg):
    """Add message to global log (keep last 5)."""
    GLOBAL_LOGS.append(msg)
    if len(GLOBAL_LOGS) > 5:
        GLOBAL_LOGS.pop(0)

def send_emails(sheet_url, message_content, accounts):
    """Threaded function to fetch sheet and send emails."""
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url).sheet1
        data = sheet.get_all_records()  # expects columns: name, email, status
        add_log(f"✅ Fetched {len(data)} recipients from Google Sheet.")
    except Exception as e:
        add_log(f"❌ Failed to fetch sheet: {e}")
        return

    if not accounts:
        add_log("⚠️ No sender accounts available for this user.")
        return

    account_index = 0
    total_accounts = len(accounts)

    for row_index, row in enumerate(data, start=2):  # Google Sheets row 1 = header
        recipient_email = row.get("email", "").strip()
        recipient_name = row.get("name", "")
        status = row.get("status", "").strip().lower()

        if not recipient_email:
            add_log(f"⚠️ Row {row_index} skipped: missing email")
            continue

        if status == "sent":
            add_log(f"ℹ️ Row {row_index} skipped: already sent")
            continue

        # Pick the next account in rotation
        account = accounts[account_index % total_accounts]
        account_index += 1

        try:
            connection = get_connection(
                host="smtp.gmail.com",
                port=587,
                username=account.email,
                password=account.app_password,
                use_tls=True,
            )

            # Replace $name with actual recipient name
            personalized_message = message_content.replace("$name", recipient_name)

            email = EmailMessage(
                subject="AI/Full Stack Engineer for Your Team",
                body=personalized_message,
                from_email=account.email,
                to=[recipient_email],
                connection=connection,
            )
            email.send()

            # Update sheet status
            sheet.update_cell(row_index, 3, "Sent")
            fmt = CellFormat(backgroundColor=color(0.85, 1, 0.85))  # light green
            format_cell_range(sheet, f"A{row_index}:C{row_index}", fmt)

            add_log(f"✅ Sent to {recipient_email} via {account.email}")

        except Exception as exc:
            add_log(f"❌ Failed to send to {recipient_email} via {account.email}: {exc}")

        # Small delay to prevent email block
        time.sleep(5)  # reduced to 5s for faster testing, adjust as needed


@login_required
def home(request):
    """Home page and email sending view."""
    # Fetch only the logged-in user's email accounts
    accounts = list(EmailAccount.objects.filter(user=request.user))
    context = {"from_emails": accounts, "logs": GLOBAL_LOGS}

    if request.method != "POST":
        return render(request, "mailer/home.html", context)

    sheet_url = request.POST.get("sheet_url", "").strip()
    message_content = request.POST.get("generated_message", "").strip()
    schedule_time_str = request.POST.get("schedule_time", "").strip()

    # Validation
    if not sheet_url:
        add_log("⚠️ Google Sheet URL is missing.")
        context["logs"] = GLOBAL_LOGS
        return render(request, "mailer/home.html", context)

    if not message_content:
        add_log("⚠️ Message content is empty.")
        context["logs"] = GLOBAL_LOGS
        return render(request, "mailer/home.html", context)

    # Convert schedule_time
    delay_seconds = 0
    if schedule_time_str:
        try:
            schedule_time = datetime.datetime.fromisoformat(schedule_time_str)
            now = datetime.datetime.now()
            delay_seconds = max(0, (schedule_time - now).total_seconds())
        except Exception:
            add_log("⚠️ Invalid schedule time format. Sending immediately.")

    # Start background thread
    def thread_func():
        if delay_seconds > 0:
            add_log(f"⏳ Emails scheduled at {schedule_time}")
            time.sleep(delay_seconds)
        send_emails(sheet_url, message_content, accounts)

    threading.Thread(target=thread_func, daemon=True).start()

    add_log("✅ Email sending process started in background.")
    context["logs"] = GLOBAL_LOGS
    return render(request, "mailer/home.html", context)
