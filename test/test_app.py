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