from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from perfumeProject.yasg import urlpatterns as yasg_urlpatterns
from perfumeProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    ] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('perfumeApp.urls'))
)

urlpatterns += yasg_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
