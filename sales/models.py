from django.db import models
from master.models import *
from django.db.models import Sum


# Create your models here.
class SalesWeb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    hardwarematerials = models.ManyToManyField(HardWareMaterial, blank=True)
    timbermaterials = models.ManyToManyField(TimberMaterial,  blank=True)
    hardwarecategories = models.ManyToManyField(HardWareMaterialCategory, blank=True)
    timbercategories = models.ManyToManyField(TimberMaterialCategory,  blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    call_status = models.ForeignKey(CallStatus, on_delete=models.CASCADE)
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.ForeignKey(OrderStatusType, on_delete=models.CASCADE, null=True, blank=True)

    mode_of_collection = models.CharField(max_length=10, null=True, blank=True)
    expected_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_payment_date = models.DateField(null=True, blank=True)
    next_meeting_date = models.DateField(null=True, blank=True)
    meeting_done = models.BooleanField(default=False)
    payment_recieved = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    final_due_date = models.DateField(null=True, blank=True)
    soa_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    expected_pdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_cdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_tt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_pdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_cdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_tt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_amount_now = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_amount_now_two = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    due_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        # Set expected_payment_amount based on sum of expected values
        self.expected_payment_amount = sum(filter(None, [
            self.expected_cash,
            self.expected_cdc,
            self.expected_pdc,
            self.expected_tt,
        ]))

        # Set payment_received as sum of collected amounts
        self.payment_recieved = sum(filter(None, [
            self.collected_cash,
            self.collected_cdc,
            self.collected_pdc,
            self.collected_tt,
        ]))
        if self.collected_amount_now is not None:
            CollectionAmount.objects.create(
                salesweb = self,
                amount = self.collected_amount_now
            )
            # self.collected_amount_now_two = self.collected_amount_now
            self.collected_amount_now = None
            
        # Calculate due if soa_amount exists
        if self.soa_amount is not None:
            self.due_amount = self.soa_amount - self.payment_recieved

        # Save the current SalesWeb instance
        super().save(*args, **kwargs)


        # if self.collected_amount_now_two:
        #     CollectionAmount.objects.create(
        #         salesweb = self,
        #         amount = self.collected_amount_now_two
        #     )
        #     self.collected_amount_now_two = None


        # Create a snapshot in history
        history = SalesWebHistory.objects.create(
            salesweb=self,
            salesman=self.salesman,
            customer=self.customer,
            call_status=self.call_status,
            prospect=self.prospect,
            order_status=self.order_status,
            mode_of_collection=self.mode_of_collection,
            expected_payment_amount=self.expected_payment_amount,
            expected_payment_date=self.expected_payment_date,
            next_meeting_date=self.next_meeting_date,
            meeting_done=self.meeting_done,
            payment_recieved=self.payment_recieved,
            final_due_date=self.final_due_date,
            soa_amount=self.soa_amount,
            expected_pdc=self.expected_pdc,
            expected_cdc=self.expected_cdc,
            expected_tt=self.expected_tt,
            expected_cash=self.expected_cash,
            collected_pdc=self.collected_pdc,
            collected_cdc=self.collected_cdc,
            collected_tt=self.collected_tt,
            collected_cash=self.collected_cash,
            due_amount=self.due_amount,
            is_active=self.is_active,
            created_by=self.created_by,
            remarks=self.remarks,
        )

        # Set many-to-many relationships for history
        history.hardwarematerials.set(self.hardwarematerials.all())
        history.timbermaterials.set(self.timbermaterials.all())

        today = timezone.now().date()

            # Get or create the DailySalesSummary for today
        summary, created = DailySalesSummary.objects.get_or_create(timestamp=today)

            # Recalculate the values on every login
        today_order = SalesWeb.objects.filter(updated_at__date=today).aggregate(total=Sum('soa_amount'))['total'] or 0
        total_order = SalesWeb.objects.aggregate(total=Sum('soa_amount'))['total'] or 0
        today_received = SalesWeb.objects.filter(updated_at__date=today).aggregate(total=Sum('payment_recieved'))['total'] or 0
        total_received = SalesWeb.objects.aggregate(total=Sum('payment_recieved'))['total'] or 0

            # Update the summary
        summary.today_order_value = today_order
        summary.total_order_value = total_order
        summary.today_recieved_value = today_received
        summary.total_recieved_value = total_received
        summary.save()

    class Meta:
        ordering = ['-updated_at']

class CollectionAmount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salesweb = models.ForeignKey(SalesWeb, on_delete=models.CASCADE, related_name="recived_history")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




class SalesWebHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salesweb = models.ForeignKey(SalesWeb, on_delete=models.CASCADE, related_name="history_entries")
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    call_status = models.ForeignKey(CallStatus, on_delete=models.CASCADE)
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.ForeignKey(OrderStatusType, on_delete=models.CASCADE, null=True, blank=True)
    # payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    mode_of_collection = models.CharField(max_length=10, null=True, blank=True)
    expected_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_payment_date = models.DateField(null=True, blank=True)
    next_meeting_date = models.DateField(null=True, blank=True)
    meeting_done = models.BooleanField(default=False)
    payment_recieved = models.IntegerField(default=0, null=True, blank=True)
    final_due_date = models.DateField(null=True, blank=True)
    soa_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    expected_pdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_cdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_tt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_pdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_cdc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_tt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    due_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created")
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ManyToMany snapshot
    hardwarematerials = models.ManyToManyField(HardWareMaterial, blank=True)
    timbermaterials = models.ManyToManyField(TimberMaterial, blank=True)

    class Meta:
        ordering = ['-created_at']



class Meetinglog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_web = models.ForeignKey('SalesWeb', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=20, decimal_places=12, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=12, null=True, blank=True)
    location_name = models.CharField(max_length=250, null=True, blank=True)
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    meeting_status = models.BooleanField(default=False)
    payment_collected = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)

class DailySalesSummary(models.Model):
    today_order_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_order_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    today_recieved_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_recieved_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    timestamp = models.DateField(auto_now_add=True)
