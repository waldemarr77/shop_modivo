import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage

@pytest.mark.django_db
def test_chatbot_view_unauthenticated(api_client):
    url = reverse('chat')
    response = api_client.post(url, {"message": "Привіт"})
    assert response.status_code == 401

@pytest.mark.django_db
def test_chatbot_view_no_message(authenticated_client):
    url = reverse('chat')
    response = authenticated_client.post(url, {})
    assert response.status_code == 400
    assert "error" in response.data

@pytest.mark.django_db
@patch('assistant.views.get_shopping_assistant')
def test_chatbot_view_success(mock_get_assistant, authenticated_client):
    mock_agent = MagicMock()
    
    mock_agent.invoke.return_value = {
        "messages": [AIMessage(content="Привіт! Я штучний інтелект. Чим можу допомогти?")]
    }
    mock_get_assistant.return_value = mock_agent

    url = reverse('chat')
    response = authenticated_client.post(url, {"message": "Привіт"})
    
    assert response.status_code == 200
    assert response.data["bot_response"] == "Привіт! Я штучний інтелект. Чим можу допомогти?"
    
    mock_agent.invoke.assert_called_once()
