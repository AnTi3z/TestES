from flask import request

from app import app
from models import Document


@app.route('/search')
def search_handler():
    query = request.args['q']
    result = Document.search(query)
    if result[1] > 0:
        return result[0].order_by(False).order_by(Document.created_date).limit(20).all()
    return result


@app.route('/<int:doc_id>', methods=['DELETE'])
def del_handler(doc_id):
    Document.query.filter_by(id=doc_id).delete()
