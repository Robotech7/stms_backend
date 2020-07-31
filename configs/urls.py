from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import MyJwtTokenView
from .yasg import urlpatterns as swagger_doc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', MyJwtTokenView.as_view(), name='token_obtain_pair'),
    path('api/accounts/', include('accounts.urls')),
]

urlpatterns += swagger_doc

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
