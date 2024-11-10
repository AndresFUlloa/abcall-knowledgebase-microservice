from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import TagRepository


@dataclass
class GetTagsQuery(Query):
    client_id: int


class GetTagsHandler(QueryBaseHandler):
    def handle(self, query: GetTagsQuery):
        repository = self.knowlede_base_factory.create_object(TagRepository)
        result = repository.get_all({'client_id': query.client_id})
        return QueryResult(result=result)


@execute_query.register(GetTagsQuery)
def execute_get_tags(query: GetTagsQuery):
    handler = GetTagsHandler()
    return handler.handle(query)
