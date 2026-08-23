from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, WishlistItem
from .serializers import ReviewSerializer, WishlistItemSerializer

class SneakerReviewsListView(generics.ListCreateAPIView):
    """List and post customer reviews for a sneaker."""
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        sneaker_id = self.kwargs.get('sneaker_id')
        return Review.objects.filter(sneaker_id=sneaker_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistView(generics.ListAPIView):
    """List items in authenticated user's wishlist."""
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('sneaker', 'custom_design')

class ToggleWishlistView(APIView):
    """Toggle a sneaker or custom design in/out of user's wishlist."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sneaker_id = request.data.get('sneaker_id')
        custom_design_id = request.data.get('custom_design_id')

        if not sneaker_id and not custom_design_id:
            return Response({'error': 'Either sneaker_id or custom_design_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        query = {'user': request.user}
        if sneaker_id:
            query['sneaker_id'] = sneaker_id
        if custom_design_id:
            query['custom_design_id'] = custom_design_id

        existing = WishlistItem.objects.filter(**query).first()
        if existing:
            existing.delete()
            return Response({'action': 'removed', 'message': 'Removed from wishlist'})
        else:
            WishlistItem.objects.create(**query)
            return Response({'action': 'added', 'message': 'Added to wishlist'})
