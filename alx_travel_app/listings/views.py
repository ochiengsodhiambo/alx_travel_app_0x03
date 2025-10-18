from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .chapa import initiate_payment, verify_payment

# listings/views.py
from django.http import JsonResponse
from django.shortcuts import redirect

def home(request):
    # Option 1: simple JSON
    return JsonResponse({"message": "Welcome to The Travel App"})
    
    # Option 2: redirect to /api/listings/
    # return redirect('/api/listings/')

@api_view(['GET'])
def listings_list(request):
    """
    Get all travel listings
    """
    data = {
        'message': 'Welcome to ALX Travel App API',
        'endpoints': {
            'listings': '/api/listings/',
            'admin': '/admin/',
            'swagger': '/swagger/',
            'redoc': '/redoc/'
        }
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_payment(request):
    """Initiate payment and return Chapa checkout URL."""
    email = request.data.get('email')
    amount = request.data.get('amount')
    if not email or not amount:
        return Response({"error": "Email and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create payment record
    payment = Payment.objects.create(
        booking_reference=f"bk-{email}-{amount}".replace(" ", ""),
        amount=amount,
        status="Pending"
    )

    # Initiate Chapa payment
    callback_url = request.build_absolute_uri(f"/api/payments/verify/{payment.booking_reference}/")
    chapa_response = initiate_payment(email=email, amount=amount, callback_url=callback_url)

    # Store transaction_id
    payment.transaction_id = chapa_response['data']['tx_ref']
    payment.save()

    return Response({"checkout_url": chapa_response['data']['checkout_url'], "payment_id": payment.id})


@api_view(['GET'])
def verify_payment_status(request, booking_reference):
    """Verify payment status and update Payment model."""
    try:
        payment = Payment.objects.get(booking_reference=booking_reference)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

    chapa_result = verify_payment(payment.transaction_id)
    payment.status = chapa_result['data']['status']
    payment.save()

    return Response({
        "booking_reference": payment.booking_reference,
        "status": payment.status,
        "amount": payment.amount,
        "currency": payment.currency,
    })
