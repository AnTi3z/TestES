from app import es


def add_to_index(index: str, model):
    if not es:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index=index, doc_type=index, id=model.id, document=payload)


def remove_from_index(index: str, model):
    if not es:
        return
    es.delete(index=index, doc_type=index, id=model.id)


def query_index(index: str, query: str, page: int, per_page: int, filter_fields=None):
    if not es:
        return [], 0
    search = es.search(
        index=index,
        query={'multi_match': {'query': query, 'fields': ['*']}},
        from_=(page - 1) * per_page,
        size=per_page,
        )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
