from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    CharField,
    DateField,
    PositiveIntegerField,
    ForeignKey,
    CASCADE,
    EmailField,
    URLField,
    TextField,
    IntegerField,
)

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
    ("name", "Full Name"),
    ("job", "Job"),
    ("email", "Email"),
    ("domain", "Domain Name"),
    ("p_number", "Phone Number"),
    ("company", "Company Name"),
    ("text", "Text"),
    ("int", "Integer"),
    ("address", "Address"),
    ("date", "Date"),
)

LINE_SEPARATOR_CHOICES = (
    (",", "Comma (,)"),
    (";", "Semicolon (;)"),
    ("\t", r"tab (\t)"),
)

STRING_CHARACTER_CHOICES = (
    ('"', 'Double-quote (")'),
    ("'", "Quote (')"),
    ("|", "Pipe (|)"),
)


class DataSet(Model):
    name = CharField(max_length=120, blank=False, verbose_name="Data set name")
    line_separator = CharField(
        max_length=64, choices=LINE_SEPARATOR_CHOICES, default=","
    )
    string_character = CharField(
        max_length=64, choices=STRING_CHARACTER_CHOICES, default='"'
    )
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
