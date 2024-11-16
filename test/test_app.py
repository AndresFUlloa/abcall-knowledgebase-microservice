import json
from datetime import datetime
from unittest import mock
from unittest.mock import patch, MagicMock

from chalice.test import Client
from app import app


def test_create_tag():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    mock_command_response = {
        "id": 1,
        "name": "test",
        "client_id": 3
    }

    mock_request_body = {
        "name": "test"
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.tags_repository.TagRepositoryPostgres.add',
                   return_value=mock_command_response):
            with Client(app) as client:
                # Realizar la solicitud POST
                response = client.http.post(
                    '/knowledgebase/tag',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )

                assert response.status_code == 200

                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['tag'] == mock_command_response


def test_get_tags():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    mock_query_response = [
        {
            "id": 1,
            "name": "test",
            "client_id": 3
        }
    ]

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.tags_repository.TagRepositoryPostgres.get_all',
                   return_value=mock_query_response):
            with Client(app) as client:
                response = client.http.get(
                    '/knowledgebase/tags',
                    headers={'Content-Type': 'application/json'}
                )

                assert response.status_code == 200

                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_get_tag():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    mock_query_response = {
        "id": 1,
        "name": "test",
        "client_id": 3
    }

    tag_id = 1

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.tags_repository.TagRepositoryPostgres.get',
                   return_value=mock_query_response):
            with Client(app) as client:
                response = client.http.get(
                    f'/knowledgebase/tag/{tag_id}',
                    headers={'Content-Type': 'application/json'}
                )

                assert response.status_code == 200

                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_update_tag():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    tag_id = 1

    mock_request_body = {
        "name": "new_test_name"
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.tags_repository.TagRepositoryPostgres.update',
                   return_value=None):
            with Client(app) as client:
                response = client.http.put(
                    f'/knowledgebase/tag/{tag_id}',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )

                assert response.status_code == 200

                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Tag updated successfully'


def test_delete_tag():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    tag_id = 1

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.tags_repository.TagRepositoryPostgres.remove',
                   return_value=None):
            with Client(app) as client:
                response = client.http.delete(
                    f'/knowledgebase/tag/{tag_id}',
                    headers={'Content-Type': 'application/json'}
                )

                assert response.status_code == 200

                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Tag deleted successfully'


def test_create_knowledgebase_article():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    mock_request_body = {
        "title": "New Article",
        "content": "Content of the new article",
        "tags": ["tag1", "tag2"]
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = mock_request_body

    mock_command_response = {
        "id": 1,
        "title": "New Article",
        "content": "Content of the new article",
        "client_id": 3,
        "tags": ["tag1", "tag2"]
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.knowledge_base_article.KnowledgeBaseArticleRepositoryPostgres.add',
                   return_value=mock_command_response):
            with Client(app) as client:
                response = client.http.post(
                    '/knowledgebase',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )
                assert response.status_code == 200
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['article'] == mock_command_response


def test_filter_knowledgebase_articles():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    mock_request_body = {
        "filters": {
            "tags": ["tag1"]
        }
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = mock_request_body

    mock_query_response = [
        {
            "id": 1,
            "title": "New Article",
            "content": "Content of the new article",
            "client_id": 3,
            "tags": ["tag1"]
        }
    ]

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.knowledge_base_article.KnowledgeBaseArticleRepositoryPostgres.get_all',
                   return_value=mock_query_response):
            with Client(app) as client:
                response = client.http.post(
                    '/knowledgebase/filters',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )
                assert response.status_code == 200
                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_get_knowledgebase_article():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    article_id = 1

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }

    mock_query_response = {
        "id": 1,
        "title": "New Article",
        "content": "Content of the new article",
        "client_id": 3,
        "tags": ["tag1"]
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.knowledge_base_article.KnowledgeBaseArticleRepositoryPostgres.get',
                   return_value=mock_query_response):
            with Client(app) as client:
                response = client.http.get(
                    f'/knowledgebase/{article_id}',
                    headers={'Content-Type': 'application/json'}
                )
                assert response.status_code == 200
                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_delete_knowledgebase_article():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    article_id = 1

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.knowledge_base_article.KnowledgeBaseArticleRepositoryPostgres.remove',
                   return_value=None):
            with Client(app) as client:
                response = client.http.delete(
                    f'/knowledgebase/{article_id}',
                    headers={'Content-Type': 'application/json'}
                )
                assert response.status_code == 200
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Article deleted'



