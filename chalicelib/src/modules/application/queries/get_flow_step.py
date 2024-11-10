from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import FlowStepRepository


@dataclass
class GetFlowStepQuery(Query):
    flow_step_id: int


class GetFlowStepHandler(QueryBaseHandler):
    def handle(self, query: GetFlowStepQuery):
        repository = self.knowlede_base_factory.create_object(FlowStepRepository)
        result = repository.get(query.flow_step_id)
        return QueryResult(result=result)


@execute_query.register(GetFlowStepQuery)
def execute_get_flow_step(query: GetFlowStepQuery):
    handler = GetFlowStepHandler()
    return handler.handle(query)
