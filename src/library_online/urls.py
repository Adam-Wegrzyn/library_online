"""library_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from library import views
from .router import router
from rest_framework.authtoken import views as rest_view
from django.contrib.auth.views import LoginView
from users import views as user_view

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('my_books/', views.my_books, name='my_books'),
    path('add_book/', views.add_book, name='add_book'),
    path('<int:book_pk>/edit_book/', views.edit_book, name='edit_book'),
    path('import_book/', views.import_book, name='import_book'),
    # path('api/book_list/', views.book_list, name='book_list'),
    path('api/', include(router.urls), name='api_view'),
    path('api-token-auth/', rest_view.obtain_auth_token, name='api-token-auth'),
    path('login/', LoginView.as_view(template_name='library/login.html'), name='login'),
    path('register/', user_view.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('<int:book_pk>/delete/', views.delete_book, name='delete_book')
]
