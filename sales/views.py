
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
        print(today)
        print()
        print()
        print()
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
            queryset = queryset.filter(updated_at__date__range=[start, end])

        # Apply salesman filter if given
        if salesman:
            queryset = queryset.filter(salesman=salesman)

        return queryset


import calendar
import datetime
from django.db.models import Sum, Q, OuterRef, Subquery
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import SalesWeb, CollectionAmount
from .serializers import CollectionReportSerializer


class CollectionReportByDate(generics.ListAPIView):
    serializer_class = CollectionReportSerializer

    def get_queryset(self):


        # Read params
        month_year = self.request.query_params.get("month")
        salesman = self.request.query_params.get("sales_id")
        print(month_year)
        if not month_year:
            raise ValidationError("'month_year' parameter is required. (format YYYY-MM)")

        try:
            year, month_num = map(int, month_year.split("-"))
        except ValueError:
            raise ValidationError(f"Invalid 'month_year': {month_year}. Expected format YYYY-MM")

        # Calculate first and last day of the month
        start = datetime.date(year, month_num, 1)
        last_day = calendar.monthrange(year, month_num)[1]
        end = datetime.date(year, month_num, last_day)
        print(start)
        print(end)
        
        # queryset = SalesWeb.objects.all()

        
        salesweb_ids = CollectionAmount.objects.filter(
            created_at__date__range=[start, end]
        ).values_list("salesweb_id", flat=True).distinct()

        # Filter SalesWeb by those IDs
        queryset = SalesWeb.objects.filter(id__in=salesweb_ids)



        # Apply salesman filter if given
        if salesman:
            queryset = queryset.filter(salesman=salesman)

        # Add annotation for sum of collection amounts
        collection_filter = Q(salesweb_id=OuterRef('pk')) & Q(created_at__date__range=[start, end])

        queryset = queryset.annotate(
            this_month_collection=Subquery(
                CollectionAmount.objects.filter(collection_filter)
                .values('salesweb_id')
                .annotate(total=Sum('amount'))
                .values('total')[:1]
            )
        )
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



