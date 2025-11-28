from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection

# Example email templates
EMAIL_TEMPLATES = {
    'welcome': 'Welcome to our service! We are glad to have you.',
    'reminder': 'This is a friendly reminder about your upcoming task.',
    'thank_you': 'Thank you for using our service!',
}

# Example sender addresses
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
        selected_templates = request.POST.getlist('templates')
        from_email = request.POST.get('from_email')

        if not recipient_email:
            messages.error(request, "⚠️ Please enter a valid recipient email.")
            return redirect('home')
        if not selected_templates:
            messages.error(request, "⚠️ Please select at least one email template.")
            return redirect('home')
        if not from_email:
            messages.error(request, "⚠️ Please select a sender email.")
            return redirect('home')

        creds = EMAIL_ACCOUNTS.get(from_email)
        if not creds:
            messages.error(request, "⚠️ Invalid sender email selected.")
            return redirect('home')

        connection = get_connection(
            host='smtp.gmail.com',
            port=587,
            username=creds["EMAIL_HOST_USER"],
            password=creds["EMAIL_HOST_PASSWORD"],
            use_tls=True
        )

        for template_key in selected_templates:
            email = EmailMessage(
                subject=f"Email: {template_key.capitalize()}",
                body=EMAIL_TEMPLATES[template_key],
                from_email=creds["EMAIL_HOST_USER"],
                to=[recipient_email],
                connection=connection
            )
            email.send(fail_silently=False)

        messages.success(request, f"✅ Emails sent from {from_email} to {recipient_email}!")
        return redirect('home')  # Redirect back to the homepage

    context = {
        'templates': EMAIL_TEMPLATES,
        'from_emails': FROM_EMAILS,
    }
    return render(request, 'mailer/home.html', context)
