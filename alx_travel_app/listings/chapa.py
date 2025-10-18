import requests
from django.conf import settings

CHAPA_BASE_URL = "https://api.chapa.co/v1/transaction"

def initiate_payment(email, amount, currency='ETB', callback_url=None):
    """Initiate payment with Chapa."""
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    data = {
        "email": email,
        "amount": amount,
        "currency": currency,
        "callback_url": callback_url,  # URL to verify payment after completion
        "tx_ref": f"tx-{email}-{amount}".replace(" ", ""),  # unique ref
    }

    response = requests.post(f"{CHAPA_BASE_URL}/initialize", json=data, headers=headers)
    response.raise_for_status()
    return response.json()  # Contains checkout_url & tx_ref

def verify_payment(tx_ref):
    """Verify payment status from Chapa."""
    headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    response = requests.get(f"{CHAPA_BASE_URL}/verify/{tx_ref}", headers=headers)
    response.raise_for_status()
    return response.json()  # Contains status, amount, currency, etc.
