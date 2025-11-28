from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
import json
from django.http import JsonResponse
from groq import Groq
from django.views.decorators.csrf import csrf_exempt
# Groq client
client = Groq(api_key="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")

@csrf_exempt
def generate_message(request):

    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        user_prompt = data.get("custom_prompt", "")

        
        print(user_prompt)
        # Force JSON output from GPT
        full_prompt = f"""
            You are an expert at writing professional emails.

            Instruction from user:
            {user_prompt}

            Using the job description below, generate an email.

            IMPORTANT — Return ONLY valid JSON in this exact structure:

            {{
            "subject": "string",
            "body": "string"
            }}

            ❌ Do NOT add markdown
            ❌ Do NOT add commentary
            ❌ Do NOT write explanations
            ✔ ONLY return JSON

            Job Description:
            {prompt}
            """

        print("=====>full prompt", full_prompt)
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "Always return your output in JSON format only."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            )

            raw_output = response.choices[0].message.content

            # Parse JSON from GPT
            try:
                email_data = json.loads(raw_output)
                subject = email_data.get("subject", "Job Application")
                body = email_data.get("body", "")
            except Exception as e:
                print("JSON PARSE ERROR:", e)
                subject = "Job Application"
                body = raw_output  # fallback to full text

            return JsonResponse({
                "subject": subject,
                "message": body
            })

        except Exception as e:
            print("GPT ERROR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=400)


# EMAIL ACCOUNTS
FROM_EMAILS = [
    'edmarIt22@gmail.com',
    'dejesusedmar72@gmail.com',
    'edmarsw4433@gmail.com',
]

EMAIL_ACCOUNTS = {
    'edmarIt22@gmail.com': {
        'EMAIL_HOST_USER': 'edmarIt22@gmail.com',
        'EMAIL_HOST_PASSWORD': 'xedm rfvb zljv lnpm',
    },
    'dejesusedmar72@gmail.com': {
        'EMAIL_HOST_USER': 'dejesusedmar72@gmail.com',
        'EMAIL_HOST_PASSWORD': 'dpsd wuip bqce xgwh',
    },
    'edmarsw4433@gmail.com': {
        'EMAIL_HOST_USER': 'edmarsw4433@gmail.com',
        'EMAIL_HOST_PASSWORD': 'eryq ssen ijus anqd',
    },
}


def home(request):
    if request.method == "POST":
        recipient_email = request.POST.get('email')
        from_email = request.POST.get('from_email')

        generated_subject = request.POST.get("generated_subject")
        generated_message = request.POST.get("generated_message")

        print("=== FINAL SUBJECT:", generated_subject)
        print("=== FINAL MESSAGE:", generated_message)

        # Validations
        if not recipient_email:
            messages.error(request, "⚠️ Please enter a recipient email.")
            return redirect('home')

        if not from_email:
            messages.error(request, "⚠️ Please select a sender email.")
            return redirect('home')

        if not generated_message or not generated_message.strip():
            messages.error(request, "⚠️ Message content is empty.")
            return redirect('home')

        if not generated_subject or not generated_subject.strip():
            messages.error(request, "⚠️ Email subject is missing.")
            return redirect('home')

        # Sender credentials
        creds = EMAIL_ACCOUNTS.get(from_email)
        if not creds:
            messages.error(request, "⚠️ Invalid sender email selected.")
            return redirect('home')

        try:
            # SMTP connection
            connection = get_connection(
                host='smtp.gmail.com',
                port=587,
                username=creds["EMAIL_HOST_USER"],
                password=creds["EMAIL_HOST_PASSWORD"],
                use_tls=True
            )

            # Send email
            email = EmailMessage(
                subject=generated_subject,
                body=generated_message,
                from_email=creds["EMAIL_HOST_USER"],
                to=[recipient_email],
                connection=connection
            )
            email.send(fail_silently=False)

            messages.success(request, f"✅ Email sent successfully!")

        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, f"❌ Email sending failed: {e}")
            return redirect('home')

        return redirect('home')

    return render(request, 'mailer/home.html', {
        'from_emails': FROM_EMAILS,
    })
