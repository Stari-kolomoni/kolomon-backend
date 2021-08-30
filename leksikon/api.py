from django.urls import path, include
from leksikon import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', views.Category, basename='category')
router.register(r'english', views.EnglishEntry, basename='english')
router.register(r'slovene', views.Translation, basename='slovene')

# All urls that start with "api/"
urlpatterns = [
    path('ping', views.ping),
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(
        template_name='swagger-ui.html',
        url_name='schema'
    ), name='swagger-ui')
]
