"""trello_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from board import views as board_views

router = routers.SimpleRouter()
router.register(r'managers', board_views.ManagerViewSet, base_name='managers')
router.register(r'projects', board_views.ProjectViewSet, base_name='projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'boards', board_views.BoardViewSet, base_name='boards')

board_router = routers.NestedSimpleRouter(project_router, r'boards', lookup='board')
board_router.register(r'cards', board_views.CardViewSet, base_name='cards')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(project_router.urls)),
    path('api/', include(board_router.urls)),
]
