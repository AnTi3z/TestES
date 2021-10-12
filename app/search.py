"""
Вспомогательные функции для работы с Elasticsearch API
"""
from app import es


def add_to_index(index: str, model):
    """
    Добавляет экземпляр модели в индекс

    :param index: Имя индекса
    :param model: Объект с __searchable__ аттрибутом
    """
    if not es:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index=index, doc_type=index, id=model.id, document=payload)


def remove_from_index(index: str, model):
    """
    Удаляет экземпляр модели из индекса

    :param index: Имя индекса
    :param model: Индексированый объект, который необходимо удалить из индекса
    """
    if not es:
        return
    es.delete(index=index, doc_type=index, id=model.id)


def query_index(index: str, query: str, page: int, per_page: int):
    """
    Полнотекстовый поиск документов в индексе

    :param index: Имя индекса
    :param query: Строка для поиска по проиндексированым полям (должны быть заданы в __searcheable__ аттрибуте модели)
    :param page: Порядковый номер "страницы"
    :param per_page: Кол-во результатов на одной "странице"
    :return: Список из двух элементов: список id найденных документов и кол-во найденых документов
    """
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
