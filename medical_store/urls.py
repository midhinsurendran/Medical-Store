from django.urls import path
from . import views
urlpatterns = [
  path('', views.home,name='home'),  
  path('create/', views.product_create,name='createproduct'),
  path('update/<int:id>/',views.product_update,name='updateproduct'),
  path('delete/<int:id>',views.product_delete,name='deleteproduct'),
  path('signup/',views.signup,name='signup'),
  path('login/',views.login_page,name='login'),
  path('logout/', views.logout_view,name='logout'),
  path('list/',views.listing,name='page_list'),
  path('search/',views.search,name='searchs')
]