import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import FlowStepRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class UpdateFlowStepCommand(Command):
    flow_id: int
    data: dict


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: UpdateFlowStepCommand):
        LOGGER.info("Handle updateTagCommand")

        repository = self.knowledge_base_factory.create_object(FlowStepRepository)
        return repository.update(command.flow_id, command.data)


@execute_command.register(UpdateFlowStepCommand)
def execute_update_information_command(command:  UpdateFlowStepCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
