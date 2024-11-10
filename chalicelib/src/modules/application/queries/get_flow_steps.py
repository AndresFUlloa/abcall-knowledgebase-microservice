from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import FlowStepRepository


@dataclass
class GetFlowStepsQuery(Query):
    queries: dict


class GetKnowledgebaseArticleHandler(QueryBaseHandler):
    def handle(self, query: GetFlowStepsQuery):
        repository = self.knowlede_base_factory.create_object(FlowStepRepository)
        result = repository.get_all(query.queries)
        return QueryResult(result=result)


@execute_query.register(GetFlowStepsQuery)
def execute_get_flow_steps(query: GetFlowStepsQuery):
    handler = GetKnowledgebaseArticleHandler()
    return handler.handle(query)
