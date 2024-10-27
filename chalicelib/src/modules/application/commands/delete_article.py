import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import KnowledgeBaseArticleRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class DeleteKnowledgebaseArticleCommand(Command):
    article_id: int
    client_id: int


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: DeleteKnowledgebaseArticleCommand):
        LOGGER.info("Handle deleteKnowledgebaseArticleCommand")

        repository = self.knowledge_base_factory.create_object(KnowledgeBaseArticleRepository)
        return repository.remove(command.article_id, command.client_id)


@execute_command.register(DeleteKnowledgebaseArticleCommand)
def execute_update_information_command(command:  DeleteKnowledgebaseArticleCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
