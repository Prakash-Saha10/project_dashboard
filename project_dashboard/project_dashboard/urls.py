from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import dashboard

urlpatterns = [
    # Home page
    path('', dashboard, name='home'),

    # Direct dashboard access
    path('dashboard/', dashboard, name='dashboard'),

    path('admin/', admin.site.urls),
    
    # Include accounts URLs (still works under /accounts/)
    path('accounts/', include('accounts.urls')),
    
    # Other apps
    path('projects/', include('projects.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
