import requests
import os
from django.conf import settings


def send_message(messenger_id, text):
    requests.post(settings.bot_api_url,
                  json={
                      'messenger_id': messenger_id,
                      'text': text
                  }
                  )
