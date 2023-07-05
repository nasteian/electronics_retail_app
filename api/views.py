from django.db.models import F, Avg
from django_filters.rest_framework import DjangoFilterBackend
import qrcode
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from api.tasks import send_email_task
from api.email import email
from api.models import RetailObject, Product, Contact, Address, Employee
from api.permissions import IsActivePermission
from api.serializers import (
    RetailObjectSerializer,
    ProductObjectSerializer,
    AddressObjectSerializer,
    ContactObjectSerializer,
)


class RetailObjectViewSet(viewsets.ModelViewSet):
    """View for CRUD operations with a retail object"""

    serializer_class = RetailObjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product__id", "contact__address__city"]
    permission_classes = [IsActivePermission]

    def get_queryset(self):
        return RetailObject.objects.all().filter(employee=self.request.user.id)


class RetailObjectStatisticsViewSet(viewsets.ModelViewSet):
    """View for displaying statistics on objects whose debt
    exceeds the average debt of all objects."""

    serializer_class = RetailObjectSerializer
    permission_classes = [IsActivePermission]

    def get_queryset(self):
        debt_avg = RetailObject.objects.all().aggregate(Avg(F("debt")))
        data = RetailObject.objects.all().filter(debt__gt=debt_avg["debt__avg"])
        return data


class ProductObjectViewSet(viewsets.ModelViewSet):
    """View for CRUD operations with a product object"""

    queryset = Product.objects.all()
    serializer_class = ProductObjectSerializer
    permission_classes = [IsActivePermission]


class SendEmailView(generics.ListAPIView):
    """Sending messages to the employee's email with contact
    data about the retail object in the form of a qr code"""

    def get(self, *args, **kwargs):
        employee_retail_obj = RetailObject.objects.get(employee=self.request.user.id)
        contact = Contact.objects.get(object=employee_retail_obj)
        contact_email = ContactObjectSerializer(contact).data
        queryset = Address.objects.get(contacts=contact)
        address = AddressObjectSerializer(queryset).data
        contact_data = address | contact_email
        send_email_task.delay(contact_data, self.request.user.id)
        return Response(
            f"Email was sent with data :{contact_data}", status=status.HTTP_200_OK
        )
