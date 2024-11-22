import logging

from sqlalchemy import or_, func

from chalicelib.src.config.db import init_db
from chalicelib.src.modules.domain.repository import KnowledgeBaseArticleRepository
from chalicelib.src.modules.infrastructure.dto import Tag, KnowledgeBaseArticleSchema, KnowledgeBaseArticle, Flow, \
    TagSchema
from chalicelib.src.seedwork.infrastructure.utils import clean_string

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')


class KnowledgeBaseArticleRepositoryPostgres(KnowledgeBaseArticleRepository):

    def __init__(self):
        self.db_session = init_db()

    def add(self, article):
        LOGGER.info(f"Repository add article: {article}")
        article_schema = KnowledgeBaseArticleSchema(many=False)
        new_article = KnowledgeBaseArticle(
            title=article.title,
            content=article.content,
            client_id=article.client_id
        )
        if article.tags:
            tags = self.db_session.query(Tag).filter(Tag.id.in_(article.tags)).all()
            new_article.tags.extend(tags)

        self.db_session.add(new_article)
        self.db_session.commit()
        return article_schema.dump(new_article)

    def get(self, article_id):
        article_schema = KnowledgeBaseArticleSchema()
        article = self.db_session.query(KnowledgeBaseArticle).filter_by(id=article_id).first()
        if not article:
            raise ValueError("Tag not found")
        json_article = article_schema.dump(article)
        tag_schema = TagSchema(many=True)
        json_article['tags'] = tag_schema.dump(article.tags)
        return json_article

    def remove(self, article_id, client_id):
        LOGGER.info(f"Repository remove article: {article_id}")
        entity = self.db_session.query(KnowledgeBaseArticle).filter_by(id=article_id).first()
        if not entity:
            raise ValueError("Article not found")
        if entity.client_id != client_id:
            raise NameError("Invalid Client Id")
        self.db_session.delete(entity)
        self.db_session.commit()
        LOGGER.info(f"Article {article_id} removed successfully")

    def get_all(self, query: dict = None):
        article_schema = KnowledgeBaseArticleSchema(many=True)

        filters = []
        if 'client_id' in query:
            filters.append(KnowledgeBaseArticle.client_id == query['client_id'])
        if 'title' in query:
            title = clean_string(query['title'])
            words = list(set(title.split(" ")))
            if words:
                title_conditions = [func.lower(KnowledgeBaseArticle.title).contains(word.lower()) for word in words]
                filters.append(or_(*title_conditions))
        if 'content' in query:
            content = clean_string(query['content'])
            words = list(set(content.split(" ")))
            if words:
                content_conditions = [func.lower(KnowledgeBaseArticle.content).contains(word) for word in words]
                filters.append(or_(*content_conditions))
        if 'tags' in query:
            for tag_id in query['tags']:
                filters.append(KnowledgeBaseArticle.tags.any(Tag.id == tag_id))

        query_base = self.db_session.query(KnowledgeBaseArticle)
        if filters:
            result = query_base.filter(*filters).all()
        else:
            result = query_base.all()

        return article_schema.dump(result)

    def update(self, article_id, data):
        LOGGER.info(f"Repository remove article: {article_id}")
        entity = self.db_session.query(KnowledgeBaseArticle).filter_by(id=article_id).first()
        if not entity:
            raise ValueError("Article not found")
        if entity.client_id != data['client_id']:
            raise NameError("Invalid Client Id")

        if 'title' in data:
            entity.title = data['title']
        if 'content' in data:
            entity.content = data['content']

        if 'tags' in data:
            new_tag_ids = data['tags']  # Suponiendo que data['tags'] es una lista de IDs
            current_tags = {tag.id for tag in entity.tags}  # IDs de los tags actuales

            # Borrar solo la relación de los tags que no están en la nueva lista
            tags_to_remove = current_tags - set(new_tag_ids)
            for tag_id in tags_to_remove:
                tag_to_remove = self.db_session.query(Tag).get(tag_id)
                if tag_to_remove in entity.tags:
                    entity.tags.remove(tag_to_remove)  # Esto solo elimina la relación

            # Agregar los nuevos tags que no están en la relación actual
            tags_to_add = set(new_tag_ids) - current_tags
            for tag_id in tags_to_add:
                new_tag = self.db_session.query(Tag).get(tag_id)
                if new_tag:  # Verificar que el tag existe
                    entity.tags.append(new_tag)  # Esto agrega la relación

        self.db_session.commit()
        LOGGER.info(f"Article {article_id} updated successfully")