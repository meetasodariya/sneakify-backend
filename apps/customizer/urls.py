from django.urls import path
from .views import (
    CustomDesignCreateView,
    CustomDesignDetailView,
    CommunityDesignsView,
    UserDesignsView,
    LikeDesignView,
)

app_name = 'customizer'

urlpatterns = [
    path('designs/', CustomDesignCreateView.as_view(), name='design_create'),
    path('designs/user/', UserDesignsView.as_view(), name='user_designs'),
    path('designs/<uuid:id>/', CustomDesignDetailView.as_view(), name='design_detail'),
    path('designs/<uuid:id>/like/', LikeDesignView.as_view(), name='design_like'),
    path('community/', CommunityDesignsView.as_view(), name='community_designs'),
]
