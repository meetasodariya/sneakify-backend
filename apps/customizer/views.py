from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomDesign
from .serializers import CustomDesignSerializer, CustomDesignDetailSerializer
from apps.sneakers.models import SneakerModel

class CustomDesignCreateView(generics.CreateAPIView):
    """Save 3D design created by user or guest."""
    serializer_class = CustomDesignSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

class CustomDesignDetailView(generics.RetrieveAPIView):
    """Fetch a saved 3D design to hydrate into 3D customizer canvas."""
    queryset = CustomDesign.objects.all().select_related('base_model', 'user')
    serializer_class = CustomDesignDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

class CommunityDesignsView(generics.ListAPIView):
    """Showcase community-designed custom sneakers."""
    serializer_class = CustomDesignSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return CustomDesign.objects.filter(is_public=True).select_related('base_model', 'user')[:16]

class UserDesignsView(generics.ListAPIView):
    """List designs created by logged in user."""
    serializer_class = CustomDesignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomDesign.objects.filter(user=self.request.user).select_related('base_model')

class LikeDesignView(APIView):
    """Increment like count for community creations."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, id):
        try:
            design = CustomDesign.objects.get(id=id)
            design.likes_count += 1
            design.save(update_fields=['likes_count'])
            return Response({'likes_count': design.likes_count})
        except CustomDesign.DoesNotExist:
            return Response({'error': 'Design not found'}, status=status.HTTP_404_NOT_FOUND)
