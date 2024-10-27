import logging

import boto3
from chalice import Chalice, BadRequestError, CognitoUserPoolAuthorizer, UnauthorizedError, ChaliceViewError

from chalicelib.src.config.db import init_db
from chalicelib.src.modules.application.commands.create_article import CreateKnowledgebaseArticleCommand
from chalicelib.src.modules.application.commands.create_tag import CreateTagCommand
from chalicelib.src.modules.application.commands.delete_tag import DeleteTagCommand
from chalicelib.src.modules.application.commands.update_tag import UpdateTagCommand
from chalicelib.src.modules.application.queries.get_article import GetKnowledgebaseArticleQuery
from chalicelib.src.modules.application.queries.get_articles import GetKnowledgebaseArticlesQuery
from chalicelib.src.modules.application.queries.get_tag import GetTagQuery
from chalicelib.src.modules.application.queries.get_tags import GetTagsQuery
from chalicelib.src.seedwork.application.commands import execute_command
from chalicelib.src.seedwork.application.queries import execute_query

app = Chalice(app_name='abcall-knowledgebase-microservice')
app.debug = True

LOGGER = logging.getLogger('abcall-knowledgebase-microservice')

authorizer = CognitoUserPoolAuthorizer(
    'AbcPool',
    provider_arns=['arn:aws:cognito-idp:us-east-1:044162189377:userpool/us-east-1_YDIpg1HiU']
)

cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

USER_POOL_ID = 'us-east-1_YDIpg1HiU'
CLIENT_ID = '65sbvtotc1hssqecgusj1p3f9g'


def check_roles(user_info: dict, roles: [str]):
    try:
        user_role = user_info['custom:custom:userRole']
        if str(user_role).lower() not in roles:
            raise UnauthorizedError("Access denied")
    except Exception as e:
        LOGGER.error(f"Error while checking roles: {str(e)}")
        raise ChaliceViewError("Error checking user role")


@app.route('/knowledgebase/tag', cors=True, methods=['POST'], authorizer=authorizer)
def tag_post():
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    client_as_json = app.current_request.json_body
    if 'name' not in client_as_json:
        raise BadRequestError('Missing required field: name')

    command = CreateTagCommand(
        client_id=int(auth_info['custom:client_id']),
        name=client_as_json['name']
    )

    try:
        result = execute_command(command)
        return {'status': 'success', 'tag': result}
    except Exception as e:
        LOGGER.error(f"Error while creating tag: {str(e)}")
        raise ChaliceViewError('An error occurred while fetching the tag')


@app.route('/knowledgebase/tags', cors=True, methods=['GET'], authorizer=authorizer)
def tag_post():
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    query = GetTagsQuery(client_id=auth_info['custom:client_id'])

    try:
        query_result = execute_query(query).result
        return query_result
    except Exception as e:
        LOGGER.error(f"Error getting tags: {str(e)}")
        raise ChaliceViewError('An error occurred while searching tags')


@app.route('/knowledgebase/tag/{tag_id}', cors=True, methods=['GET'], authorizer=authorizer)
def get_tag(tag_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    query = GetTagQuery(tag_id=tag_id)

    try:
        query_result = execute_query(query).result
    except Exception as e:
        LOGGER.error(f"Error getting tags: {str(e)}")
        raise ChaliceViewError('An error occurred while searching tags')

    if query_result['client_id'] != int(auth_info['custom:client_id']):
        raise UnauthorizedError("User does not have access to the client")

    return query_result


@app.route('/knowledgebase/tag/{tag_id}', cors=True, methods=['PUT'], authorizer=authorizer)
def update_tag(tag_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    client_as_json = app.current_request.json_body
    if 'name' not in client_as_json:
        raise BadRequestError('Missing required field: name')

    client_as_json['client_id'] = int(auth_info['custom:client_id'])
    command = UpdateTagCommand(tag_id=tag_id, data=client_as_json)

    try:
        execute_command(command)
        return {'status': 'success', 'message': 'Tag updated successfully'}
    except NameError as ne:
        LOGGER.error(f"Error updating tag: {str(ne)}")
        raise UnauthorizedError("User does not have access to the client")
    except Exception as e:
        LOGGER.error(f"Error updating tag: {str(e)}")
        raise ChaliceViewError('An error occurred while searching tags')


@app.route('/knowledgebase/tag/{tag_id}', cors=True, methods=['DELETE'], authorizer=authorizer)
def delete_tag(tag_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    command = DeleteTagCommand(tag_id=tag_id, client_id=int(auth_info['custom:client_id']))

    try:
        execute_command(command)
        return {'status': 'success', 'message': 'Tag deleted successfully'}
    except NameError as ne:
        LOGGER.error(f"Error updating tag: {str(ne)}")
        raise UnauthorizedError("User does not have access to the client")
    except Exception as e:
        LOGGER.error(f"Error updating tag: {str(e)}")
        raise ChaliceViewError('An error occurred while searching tags')


@app.route('/knowledgebase', cors=True, methods=['POST'], authorizer=authorizer)
def knowledgebase_post():
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    client_as_json = app.current_request.json_body
    required_fields = ['title', 'content']
    for field in required_fields:
        if field not in client_as_json:
            raise BadRequestError(f"Missing required field: {field}")

    command = CreateKnowledgebaseArticleCommand(
        title=client_as_json['title'],
        content=client_as_json['content'],
        client_id=int(auth_info['custom:client_id']),
        tags=[]
    )

    if 'tags' in client_as_json:
        command.tags = client_as_json['tags']

    try:
        result = execute_command(command)
        return {'status': 'success', 'article': result}
    except Exception as e:
        LOGGER.error(f"Error creating knowledgebase article: {str(e)}")
        raise ChaliceViewError('Error creating knowledgebase article')

@app.route('/knowledgebase/filters', cors=True, methods=['POST'], authorizer=authorizer)
def knowledgebase_filters():
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    client_as_json = app.current_request.json_body
    client_as_json['client_id'] = int(auth_info['custom:client_id'])

    query = GetKnowledgebaseArticlesQuery(queries=client_as_json)

    try:
        result = execute_query(query).result
        return result
    except Exception as e:
        LOGGER.error(f"Error loading knowledgebase articles: {str(e)}")
        raise ChaliceViewError('Error loading knowledgebase articles')


@app.route('/knowledgebase/{article_id}', cors=True, methods=['GET'], authorizer=authorizer)
def get_knowledgebase_article(article_id):
    auth_info = app.current_request.context['authorizer']['claims']
    check_roles(auth_info, ['superadmin', 'admin', 'agent'])

    if 'custom:client_id' not in auth_info:
        LOGGER.error(f"User: {auth_info['sub']} does not have client id")
        raise BadRequestError('User does not have client id')

    query = GetKnowledgebaseArticleQuery(article_id=article_id)

    try:
        result = execute_query(query).result
    except Exception as e:
        LOGGER.error(f"Error loading knowledgebase article {article_id}: {str(e)}")
        raise ChaliceViewError(f'Error loading knowledgebase article {article_id}')
    print(result)
    if result['client_id'] != int(auth_info['custom:client_id']):
        raise UnauthorizedError('User does not have access to the client')

    return result


@app.route('/migrate', methods=['POST'])
def migrate():
    try:
        init_db(migrate=True)
        return {"message": "Tablas creadas con éxito"}
    except Exception as e:
        return {"error": str(e)}
