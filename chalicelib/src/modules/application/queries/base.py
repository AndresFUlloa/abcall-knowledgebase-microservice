from chalicelib.src.modules.infrastructure.factory import KnowledgeBaseFactory
from chalicelib.src.seedwork.application.commands import CommandHandler
from chalicelib.src.seedwork.application.queries import QueryHandler


class QueryBaseHandler(QueryHandler):
    def __init__(self):
        self._knowledge_base_factory: KnowledgeBaseFactory = KnowledgeBaseFactory()

    @property
    def knowlede_base_factory(self):
        return self._knowledge_base_factory