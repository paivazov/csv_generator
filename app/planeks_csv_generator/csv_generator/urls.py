from django.urls import path

from planeks_csv_generator.csv_generator.views import (
    DatasetListView,
    DatasetDetailView,
    CreateDataSetView,
    SchemaFormCreationView,
    SchemaFormManagingView,
    CSVGenerateView,
    DatasetGeneratingView,
    DatasetDeleteView,
    DownloadView,
)

urlpatterns = [
    path(
        "create/",
        CreateDataSetView.as_view(),
        name="create-dataset",
    ),
    path("", DatasetListView.as_view(), name="list-dataset"),
    path(
        "<int:dataset_id>/",
        DatasetDetailView.as_view(),
        name="detail-dataset",
    ),
    path("<int:pk>/delete/", DatasetDeleteView.as_view(), name="delete"),
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
        "generate/",
        CSVGenerateView.as_view(),
        name="generate-csv",
    ),
    path("csv/", DatasetGeneratingView.as_view(), name="specify-csv"),
    path(
        "csv/download/<int:dataset_id>/",
        DownloadView.as_view(),
        name="download-csv",
    )
    # path("create_csv/", some_view),
]
