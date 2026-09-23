from rest_framework import serializers

from .models import SoapTransaction


class SoapTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoapTransaction
        fields = [
            "id",
            "direction",
            "request_data",
            "response_data",
            "external_response",
            "status",
            "created_at",
            "updated_at",
        ]
