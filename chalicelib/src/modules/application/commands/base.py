from chalicelib.src.modules.infrastructure.factory import KnowledgeBaseFactory
from chalicelib.src.seedwork.application.commands import CommandHandler


class CommandBaseHandler(CommandHandler):
    def __init__(self):
        self._knowledge_base_factory: KnowledgeBaseFactory = KnowledgeBaseFactory()

    @property
    def knowledge_base_factory(self):
        return self._knowledge_base_factory
