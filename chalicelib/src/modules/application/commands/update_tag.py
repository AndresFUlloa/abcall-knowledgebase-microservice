import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import TagRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class UpdateTagCommand(Command):
    tag_id: int
    data: dict


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: UpdateTagCommand):
        LOGGER.info("Handle updateTagCommand")

        repository = self.knowledge_base_factory.create_object(TagRepository)
        return repository.update(command.tag_id, command.data)


@execute_command.register(UpdateTagCommand)
def execute_update_information_command(command:  UpdateTagCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
