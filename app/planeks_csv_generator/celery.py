from celery import Celery

from planeks_csv_generator.csv_generator.services import generate_csv_schema

app = Celery(
    "csv_generator",
    # backend=settings.CELERY_RESULT_BACKEND,
    # broker=settings.CELERY_BROKER_URL,
    backend="redis://redis/1",
    broker="redis://redis/0",
)
app.autodiscover_tasks()


@app.task
def create_csv(
    row_quantity: int,
    dataset_id: int,
    user_id: int,
    columns: list,
    delimiter: str,
    quotechar: str,
):
    generate_csv_schema(
        row_quantity,
        dataset_id,
        user_id,
        columns,
        delimiter,
        quotechar,
    )
