from flask_sqlalchemy import event
import asyncio

from app import db
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin:
    """
    Mixin класс, для моделей, по полям которых необходимо осуществлять полнотекстовый поиск.
    Имена аттрибутов, которые должны быть добавлены в индекс, перечисляются в аттрибуте
    __searchable__(список строк с именами аттрибутов).
    """
    @classmethod
    async def search(cls, expression: str, page: int = 1, per_page: int = 10000):
        """
        Полнотекстовый поиск по аттрибутам объектов модели

        :param expression: Строка поиска
        :param page: Порядковый номер "страницы" (default: 1)
        :param per_page: Кол-во результатов на одной "странице" (default: 10000)
        :return: Список из двух элементов: query-объект запроса, возвращающий объекты удовлетворяющих
         поисковому запросу и кол-во найденых объектов
        """
        ids, total = await query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    async def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                await add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                await add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                await remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    async def reindex(cls):
        """
        Полное обновление индекса в соответствии с моделью
        """
        for obj in cls.query:
            await add_to_index(cls.__tablename__, obj)


event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
event.listen(db.session, 'after_commit', lambda s: asyncio.run(SearchableMixin.after_commit(s)))


class Document(db.Model, SearchableMixin):
    id = db.Column(db.Integer, primary_key=True)
    rubrics = db.Column(db.String)
    text = db.Column(db.Text)
    created_date = db.Column(db.DateTime, index=True)
    __searchable__ = ['text']

    def __init__(self, rubrics, text, created_date):
        self.rubrics = rubrics
        self.text = text
        self.created_date = created_date

    def __repr__(self):
        return f'<Document id:{self.id} date:{self.created_date}>'

    def serialize(self):
        return {
            "id": self.id,
            "rubrics": self.rubrics,
            "text": self.text,
            "created_date": self.created_date
        }
