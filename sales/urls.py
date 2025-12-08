from django.urls import path
from .views import *

urlpatterns = [

    path('view_allSalesWebs/bysalesman/<uuid:pk>/', SalesWebListViewbySalesman.as_view(), name='all_SalesMobile'),
    path('view_activeSalesWeb/bysalesman/<uuid:pk>/', SalesWebActiveListViewbySalesman.as_view(), name='active_SalesMobile'),

    path('view_allMeetingLog/', MeetingLogListView.as_view(), name='all_SalesWeb'),
    path('view_allMeetingLog_first100/', MeetingLogListView100.as_view(), name='all_SalesWeb'),

    path('view_allSalesWebs/', SalesWebListView.as_view(), name='all_SalesWeb'),
    path('view_activeSalesWeb/', SalesWebActiveListView.as_view(), name='active_SalesWeb'),

    path('create_SalesWeb/', SalesWebCreateView.as_view(), name='create_SalesWeb'),
    path('update_SalesWeb/<uuid:pk>/', SalesWebUpdateView.as_view(), name='update_SalesWeb'),

    path('disable_SalesWeb/<uuid:pk>/', SalesWebDisableView.as_view(), name='disable_SalesWeb'),
    path('enable_SalesWeb/<uuid:pk>/', SalesWebEnableView.as_view(), name='enable_SalesWeb'),


    path('salesman/sales/anycheckin/<uuid:pk>/', AnyCheckInChecker.as_view(), name='check in checker'),

    path('salesman/sales/todaypending/<uuid:pk>/', TodaySalemeetPending.as_view(), name='sales man list'),
    path('salesman/sales/scheduled/<uuid:pk>/', Scheduledpendingmeets.as_view(), name='sales man list'),
    path('salesman/sales/todaydone/<uuid:pk>/', TodaySalesMeetDone.as_view(), name='sales meet done'),
    path('salesman/sales/checkin/', MeetingCheckIn.as_view(), name='sales meet done'),
    path('salesman/sales/checkout/<uuid:pk>/', MeetingCheckOut.as_view(), name='sales meet done'),



    path('admin/report/', DailyReport.as_view(), name ='daily report'),
    path('admin/collectionreport/', CollectionReport.as_view(), name ='Collection report'),
    path('admin/collection-report-by-date/', CollectionReportByDate.as_view(), name ='Collection report'),
]
