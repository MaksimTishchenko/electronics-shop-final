from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Router для DRF ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)

# Объединяем все URL-пути в одном списке
urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # API маршруты
    path('api/', include(router.urls)),
    path('api/cart/', include(('cart.urls', 'cart'), namespace='api_cart')),  # Предпочтительнее подключать отдельный urls.py
    path('api/orders/', include(('orders.urls', 'orders'), namespace='api_orders')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Webhooks
    path("webhooks/stripe/", include("webhooks.urls")),

    # Приложения
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    path('', include('products.urls')),

    # Авторизация
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Добавляем MEDIA_URL только в DEBUG режиме
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)