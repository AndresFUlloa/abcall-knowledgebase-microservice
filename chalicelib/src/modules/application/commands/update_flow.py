import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import FlowRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class UpdateFlowCommand(Command):
    flow_id: int
    data: dict


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: UpdateFlowCommand):
        LOGGER.info("Handle updateTagCommand")

        repository = self.knowledge_base_factory.create_object(FlowRepository)
        return repository.update(command.flow_id, command.data)


@execute_command.register(UpdateFlowCommand)
def execute_update_information_command(command:  UpdateFlowCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
