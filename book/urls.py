from django.urls import path
from django.conf.urls import url

from . import views
#from .views import HomePageView, CreatePostView

app_name = 'book'


urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('rental/', views.rental, name='rental'),
    path('return/', views.return_book, name='return'),
    # path('display/', views.display, name='display'),
    # url(r'^status/cache/$', views.memcached),
]
