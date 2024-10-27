from dataclasses import dataclass
from chalicelib.src.seedwork.domain.factory import Factory
from chalicelib.src.seedwork.domain.repository import Repository
from chalicelib.src.modules.domain.repository import TagRepository, KnowledgeBaseArticleRepository
from .exceptions import ImplementationNotExistsForFactoryException
from .repositories.tags_repository import TagRepositoryPostgres
from .repositories.knowledge_base_article import KnowledgeBaseArticleRepositoryPostgres


@dataclass
class KnowledgeBaseFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TagRepository:
            return TagRepositoryPostgres()

        if obj == KnowledgeBaseArticleRepository:
            return KnowledgeBaseArticleRepositoryPostgres()

        raise ImplementationNotExistsForFactoryException()
