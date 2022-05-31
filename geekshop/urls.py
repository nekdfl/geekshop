"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from mainapp.views import IndexTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', cache_page(3600)( IndexTemplateView.as_view()), name='index'),
    path('', IndexTemplateView.as_view(), name='index'),
    path('products/', include('mainapp.urls', namespace='mainapp')),
    path('authapp/', include('authapp.urls', namespace='authapp')),
    path('basketapp/', include('basketapp.urls', namespace='basketapp')),
    path('adminapp/', include('adminapp.urls', namespace='adminapp')),
    path('ordersapp/', include('ordersapp.urls', namespace='ordersapp')),
    path('', include('social_django.urls', namespace='social')),

]

if settings.PRODUCTION == False:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

urlpatterns += [path('debug', include(debug_toolbar.urls))]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
