from django.urls import path

from planeks_csv_generator.csv_generator.views import (
    DatasetListView,
    DatasetDetailView,
    CreateDataSetView,
    SchemaFormCreationView,
    SchemaFormManagingView,
)

urlpatterns = [
    path(
        "create/",
        CreateDataSetView.as_view(),
        name="create-dataset",
    ),
    path("", DatasetListView.as_view()),
    path(
        "<int:dataset_id>/",
        DatasetDetailView.as_view(),
        name="create-schema",
    ),
    path(
        "<int:dataset_id>/schema_column/<int:datacolumn_id>/",
        SchemaFormManagingView.as_view(),
        name="detail-schema",
    ),
    path(
        "<int:dataset_id>/schema_column/",
        SchemaFormCreationView.as_view(),
        name="create-schema",
    ),
    # path("create_csv/", some_view),
]
