from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import FlowRepository


@dataclass
class GetFlowsQuery(Query):
    queries: dict


class GetKnowledgebaseArticleHandler(QueryBaseHandler):
    def handle(self, query: GetFlowsQuery):
        repository = self.knowlede_base_factory.create_object(FlowRepository)
        result = repository.get_all(query.queries)
        return QueryResult(result=result)


@execute_query.register(GetFlowsQuery)
def execute_get_flows(query: GetFlowsQuery):
    handler = GetKnowledgebaseArticleHandler()
    return handler.handle(query)
