from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import SoapTransaction
from .serializers import SoapTransactionSerializer


class SoapTransactionListView(ModelViewSet):
    queryset = SoapTransaction.objects.all()
    serializer_class = SoapTransactionSerializer
