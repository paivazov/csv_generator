import csv
import os

from django.conf import settings

import faker

fake = faker.Faker("uk_UA")


def generate_csv_schema(
    row_quantity: int,
    dataset_id: int,
    user_id: int,
    columns: list,
    delimiter: str,
    quotechar: str,
):
    header = []
    types = []
    filename = settings.BASE_DIR.parent.joinpath(
        "var", "csv_files", f"user_{user_id}", f"dataset_{dataset_id}.csv"
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    for column in columns:
        header.append(column["column_name"])
        types.append(column["column_type"])

    with open(filename, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file, quotechar=quotechar, delimiter=delimiter)
        writer.writerow(header)

        for _ in range(row_quantity):
            writer.writerow([generate_fake_data(dt) for dt in types])


def generate_fake_data(value: str):
    # mypy is arguing on mypy, check it
    match value:
        case "name":
            return fake.name()
        case "job":
            return fake.job()
        case "email":
            return fake.email()
        case "domain":
            return fake.domain_name()
        case "p_number":
            return fake.phone_number()
        case "company":
            return fake.company()
        case "text":
            return fake.text()
        case "int":
            return fake.pyint()
        case "address":
            return fake.address()
        case "date":
            return fake.date()
