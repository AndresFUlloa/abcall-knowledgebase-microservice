from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import KnowledgeBaseArticleRepository


@dataclass
class GetKnowledgebaseArticleQuery(Query):
    article_id: int


class GetKnowledgebaseArticleHandler(QueryBaseHandler):
    def handle(self, query: GetKnowledgebaseArticleQuery):
        repository = self.knowlede_base_factory.create_object(KnowledgeBaseArticleRepository)
        result = repository.get(query.article_id)
        return QueryResult(result=result)


@execute_query.register(GetKnowledgebaseArticleQuery)
def execute_get_client(query: GetKnowledgebaseArticleQuery):
    handler = GetKnowledgebaseArticleHandler()
    return handler.handle(query)
