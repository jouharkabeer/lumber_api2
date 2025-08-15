
from .serializers import *
from rest_framework import generics,status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone


#------------------------------------SalesWeb ------------------------------
class SalesWebListView(generics.ListAPIView):
    queryset = SalesWeb.objects.all()
    serializer_class = SalesWebSerializer

class SalesWebActiveListView(generics.ListAPIView):
    queryset = SalesWeb.objects.filter(is_active=True)
    serializer_class = SalesWebSerializer

class SalesWebCreateView(generics.CreateAPIView):
    serializer_class = SalesWebSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class SalesWebUpdateView(generics.RetrieveUpdateAPIView):
    queryset = SalesWeb.objects.all()
    serializer_class = SalesWebSerializer


class SalesWebDisableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(SalesWeb, id=pk)
        item.is_active = False
        item.save()
        return Response({"message": "disabled successfully."}, status=status.HTTP_200_OK)

class SalesWebEnableView(APIView):
    def delete(self, request, pk):
        item = get_object_or_404(SalesWeb, id=pk)
        if not item.is_active:  # ✅ If currently inactive
            item.is_active = True  # ✅ Set active
            item.save()
            return Response({"message": "Activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Already Active."}, status=status.HTTP_200_OK)
        

class SalesWebListViewbySalesman(generics.ListAPIView):
    serializer_class = SalesWebSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SalesWeb.objects.filter(salesman = pk)

class SalesWebActiveListViewbySalesman(generics.ListAPIView):
    serializer_class = SalesWebSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SalesWeb.objects.filter(salesman = pk, is_active = True)


today = timezone.now().date()



class AnyCheckInChecker(generics.ListAPIView):
    serializer_class = MeetingLogSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Meetinglog.objects.filter(
            sales_web__salesman_id=pk,
            time_in__isnull=False,
            time_out__isnull=True
        )



class Scheduledpendingmeets(generics.ListAPIView):
    serializer_class = SalesWebSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SalesWeb.objects.filter(
            next_meeting_date__gt=today,
            salesman_id=pk,
            meeting_done = False
        )


class TodaySalemeetPending(generics.ListAPIView):
    serializer_class = SalesWebSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SalesWeb.objects.filter(
            next_meeting_date=today,
            salesman_id=pk,
            meeting_done = False
        )
    
class TodaySalesMeetDone(generics.ListAPIView):
    serializer_class = MeetingLogSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Meetinglog.objects.filter(
            created_at__date=today,
            sales_web__salesman_id=pk,
            time_in__isnull=False,
            time_out__isnull=False
        )

class MeetingCheckIn(generics.CreateAPIView):
    serializer_class = MeetingLogSerializer
    def perform_create(self, serializer):
        if (self.request.user):
            serializer.save(created_by=self.request.user)

class MeetingCheckOut(generics.RetrieveUpdateAPIView):
    queryset = Meetinglog.objects.all()
    serializer_class = MeetingLogSerializer



class CollectionReport(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = SalesWeb.objects.all()
    serializer_class = CollectionReportSerializer


class MeetingLogListView(generics.ListAPIView):
    queryset = Meetinglog.objects.all()
    serializer_class = MeetingLogSerializer


from rest_framework import generics, permissions
from django.utils.dateparse import parse_date

from django.utils.dateparse import parse_date
from rest_framework import generics, permissions

class CollectionReportByDate(generics.ListAPIView):
    # permission_classes = [permissions.AllowAny]
    serializer_class = CollectionReportSerializer

    def get_queryset(self):
        queryset = SalesWeb.objects.all()

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        salesman = self.request.query_params.get('sales_id')
        print(queryset)
        # Parse the dates safely
        start = parse_date(start_date) if start_date else None
        end = parse_date(end_date) if end_date else None
        print(start)
        # Apply date filter if both start and end are valid
        if start and end:
            queryset = queryset.filter(created_at__date__range=[start, end])

        # Apply salesman filter if given
        if salesman:
            queryset = queryset.filter(salesman=salesman)

        return queryset


class DailyReport(generics.ListAPIView):

    serializer_class = ReportSerializer
    def get_queryset(self):
    
        queryset = Meetinglog.objects.all()
        salesman = self.request.query_params.get('sales_id')
        date = self.request.query_params.get('date')

        if salesman:
            queryset = queryset.filter(sales_web__salesman=salesman)
        
        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset



