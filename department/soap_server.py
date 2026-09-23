from django.views.decorators.csrf import csrf_exempt
from spyne import ComplexModel, Integer, Unicode, rpc, Array, Application
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication

from department.models import Department, create_department, list_departments

NS = "http://example.local/department"


class DepartmentType(ComplexModel):
    __namespace__ = NS
    Id = Integer.customize(min_occurs=0, max_occurs=1)
    Name = Unicode.customize(min_occurs=0, max_occurs=1)


class StatusResult(ComplexModel):
    __namespace__ = NS
    Status = Unicode.customize(min_occurs=1, max_occurs=1)
    Message = Unicode.customize(min_occurs=0, max_occurs=1)
    Id = Integer.customize(min_occurs=0, max_occurs=1)


class GetDepartmentResult(ComplexModel):
    __namespace__ = NS
    Status = Unicode.customize(min_occurs=0, max_occurs=1)
    Message = Unicode.customize(min_occurs=0, max_occurs=1)
    Department = DepartmentType.customize(min_occurs=0, max_occurs=1)


def to_soap(obj: Department):
    return DepartmentType(
        Id=obj.id,
        Name=obj.name
    )


class DepartmentService(ServiceBase):
    @rpc(DepartmentType, _in_variable_names={"record": "Department"}, _returns=StatusResult)
    def CreateDepartment(self, record):
        try:
            obj = create_department(record)
        except Exception as e:
            return StatusResult(Status="REJECTED", Message="Department create failed")
        return StatusResult(Status="OK", Message="Created", Id=obj.id)

    @rpc(_returns=Array(DepartmentType))
    def GetDepartmentList(self):
        return [to_soap(department) for department in list_departments()]


soap_application = Application(
    services=[DepartmentService],
    tns=NS,
    in_protocol=Soap11(validator='soft'),
    out_protocol=Soap11(),
    name='DepartmentService'
)

django_soap_application = csrf_exempt(DjangoApplication(soap_application))
