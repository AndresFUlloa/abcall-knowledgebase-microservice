from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import FlowRepository


@dataclass
class GetFlowQuery(Query):
    flow_id: int


class GetFlowHandler(QueryBaseHandler):
    def handle(self, query: GetFlowQuery):
        repository = self.knowlede_base_factory.create_object(FlowRepository)
        result = repository.get(query.flow_id)
        return QueryResult(result=result)


@execute_query.register(GetFlowQuery)
def execute_get_flow(query: GetFlowQuery):
    handler = GetFlowHandler()
    return handler.handle(query)
