from django.contrib.auth import authenticate, login
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, ListView, CreateView
import csv

from planeks_csv_generator.books.forms import BookForm
from planeks_csv_generator.books.models import Author, Book
from planeks_csv_generator.csv_generator.forms import DataSetForm, DataColumnForm
from planeks_csv_generator.csv_generator.models import DataSet, DataColumn


class CreateDataSetView(FormView):
    template_name = 'csv_generator/create_dataset.html'
    form_class = DataSetForm

    def __init__(self, **kwargs):
        self.dataset = None
        super().__init__(**kwargs)

    def get_success_url(self):
        return f'/schemas/create_schema/{self.dataset.id}'

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        if user is not None:
            self.dataset = DataSet.objects.create(**data, user=user)
        else:
            return redirect("/login/")
        return super().form_valid(form)


class CreateSchema(View):
    def get(self, request, pk):
        self.pk = pk
        columns = DataColumn.objects.filter(data_set__user=request.user)
        datacolumn_form = DataColumnForm()
        dataset_form = DataSetForm()
        context = {
            "dataset_form": dataset_form,
            # "datacolumn_form": datacolumn_form,
            "columns": columns
        }

        return render(request, "csv_generator/create_schema.html", context)

    def post(self, request, pk):
        data_set = DataSet.objects.get(pk=pk)
        datacolumn_form = DataColumnForm(request.POST)
        dataset_form = DataSetForm(request.POST)

        if datacolumn_form.is_valid():
            data_column = datacolumn_form.save(commit=False)
            data_column.data_set = data_set
            data_column.save()
            return redirect("detail-book", pk=data_column.id)
        else:
            return render(request, "csv_generator/partials/book_form.html", context={
                "form": datacolumn_form,
                "data_set_id": 2
            })

def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    if request.method == "POST":
        book.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def detail_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    context = {
        "book": book
    }
    return render(request, "book/partials/book_detail.html", context)


def create_schema_form(request):
    datacolumn_form = DataColumnForm()
    context = {
        "form": datacolumn_form
    }
    return render(request, "csv_generator/partials/book_form.html", context)


def create_book(request, pk):
    author = Author.objects.get(id=pk)
    books = Book.objects.filter(author=author)
    form = BookForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            book = form.save(commit=False)
            book.author = author
            book.save()
            return redirect("detail-book", pk=book.id)
        else:
            return render(request, "book/partials/book_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "author": author,
        "books": books
    }

    return render(request, "csv_generator/create_schema.html", context)


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
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


class SchemasListView(ListView):
    # model = DataSchema
    template_name = "csv_generator/schemas_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = DataSet.objects.filter(user=user)
            return queryset
