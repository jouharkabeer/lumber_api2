from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('view_allUsers/', UserListView.as_view(), name='all_User'),
    path('view_activeUser/', UserActiveListView.as_view(), name='active_User'),

    path('create_User/', RegisterView.as_view(), name='create_User'),
    path('update_User/<uuid:pk>/', UserUpdateView.as_view(), name='update_User'),

    path('disable_User/<uuid:pk>/', UserDisableView.as_view(), name='disable_User'),
    path('enable_User/<uuid:pk>/', UserEnableView.as_view(), name='enable_User'),


    path('view_allUserTypes/', UserTypeListView.as_view(), name='all_UserType'),
    path('view_activeUserType/', UserTypeActiveListView.as_view(), name='active_UserType'),

    path('create_UserType/', UserTypeCreateView.as_view(), name='create_UserType'),
    path('update_UserType/<uuid:pk>/', UserTypeUpdateView.as_view(), name='update_UserType'),

    path('disable_UserType/<uuid:pk>/', UserTypeDisableView.as_view(), name='disable_UserType'),
    path('enable_UserType/<uuid:pk>/', UserTypeEnableView.as_view(), name='enable_UserType'),

    path('view_activeSalesman/', SalesmanActiveView.as_view(), name='active salesman'),

    path('validity/', TokenValidity.as_view(), name='tffytty'),

    path('change_password/<uuid:pk>/', ChangePassword.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('change_password/byadmin/', AdminSetPasswordView.as_view()),
    path('dashboarddetails/', Dashboard.as_view()),
    path('dashboarddetails/bysalesman/<uuid:pk>/', DashboardforSalesman.as_view()),
    path('order_amount_data/', OrderAmount.as_view()),
    path('order_chart_data/', Orderchartdata.as_view()),

]
