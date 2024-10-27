from abc import ABC
from chalicelib.src.seedwork.domain.repository import Repository


class TagRepository(Repository, ABC):
    pass


class KnowledgeBaseArticleRepository(Repository, ABC):
    pass


class FlowStepRepository(Repository, ABC):
    pass


class FlowRepository(Repository, ABC):
    pass
