from dataclasses import dataclass
from chalicelib.src.seedwork.domain.factory import Factory
from chalicelib.src.seedwork.domain.repository import Repository
from chalicelib.src.modules.domain.repository import TagRepository, KnowledgeBaseArticleRepository, FlowRepository, \
    FlowStepRepository
from .exceptions import ImplementationNotExistsForFactoryException
from .repositories.flow_steps_repository import FlowStepsRepositoryPostgres
from .repositories.flows_repository import FlowsRepositoryPostgres
from .repositories.tags_repository import TagRepositoryPostgres
from .repositories.knowledge_base_article import KnowledgeBaseArticleRepositoryPostgres


@dataclass
class KnowledgeBaseFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TagRepository:
            return TagRepositoryPostgres()

        if obj == KnowledgeBaseArticleRepository:
            return KnowledgeBaseArticleRepositoryPostgres()

        if obj == FlowRepository:
            return FlowsRepositoryPostgres()

        if obj == FlowStepRepository:
            return FlowStepsRepositoryPostgres()

        raise ImplementationNotExistsForFactoryException()
