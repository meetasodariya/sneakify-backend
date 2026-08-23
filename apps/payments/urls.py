from django.urls import path
from .views import (
    CreateRazorpayOrderView,
    VerifyRazorpayPaymentView,
)

app_name = 'payments'

urlpatterns = [
    path('razorpay/create-order/', CreateRazorpayOrderView.as_view(), name='razorpay_create_order'),
    path('razorpay/verify/', VerifyRazorpayPaymentView.as_view(), name='razorpay_verify'),
]
