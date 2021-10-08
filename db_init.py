import csv
from datetime import datetime

from app.models import Document
from app import db


def import_from_csv(filename):
    db.create_all()
    with open(filename, encoding='utf-8') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            row['created_date'] = datetime.fromisoformat(row['created_date'])
            db.session.add(Document(**row))
        db.session.commit()
