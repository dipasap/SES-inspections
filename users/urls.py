from django.urls import path
from users import views

urlpatterns =[
	path('list/', views.CustomUserListView.as_view(), name='user-list'),
	path('create/', views.CustomUserCreateView.as_view(), name='user-create'),
	path('update/<int:pk>/', views.CustomUserUpdateView.as_view(), name='user-update'),
	path('details/<int:pk>/', views.CustomUserDetailView.as_view(), name='user-details'),
]
