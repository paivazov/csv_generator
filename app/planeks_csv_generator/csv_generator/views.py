from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView, DetailView

from planeks_csv_generator.csv_generator.models import DataSet, DataColumn
from planeks_csv_generator.csv_generator.forms import (  # noqa
    DataColumnForm,
    DataSetForm,
)


class ManageSchemaView(LoginRequiredMixin, View):
    def get(self, request, pk):
        columns = DataColumn.objects.filter(data_set__user=request.user)
        data_columns = DataColumn.objects.filter(data_set_id=pk)
        dataset_form = DataSetForm()
        context = {
            "dataset_form": dataset_form,
            "data_columns": data_columns,
            "columns": columns,
            "dataset_id": pk,
        }

        return render(request, "csv_generator/create_schema.html", context)

    def post(self, request, pk):
        data_set = DataSet.objects.get(pk=pk)
        datacolumn_form = DataColumnForm(request.POST)

        if datacolumn_form.is_valid():
            with atomic():
                data_column = datacolumn_form.save(commit=False)
                data_column.data_set = data_set
                data_column.save()
            context = {"column": data_column}
            return render(
                request,
                "csv_generator/partials/book_detail.html",
                context=context,
            )
        else:
            return redirect("create-schema-form")

    def delete(self, request, pk):
        data_column = get_object_or_404(DataColumn, id=pk)
        data_column.delete()
        return HttpResponse(status=200)

    def patch(self, request, pk):
        data_column = get_object_or_404(DataColumn, id=pk)
        form = DataColumnForm(request.POST, instance=data_column)

        if form.is_valid():
            form.save()
            return redirect("schema-detail", pk=data_column.id)

        context = {
            "form": form,
            "data_column": data_column,
        }

        return render(
            request, "csv_generator/partials/book_form.html", context
        )


class DetailColumnView(DetailView):
    model = DataColumn
    template_name = "csv_generator/partials/book_detail.html"


def create_schema_form(request, dataset_id):
    datacolumn_form = DataColumnForm()
    context = {
        "form": datacolumn_form,
        "dataset_id": dataset_id,
    }
    return render(request, "csv_generator/partials/book_form.html", context)


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="somefilename.csv"'
        },
    )

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('csv_generator/my_template_name.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response


class CreateDataSetView(LoginRequiredMixin, FormView):
    template_name = 'csv_generator/create_dataset.html'
    form_class = DataSetForm

    def __init__(self, **kwargs):
        self.dataset = None
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse("create-schema", kwargs={"pk": self.dataset.id})

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        if user is not None:
            self.dataset = DataSet.objects.create(**data, user=user)
        else:
            return redirect("/login/")
        return super().form_valid(form)


class SchemasListView(LoginRequiredMixin, ListView):
    template_name = "csv_generator/schemas_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = DataSet.objects.filter(user=user)
            return queryset
