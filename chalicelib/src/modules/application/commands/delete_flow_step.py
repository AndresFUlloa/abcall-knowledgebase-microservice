import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import FlowStepRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class DeleteFlowStepCommand(Command):
    flow_step_id: int
    client_id: int


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: DeleteFlowStepCommand):
        LOGGER.info("Handle deleteFlowStepCommand")

        repository = self.knowledge_base_factory.create_object(FlowStepRepository)
        return repository.remove(command.flow_step_id, command.client_id)


@execute_command.register(DeleteFlowStepCommand)
def execute_update_information_command(command:  DeleteFlowStepCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
