from rest_framework import serializers
from .models import *

# class SalesWebSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesWeb
#         fields = '__all__'
#         read_only_fields = ['created_by', 'created_at', 'updated_at']
    
#     customer_name = serializers.SerializerMethodField()
#     def get_customer_name(self, obj):
#         return obj.customer.customer_name if obj.customer else None
    
#     call_status_name = serializers.SerializerMethodField()
#     def get_call_status_name(self, obj):
#         return obj.call_status.call_status_name if obj.call_status else None
    
#     prospect_name = serializers.SerializerMethodField()
#     def get_prospect_name(self, obj):
#         return obj.prospect.prospect_name if obj.prospect else None

#     order_status_name = serializers.SerializerMethodField()
#     def get_order_status_name(self, obj):
#         return obj.order_status.order_type_name if obj.order_status else None
    
#     region_name = serializers.SerializerMethodField()
#     def get_region_name(self, obj):
#         return obj.region.region_name if obj.region else None
    
#     payment_method_name = serializers.SerializerMethodField()
#     def get_payment_method_name(self, obj):
#         return obj.payment_method.payment_type_name if obj.payment_method else None


class SalesWebSerializer(serializers.ModelSerializer):
    # sales_man = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    call_status_name = serializers.SerializerMethodField()
    prospect_name = serializers.SerializerMethodField()
    prospect_bg = serializers.SerializerMethodField()
    prospect_text = serializers.SerializerMethodField()
    order_status_name = serializers.SerializerMethodField()
    order_text = serializers.SerializerMethodField()
    order_bg = serializers.SerializerMethodField()
    salesman_name = serializers.SerializerMethodField()
    hardware_material_name = serializers.SerializerMethodField()
    timber_material_name = serializers.SerializerMethodField()
    hardware_category_name = serializers.SerializerMethodField()
    timber_category_name = serializers.SerializerMethodField()

    class Meta:
        model = SalesWeb
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_sales_man(self, obj):
        return obj.created_by.namefull if obj.created_by else None

    def get_customer_name(self, obj):
        return obj.customer.customer_name if obj.customer else None

    def get_call_status_name(self, obj):
        return obj.call_status.call_status_name if obj.call_status else None

    def get_prospect_name(self, obj):
        return obj.prospect.prospect_name if obj.prospect else None
    def get_prospect_bg(self, obj):
        return obj.prospect.text_bg if obj.prospect else None    
    def get_prospect_text(self, obj):
        return obj.prospect.text_color if obj.prospect else None
    
    def get_order_status_name(self, obj):
        return obj.order_status.order_type_name if obj.order_status else None
    def get_order_bg(self, obj):
        return obj.order_status.text_bg if obj.order_status else None
    def get_order_text(self, obj):
        return obj.order_status.text_color if obj.order_status else None
    
    def get_salesman_name(self, obj):
        return obj.salesman.namefull if obj.salesman else None

    def get_hardware_material_name(self, obj):
        return [m.hardware_material_name for m in obj.hardwarematerials.all()]
      
    def get_timber_material_name(self, obj):
        return [m.timber_material_name for m in obj.timbermaterials.all()]  

    def get_hardware_category_name(self, obj):
        return [m.hardware_material_catagory_name for m in obj.hardwarecategories.all()]
      
    def get_timber_category_name(self, obj):
        return [m.timber_material_catagory_name for m in obj.timbercategories.all()]  


class MeetingLogSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    salesman_name = serializers.SerializerMethodField()
    hardware_material_name = serializers.SerializerMethodField()
    timber_material_name = serializers.SerializerMethodField()

    class Meta:
        model = Meetinglog
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_customer_name(self, obj):
        return obj.sales_web.customer.customer_name if obj.sales_web.customer else None
    
    def get_salesman_name(self, obj):
        return obj.sales_web.salesman.namefull if obj.sales_web.salesman else None
    
    def get_hardware_material_name(self, obj):
        return [m.hardware_material_name for m in obj.sales_web.hardwarematerials.all()]
      
    def get_timber_material_name(self, obj):
        return [m.timber_material_name for m in obj.sales_web.timbermaterials.all()]  

class CollectionReportSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    salesman_name = serializers.SerializerMethodField()
    branch_code = serializers.SerializerMethodField()
    this_month_collection = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = SalesWeb
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_salesman_name(self, obj):
        return obj.salesman.namefull if obj.salesman else None
    
    def get_branch_code(self, obj):
        return obj.salesman.branch.branch_code if obj.salesman.branch else None
    
    def get_customer_name(self, obj):
        return obj.customer.customer_name if obj.customer else None
    

    

class ReportSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    salesman_name = serializers.SerializerMethodField()
    payment_recived = serializers.SerializerMethodField()
    call_status = serializers.SerializerMethodField()
    hardware_material_name = serializers.SerializerMethodField()
    timber_material_name = serializers.SerializerMethodField()

    class Meta:
        model = Meetinglog
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_salesman_name(self, obj):
        return obj.sales_web.salesman.namefull if obj.sales_web.salesman else None

    def get_customer_name(self, obj):
        return obj.sales_web.customer.customer_name if obj.sales_web.customer else None

    def get_call_status(self, obj):
        return obj.sales_web.call_status.call_status_name if obj.sales_web.call_status else None
    
    def get_payment_recived(self, obj):
        return obj.sales_web.payment_recieved if obj.sales_web else None
    
    def get_hardware_material_name(self, obj):
        return [m.hardware_material_name for m in obj.sales_web.hardwarematerials.all()]
      
    def get_timber_material_name(self, obj):
        return [m.timber_material_name for m in obj.sales_web.timbermaterials.all()]  
    
class DailySalesSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySalesSummary
        fields = '__all__'