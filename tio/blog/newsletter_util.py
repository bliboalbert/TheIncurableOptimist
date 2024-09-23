import requests
from django.conf import settings


def subscribe_email_to_mailchimp(email):
    """
    Subscribes an email to the Mailchimp newsletter.
    """
    api_key = settings.MAILCHIMP_API_KEY
    audience_id = settings.MAILCHIMP_AUDIENCE_ID
    data_center = settings.MAILCHIMP_DATA_CENTER

    url = f'https://{data_center}.api.mailchimp.com/3.0/lists/{audience_id}/members'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'email_address': email,
        'status': 'subscribed'
    }
    response = requests.post(url, json=data, headers=headers)

    return response.status_code, response.json()
