from flask import request, jsonify

from app import app, db
from app.models import Document


@app.route('/search')
def search_handler():
    query = request.args['q']
    result = Document.search(query)
    if result[1] > 0:
        reordered_query = result[0].order_by(False).order_by(Document.created_date)
        response = [row.serialize() for row in reordered_query.limit(20).all()]
        return jsonify(response)
    else:
        return "", 204


@app.route('/<int:doc_id>', methods=['DELETE'])
def del_handler(doc_id):
    doc = Document.query.get_or_404(id=doc_id)
    doc.delete()
    db.session.commit()
    return "", 204
