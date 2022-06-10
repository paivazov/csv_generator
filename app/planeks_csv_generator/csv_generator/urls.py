from django.urls import path

from planeks_csv_generator.csv_generator.views import SchemasListView, some_view, CreateSchema, create_schema_form, \
    CreateDataSetView

urlpatterns = [
    path("", SchemasListView.as_view()),
    path("create/", some_view),
    path("create_schema/<int:pk>", CreateSchema.as_view(), name="create-schema"),
    path("create_schema_form/", create_schema_form, name="create-schema-form"),
    path("create_dataset/", CreateDataSetView.as_view(), name="create-dataset-form")
]
