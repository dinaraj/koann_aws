from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('common.urls', 'common'), namespace='common')),
    path('account/', include('allauth.urls')),
    path('jobs/', include(('jobs.urls', 'jobs'), namespace='jobs')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
