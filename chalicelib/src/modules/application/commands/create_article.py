import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import KnowledgeBaseArticleRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class CreateKnowledgebaseArticleCommand(Command):
    title: str
    content: str
    client_id: int
    tags: [int]


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateKnowledgebaseArticleCommand):
        LOGGER.info("Handle createKnowledgebaseArticleCommand")

        repository = self.knowledge_base_factory.create_object(KnowledgeBaseArticleRepository)
        return repository.add(command)


@execute_command.register(CreateKnowledgebaseArticleCommand)
def execute_update_information_command(command:  CreateKnowledgebaseArticleCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
