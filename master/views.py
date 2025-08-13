
from .serializers import *
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q


from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from sales.models import SalesWeb, DailySalesSummary
from sales.serializers import DailySalesSummarySerializer
from django.db.models import Sum

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is not None and user.is_active:
            # Handle daily summary update


            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usertype': str(user.user_type.name) if user.user_type else 'SuperAdmin',
                'user_id': str(user.id),
                'login_name': str(user.namefull)
            })

        return Response({'detail': 'Invalid credentials or inactive user'}, status=status.HTTP_401_UNAUTHORIZED)



class UserTypeCreateView(generics.CreateAPIView):
    serializer_class = UserTypeSerializer
    permission_classes = [AllowAny]


class UserTypeListView(generics.ListAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer

class UserTypeActiveListView(generics.ListAPIView):
    queryset = UserType.objects.filter(is_active=True)
    serializer_class = UserTypeSerializer

class UserTypeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer


class UserTypeDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(UserType, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class UserTypeEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(UserType, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)




class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(
            is_superuser=False
        ).exclude(id=self.request.user.id)

class UserActiveListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(User, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class UserEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(User, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)




class SalesmanActiveView(generics.ListAPIView):
    queryset = User.objects.filter(user_type__name = 'Salesman', is_active = True)
    serializer_class = UserSerializer        


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.conf import settings
from django.apps import apps
from django.db import transaction
from django.contrib.auth import get_user_model

user = get_user_model()

class ChangePassword(APIView):

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password:
            return Response({"error": "Old password is required"}, status=400)
        if not new_password:
            return Response({"error": "New password is required"}, status=400)

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"success": "Password updated successfully"}, status=200)

from rest_framework import generics, permissions, serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

User = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the logged-in user
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"success": "Password updated successfully"})


class AdminSetPasswordSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class AdminSetPasswordView(generics.UpdateAPIView):
    serializer_class = AdminSetPasswordSerializer


    def get_object(self):
        user_id = self.request.data.get("user_id")
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

    def update(self, request, *args, **kwargs):

        super().update(request, *args, **kwargs)
        return Response({"success": "Password updated successfully"})


from django.utils.timezone import now

