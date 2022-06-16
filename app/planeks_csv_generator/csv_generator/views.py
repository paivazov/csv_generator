from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView

from planeks_csv_generator.csv_generator.models import DataSet, DataColumn
from planeks_csv_generator.csv_generator.forms import (  # noqa
    DataColumnForm,
    DataSetForm,
)


class CreateDataSetView(LoginRequiredMixin, FormView):
    template_name = 'csv_generator/create_dataset.html'
    form_class = DataSetForm

    def __init__(self, **kwargs):
        self.dataset = None
        super().__init__(**kwargs)

    def get_success_url(self):
        return reverse("create-schema", kwargs={"dataset_id": self.dataset.id})

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        if user is not None:
            self.dataset = DataSet.objects.create(**data, user=user)
        else:
            return redirect("/login/")
        return super().form_valid(form)


class DatasetListView(LoginRequiredMixin, ListView):
    template_name = "csv_generator/schemas_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = DataSet.objects.filter(user=user)
            return queryset


class DatasetDetailView(LoginRequiredMixin, View):
    def get(self, request, dataset_id):
        columns = DataColumn.objects.filter(data_set__user=request.user)
        data_columns = DataColumn.objects.filter(data_set_id=dataset_id)
        dataset_form = DataSetForm()
        context = {
            "dataset_form": dataset_form,
            "data_columns": data_columns,
            "columns": columns,
            "dataset_id": dataset_id,
        }

        return render(request, "csv_generator/create_schema.html", context)


class SchemaFormCreationView(LoginRequiredMixin, View):
    def get(self, request, dataset_id):
        datacolumn_form = DataColumnForm()
        context = {
            "form": datacolumn_form,
            "dataset_id": dataset_id,
        }
        return render(
            request, "csv_generator/partials/book_form.html", context
        )

    def post(self, request, dataset_id):
        data_set = DataSet.objects.get(pk=dataset_id)
        datacolumn_form = DataColumnForm(request.POST)

        if datacolumn_form.is_valid():
            with atomic():
                data_column = datacolumn_form.save(commit=False)
                data_column.data_set = data_set
                data_column.save()
            context = {"column": data_column, "dataset_id": dataset_id}
            return render(
                request,
                "csv_generator/partials/book_detail.html",
                context=context,
            )
        else:
            return redirect("create-schema", dataset_id=dataset_id)


class SchemaFormManagingView(LoginRequiredMixin, View):
    def get(self, request, dataset_id, datacolumn_id):
        data_set = get_object_or_404(DataSet, id=dataset_id)

        data_column = self._grab_datacloumn_and_check_permission(
            data_set, datacolumn_id
        )

        context = {"column": data_column, "dataset_id": dataset_id}
        return render(
            request,
            "csv_generator/partials/book_detail.html",
            context=context,
        )

    def post(self, request, dataset_id, datacolumn_id):
        data_set = get_object_or_404(DataSet, id=dataset_id)

        data_column = self._grab_datacloumn_and_check_permission(
            data_set, datacolumn_id
        )
        form = DataColumnForm(request.POST)
        if form.is_valid():
            with atomic():
                data_column.order = form.cleaned_data.get("order")
                data_column.column_name = form.cleaned_data.get("column_name")
                data_column.column_type = form.cleaned_data.get("column_type")
                data_column.save()
            return redirect(
                "detail-schema",
                dataset_id=dataset_id,
                datacolumn_id=datacolumn_id,
            )
        context = {
            "form": form,
            "data_column": data_column,
            "dataset_id": dataset_id,
        }
        return render(
            request, "csv_generator/partials/book_form.html", context
        )

    def delete(self, request, dataset_id, datacolumn_id):
        data_set = get_object_or_404(DataSet, id=dataset_id)
        data_column = self._grab_datacloumn_and_check_permission(
            data_set, datacolumn_id
        )
        data_column.delete()
        return HttpResponse(status=200)

    def _grab_datacloumn_and_check_permission(self, data_set, datacolumn_id):
        if data_set.user == self.request.user:
            return get_object_or_404(DataColumn, id=datacolumn_id)
        else:
            return HttpResponseForbidden("<h2>You are not allowed</h2>")


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
