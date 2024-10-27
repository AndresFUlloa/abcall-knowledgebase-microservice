from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import KnowledgeBaseArticleRepository


@dataclass
class GetKnowledgebaseArticlesQuery(Query):
    queries: dict


class GetKnowledgebaseArticleHandler(QueryBaseHandler):
    def handle(self, query: GetKnowledgebaseArticlesQuery):
        repository = self.knowlede_base_factory.create_object(KnowledgeBaseArticleRepository)
        result = repository.get_all(query.queries)
        return QueryResult(result=result)


@execute_query.register(GetKnowledgebaseArticlesQuery)
def execute_get_clients(query: GetKnowledgebaseArticlesQuery):
    handler = GetKnowledgebaseArticleHandler()
    return handler.handle(query)
