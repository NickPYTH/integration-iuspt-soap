from django.views.decorators.csrf import csrf_exempt
from spyne import ServiceBase, rpc, Application
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Unicode, Date, Integer
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication

from agrcard.models import soap_to_payload, create_agrcard

NS = "http://inform.gazprom.ru/I/KSAD_SRGT/DIRECTUM/AgrCard"


class AgrCardRecord(ComplexModel):
    __namespace__ = NS

    IUSPTCard = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=10)
    DirectumCard = Integer.customize(min_occurs=1, max_occurs=1, nillable=False)
    CR_ED = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=1)
    IUSPTCard_2 = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=10)
    Card_Date = Date.customize(min_occurs=1, max_occurs=1, nillable=False)
    HistID = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=10)
    VendorCard = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=10)
    CardTitle = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=255)
    IUSPTVendor = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=10)
    CardKurator = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False, max_length=12)


class StatusResult(ComplexModel):
    __namespace__ = NS

    Status = Unicode.customize(min_occurs=1, max_occurs=1, nillable=False)
    Message = Unicode.customize(min_occurs=0, max_occurs=1, nillable=False)


class AgrCardService(ServiceBase):
    @rpc(
        AgrCardRecord.customize(min_occurs=1, max_occurs="unbounded", nillable=False),
        _in_variable_names={"record": "Record"},
        _returns=StatusResult.customize(min_occurs=1, nillable=False)
    )
    def AgrCardReceiverAsync(self, record):
        try:
            for item in record:
                create_agrcard(item)
        except ValueError as exc:
            return StatusResult(Status="REJECTED", Message=str(exc))
        return StatusResult(Status="ACCEPTED", Message="Processed")


soap_application = Application(
    services=[AgrCardService],
    tns=NS,
    in_protocol=Soap11(validator='soft'),
    out_protocol=Soap11(),
    name='AgrCardService'
)

django_soap_application = csrf_exempt(DjangoApplication(soap_application))
