import csv
from datetime import datetime

from app.models import Document
from app import db


def import_from_csv(filename):
    print("Creating DB...")
    db.create_all()
    with open(filename, encoding='utf-8') as csvfile:
        data_reader = csv.DictReader(csvfile)
        print("Importing data from .csv file...")
        for row in data_reader:
            row['created_date'] = datetime.fromisoformat(row['created_date'])
            db.session.add(Document(**row))
        print("Save data to new DB...")
        db.session.commit()
        print("Complete")


if __name__ == "__main__":
    import_from_csv("posts.csv")
