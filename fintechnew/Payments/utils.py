# utils.py

import base64
from django.conf import settings

def get_vtpass_basic_auth():
    username = settings.VT_PASS_USERNAME  # Update with the actual setting name
    password = settings.VT_PASS_PASSWORD  # Update with the actual setting name
    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('utf-8')
    base64_auth = base64.b64encode(auth_bytes).decode('utf-8')
    return f"Basic {base64_auth}"
