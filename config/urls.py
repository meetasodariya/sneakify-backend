"""
Root URL Configuration for Sneakify Studio Backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connection
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def health_check(request):
    """
    Lightweight health check endpoint for UptimeRobot / monitoring keep-alive pings.
    Verifies Django web service and Neon PostgreSQL database connectivity.
    """
    db_status = "connected"
    try:
        connection.ensure_connection()
    except Exception as e:
        db_status = f"unreachable: {str(e)}"

    is_healthy = db_status == "connected"
    return JsonResponse(
        {
            "status": "healthy" if is_healthy else "degraded",
            "service": "sneakify-backend",
            "database": db_status,
            "version": "1.0.0",
        },
        status=200 if is_healthy else 503,
    )

urlpatterns = [
    # Health Check (for UptimeRobot / Monitoring)
    path('', health_check, name='root-health'),
    path('health/', health_check, name='health-check'),
    path('api/health/', health_check, name='api-health-check'),

    # Admin Interface
    path('admin/', admin.site.urls),

    # OpenAPI 3.0 Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 Endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/sneakers/', include('apps.sneakers.urls')),
    path('api/v1/customizer/', include('apps.customizer.urls')),
    path('api/v1/cart/', include('apps.cart.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
