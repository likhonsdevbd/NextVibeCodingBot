"""
Basic tests for NextVibeBot client library
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from nextvibe_bot.client import NextVibeClient
from nextvibe_bot.types import RequestResult, ParseModeType
from nextvibe_bot.clients.messages import MessageClient
from nextvibe_bot.clients.auth import AuthClient
from nextvibe_bot.clients.help import HelpClient


class TestNextVibeClient:
    """Test the main NextVibeClient class"""
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = NextVibeClient(token="test_token")
        
        assert client.token == "test_token"
        assert client.messages is not None
        assert client.auth is not None
        assert client.help is not None
        assert hasattr(client, 'keyboards')
        assert hasattr(client, 'users')
        assert hasattr(client, 'chats')
    
    def test_client_config(self):
        """Test client configuration"""
        client = NextVibeClient(token="test_token")
        config = client.get_config()
        
        assert "token_set" in config
        assert "has_application" in config
        assert "modules" in config
        assert config["modules"]["messages"] is True
        assert config["modules"]["auth"] is True
        assert config["modules"]["help"] is True


class TestMessageClient:
    """Test the MessageClient class"""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing"""
        client = Mock()
        client.bot = AsyncMock()
        return client
    
    @pytest.fixture
    def message_client(self, mock_client):
        """Create a MessageClient for testing"""
        return MessageClient(mock_client)
    
    @pytest.mark.asyncio
    async def test_send_message_success(self, message_client):
        """Test successful message sending"""
        # Setup mock
        expected_message = Mock()
        expected_message.message_id = 123
        message_client.main_client.bot.send_message = AsyncMock(return_value=expected_message)
        
        # Test
        result = await message_client.send_message(
            chat_id=123,
            text="Hello World!"
        )
        
        # Verify
        assert result.success is True
        assert result.data == expected_message
        message_client.main_client.bot.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_message_failure(self, message_client):
        """Test failed message sending"""
        # Setup mock to raise exception
        message_client.main_client.bot.send_message = AsyncMock(
            raise Exception("Network error")
        )
        
        # Test
        result = await message_client.send_message(
            chat_id=123,
            text="Hello World!"
        )
        
        # Verify
        assert result.success is False
        assert "Network error" in result.error
    
    @pytest.mark.asyncio
    async def test_edit_message_text_success(self, message_client):
        """Test successful message editing"""
        # Setup mock
        expected_message = Mock()
        expected_message.message_id = 123
        message_client.main_client.bot.edit_message_text = AsyncMock(return_value=expected_message)
        
        # Test
        result = await message_client.edit_message_text(
            chat_id=123,
            message_id=123,
            text="Updated text"
        )
        
        # Verify
        assert result.success is True
        assert result.data == expected_message
    
    @pytest.mark.asyncio
    async def test_delete_message_success(self, message_client):
        """Test successful message deletion"""
        # Setup mock
        message_client.main_client.bot.delete_message = AsyncMock()
        
        # Test
        result = await message_client.delete_message(
            chat_id=123,
            message_id=456
        )
        
        # Verify
        assert result.success is True
        assert result.data is True
        message_client.main_client.bot.delete_message.assert_called_once_with(
            chat_id=123,
            message_id=456
        )


class TestAuthClient:
    """Test the AuthClient class"""
    
    def test_sign_in_success(self):
        """Test successful sign in"""
        # Create a real client for testing
        client = NextVibeClient(token="test_token")
        
        # Run in async context
        async def test_signin():
            result = await client.auth.sign_in(
                user_id=123456,
                username="testuser"
            )
            
            assert result.success is True
            assert result.data is not None
            assert "auth_token" in result.data
            assert result.data["user_id"] == 123456
            assert result.data["username"] == "testuser"
            assert result.data["status"] == "authenticated"
        
        asyncio.run(test_signin())
    
    def test_validate_token_success(self):
        """Test successful token validation"""
        client = NextVibeClient(token="test_token")
        
        async def test_validate():
            # First sign in to get a token
            signin_result = await client.auth.sign_in(
                user_id=123456,
                username="testuser"
            )
            
            # Then validate the token
            token = signin_result.data["auth_token"]
            result = await client.auth.validate_token(token)
            
            assert result.success is True
            assert result.data["valid"] is True
            assert result.data["user_id"] == 123456
        
        asyncio.run(test_validate())
    
    def test_sign_out_success(self):
        """Test successful sign out"""
        client = NextVibeClient(token="test_token")
        
        async def test_signout():
            # First sign in
            await client.auth.sign_in(user_id=123456, username="testuser")
            
            # Then sign out
            result = await client.auth.sign_out(123456)
            
            assert result.success is True
            assert result.data["status"] == "signed_out"
        
        asyncio.run(test_signout())


class TestHelpClient:
    """Test the HelpClient class"""
    
    def test_get_config_success(self):
        """Test successful config retrieval"""
        client = NextVibeClient(token="test_token")
        
        async def test_config():
            result = await client.help.get_config()
            
            assert result.success is True
            assert result.data is not None
            assert "bot_config" in result.data
            assert "api_limits" in result.data
            assert "supported_features" in result.data
            assert "metadata" in result.data
        
        asyncio.run(test_config())
    
    def test_get_commands_success(self):
        """Test successful command list retrieval"""
        client = NextVibeClient(token="test_token")
        
        async def test_commands():
            result = await client.help.get_commands()
            
            assert result.success is True
            assert result.data is not None
            assert "basic_commands" in result.data
            assert "programming_commands" in result.data
            assert "admin_commands" in result.data
        
        asyncio.run(test_commands())
    
    def test_get_feature_info_success(self):
        """Test successful feature info retrieval"""
        client = NextVibeClient(token="test_token")
        
        async def test_features():
            result = await client.help.get_feature_info("voice_transcription")
            
            assert result.success is True
            assert result.data is not None
            assert "description" in result.data
            assert "supported_formats" in result.data
            assert result.data["status"] == "available"
        
        asyncio.run(test_features())


if __name__ == "__main__":
    # Run basic tests
    print("Running NextVibeBot client tests...")
    
    # Test client initialization
    client = NextVibeClient(token="test_token")
    print("✓ Client initialization test passed")
    
    # Test auth client
    async def test_auth():
        result = await client.auth.sign_in(user_id=123, username="test")
        assert result.success
        print("✓ Auth client test passed")
    
    asyncio.run(test_auth())
    
    # Test help client
    async def test_help():
        result = await client.help.get_config()
        assert result.success
        print("✓ Help client test passed")
    
    asyncio.run(test_help())
    
    print("All basic tests passed! 🎉")