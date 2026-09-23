from django.views.decorators.csrf import csrf_exempt
from spyne import Application, Array, ComplexModel, Integer, Unicode, rpc
from spyne.model.primitive import Date
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase

from department.soap_server import DepartmentType
from department.soap_server import to_soap as department_to_soap
from .models import (
    Employer,
    create_employer,
    delete_employer,
    get_employer,
    list_employers,
    update_employer,
)


NS = "http://example.local/employer"


class EmployerType(ComplexModel):
    """xml карточка, из нее спайн создает xsd"""
    __namespace__ = NS
    Id = Integer.customize(min_occurs=0, max_occurs=1)
    LastName = Unicode.customize(min_occurs=1, max_occurs=1)
    FirstName = Unicode.customize(min_occurs=1, max_occurs=1)
    MiddleName = Unicode.customize(min_occurs=0, max_occurs=1)
    Inn = Unicode.customize(min_occurs=1, max_occurs=1)
    Snils = Unicode.customize(min_occurs=0, max_occurs=1)
    Position = Unicode.customize(min_occurs=1, max_occurs=1)
    Department = DepartmentType.customize(min_occurs=1, max_occurs=1)
    HireDate = Date.customize(min_occurs=1, max_occurs=1)
    Phone = Unicode.customize(min_occurs=0, max_occurs=1)
    Email = Unicode.customize(min_occurs=0, max_occurs=1)


class StatusResult(ComplexModel):
    __namespace__ = NS
    Status = Unicode.customize(min_occurs=1, max_occurs=1)
    Message = Unicode.customize(min_occurs=0, max_occurs=1)
    Id = Integer.customize(min_occurs=0, max_occurs=1)


class GetEmployerResult(ComplexModel):
    __namespace__ = NS
    Status = Unicode.customize(min_occurs=1, max_occurs=1)
    Message = Unicode.customize(min_occurs=0, max_occurs=1)
    Employer = EmployerType.customize(min_occurs=0, max_occurs=1)


def to_soap(obj: Employer):
    return EmployerType(
        Id=obj.pk,
        LastName=obj.last_name,
        FirstName=obj.first_name,
        MiddleName=obj.middle_name or None,
        Inn=obj.inn,
        Snils=obj.snils or None,
        Position=obj.position,
        Department=department_to_soap(obj.department),
        HireDate=obj.hire_date,
        Phone=obj.phone or None,
        Email=obj.email or None,
    )


class EmployerService(ServiceBase):
    # 1. Первый параметр для определения входящего типа
    # 2. Второй это то как в envelope называть передаваемую сущность, если убрать то name='record'
    # ps вообще название берется от имени аргумента в функции def CreateEmployer(self, record)
    # 3. Что возвращаем
    @rpc(EmployerType, _in_variable_names={"record": "Employer"}, _returns=StatusResult)
    def CreateEmployer(self, record):
        try:
            obj = create_employer(record)
        except ValueError as exc:
            return StatusResult(Status="REJECTED", Message=str(exc))
        return StatusResult(Status="OK", Message="created", Id=obj.pk)

    @rpc(Integer, _in_variable_names={"id": "Id"}, _returns=GetEmployerResult)
    def GetEmployer(self, id):
        obj = get_employer(id)
        if obj is None:
            return GetEmployerResult(Status="NOT_FOUND", Message=f"{id}")
        response = to_soap(obj)
        return GetEmployerResult(Status="OK", Employer=response)

    @rpc(_returns=Array(EmployerType))
    def GetEmployerList(self):
        return [to_soap(obj) for obj in list_employers()]

    @rpc(EmployerType, _in_variable_names={"record": "Employer"}, _returns=GetEmployerResult)
    def UpdateEmployer(self, record):
        if record.Id is None:
            return StatusResult(Status="REJECTED", Message="id is null")
        try:
            update_employer(record.Id, record)
            return GetEmployerResult(Status="OK", Message="update ok", Employer=record)
        except Exception:
            return StatusResult(Status="REJECTED", Message="update error")

    @rpc(Integer, _in_variable_names={"id": "Id"}, _returns=StatusResult)
    def DeleteEmployer(self, id):
        try:
            result = delete_employer(id)
            if result:
                return StatusResult(Status="OK")
            else:
                return StatusResult(Status="REJECTED", Message="employer not found")
        except Exception:
            return StatusResult(Status="REJECTED", Message="delete error")


soap_application = Application(
    [EmployerService],
    tns=NS,
    in_protocol=Soap11(validator="soft"),
    out_protocol=Soap11(),
    name="EmployerService",
)

django_soap_application = csrf_exempt(DjangoApplication(soap_application))
