from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserType
from sales.models import DailySalesSummary
from master.models import Branch

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','branch', 'user_type', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            branch=validated_data['branch'],
            user_type=validated_data['user_type'],
            password=validated_data['password'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'] 
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class OrderAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySalesSummary
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    user_type_name = serializers.SerializerMethodField()
    branch_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','branch','namefull', 'user_type', 'password','branch_code', 'user_type_name', 'is_active']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def get_user_type_name(self, obj):
        return obj.user_type.name if obj.user_type else None

    def get_branch_code(self, obj):
        return obj.branch.branch_code if obj.branch else None










class CustomerSerializer(serializers.ModelSerializer):
    creater_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_creater_name(self, obj):
        return obj.created_by.namefull if obj.created_by else None

class HardWareMaterialCategorySerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = HardWareMaterialCategory
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.username if obj.created_by else None


class HardWareMaterialSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = HardWareMaterial
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.username if obj.created_by else None
    
    def get_category_name(self, obj):
        return obj.hardware_material_category.hardware_material_catagory_name if obj.hardware_material_category else None

class TimberMaterialCategorySerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = TimberMaterialCategory
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.username if obj.created_by else None


class TimberMaterialSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = TimberMaterial
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.username if obj.created_by else None
    
    def get_category_name(self, obj):
        return obj.timber_material_category.timber_material_catagory_name if obj.timber_material_category else None



class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class CallStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStatus
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        

class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    creater_name = serializers.SerializerMethodField()
    def get_creater_name(self, obj):
        return obj.created_by.namefull if obj.created_by else None
        

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class OrderStatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']