from django.forms import ModelForm, Form, IntegerField

from planeks_csv_generator.csv_generator.models import DataSet, DataColumn


class DataSetForm(ModelForm):
    class Meta:
        model = DataSet
        fields = ('name', "string_character", "line_separator")


class DataColumnForm(ModelForm):
    class Meta:
        model = DataColumn
        fields = (
            'order',
            "column_type",
            "column_name",
        )


class RowQuantityForm(Form):
    rows = IntegerField(min_value=1)
