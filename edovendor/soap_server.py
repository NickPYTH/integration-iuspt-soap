from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt
from spyne import ServiceBase, rpc, Application
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication

from edovendor.models import create_edovendor

# Пространство имен согласно проекту
NS = "http://inform.gazprom.ru/I/IUSPT/ERP/EDOVendor"


class EDOVendorRecord(ComplexModel):
    __namespace__ = NS

    INN = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=25)
    KPP = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=9)
    FNS_ID = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=46)
    Vendor = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=10)


class StatusResult(ComplexModel):
    __namespace__ = NS

    Status = Unicode.customize(min_occurs=1, max_occurs=1)
    Message = Unicode.customize(min_occurs=0, max_occurs=1)


class EDOVendorService(ServiceBase):
    @rpc(
        Array(EDOVendorRecord, min_occurs=1, max_occurs=Decimal("Infinity"), wrapped=False),
        _in_variable_names={"record": "Record"},  # Приходит Record, а переменная record
        _returns=StatusResult.customize(max_occurs=1, nillable=False),
    )
    def EDOVendorReceiverAsync(self, record):
        try:
            for item in record:
                create_edovendor(item)
        except ValueError as exc:
            return StatusResult(Status="REJECTED", Message=str(exc))

        return StatusResult(Status="ACCEPTED", Message="Processed successfully")


soap_application = Application(
    [EDOVendorService],
    tns=NS,
    in_protocol=Soap11(validator="soft"),
    out_protocol=Soap11(),
    name="EDOVendorService",
)

django_soap_application = csrf_exempt(DjangoApplication(soap_application))
