import pytest
from unittest.mock import patch, Mock, create_autospec
from api.user.services import update_user_fcm_token
from api.user.entities import User
from api.quant.entities import Quant
from api import db

@pytest.fixture
def mock_db_session():
    with patch('api.db.session') as mock_session:
        yield mock_session

@pytest.fixture
def mock_user():
    # User 클래스의 속성만 Mock
    user = Mock()
    user.email = 'test@example.com'
    user.app_token = 'old_token'
    # relationship 속성은 빈 리스트로 설정
    user.quants = []
    return user

@patch('api.user.services.get_jwt_identity')
def test_update_user_fcm_token(mock_get_jwt_identity, mock_db_session, mock_user):
    # Given
    test_email = 'test@example.com'
    new_token = 'new_fcm_token'
    mock_get_jwt_identity.return_value = test_email
    
    with patch('api.user.entities.User.query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_user
        
        # When
        result = update_user_fcm_token(new_token)
        
        # Then
        assert result is True
        assert mock_user.app_token == new_token
        mock_get_jwt_identity.assert_called_once()
        mock_query.filter_by.assert_called_once_with(email=test_email)
        mock_db_session.commit.assert_called_once()