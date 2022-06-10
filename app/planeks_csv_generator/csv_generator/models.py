from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, DateField, FileField, PositiveIntegerField, ForeignKey, CASCADE, \
    DO_NOTHING, OneToOneField, EmailField, URLField, TextField, IntegerField

import pathlib
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

User = get_user_model()


class ColumnType(Model):
    full_name = CharField(max_length=120, verbose_name="Full Name")
    job = CharField(max_length=120, verbose_name="Job")
    email = EmailField()
    domain_name = URLField()
    phone_number = CharField(max_length=15)
    company_name = CharField(max_length=120)
    text = TextField()
    integer = IntegerField()
    address = CharField(max_length=150)
    date = DateField()


CHOICES = (
    ("Full Name", "Full Name"),
    ("Job", "Job"),
    ("Email", "Email"),
    ("Domain Name", "Domain Name"),
    ("Phone Number", "Phone Number"),
    ("Company Name", "Company Name"),
    ("Text", "Text"),
    ("Integer", "Integer"),
    ("Address", "Address"),
    ("Date", "Date"),
)

LINE_SEPARATOR_CHOICES = (
    (",", "Comma (,)"),
    (";", "Semicolon (;)"),
    ("\t", r"tab (\t)"),
)

STRING_CHARACTER_CHOICES = (
    ('"', 'Double-quote (")'),
    ("'", "Quote (')"),
)


class DataSet(Model):
    name = CharField(max_length=120, blank=False, verbose_name="Data set name")
    line_separator = CharField(max_length=64, choices=LINE_SEPARATOR_CHOICES, default=",")
    string_character = CharField(max_length=64, choices=STRING_CHARACTER_CHOICES, default='"')
    created_at = DateField(auto_now_add=True)
    modified_at = DateField(auto_now=True)

    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name


class DataColumn(Model):
    order = PositiveIntegerField()
    column_name = CharField(max_length=120)
    column_type = CharField(max_length=64, choices=CHOICES)
    data_set = ForeignKey(DataSet, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.column_name





