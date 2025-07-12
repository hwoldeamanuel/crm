"""
URL configuration for cnms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

handler404 = 'home.views.error_404' 
# Custom 500 error view
handler500 = 'home.views.error_500' 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('user/', include('user.urls')),
    path('program/', include('program.urls')),
    path('setting/', include('app_admin.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('conceptnote/', include('conceptnote.urls')),
    path('report/', include('report.urls')),
    path('travel/', include('travel.urls')),
    path('partnership/', include('partnership.urls')),
    path("select2/", include("django_select2.urls")),
    path("api/", include("api.urls")),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
