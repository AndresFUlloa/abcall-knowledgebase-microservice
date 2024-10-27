import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import TagRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class DeleteTagCommand(Command):
    tag_id: int
    client_id: int


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: DeleteTagCommand):
        LOGGER.info("Handle deleteTagCommand")

        repository = self.knowledge_base_factory.create_object(TagRepository)
        return repository.remove(command.tag_id, command.client_id)


@execute_command.register(DeleteTagCommand)
def execute_update_information_command(command:  DeleteTagCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
