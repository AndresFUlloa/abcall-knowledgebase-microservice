import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import FlowRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class DeleteFlowCommand(Command):
    flow_id: int
    client_id: int


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: DeleteFlowCommand):
        LOGGER.info("Handle deleteFlowCommand")

        repository = self.knowledge_base_factory.create_object(FlowRepository)
        return repository.remove(command.flow_id, command.client_id)


@execute_command.register(DeleteFlowCommand)
def execute_update_information_command(command:  DeleteFlowCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
