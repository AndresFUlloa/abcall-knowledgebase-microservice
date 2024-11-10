import logging

from chalicelib.src.config.db import init_db
from chalicelib.src.modules.domain.repository import FlowRepository
from chalicelib.src.modules.infrastructure.dto import Tag, Flow, \
    TagSchema, FlowSchema, FlowStepSchema

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


class FlowsRepositoryPostgres(FlowRepository):

    def __init__(self):
        super().__init__()
        self.db_session = init_db()

    def add(self, flow):
        LOGGER.info(f"Repository add flow: {flow}")
        flow_schema = FlowSchema(many=False)
        new_flow = Flow(
            client_id=flow.client_id,
            user_sub=flow.user_sub,
            name=flow.name,
            description=flow.description
        )
        if flow.tags:
            tags = self.db_session.query(Tag).filter(Tag.id.in_(flow.tags)).all()
            new_flow.tags.extend(tags)

        self.db_session.add(new_flow)
        self.db_session.commit()
        return flow_schema.dump(new_flow)

    def get(self, flow_id):
        flow_schema = FlowSchema()
        flow = self.db_session.query(Flow).filter_by(id=flow_id).first()
        if not flow:
            raise ValueError("Tag not found")
        json_article = flow_schema.dump(flow)
        tag_schema = TagSchema(many=True)
        json_article['tags'] = tag_schema.dump(flow.tags)
        json_article['steps'] = []
        if flow.steps:
            steps_schema = FlowStepSchema(many=True)
            json_article['steps'] = steps_schema.dump(flow.steps)

        return json_article

    def remove(self, flow_id, client_id):
        LOGGER.info(f"Repository remove flow: {flow_id}")
        entity = self.db_session.query(Flow).filter_by(id=flow_id).first()
        if not entity:
            raise ValueError("Flow not found")
        if entity.client_id != client_id:
            raise PermissionError("Invalid Client Id")
        self.db_session.delete(entity)
        self.db_session.commit()
        LOGGER.info(f"Flow {flow_id} removed successfully")

    def get_all(self, query: dict = None):
        flow_schema = FlowSchema(many=True)

        filters = []
        if 'client_id' in query:
            filters.append(Flow.client_id == query['client_id'])
        if 'user_sub' in query:
            filters.append(Flow.user_sub == query['user_sub'])
        if 'name' in query:
            filters.append(Flow.name == query['name'])
        if 'description' in query:
            filters.append(Flow.description == query['description'])

        if 'tags' in query:
            for tag_id in query['tags']:
                filters.append(Flow.tags.any(Tag.id == tag_id))

        query_base = self.db_session.query(Flow)
        if filters:
            result = query_base.filter(*filters).all()
        else:
            result = query_base.all()

        return flow_schema.dump(result)

    def update(self, flow_id, data):
        LOGGER.info(f"Repository update flow: {flow_id}")
        entity = self.db_session.query(Flow).filter_by(id=flow_id).first()
        if not entity:
            raise ValueError("Flow not found")
        if entity.client_id != data['client_id']:
            raise NameError("Invalid Client Id")

        if 'name' in data:
            entity.name = data['name']
        if 'description' in data:
            entity.description = data['description']

        if 'tags' in data:
            new_tag_ids = data['tags']
            current_tags = {tag.id for tag in entity.tags}

            tags_to_remove = current_tags - set(new_tag_ids)
            for tag_id in tags_to_remove:
                tag_to_remove = self.db_session.query(Tag).get(tag_id)
                if tag_to_remove in entity.tags:
                    entity.tags.remove(tag_to_remove)

            tags_to_add = set(new_tag_ids) - current_tags
            for tag_id in tags_to_add:
                new_tag = self.db_session.query(Tag).get(tag_id)
                if new_tag:
                    entity.tags.append(new_tag)

        self.db_session.commit()
        LOGGER.info(f"Article {flow_id} updated successfully")
