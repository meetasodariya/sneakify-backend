from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderDetailSerializer, OrderCreateSerializer
from apps.cart.views import get_or_create_cart

class CreateOrderFromCartView(APIView):
    """Convert user's active cart into an Order."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = get_or_create_cart(request)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        subtotal = cart.subtotal
        shipping_fee = 0.00
        tax_amount = 0.00
        total_amount = subtotal + shipping_fee + tax_amount

        user = request.user if request.user.is_authenticated else None

        # Create Order
        order = Order.objects.create(
            user=user,
            customer_name=serializer.validated_data['customer_name'],
            customer_email=serializer.validated_data['customer_email'],
            customer_phone=serializer.validated_data['customer_phone'],
            shipping_address_line1=serializer.validated_data['shipping_address_line1'],
            shipping_address_line2=serializer.validated_data.get('shipping_address_line2', ''),
            shipping_city=serializer.validated_data['shipping_city'],
            shipping_state=serializer.validated_data['shipping_state'],
            shipping_postal_code=serializer.validated_data['shipping_postal_code'],
            shipping_country=serializer.validated_data.get('shipping_country', 'India'),
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status='pending',
        )

        # Create Order Items from Cart Items
        for ci in cart_items:
            OrderItem.objects.create(
                order=order,
                sneaker=ci.sneaker,
                custom_design=ci.custom_design,
                design_snapshot=ci.custom_design.configuration if ci.custom_design else None,
                item_title=ci.item_name,
                preview_image_url=ci.preview_image,
                size=ci.size,
                quantity=ci.quantity,
                unit_price=ci.unit_price,
                total_price=ci.total_price,
            )

        # Clear cart
        cart_items.delete()

        detail_serializer = OrderDetailSerializer(order)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

class UserOrdersListView(generics.ListAPIView):
    """List authenticated user's order history."""
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve order details by order_number."""
    queryset = Order.objects.all().prefetch_related('items')
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'order_number'

class TrackOrderView(APIView):
    """Public tracking endpoint by tracking number or order number."""
    permission_classes = [permissions.AllowAny]

    def get(self, request, identifier):
        order = Order.objects.filter(
            tracking_number__iexact=identifier
        ).first() or Order.objects.filter(
            order_number__iexact=identifier
        ).first()

        if not order:
            return Response({'error': 'Order tracking ID not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
