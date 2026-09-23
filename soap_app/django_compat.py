"""Django 4.2 + Python 3.14: copy(super()) breaks template Context in admin."""

from copy import copy

from django.template.context import BaseContext


def _basecontext_copy(self):
    duplicate = BaseContext()
    duplicate.__class__ = self.__class__
    duplicate.__dict__ = copy(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate


BaseContext.__copy__ = _basecontext_copy
