from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
import json
from django.http import JsonResponse
from groq import Groq
from django.views.decorators.csrf import csrf_exempt
from .models import EmailAccount
# Groq client
client = Groq(api_key="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")

@csrf_exempt
def generate_message(request):

    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        user_prompt = data.get("custom_prompt", "")
        user_resume = data.get("resume", "")

        full_prompt = f"""
            You must return ONLY valid JSON.
            No markdown. No commentary. No code blocks.
            The ONLY valid structure is:

            {{
            "subject": "string",
            "body": "string"
            }}

            RULES:
            - JSON must start with {{ and end with }}.
            - No extra keys.
            - No nested JSON.
            - No placeholders.
            - No raw blank lines.
            - Paragraphs MUST be separated using \\n\\n (escaped newlines).
            - Body must be plain text—not markdown.

            WRITING STYLE:
            - Human, warm, professional.
            - 3–5 line paragraphs.
            - Clean spacing.
            - No repeated ideas.

            CONTEXT:
            USER RESUME:
            {user_resume}

            USER REQUEST:
            {user_prompt}

            JOB DESCRIPTION:
            {prompt}

            RETURN JSON ONLY.
            """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Output ONLY valid JSON. No markdown."},
                    {"role": "user", "content": full_prompt}
                ]
            )

            raw_output = response.choices[0].message.content.strip()

            # Extract JSON safely
            try:
                json_start = raw_output.index("{")
                json_end = raw_output.rindex("}") + 1
                cleaned = raw_output[json_start:json_end]

                email_data = json.loads(cleaned)

                subject = email_data.get("subject", "")
                body = email_data.get("body", "")

                # Convert escaped newlines → real newlines
                body = body.replace("\\n", "\n")

            except Exception as e:
                print("JSON PARSE ERROR:", e)
                return JsonResponse({
                    "error": "Model returned invalid JSON.",
                    "raw": raw_output
                }, status=500)

            return JsonResponse({"subject": subject, "message": body})

        except Exception as e:
            print("GPT ERROR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=400)



def home(request):
    # Load dynamic email accounts
    accounts = EmailAccount.objects.all()

    if request.method == "POST":
        recipient_email = request.POST.get('email')
        from_email = request.POST.get('from_email')

        generated_subject = request.POST.get("generated_subject")
        generated_message = request.POST.get("generated_message")

        # Keep these fields
        saved_prompt = request.POST.get("custom_prompt", "")
        saved_resume = request.POST.get("resume", "")

        # Validation
        if not recipient_email:
            messages.error(request, "⚠️ Please enter a recipient email.")
            return render(request, 'mailer/home.html', {
                'from_emails': accounts,
                'saved_prompt': saved_prompt,
                'saved_resume': saved_resume
            })

        if not from_email:
            messages.error(request, "⚠️ Please select a sender email.")
            return render(request, 'mailer/home.html', {
                'from_emails': accounts,
                'saved_prompt': saved_prompt,
                'saved_resume': saved_resume
            })

        if not generated_message.strip():
            messages.error(request, "⚠️ Message content is empty.")
            return render(request, 'mailer/home.html', {
                'from_emails': accounts,
                'saved_prompt': saved_prompt,
                'saved_resume': saved_resume
            })

        if not generated_subject.strip():
            messages.error(request, "⚠️ Email subject is missing.")
            return render(request, 'mailer/home.html', {
                'from_emails': accounts,
                'saved_prompt': saved_prompt,
                'saved_resume': saved_resume
            })

        # Fetch dynamic credentials
        account = EmailAccount.objects.filter(email=from_email).first()
        if not account:
            messages.error(request, "⚠️ This sender email does not exist.")
            return render(request, 'mailer/home.html', {
                'from_emails': accounts,
                'saved_prompt': saved_prompt,
                'saved_resume': saved_resume
            })

        # Try sending email
        try:
            connection = get_connection(
                host='smtp.gmail.com',
                port=587,
                username=account.email,
                password=account.app_password,
                use_tls=True
            )

            email = EmailMessage(
                subject=generated_subject,
                body=generated_message,
                from_email=account.email,
                to=[recipient_email],
                connection=connection
            )
            email.send(fail_silently=False)

            messages.success(request, "✅ Email sent successfully!")

        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, f"❌ Email sending failed: {e}")

        # Reload page but KEEP prompt + resume
        return render(request, 'mailer/home.html', {
            'from_emails': accounts,
            'saved_prompt': saved_prompt,
            'saved_resume': saved_resume
        })

    # GET request
    return render(request, 'mailer/home.html', {
        'from_emails': accounts
    })