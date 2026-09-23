import io
import json

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from zeep import Client
from zeep.transports import Transport

from soap_app.models import SoapTransaction


class CaptureTransport(Transport):
    def __init__(self):
        super().__init__()
        self.last_url = None
        self.last_headers = None
        self.last_body = None

    def post(self, address, message, headers, timeout=None, operation=None):

        self.last_url = address
        self.last_headers = headers
        self.last_body = message  # ловим сформированный envelope

        raise RuntimeError("__CAPTURED__")


def send_request_to_proxy(proxy_url, wsdl_url, envelope, soap_action, soap_transaction):
    envelope = envelope.decode("utf-8")
    response = requests.post(
        proxy_url,
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
        auth=("Integration Service", "1"),
        json={
            "wsdl_url": wsdl_url,
            "envelope": envelope,
            "soap_action": soap_action,
            "transaction_id": soap_transaction.id
        },
        timeout=90,
    )
    response_pretty = json.loads(response.text)
    if 'value' in response_pretty.keys():
        value_pretty = json.loads(response_pretty['value'])
        xml = value_pretty['body']
        if value_pretty['status'] == "ok":
            soap_transaction.status = 'processed'
            soap_transaction.response_data = xml
            soap_transaction.save()
        else:
            soap_transaction.status = 'error'
            soap_transaction.response_data = xml
            soap_transaction.save()


def get_wsdl_by_wsdl_url(get_wsdl_url, wsdl_url):
    response = requests.post(
        get_wsdl_url,
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
        auth=("Integration Service", "1"),
        json={
            "wsdl_url": wsdl_url,
        },
        timeout=90,
    )
    try:
        response_pretty = json.loads(response.text)
        if 'value' in response_pretty.keys():
            value_pretty = json.loads(response_pretty['value'])
            wsdl = value_pretty['body']
            return wsdl
    except Exception as e:
        print(e)


@api_view(['POST'])
def send_edovendor_test(request):
    """Для отладки"""
    WSDL_URL = "http://127.0.0.1:8000/edovendor/soap/?wsdl"
    transport = CaptureTransport()
    client = Client(WSDL_URL, transport=transport)
    record = {
        "INN": "7701234567",
        "KPP": "770101001",
        "FNS_ID": "1234567890",
        "Vendor": "ООО Ромашка",
    }
    response = client.service.EDOVendorReceiverAsync(Record=[record])

    return Response({
        "Status": response.Status,
        "Message": response.Message
    })


@api_view(['POST'])
def send_envelope_via_proxy(request):
    if "wsdl_url" not in request.data:
        return Response({
            "Status": "error",
            "Message": "wsdl_url not provided"
        }, status=400)
    if "proxy_url" not in request.data:
        return Response({
            "Status": "error",
            "Message": "proxy_url not provided"
        }, status=400)
    if "soap_action" not in request.data:
        return Response({
            "Status": "error",
            "Message": "soap_action not provided"
        }, status=400)
    if "payload" not in request.data:
        return Response({
            "Status": "error",
            "Message": "payload not provided"
        }, status=400)
    if "get_wsdl_url" not in request.data:
        return Response({
            "Status": "error",
            "Message": "get_wsdl_url not provided"
        }, status=400)

    proxy_url = request.data["proxy_url"]
    wsdl_url = request.data["wsdl_url"]
    get_wsdl_url = request.data["get_wsdl_url"]
    soap_action = request.data["soap_action"]
    payload = request.data["payload"]

    # Инициализируем транзакцию
    soap_transaction = SoapTransaction.objects.create(
        direction="out"
    )
    soap_transaction.save()

    # Получаем WSDL из SOAP сервиса через прокси метод
    wsdl_text = ""
    try:
        wsdl_text = get_wsdl_by_wsdl_url(get_wsdl_url, wsdl_url)
    except Exception as e:
        soap_transaction.status = "error"
        soap_transaction.response_data = e.__str__()
        soap_transaction.save()
        return Response({
            "Status": "error",
            "Message": e.__str__()
        }, status=400)

    # Создаем клиент с уже полученным через прокси WSDL
    try:
        transport = CaptureTransport()
        client = Client(io.BytesIO(wsdl_text.encode("utf-8")), transport=transport)
    except Exception as e:
        soap_transaction.status = "error"
        soap_transaction.response_data = e.__str__()
        soap_transaction.save()
        return Response({
            "Status": "error",
            "Message": e.__str__()
        }, status=400)

    # Тут обязательно летит исключение тк обработка кастомным классом Transport
    try:
        soap_method = getattr(client.service, soap_action, None)
        if soap_method is None:
            soap_transaction.status = "error"
            soap_transaction.response_data = f"soap action '{soap_action}' not provided"
            soap_transaction.save()
            return Response({
                "Status": "error",
                "Message": f"soap action '{soap_action}' not provided"
            }, status=400)
        soap_method(Record=payload)
        #client.service.EDOVendorReceiverAsync(Record=payload)
    except Exception as e:
        if e.__str__() == "__CAPTURED__":
            soap_transaction.request_data = transport.last_body.decode("utf-8")
            soap_transaction.save()
        else:
            soap_transaction.status = "error"
            soap_transaction.response_data = e.__str__()
            soap_transaction.save()
            return Response({
                "Status": "error",
                "Message": e.__str__()
            }, status=400)

    try:
        send_request_to_proxy(proxy_url, wsdl_url, transport.last_body, soap_action, soap_transaction)
    except Exception as e:
        soap_transaction.status = "error"
        soap_transaction.response_data = e.__str__()
        soap_transaction.save()
        return Response({
            "Status": "error",
            "Message": e.__str__()
        }, status=400)

    return Response({
        "Status": "ok",
        "Message": "Request sent to proxy"
    })


@api_view(['POST'])
def send_edovendor(request):
    """Для отладки"""
    WSDL_URL = "http://127.0.0.1:8000/edovendor/soap/?wsdl"
    client = Client(WSDL_URL)
    record_list = request.data
    response = client.service.EDOVendorReceiverAsync(Record=record_list)
    return Response({
        "Status": response.Status,
        "Message": response.Message
    })


@api_view(['POST'])
def send_agrcard_test(request):
    """Для отладки"""
    WSDL_URL = "http://127.0.0.1:8000/agrcard/soap/?wsdl"
    client = Client(WSDL_URL)
    record = {
        "IUSPTCard": "ABC123",
        "DirectumCard": 42,
        "CR_ED": "CR-1",
        "IUSPTCard_2": "XYZ",
        "Card_Date": "2026-09-21",
        "HistID": "H-001",
        "VendorCard": "VC-1",
        "CardTitle": "Договор",
        "IUSPTVendor": "Ромашка",
        "CardKurator": "Иванов",
    }
    response = client.service.AgrCardReceiverAsync(Record=[record, record])
    return Response({
        "Status": response.Status,
        "Message": response.Message
    })


@api_view(['POST'])
def send_agrcard(request):
    """Для отладки"""
    WSDL_URL = "http://127.0.0.1:8000/agrcard/soap/?wsdl"
    client = Client(WSDL_URL)
    record_list = request.data
    response = client.service.AgrCardReceiverAsync(Record=record_list)
    return Response({
        "Status": response.Status,
        "Message": response.Message
    })
