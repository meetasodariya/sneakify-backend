from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.sneakers.models import SneakerModel
from apps.customizer.models import CustomDesign

def get_or_create_cart(request):
    """Retrieve existing cart by authenticated user or session key."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart

class CartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        cart = get_or_create_cart(request)
        sneaker_id = request.data.get('sneaker_id')
        custom_design_id = request.data.get('custom_design_id')
        size = request.data.get('size', 'UK 9')
        quantity = int(request.data.get('quantity', 1))

        if custom_design_id:
            try:
                design = CustomDesign.objects.get(id=custom_design_id)
                unit_price = design.total_price
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    custom_design=design,
                    size=size,
                    defaults={'quantity': quantity, 'unit_price': unit_price}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
            except CustomDesign.DoesNotExist:
                return Response({'error': 'Custom design not found'}, status=status.HTTP_404_NOT_FOUND)
        elif sneaker_id:
            try:
                sneaker = SneakerModel.objects.get(id=sneaker_id)
                unit_price = sneaker.base_price
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    sneaker=sneaker,
                    size=size,
                    defaults={'quantity': quantity, 'unit_price': unit_price}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
            except SneakerModel.DoesNotExist:
                return Response({'error': 'Sneaker model not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Either sneaker_id or custom_design_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateCartItemView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, item_id):
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            quantity = request.data.get('quantity')
            if quantity is not None:
                quantity = int(quantity)
                if quantity <= 0:
                    item.delete()
                else:
                    item.quantity = quantity
                    item.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

class ClearCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
