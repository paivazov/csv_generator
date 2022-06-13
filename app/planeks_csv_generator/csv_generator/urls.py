from django.urls import path

from planeks_csv_generator.csv_generator.views import (
    SchemasListView,
    some_view,
    ManageSchemaView,
    create_schema_form,
    CreateDataSetView,
    DetailColumnView,
)

urlpatterns = [
    path("", SchemasListView.as_view()),
    path("create/", some_view),
    path(
        "create_schema/<int:pk>",
        ManageSchemaView.as_view(),
        name="create-schema",
    ),
    path(
        "create_schema_form/<int:dataset_id>",
        create_schema_form,
        name="create-schema-form",
    ),
    path(
        "create_dataset/",
        CreateDataSetView.as_view(),
        name="create-dataset-form",
    ),
    path(
        "schema_detail/<int:pk>",
        DetailColumnView.as_view(),
        name="schema-detail",
    ),
]
