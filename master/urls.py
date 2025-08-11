from django.urls import path
# from . import views
from .views import *

urlpatterns = [

    #customer

    path('view_allCustomers/', CustomerListView.as_view(), name='all_customer'),
    path('view_activeCustomer/', CustomerActiveListView.as_view(), name='active_customer'),
    path('view_activeCustomer/bysalesman/<uuid:pk>/', CustomerActiveListBySalesManView.as_view(), name='active_customer'),

    path('create_Customer/', CustomerCreateView.as_view(), name='create_customer'),
    path('update_Customer/<uuid:pk>/', CustomerUpdateView.as_view(), name='update_customer'),

    path('disable_Customer/<uuid:pk>/', CustomerDisableView.as_view(), name='disable_customer'),
    path('enable_Customer/<uuid:pk>/', CustomerEnableView.as_view(), name='enable_customer'),

    #HardWareMaterialCategory

    path('view_allHardWareMaterialCategorys/', HardWareMaterialCategoryListView.as_view(), name='all_HardWareMaterialCategory'),
    path('view_activeHardWareMaterialCategory/', HardWareMaterialCategoryActiveListView.as_view(), name='active_HardWareMaterialCategory'),

    path('create_HardWareMaterialCategory/', HardWareMaterialCategoryCreateView.as_view(), name='create_HardWareMaterialCategory'),
    path('update_HardWareMaterialCategory/<uuid:pk>/', HardWareMaterialCategoryUpdateView.as_view(), name='update_HardWareMaterialCategory'),

    path('disable_HardWareMaterialCategory/<uuid:pk>/', HardWareMaterialCategoryDisableView.as_view(), name='disable_HardWareMaterialCategory'),
    path('enable_HardWareMaterialCategory/<uuid:pk>/', HardWareMaterialCategoryEnableView.as_view(), name='enable_HardWareMaterialCategory'),


    #HardWareMaterial

    path('view_allHardWareMaterials/', HardWareMaterialListView.as_view(), name='all_HardWareMaterial'),
    path('view_activeHardWareMaterial/', HardWareMaterialActiveListView.as_view(), name='active_HardWareMaterial'),

    path('create_HardWareMaterial/', HardWareMaterialCreateView.as_view(), name='create_HardWareMaterial'),
    path('update_HardWareMaterial/<uuid:pk>/', HardWareMaterialUpdateView.as_view(), name='update_HardWareMaterial'),

    path('disable_HardWareMaterial/<uuid:pk>/', HardWareMaterialDisableView.as_view(), name='disable_HardWareMaterial'),
    path('enable_HardWareMaterial/<uuid:pk>/', HardWareMaterialEnableView.as_view(), name='enable_HardWareMaterial'),


#TimberMaterialCategory

    path('view_allTimberMaterialCategorys/', TimberMaterialCategoryListView.as_view(), name='all_TimberMaterialCategory'),
    path('view_activeTimberMaterialCategory/', TimberMaterialCategoryActiveListView.as_view(), name='active_TimberMaterialCategory'),

    path('create_TimberMaterialCategory/', TimberMaterialCategoryCreateView.as_view(), name='create_TimberMaterialCategory'),
    path('update_TimberMaterialCategory/<uuid:pk>/', TimberMaterialCategoryUpdateView.as_view(), name='update_TimberMaterialCategory'),

    path('disable_TimberMaterialCategory/<uuid:pk>/', TimberMaterialCategoryDisableView.as_view(), name='disable_TimberMaterialCategory'),
    path('enable_TimberMaterialCategory/<uuid:pk>/', TimberMaterialCategoryEnableView.as_view(), name='enable_TimberMaterialCategory'),


    #TimberMaterial

    path('view_allTimberMaterials/', TimberMaterialListView.as_view(), name='all_TimberMaterial'),
    path('view_activeTimberMaterial/', TimberMaterialActiveListView.as_view(), name='active_TimberMaterial'),

    path('create_TimberMaterial/', TimberMaterialCreateView.as_view(), name='create_TimberMaterial'),
    path('update_TimberMaterial/<uuid:pk>/', TimberMaterialUpdateView.as_view(), name='update_TimberMaterial'),

    path('disable_TimberMaterial/<uuid:pk>/', TimberMaterialDisableView.as_view(), name='disable_TimberMaterial'),
    path('enable_TimberMaterial/<uuid:pk>/', TimberMaterialEnableView.as_view(), name='enable_TimberMaterial'),


    #Region

    path('view_allRegions/', RegionListView.as_view(), name='all_Region'),
    path('view_activeRegion/', RegionActiveListView.as_view(), name='active_Region'),

    path('create_Region/', RegionCreateView.as_view(), name='create_Region'),
    path('update_Region/<uuid:pk>/', RegionUpdateView.as_view(), name='update_Region'),

    path('disable_Region/<uuid:pk>/', RegionDisableView.as_view(), name='disable_Region'),
    path('enable_Region/<uuid:pk>/', RegionEnableView.as_view(), name='enable_Region'),


    #CallStatus

    path('view_allCallStatuss/', CallStatusListView.as_view(), name='all_CallStatus'),
    path('view_activeCallStatus/', CallStatusActiveListView.as_view(), name='active_CallStatus'),

    path('create_CallStatus/', CallStatusCreateView.as_view(), name='create_CallStatus'),
    path('update_CallStatus/<uuid:pk>/', CallStatusUpdateView.as_view(), name='update_CallStatus'),

    path('disable_CallStatus/<uuid:pk>/', CallStatusDisableView.as_view(), name='disable_CallStatus'),
    path('enable_CallStatus/<uuid:pk>/', CallStatusEnableView.as_view(), name='enable_CallStatus'),


    #Prospect

    path('view_allProspects/', ProspectListView.as_view(), name='all_Prospect'),
    path('view_activeProspect/', ProspectActiveListView.as_view(), name='active_Prospect'),

    path('create_Prospect/', ProspectCreateView.as_view(), name='create_Prospect'),
    path('update_Prospect/<uuid:pk>/', ProspectUpdateView.as_view(), name='update_Prospect'),

    path('disable_Prospect/<uuid:pk>/', ProspectDisableView.as_view(), name='disable_Prospect'),
    path('enable_Prospect/<uuid:pk>/', ProspectEnableView.as_view(), name='enable_Prospect'),


    #PaymentMethod

    path('view_allPaymentMethods/', PaymentMethodListView.as_view(), name='all_PaymentMethod'),
    path('view_activePaymentMethod/', PaymentMethodActiveListView.as_view(), name='active_PaymentMethod'),

    path('create_PaymentMethod/', PaymentMethodCreateView.as_view(), name='create_PaymentMethod'),
    path('update_PaymentMethod/<uuid:pk>/', PaymentMethodUpdateView.as_view(), name='update_PaymentMethod'),

    path('disable_PaymentMethod/<uuid:pk>/', PaymentMethodDisableView.as_view(), name='disable_PaymentMethod'),
    path('enable_PaymentMethod/<uuid:pk>/', PaymentMethodEnableView.as_view(), name='enable_PaymentMethod'),

    #OrderStatusType

    path('view_allOrderStatusTypes/', OrderStatusTypeListView.as_view(), name='all_OrderStatusType'),
    path('view_activeOrderStatusType/', OrderStatusTypeActiveListView.as_view(), name='active_OrderStatusType'),

    path('create_OrderStatusType/', OrderStatusTypeCreateView.as_view(), name='create_OrderStatusType'),
    path('update_OrderStatusType/<uuid:pk>/', OrderStatusTypeUpdateView.as_view(), name='update_OrderStatusType'),

    path('disable_OrderStatusType/<uuid:pk>/', OrderStatusTypeDisableView.as_view(), name='disable_OrderStatusType'),
    path('enable_OrderStatusType/<uuid:pk>/', OrderStatusTypeEnableView.as_view(), name='enable_OrderStatusType'),


    #Branch

    path('view_allBranchs/', BranchListView.as_view(), name='all_Branch'),
    path('view_activeBranch/', BranchActiveListView.as_view(), name='active_Branch'),

    path('create_Branch/', BranchCreateView.as_view(), name='create_Branch'),
    path('update_Branch/<uuid:pk>/', BranchUpdateView.as_view(), name='update_Branch'),

    path('disable_Branch/<uuid:pk>/', BranchDisableView.as_view(), name='disable_Branch'),
    path('enable_Branch/<uuid:pk>/', BranchEnableView.as_view(), name='enable_Branch'),

    path('filter_timber_materials/', FilterTimberMaterialView.as_view()),
    path('filter_hardware_materials/', FilterHardwareMaterialView.as_view()),
]
