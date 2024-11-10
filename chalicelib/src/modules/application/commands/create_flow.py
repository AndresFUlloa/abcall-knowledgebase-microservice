import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import FlowRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class CreateFlowCommand(Command):
    name: str
    description: str
    client_id: int
    user_sub: str
    tags: [int]


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateFlowCommand):
        LOGGER.info("Handle createKnowledgebaseArticleCommand")

        repository = self.knowledge_base_factory.create_object(FlowRepository)
        return repository.add(command)


@execute_command.register(CreateFlowCommand)
def execute_update_information_command(command:  CreateFlowCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
