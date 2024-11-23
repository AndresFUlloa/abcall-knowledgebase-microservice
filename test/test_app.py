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


def test_add_flow():
    # Mock context with authorizer claims
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

    # Mock request payload
    mock_request_body = {
        "name": "Test Flow",
        "description": "This is a test flow",
        "tags": [1, 2]
    }

    # Mock the response from the repository
    mock_command_response = {
        "id": 1,
        "name": "Test Flow",
        "description": "This is a test flow",
        "client_id": 3,
        "tags": [{"id": 1, "name": "Tag1"}, {"id": 2, "name": "Tag2"}]
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to return the mocked flow
        with patch('chalicelib.src.modules.infrastructure.repositories.flows_repository.FlowsRepositoryPostgres.add',
                   return_value=mock_command_response):
            with Client(app) as client:
                # Perform the POST request to the endpoint
                response = client.http.post(
                    '/knowledgebase/flow',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['flow'] == mock_command_response



def test_flows_index():
    # Mock context with authorizer claims
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

    # Mock the response from the query
    mock_query_response = [
        {
            "id": 1,
            "name": "Flow 1",
            "description": "Description of Flow 1",
            "client_id": 3,
            "tags": [{"id": 1, "name": "Tag1"}]
        },
        {
            "id": 2,
            "name": "Flow 2",
            "description": "Description of Flow 2",
            "client_id": 3,
            "tags": [{"id": 2, "name": "Tag2"}]
        }
    ]

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the query execution to return the mocked flows
        with patch('chalicelib.src.modules.infrastructure.repositories.flows_repository.FlowsRepositoryPostgres.get_all',
                   return_value=mock_query_response):
            with Client(app) as client:
                # Perform the GET request to the endpoint
                response = client.http.get(
                    '/knowledgebase/flows',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_get_flow():
    # Mock context with authorizer claims
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

    # Flow ID to fetch
    flow_id = 1

    # Mock the response from the query
    mock_query_response = {
        "id": flow_id,
        "name": "Flow 1",
        "description": "Description of Flow 1",
        "client_id": 3,
        "tags": [{"id": 1, "name": "Tag1"}]
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the query execution to return the mocked flow
        with patch('chalicelib.src.modules.infrastructure.repositories.flows_repository.FlowsRepositoryPostgres.get',
                   return_value=mock_query_response):
            with Client(app) as client:
                # Perform the GET request to the endpoint
                response = client.http.get(
                    f'/knowledgebase/flow/{flow_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data == mock_query_response
                assert response_data['client_id'] == 3  # Validate client_id matches


def test_update_flow():
    # Mock context with authorizer claims
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

    # Flow ID and payload for update
    flow_id = 1
    mock_request_body = {
        "name": "Updated Flow",
        "description": "Updated description of the flow",
        "tags": [1, 2]
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to return successfully
        with patch('chalicelib.src.modules.infrastructure.repositories.flows_repository.FlowsRepositoryPostgres.update',
                   return_value=None):
            with Client(app) as client:
                # Perform the PUT request to the endpoint
                response = client.http.put(
                    f'/knowledgebase/flow/{flow_id}',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Article updated'

def test_update_flow_missing_client_id():
    # Mock context with authorizer claims missing custom:client_id
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    # Flow ID and payload for update
    flow_id = 1
    mock_request_body = {
        "name": "Updated Flow",
        "description": "Updated description of the flow",
        "tags": [1, 2]
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        with Client(app) as client:
            # Perform the PUT request to the endpoint
            response = client.http.put(
                f'/knowledgebase/flow/{flow_id}',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(mock_request.json_body)
            )

            # Assert the response status code
            assert response.status_code == 400

            # Parse and validate the response
            response_data = json.loads(response.body)
            assert response_data['Message'] == 'User does not have client id'


def test_delete_flow():
    # Mock context with authorizer claims
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

    # Flow ID to delete
    flow_id = 1

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to succeed
        with patch('chalicelib.src.modules.infrastructure.repositories.flows_repository.FlowsRepositoryPostgres.remove',
                   return_value=None):
            with Client(app) as client:
                # Perform the DELETE request to the endpoint
                response = client.http.delete(
                    f'/knowledgebase/flow/{flow_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Flow deleted'


def test_delete_flow_unexpected_error():
    # Mock context with authorizer claims
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

    # Flow ID to delete
    flow_id = 1

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to raise a generic exception
        with patch('chalicelib.src.modules.infrastructure.repositories.flows_repository.FlowsRepositoryPostgres.remove',
                   side_effect=Exception("Unexpected error")):
            with Client(app) as client:
                # Perform the DELETE request to the endpoint
                response = client.http.delete(
                    f'/knowledgebase/flow/{flow_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 500

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['Message'] == 'Error deleting flow'


def test_delete_flow_missing_client_id():
    # Mock context with authorizer claims missing custom:client_id
    mock_context = {
        'authorizer': {
            'claims': {
                'sub': 'user123',
                'email': 'user@example.com',
                'custom:custom:userRole': 'superadmin'
            }
        }
    }

    # Flow ID to delete
    flow_id = 1

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        with Client(app) as client:
            # Perform the DELETE request to the endpoint
            response = client.http.delete(
                f'/knowledgebase/flow/{flow_id}',
                headers={'Content-Type': 'application/json'}
            )

            # Assert the response status code
            assert response.status_code == 400

            # Parse and validate the response
            response_data = json.loads(response.body)
            assert response_data['Message'] == 'User does not have client id'


def test_add_flow_step_success():
    # Mock context with authorizer claims
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

    # Mock request body
    mock_request_body = {
        "type": "Validation",
        "description": "Step for validation purposes",
        "flow_id": 1
    }

    # Mock the response from the command
    mock_command_response = {
        "id": 1,
        "description": "Step for validation purposes",
        "type": "Validation",
        "flow_id": 1
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to return the mocked flow step
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.add',
                   return_value=mock_command_response):
            with Client(app) as client:
                # Perform the POST request to the endpoint
                response = client.http.post(
                    '/knowledgebase/flow/step',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['flow step'] == mock_command_response


def test_get_flow_step_success():
    # Mock context with authorizer claims
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

    # Flow step ID to fetch
    flow_step_id = 1

    # Mock the response from the query
    mock_query_response = {
        "id": flow_step_id,
        "description": "Step for validation purposes",
        "type": "Validation",
        "flow": {
            "id": 1,
            "client_id": 3
        }
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the query execution to return the mocked flow step
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.get',
                   return_value=mock_query_response):
            with Client(app) as client:
                # Perform the GET request to the endpoint
                response = client.http.get(
                    f'/knowledgebase/flow/step/{flow_step_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_get_flow_step_unexpected_error():
    # Mock context with authorizer claims
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

    # Flow step ID to fetch
    flow_step_id = 1

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the query execution to raise a generic exception
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.get',
                   side_effect=Exception("Unexpected error")):
            with Client(app) as client:
                # Perform the GET request to the endpoint
                response = client.http.get(
                    f'/knowledgebase/flow/step/{flow_step_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 500

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['Message'] == f'Error loading flow step {flow_step_id}'


def test_flows_steps_index_success():
    # Mock context with authorizer claims
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

    # Flow ID for which steps are fetched
    flow_id = 1

    # Mock the response from the query
    mock_query_response = [
        {
            "id": 1,
            "description": "Step 1",
            "type": "Validation",
            "flow_id": flow_id
        },
        {
            "id": 2,
            "description": "Step 2",
            "type": "Diagnostic",
            "flow_id": flow_id
        }
    ]

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the query execution to return the mocked steps
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.get_all',
                   return_value=mock_query_response):
            with Client(app) as client:
                # Perform the GET request to the endpoint
                response = client.http.get(
                    f'/knowledgebase/flow/steps/{flow_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data == mock_query_response


def test_flows_steps_index_flow_not_found():
    # Mock context with authorizer claims
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

    # Flow ID for which steps are fetched
    flow_id = 999  # Non-existent flow_id

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the query execution to raise a ValueError
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.get_all',
                   side_effect=ValueError("Flow not found")):
            with Client(app) as client:
                # Perform the GET request to the endpoint
                response = client.http.get(
                    f'/knowledgebase/flow/steps/{flow_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 400

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['Message'] == 'Flow not found'


def test_delete_flow_step_success():
    # Mock context with authorizer claims
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

    # Flow step ID to delete
    flow_step_id = 1

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to succeed
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.remove',
                   return_value=None):
            with Client(app) as client:
                # Perform the DELETE request to the endpoint
                response = client.http.delete(
                    f'/knowledgebase/flow/step/{flow_step_id}',
                    headers={'Content-Type': 'application/json'}
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Flow step deleted'


def test_update_flow_step_success():
    # Mock context with authorizer claims
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

    # Flow step ID to update
    flow_step_id = 1

    # Mock request body
    mock_request_body = {
        "description": "Updated description",
        "type": "Diagnostic"
    }

    # Mock request
    mock_request = MagicMock()
    mock_request.context = mock_context
    mock_request.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer mocktoken'
    }
    mock_request.json_body = mock_request_body

    with patch('chalice.app.Request', return_value=mock_request):
        # Mock the command execution to succeed
        with patch('chalicelib.src.modules.infrastructure.repositories.flow_steps_repository.FlowStepsRepositoryPostgres.update',
                   return_value=None):
            with Client(app) as client:
                # Perform the PUT request to the endpoint
                response = client.http.put(
                    f'/knowledgebase/flow/step/{flow_step_id}',
                    headers={'Content-Type': 'application/json'},
                    body=json.dumps(mock_request.json_body)
                )

                # Assert the response status code
                assert response.status_code == 200

                # Parse and validate the response
                response_data = json.loads(response.body)
                assert response_data['status'] == 'success'
                assert response_data['message'] == 'Flow step updated'