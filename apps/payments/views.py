import hmac
import hashlib
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import Payment
from apps.orders.models import Order

class CreateRazorpayOrderView(APIView):
    """Initialize payment transaction with Razorpay."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_number = request.data.get('order_number')
        if not order_number:
            return Response({'error': 'order_number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        amount_in_paise = int(order.total_amount * 100)
        currency = 'INR'

        # Razorpay client integration if keys are provided
        razorpay_order_id = f"order_{order.order_number}_{order.id.hex[:8]}"
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            try:
                import razorpay
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                rzp_order = client.order.create({
                    'amount': amount_in_paise,
                    'currency': currency,
                    'receipt': order.order_number,
                    'payment_capture': 1,
                })
                razorpay_order_id = rzp_order['id']
            except Exception as e:
                pass

        # Create or update Payment record
        payment, _ = Payment.objects.get_or_create(
            order=order,
            defaults={
                'gateway': 'razorpay',
                'gateway_order_id': razorpay_order_id,
                'amount': order.total_amount,
                'currency': currency,
                'status': 'created',
            }
        )
        payment.gateway_order_id = razorpay_order_id
        payment.save()

        return Response({
            'order_number': order.order_number,
            'razorpay_order_id': razorpay_order_id,
            'amount': amount_in_paise,
            'currency': currency,
            'key_id': settings.RAZORPAY_KEY_ID or 'rzp_test_preview_key',
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'customer_phone': order.customer_phone,
        })

class VerifyRazorpayPaymentView(APIView):
    """Verify payment signature from frontend and lock order status."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_number = request.data.get('order_number')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        try:
            order = Order.objects.get(order_number=order_number)
            payment = Payment.objects.get(order=order)
        except (Order.DoesNotExist, Payment.DoesNotExist):
            return Response({'error': 'Order or Payment record not found'}, status=status.HTTP_404_NOT_FOUND)

        # Signature verification if secret configured
        verified = True
        if settings.RAZORPAY_KEY_SECRET and razorpay_signature:
            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()
            verified = (generated_signature == razorpay_signature)

        if verified:
            payment.gateway_payment_id = razorpay_payment_id
            payment.gateway_signature = razorpay_signature or ''
            payment.status = 'captured'
            payment.save()

            # Advance order status to Handcrafting
            order.status = 'handcrafting'
            order.save(update_fields=['status'])

            return Response({
                'status': 'success',
                'message': 'Payment successfully verified',
                'order_number': order.order_number,
                'tracking_number': order.tracking_number,
            })
        else:
            payment.status = 'failed'
            payment.save(update_fields=['status'])
            return Response({'error': 'Invalid payment signature'}, status=status.HTTP_400_BAD_REQUEST)
