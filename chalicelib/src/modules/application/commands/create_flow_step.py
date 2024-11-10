import logging
from dataclasses import dataclass
from chalicelib.src.modules.application.commands.base import CommandBaseHandler
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.commands import Command
from chalicelib.src.modules.domain.repository import FlowStepRepository

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


@dataclass
class CreateFlowStepCommand(Command):
    description: str
    type: str
    client_id: int
    flow_id: int


class UpdateInformationHandler(CommandBaseHandler):
    def handle(self, command: CreateFlowStepCommand):
        LOGGER.info("Handle createFlowStepCommand")

        repository = self.knowledge_base_factory.create_object(FlowStepRepository)
        return repository.add(command)


@execute_command.register(CreateFlowStepCommand)
def execute_update_information_command(command:  CreateFlowStepCommand):
    handler = UpdateInformationHandler()
    return handler.handle(command)
