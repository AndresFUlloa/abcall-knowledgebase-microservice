import enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Text, UniqueConstraint
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

article_tag_association = Table(
    'article_tag_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('knowledge_base_articles.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

flow_tag_association = Table(
    'flow_tag_association',
    Base.metadata,
    Column('flow_id', Integer, ForeignKey('flows.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    client_id = Column(Integer, autoincrement=True)

    __table_args__ = (UniqueConstraint('client_id', 'name', name='uq_client_id_name'),)
    articles = relationship("KnowledgeBaseArticle", secondary=article_tag_association, back_populates="tags")
    flows = relationship("Flow", secondary=flow_tag_association, back_populates="tags")


class KnowledgeBaseArticle(Base):
    __tablename__ = 'knowledge_base_articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    client_id = Column(Integer, nullable=False)

    tags = relationship("Tag", secondary=article_tag_association, back_populates="articles")


class StepType(enum.Enum):
    VALIDATION = "Validation"
    DIAGNOSTIC = "Diagnostic"
    RESOLUTION = "Resolution"
    ESCALATION = "Escalation"
    CLOSURE = "Closure"


class FlowStep(Base):
    __tablename__ = 'flow_steps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    type = Column(Enum(StepType), nullable=False)
    flow_id = Column(Integer, ForeignKey('flows.id'), nullable=False)
    flow = relationship("Flow", back_populates="steps")


class Flow(Base):
    __tablename__ = 'flows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, nullable=False)
    user_sub = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    steps = relationship("FlowStep", back_populates="flow", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=flow_tag_association, back_populates="flows")


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True


class KnowledgeBaseArticleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KnowledgeBaseArticle
        load_instance = True


class FlowStepSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FlowStep
        load_instance = True


class FlowSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Flow
        load_instance = True
