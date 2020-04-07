"""property_passport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from passport_app import views
from passport_app.views import NewUserProfileView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'owners', views.OwnerViewSet)
router.register(r'types', views.TypeOfRealEstateViewSet)
router.register(r'subtypes', views.SubtypeOfRealEstateViewSet)
router.register(r'subsubtypes', views.SubsubtypeOfRealEstateViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'classifiers', views.ClassifierViewSet)
router.register(r'groupvisits', views.GroupVisitViewSet)
router.register(r'fields', views.FieldViewSet)
router.register(r'data_fields', views.DataFieldViewSet)
router.register(r'forms', views.SearchFormViewSet)
router.register(r'uservisits', views.UserVisitViewSet)
router.register(r'userusers', views.UserUserViewSet)
router.register(r'notloginusers', views.NotLoginUserVisitViewSet)


app_name = 'passport_app'

urlpatterns = [
    url('', include('passport_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^select2/', include('django_select2.urls')),
]

#urlpatterns += router.urls
