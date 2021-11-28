from django.urls import path
#from .views_dn import *
from .views import views_rc, views_dn, views

app_name = "users_auth"

urlpatterns = [

    path('', views.index_page, name='index'),
    #path('userpage/', userpage, name="userpage"),
    #path('login/', login_profile, name="login"),
    #path('logout/', logout_profile, name='logout'),
    #path('register_profile/', register_profile, name='register_profile'),

    path('userpage_dn/', views_dn.userpage, name='userpage_dn'),
    path('login_dn/', views_dn.login_dn, name='login_dn'),
    path('logout_dn/', views_dn.logout_dn, name='logout_dn'),
    path('register_dn/', views_dn.register, name='register_dn'),
    path('my_donations/', views_dn.my_donations, name="my_donations"),
    path('pending_donations_dn/', views_dn.pending_donations, name='pending_donations_dn'),

    path('userpage_rc/', views_rc.userpage, name="userpage_rc"),
    path('login_rc/', views_rc.login_rc, name='login_rc'),
    path('logout_rc', views_rc.logout_rc, name='logout_rc'),
    path('register_rc/', views_rc.register, name='register_rc'),
    path('pending_donations/', views_rc.pending_donations, name='pending_donations'),
    path('my_donations_rc/', views_rc.my_donations_rc, name='my_donations_rc'),

    # rankng
    path('ranking/', views_dn.ranking, name='ranking'),
    
    #coupons
    path('coupons/', views_dn.coupons_page, name='coupons'),
    path('remove_coupon/<id>/', views_dn.remove_coupon, name='remove_coupon'),

]