class Dashboard(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        salesman_count = User.objects.filter(user_type__name='Salesman', is_active=True).count()
        total_orders = SalesWeb.objects.count()
        active_orders = SalesWeb.objects.filter(is_active=True).count()
    

        today = now().date()

        # Get today's total order value, assuming `timestamp` field exists in DailySalesSummary
        today_summary = DailySalesSummary.objects.filter(timestamp=today).last()
        today_order_value = today_summary.today_order_value if today_summary else 0
        total_order_value = today_summary.total_order_value if today_summary else 0
        total_recieved_value = today_summary.total_recieved_value if today_summary else 0
        today_recieved_value = today_summary.total_recieved_value if today_summary else 0

        data = {
            'salesman_count': salesman_count,
            'total_orders': total_orders,
            'active_orders': active_orders,
            'daily_order_value': today_order_value,
            'total_order_value': total_order_value,
            'today_recived_value': today_recieved_value,
            'total_recived_value' : total_recieved_value,
        }

        return Response(data)


class DashboardforSalesman(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        total_orders = SalesWeb.objects.filter(salesman=pk).count()
        active_orders = SalesWeb.objects.filter(is_active=True, salesman=pk).count()
        total_order_value = SalesWeb.objects.filter(is_active=True, salesman=pk).aggregate(total=Sum('order_value'))['total'] or 0
        total_due_value = SalesWeb.objects.filter(is_active=True, salesman=pk).aggregate(total=Sum('due_amount'))['total'] or 0

        data = {
            'total_orders': total_orders,
            'active_orders': active_orders,
            'total_order_value': total_order_value,
            'total_due_value': total_due_value,
        }
        return Response(data)


# class OrderAmount(generics.ListAPIView):
#     permission_classes = [AllowAny]

#     queryset = DailySalesSummary.objects.all()
#     serializer_class = OrderAmountSerializer

class Orderchartdata(generics.ListAPIView):
    queryset = DailySalesSummary.objects.all()
    serializer_class = DailySalesSummarySerializer
    

class OrderAmount(generics.ListAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        data = [
            {
                "id": 1,
                "today_order_value": "4500.00",
                "total_order_value": "4500.00",
                "today_recieved_value": "300.00",
                "total_recieved_value": "300.00",
                "timestamp": "2025-07-10"
            },
            {
                "id": 2,
                "today_order_value": "3800.00",
                "total_order_value": "8300.00",
                "today_recieved_value": "200.00",
                "total_recieved_value": "500.00",
                "timestamp": "2025-07-11"
            },
            {
                "id": 3,
                "today_order_value": "5200.00",
                "total_order_value": "13500.00",
                "today_recieved_value": "800.00",
                "total_recieved_value": "1300.00",
                "timestamp": "2025-07-12"
            },
            {
                "id": 4,
                "today_order_value": "5000.00",
                "total_order_value": "18500.00",
                "today_recieved_value": "500.00",
                "total_recieved_value": "1800.00",
                "timestamp": "2025-07-13"
            },
            {
                "id": 5,
                "today_order_value": "6000.00",
                "total_order_value": "24500.00",
                "today_recieved_value": "1000.00",
                "total_recieved_value": "2800.00",
                "timestamp": "2025-07-14"
            },
            {
                "id": 6,
                "today_order_value": "4700.00",
                "total_order_value": "29200.00",
                "today_recieved_value": "300.00",
                "total_recieved_value": "3100.00",
                "timestamp": "2025-07-15"
            },
            {
                "id": 7,
                "today_order_value": "5300.00",
                "total_order_value": "34500.00",
                "today_recieved_value": "900.00",
                "total_recieved_value": "4000.00",
                "timestamp": "2025-07-16"
            },
            {
                "id": 8,
                "today_order_value": "4900.00",
                "total_order_value": "39400.00",
                "today_recieved_value": "400.00",
                "total_recieved_value": "4400.00",
                "timestamp": "2025-07-17"
            },
            {
                "id": 9,
                "today_order_value": "6100.00",
                "total_order_value": "45500.00",
                "today_recieved_value": "1200.00",
                "total_recieved_value": "5600.00",
                "timestamp": "2025-07-18"
            },
            {
                "id": 10,
                "today_order_value": "5500.00",
                "total_order_value": "51000.00",
                "today_recieved_value": "1100.00",
                "total_recieved_value": "6700.00",
                "timestamp": "2025-07-19"
            }
        ]

        return Response(data)

class TokenValidity(generics.ListAPIView):
    def get(self, request):
        return Response({"message": "its a valid token"}, status=200)









#------------------------------------customer ------------------------------
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

           

class CustomerActiveListView(generics.ListAPIView):
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer

class CustomerActiveListBySalesManView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Customer.objects.filter(
            Q(created_by=pk, is_active=True) |
            Q(view_all=True, is_active=True)
        ).distinct()

class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class CustomerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Customer, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class CustomerEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Customer, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)


######################## HardWareMaterialCategory ############################

class HardWareMaterialCategoryListView(generics.ListAPIView):
    queryset = HardWareMaterialCategory.objects.all()
    serializer_class = HardWareMaterialCategorySerializer

class HardWareMaterialCategoryActiveListView(generics.ListAPIView):
    queryset = HardWareMaterialCategory.objects.filter(is_active=True)
    serializer_class = HardWareMaterialCategorySerializer

class HardWareMaterialCategoryCreateView(generics.CreateAPIView):
    serializer_class = HardWareMaterialCategorySerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class HardWareMaterialCategoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HardWareMaterialCategory.objects.all()
    serializer_class = HardWareMaterialCategorySerializer


class HardWareMaterialCategoryDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(HardWareMaterialCategory, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class HardWareMaterialCategoryEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(HardWareMaterialCategory, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)




######################## HardWareMaterial ############################

class HardWareMaterialListView(generics.ListAPIView):
    queryset = HardWareMaterial.objects.all()
    serializer_class = HardWareMaterialSerializer

class HardWareMaterialActiveListView(generics.ListAPIView):
    queryset = HardWareMaterial.objects.filter(is_active=True)
    serializer_class = HardWareMaterialSerializer

class HardWareMaterialCreateView(generics.CreateAPIView):
    serializer_class = HardWareMaterialSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class HardWareMaterialUpdateView(generics.RetrieveUpdateAPIView):
    queryset = HardWareMaterial.objects.all()
    serializer_class = HardWareMaterialSerializer


class HardWareMaterialDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(HardWareMaterial, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class HardWareMaterialEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(HardWareMaterial, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)



######################## TimberMaterialCategory ############################

class TimberMaterialCategoryListView(generics.ListAPIView):
    queryset = TimberMaterialCategory.objects.all()
    serializer_class = TimberMaterialCategorySerializer

class TimberMaterialCategoryActiveListView(generics.ListAPIView):
    queryset = TimberMaterialCategory.objects.filter(is_active=True)
    serializer_class = TimberMaterialCategorySerializer

class TimberMaterialCategoryCreateView(generics.CreateAPIView):
    serializer_class = TimberMaterialCategorySerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class TimberMaterialCategoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TimberMaterialCategory.objects.all()
    serializer_class = TimberMaterialCategorySerializer


class TimberMaterialCategoryDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(TimberMaterialCategory, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class TimberMaterialCategoryEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(TimberMaterialCategory, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)




######################## TimberMaterial ############################

class TimberMaterialListView(generics.ListAPIView):
    queryset = TimberMaterial.objects.all()
    serializer_class = TimberMaterialSerializer

class TimberMaterialActiveListView(generics.ListAPIView):
    queryset = TimberMaterial.objects.filter(is_active=True)
    serializer_class = TimberMaterialSerializer

class TimberMaterialCreateView(generics.CreateAPIView):
    serializer_class = TimberMaterialSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class TimberMaterialUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TimberMaterial.objects.all()
    serializer_class = TimberMaterialSerializer


class TimberMaterialDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(TimberMaterial, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class TimberMaterialEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(TimberMaterial, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)



######################## Region ############################

class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionActiveListView(generics.ListAPIView):
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer

class RegionCreateView(generics.CreateAPIView):
    serializer_class = RegionSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class RegionUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class RegionDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Region, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class RegionEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Region, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)
        

######################## CallStatus ############################

class CallStatusListView(generics.ListAPIView):
    queryset = CallStatus.objects.all()
    serializer_class = CallStatusSerializer

class CallStatusActiveListView(generics.ListAPIView):
    queryset = CallStatus.objects.filter(is_active=True)
    serializer_class = CallStatusSerializer

class CallStatusCreateView(generics.CreateAPIView):
    serializer_class = CallStatusSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class CallStatusUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CallStatus.objects.all()
    serializer_class = CallStatusSerializer


class CallStatusDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(CallStatus, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class CallStatusEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(CallStatus, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)



######################## Prospect ############################

class ProspectListView(generics.ListAPIView):
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer

class ProspectActiveListView(generics.ListAPIView):
    queryset = Prospect.objects.filter(is_active=True)
    serializer_class = ProspectSerializer

class ProspectCreateView(generics.CreateAPIView):
    serializer_class = ProspectSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class ProspectUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer


class ProspectDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Prospect, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class ProspectEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Prospect, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)




######################## PaymentMethod ############################

class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class PaymentMethodActiveListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer

class PaymentMethodCreateView(generics.CreateAPIView):
    serializer_class = PaymentMethodSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class PaymentMethodUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentMethodDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(PaymentMethod, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class PaymentMethodEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(PaymentMethod, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)





######################## OrderStatusType ############################

class OrderStatusTypeListView(generics.ListAPIView):
    queryset = OrderStatusType.objects.all()
    serializer_class = OrderStatusTypeSerializer

class OrderStatusTypeActiveListView(generics.ListAPIView):
    queryset = OrderStatusType.objects.filter(is_active=True)
    serializer_class = OrderStatusTypeSerializer

class OrderStatusTypeCreateView(generics.CreateAPIView):
    serializer_class = OrderStatusTypeSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class OrderStatusTypeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = OrderStatusType.objects.all()
    serializer_class = OrderStatusTypeSerializer


class OrderStatusTypeDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(OrderStatusType, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class OrderStatusTypeEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(OrderStatusType, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)




######################## Branch ############################

class BranchListView(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class BranchActiveListView(generics.ListAPIView):
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchSerializer

class BranchCreateView(generics.CreateAPIView):
    serializer_class = BranchSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class BranchUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Branch, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class BranchEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(Branch, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)





from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import TimberMaterial, HardWareMaterial
from .serializers import TimberMaterialSerializer, HardWareMaterialSerializer

class FilterTimberMaterialView(GenericAPIView, ListModelMixin):
    serializer_class = TimberMaterialSerializer

    def post(self, request, *args, **kwargs):
        category_ids = request.data.get('category_ids', [])
        if not category_ids:
            return Response({"detail": "No category_ids provided."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = TimberMaterial.objects.filter(
            timber_material_category__id__in=category_ids,
            is_active=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FilterHardwareMaterialView(GenericAPIView, ListModelMixin):
    serializer_class = HardWareMaterialSerializer

    def post(self, request, *args, **kwargs):
        category_ids = request.data.get('category_ids', [])
        if not category_ids:
            return Response({"detail": "No category_ids provided."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = HardWareMaterial.objects.filter(
            hardware_material_category__id__in=category_ids,
            is_active=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
