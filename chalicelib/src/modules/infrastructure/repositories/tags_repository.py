import logging

from chalicelib.src.config.db import init_db
from chalicelib.src.modules.domain.repository import TagRepository
from chalicelib.src.modules.infrastructure.dto import Tag, TagSchema, KnowledgeBaseArticle, Flow

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


class TagRepositoryPostgres(TagRepository):

    def __init__(self):
        self.db_session = init_db()

    def add(self, tag):
        LOGGER.info(f"Repository add client: {tag}")
        tag_schema = TagSchema(many=False)
        new_tag = Tag(
            name=tag.name,
            client_id=tag.client_id
        )
        self.db_session.add(new_tag)
        self.db_session.commit()
        return tag_schema.dump(new_tag)

    def get(self, tag_id):
        tag_schema = TagSchema()
        tag = self.db_session.query(Tag).filter_by(id=tag_id).first()
        if not tag:
            raise ValueError("Tag not found")
        return tag_schema.dump(tag)

    def remove(self, tag_id, client_id):
        LOGGER.info(f"Repository remove tag: {tag_id}")
        entity = self.db_session.query(Tag).filter_by(id=tag_id).first()
        if not entity:
            raise ValueError("Client not found")
        if entity.client_id != client_id:
            raise NameError("Invalid Client")
        self.db_session.delete(entity)
        self.db_session.commit()
        LOGGER.info(f"Client {tag_id} removed successfully")

    def get_all(self, query: dict[str, str]):
        tag_schema = TagSchema(many=True)

        filters = []
        if 'client_id' in query:
            filters.append(Tag.client_id == query['client_id'])
        if 'article_id' in query:
            article_id = query['article_id']
            filters.append(Tag.articles.any(KnowledgeBaseArticle.id == article_id))
        if 'flow_id' in query:
            flow_id = query['flow_id']
            filters.append(Tag.flows.any(Flow.id == flow_id))

        query_base = self.db_session.query(Tag)
        if filters:
            result = query_base.filter(*filters).all()
        else:
            result = query_base.all()

        return tag_schema.dump(result)

    def update(self, tag_id, data):
        LOGGER.info(f"Repository remove tag: {tag_id}")
        entity = self.db_session.query(Tag).filter_by(id=tag_id).first()
        if not entity:
            raise ValueError("Client not found")
        if entity.client_id != data['client_id']:
            raise NameError("Invalid Client")

        if 'name' in data:
            entity.name = data['name']

        self.db_session.commit()
        LOGGER.info(f"Tag {tag_id} updated successfully")
