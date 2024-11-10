import logging

from chalicelib.src.config.db import init_db
from chalicelib.src.modules.domain.repository import FlowStepRepository
from chalicelib.src.modules.infrastructure.dto import Tag, Flow, \
    TagSchema, FlowSchema, FlowStepSchema, FlowStep, StepType

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


class FlowStepsRepositoryPostgres(FlowStepRepository):

    def __init__(self):
        super().__init__()
        self.db_session = init_db()

    def add(self, flow_step):
        LOGGER.info(f"Repository add flowstep: {flow_step}")
        flow = self.db_session.query(Flow).filter_by(id=flow_step.flow_id).first()
        if not flow:
            raise ValueError("Flow not found for the provided flow_id")
        if flow.client_id != flow_step.client_id:
            raise PermissionError("Invalid Client Id")

        flow_step_schema = FlowStepSchema(many=False)
        new_flow = FlowStep(
            description=flow_step.description,
            type=StepType(flow_step.type),
            flow_id=flow_step.flow_id
        )

        self.db_session.add(new_flow)
        self.db_session.commit()
        return flow_step_schema.dump(new_flow)

    def get(self, flow_step_id):
        flow_step_schema = FlowStepSchema()
        flow_step = self.db_session.query(FlowStep).filter_by(id=flow_step_id).first()
        if not flow_step:
            raise ValueError("Tag not found")
        json_flow_step = flow_step_schema.dump(flow_step)
        flow_schema = FlowSchema()
        json_flow_step['flow'] = flow_schema.dump(flow_step.flow)

        return json_flow_step

    def remove(self, flow_step_id, client_id):
        LOGGER.info(f"Repository remove flow: {flow_step_id}")
        entity = self.db_session.query(FlowStep).filter_by(id=flow_step_id).first()
        if not entity:
            raise ValueError("Flow not found")
        if entity.flow.client_id != client_id:
            raise PermissionError("Invalid Client Id")
        self.db_session.delete(entity)
        self.db_session.commit()
        LOGGER.info(f"Flow {flow_step_id} removed successfully")

    def get_all(self, query: dict = None):
        flow_step_schema = FlowStepSchema(many=True)

        filters = []
        if 'client_id' not in query:
            raise ValueError('Client id is missing')

        if 'flow_id' not in query:
            raise ValueError('Flow id is missing')

        flow = self.db_session.query(Flow).filter_by(id=query['flow_id']).first()
        if not flow:
            raise ValueError('Flow not found')
        if flow.client_id != query['client_id']:
            raise PermissionError("Invalid client id")

        filters.append(FlowStep.flow_id == query['flow_id'])
        if 'description' in query:
            filters.append(FlowStep.description == query['description'])

        query_base = self.db_session.query(FlowStep)
        if filters:
            result = query_base.filter(*filters).all()
        else:
            result = query_base.all()

        return flow_step_schema.dump(result)

    def update(self, flow_step_id, data):
        LOGGER.info(f"Repository update flow: {flow_step_id}")
        entity = self.db_session.query(FlowStep).filter_by(id=flow_step_id).first()
        if not entity:
            raise ValueError("Flow not found")
        if entity.flow.client_id != data['client_id']:
            raise NameError("Invalid Client Id")

        if 'description' in data:
            entity.description = data['description']
        if 'type':
            entity.type = StepType(data['type'])

        self.db_session.commit()
        LOGGER.info(f"Article {flow_step_id} updated successfully")
