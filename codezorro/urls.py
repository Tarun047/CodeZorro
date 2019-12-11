"""codezorro URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from codecompiler.models import Code
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

# constants
RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '9af3a300df000f388af74efdd9304c258a91ab8a'

def solve(source,language):
    data = {
    'client_secret': CLIENT_SECRET,
    'async': 0,
    'source': source,
    'lang': language,
    'time_limit': 5,
    'memory_limit': 262144,
    }
    r = requests.post(RUN_URL, data=data)
    return r.json()

class CodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Code
        fields = ['source','language']

class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer

    @action(detail=False, methods=['post'])
    def compile(self,request,pk=None):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            feedback = solve(serializer.data['source'],serializer.data['language'])
            return Response(feedback)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'code', CodeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
