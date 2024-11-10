from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import TagRepository


@dataclass
class GetTagQuery(Query):
    tag_id: int


class GetClientHandler(QueryBaseHandler):
    def handle(self, query: GetTagQuery):
        repository = self.knowlede_base_factory.create_object(TagRepository)
        result = repository.get(query.tag_id)
        return QueryResult(result=result)


@execute_query.register(GetTagQuery)
def execute_get_tag(query: GetTagQuery):
    handler = GetClientHandler()
    return handler.handle(query)
