from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

def send_search_result(email_data, email, search_param):
    error = None
    try:
    # subject = 'Search by %s' %  search_param
    #
    #
    # html_message = loader.render_to_string(
    #     'email_search_result.html',
    #     {
    #         'data': email_data,
    #         'search_param':search_param
    #     }
    # )
    # send_mail(subject,"",email_from,[email],fail_silently=True,html_message=html_message)
    #     send_mail("Test",
    #               "Test message",
    #               'baibakepc@gmail.com',
    #               ['baibakepc@gmail.com'],
    #               fail_silently=False,)
        email = EmailMessage('Test1', 'Body1', to=['baibakepc@gmail.com'])
        email.send()
    except Exception as e:
        error = e
    return  error

def send_email_message(title, message, emails):
    error = None
    try:
        email = EmailMessage(title, message, to=emails)
        email.send()
    except Exception as e:
        error = e
    return  error

def send_error(message):
    send_email_message('Error', message, [settings.EMAIL_HOST_USER])
