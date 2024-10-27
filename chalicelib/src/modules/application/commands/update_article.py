import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import KnowledgeBaseArticleRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class UpdateKnowledgebaseArticleCommand(Command):
    article_id: int
    data: dict


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: UpdateKnowledgebaseArticleCommand):
        LOGGER.info("Handle updateTagCommand")

        repository = self.knowledge_base_factory.create_object(KnowledgeBaseArticleRepository)
        return repository.update(command.article_id, command.data)


@execute_command.register(UpdateKnowledgebaseArticleCommand)
def execute_update_information_command(command:  UpdateKnowledgebaseArticleCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
