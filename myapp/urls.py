from django.urls import path,include
from . import views
urlpatterns=[path('',views.home,name='home'),
             path('signin/',views.signin,name='signin'),
             path('register/',views.register,name='register'),
             path('registration/',views.registration,name='registration'),
             path('user/',views.user_dashboard,name='user'),
             path('addserver/',views.addserver,name='addserver'),
             path('delete_server/<int:id>/',views.delete_server,name='delete_server'),
             path('edit_server/<int:id>/',views.edit_server,name='edit_server'),
             path('logout/',views.user_logout,name='logout'),
             path('dashboard_selection/', views.dashboard_selection, name='dashboard_selection'),
             path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
             path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
            #path('accounts/',include('django.contrib.auth.urls')),

             ]
