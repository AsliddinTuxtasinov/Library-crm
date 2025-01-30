import re
import threading

from django.core.mail import EmailMessage
from rest_framework import serializers, validators

from apps.ausers.enums import AuthTypeChoices

# Regular expression pattern for validating email addresses
email_regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
# Regular expression pattern for validating phone numbers
phone_regex = re.compile(r'^\+?\d{1,3}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')


def check_phone_number(phone_number):
    # Checking if the input matches the phone_regex pattern
    return re.fullmatch(phone_regex, phone_number)


# Function to check if a given input is a valid email address or phone number
def check_email_or_phone(email_or_phone):
    # Checking if the input matches the email_regex pattern
    if re.fullmatch(email_regex, email_or_phone):
        return AuthTypeChoices.VIA_EMAIL
    # Checking if the input matches the phone_regex pattern
    elif re.fullmatch(phone_regex, email_or_phone):
        return AuthTypeChoices.VIA_PHONE
    else:
        # If the input doesn't match either pattern, raising a validation error
        raise serializers.ValidationError("Invalid input format")


def check_user_type(user_input: str) -> str:
    # Checking if the input matches the email_regex pattern
    if re.fullmatch(email_regex, user_input):
        return AuthTypeChoices.VIA_EMAIL.value

    # Checking if the input matches the phone_regex pattern
    elif re.fullmatch(phone_regex, user_input):
        return AuthTypeChoices.VIA_PHONE.value

    else:
        # If the input doesn't match either pattern, raising a validation error
        raise serializers.ValidationError("Invalid input format")


# Custom Thread class for sending emails asynchronously
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    # Static method to send an email with the provided data
    @staticmethod
    def send_email(data):
        # Creating an EmailMessage object with the subject, body, and recipient(s) from the provided data
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            to=[data["to_email"]]
        )

        # Checking if the content type is set to "html"
        if data.get("content_type") == "html":
            # Setting the content_subtype to "html" for sending HTML-formatted emails
            email.content_subtype = "html"

        # Starting a new thread to send the email asynchronously
        EmailThread(email).start()


# Function to send a message to the provided email address
def send_message_to_email(email, code):
    # # Rendering the HTML content for the email using a template and the provided code
    # html_content = render_to_string(
    #     template_name="email/authentication/activate_account.html",
    #     context={"code": code}
    # )
    #
    # # Sending the email by calling the send_email method of the Email class
    # Email.send_email(data={
    #     "subject": "Sign Up",
    #     "body": html_content,
    #     "to_email": email,
    #     "content_type": "html"
    # })
    print(f"Hello there!, Your verification code is: {code}")


def send_phone_code(phone_number, code):
    # account_sid = config("account_sid")
    # auth_token = config("your_auth_token")

    # client = Client(account_sid, auth_token)
    # client.messages.create(
    #     to=phone_number,  # +12316851234,
    #     from_="+15555555555",  # from twilio
    #     body=f"Hello there!, Your verification code is: {code}"
    # )
    print(f"Hello there!, Your verification code is: {code}")


def error_response_message(message, status_code):
    raise validators.ValidationError(
        detail={"message": f"{message}"}, code=status_code)
