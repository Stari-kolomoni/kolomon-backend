from django.urls import path
from leksikon import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# All urls that start with "api/"
urlpatterns = [
    path("ping", views.Test.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(
        template_name='swagger-ui.html',
        url_name='schema'
    ), name='swagger-ui')
]