def test_update_knowledgebase_article():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    article_id = 1

    mock_request_body = {
        "title": "Updated Article",
        "content": "Updated content of the article",
        "tags": ["tag1", "tag2"]
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.knowledge_base_article.KnowledgeBaseArticleRepositoryPostgres.update',
                   return_value=None):
            with Client(app) as client:
                response = client.http.put(
                    f'/knowledgebase/{article_id}',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )
                assert response.status_code == 200
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Article updated'


def test_unauthorized_user_role_for_tag():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'user'
            }
        }
    }

    mock_command_response = {
        "id": 1,
        "name": "test",
        "client_id": 3
    }
    mock_request_body = {
        "name": "test"
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        with patch('chalicelib.src.modules.infrastructure.repositories.tags_repository.TagRepositoryPostgres.add',
                   return_value=mock_command_response):
            with Client(app) as client:
                response = client.http.post(
                    '/knowledgebase/tag',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )
                assert response.status_code == 500
                response_data = json.loads(response.body)
                assert response_data['Message'] == "Error checking user role"


def test_missing_name_field_in_tag_post():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:client_id': '3',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = {}

    with patch('chalice.app.Request', return_value=mock_request):
        with Client(app) as client:
            response = client.http.post(
                '/knowledgebase/tag',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(mock_request.json_body)
            )
            assert response.status_code == 400
            response_data = json.loads(response.body)
            assert response_data['Message'] == 'Missing required field: name'


def test_missing_client_id_in_auth_info():
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:custom:userRole': 'superadmin',
            }
        }
    }

    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }
    mock_request.json_body = {"name": "test"}

    with patch('chalice.app.Request', return_value=mock_request):
        with Client(app) as client:
            response = client.http.post(
                '/knowledgebase/tag',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(mock_request.json_body)
            )
            assert response.status_code == 400
            response_data = json.loads(response.body)
            assert response_data['Message'] == 'User does not have client id'


def test_risk_evaluation():
    # Mock context with authorizer claims
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:custom:userRole': 'superadmin',
                'custom:client_id': '3',
            }
        }
    }

    # Mock request object
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer asdajdahsda'
    }

    # Mock the facade to return a fixed risk level and recommendation
    mock_risk_level = 'medio'
    mock_recommendation = 'Revisar la configuración del dispositivo y verificar la conexión.'

    # Use patch to mock the request and test the endpoint
    with patch('chalicelib.src.modules.infrastructure.fecades.MicroservicesFacade') as MockFacade:
        mock_facade_instance = MockFacade.return_value
        mock_facade_instance.generate_risk_evaluation.return_value = (mock_risk_level, mock_recommendation)

        with patch('chalice.app.Request', return_value=mock_request):
            with Client(app) as client:
                response = client.http.get(
                    '/knowledgebase/risk-evaluation/1',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Assert the structure of the response
                response_data = json.loads(response.body)
                assert 'incident_id' in response_data
                assert 'risk_level' in response_data
                assert 'recommendation' in response_data

                # Check that incident_id matches
                assert response_data['incident_id'] == '1'

                # Check risk_level is one of the expected values
                assert response_data['risk_level'] in ['alto', 'medio', 'bajo']

                # Check recommendation is a non-empty string
                assert isinstance(response_data['recommendation'], str)
                assert len(response_data['recommendation']) > 0