import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import TagRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class CreateTagCommand(Command):
    client_id: int
    name: str


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateTagCommand):
        LOGGER.info("Handle createClientCommand")

        repository = self.knowledge_base_factory.create_object(TagRepository)
        return repository.add(command)


@execute_command.register(CreateTagCommand)
def execute_update_information_command(command:  CreateTagCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
