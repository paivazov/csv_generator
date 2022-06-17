from django.urls import path

from planeks_csv_generator.csv_generator.views import (
    DatasetListView,
    DatasetDetailView,
    CreateDataSetView,
    SchemaFormCreationView,
    SchemaFormManagingView,
    CSVGenerateView,
    DatasetGeneratingView,
)

urlpatterns = [
    path(
        "create/",
        CreateDataSetView.as_view(),
        name="create-dataset",
    ),
    path("", DatasetListView.as_view(), name="dataset-list"),
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
    path(
        "<int:dataset_id>/generate/",
        CSVGenerateView.as_view(),
        name="generate-csv",
    ),
    path("schema_action/", DatasetGeneratingView.as_view())
    # path("create_csv/", some_view),
]
