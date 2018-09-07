from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class SendMailMixin(object):

    def send_mail(self, subject_template_name, email_template_name,
                context, from_email, to_email):

        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMessage(subject, body, from_email, [to_email])
        email_message.send()
