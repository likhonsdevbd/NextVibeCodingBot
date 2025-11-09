# NextVibeCodingBot

Next Vibe Coding - An Autonomous Coding Agent that tackles bugs, small feature requests, and other software engineering sessions, with direct export to Telegram.

## Features

- 🐛 **Bug fixing** - Find and fix errors in your code
- ⚡ **Feature development** - Implement new functionality  
- 🔍 **Code analysis** - Review and optimize your code
- 🛠️ **Debugging** - Help troubleshoot issues
- 📚 **General coding** - Answer questions and provide guidance
- 🎤 **Voice messages** - Send me voice notes for coding help
- 🌐 **Web apps** - Interact through mini applications

## Project Structure

```
nextvibe_bot/
├── bot.py                    # Main bot application
├── config.py                 # Configuration management
├── handlers/                 # Message and command handlers
│   ├── command_handlers.py   # Command processing (/start, /help, etc.)
│   ├── message_handler.py    # Main message processing logic
│   ├── keyboard_handlers.py  # Inline keyboard interactions
│   └── __init__.py
├── services/                 # Core business logic services
│   ├── voice_transcriber.py  # Voice message transcription
│   ├── code_analyzer.py      # Code analysis and understanding
│   ├── code_executor.py      # Safe code execution
│   ├── response_formatter.py # Response formatting and presentation
│   └── task_parser.py        # Task parsing and classification
├── utils/                    # Utility modules
│   ├── ai_client.py          # AI service integration
│   ├── rate_limiter.py       # Rate limiting functionality
│   └── error_handling.py     # Error handling utilities
```

## API Method Reference

### Message Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `messages.sendMessage` | Send a text message to chat | `chat_id`, `text`, `parse_mode`, `reply_markup` | `Message` |
| `messages.editMessageText` | Edit existing message text | `chat_id`, `message_id`, `text` | `Message` |
| `messages.deleteMessage` | Delete a message | `chat_id`, `message_id` | `bool` |
| `messages.sendVoice` | Send voice message | `chat_id`, `voice`, `caption` | `Message` |
| `messages.sendPhoto` | Send photo with optional caption | `chat_id`, `photo`, `caption` | `Message` |
| `messages.sendDocument` | Send document/file | `chat_id`, `document`, `caption` | `Message` |
| `messages.sendLocation` | Send location coordinates | `chat_id`, `latitude`, `longitude` | `Message` |
| `messages.sendContact` | Send contact information | `chat_id`, `phone_number`, `first_name` | `Message` |

### Keyboard Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `keyboards.createInlineKeyboard` | Create inline keyboard markup | `buttons` | `InlineKeyboardMarkup` |
| `keyboards.createReplyKeyboard` | Create reply keyboard markup | `keyboard`, `resize_keyboard` | `ReplyKeyboardMarkup` |
| `keyboards.createForceReply` | Create force reply markup | `selective` | `ForceReply` |
| `keyboards.removeKeyboard` | Remove custom keyboard | `selective` | `ReplyKeyboardRemove` |

### User Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `users.getMe` | Get bot information | - | `User` |
| `users.getChatMember` | Get chat member information | `chat_id`, `user_id` | `ChatMember` |
| `users.getUserProfilePhotos` | Get user profile photos | `user_id`, `offset`, `limit` | `UserProfilePhotos` |

### Chat Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `chats.getChat` | Get chat information | `chat_id` | `Chat` |
| `chats.getChatAdministrators` | Get chat administrators | `chat_id` | `List[ChatMember]` |
| `chats.getChatMemberCount` | Get chat member count | `chat_id` | `int` |

### Callback Query Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `callback.answerCallbackQuery` | Answer callback query | `callback_query_id`, `text`, `show_alert` | `bool` |
| `callback.editMessageText` | Edit message from callback | `chat_id`, `message_id`, `text` | `Message` |

### File Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `files.getFile` | Get file information | `file_id` | `File` |
| `files.downloadFile` | Download file to local | `file_id`, `destination` | `bytes` |

### Payment Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `payments.sendInvoice` | Send invoice | `chat_id`, `title`, `description`, `payload` | `Message` |
| `payments.answerPreCheckoutQuery` | Answer pre-checkout query | `pre_checkout_query_id`, `ok` | `bool` |

### Game Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `games.sendGame` | Send game | `chat_id`, `game_short_name` | `Message` |
| `games.setGameScore` | Set game score | `user_id`, `score`, `chat_id`, `message_id` | `Message` |

### Webhook Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `webhooks.setWebhook` | Set webhook URL | `url`, `certificate` | `bool` |
| `webhooks.deleteWebhook` | Delete webhook | `drop_pending_updates` | `bool` |
| `webhooks.getWebhookInfo` | Get webhook info | - | `WebhookInfo` |

### Bot Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `bot.getMe` | Get bot information | - | `User` |
| `bot.logOut` | Log out bot | - | `bool` |
| `bot.close` | Close bot instance | - | `bool` |

## Python Client Library

### Installation

```python
from nextvibe_bot.client import NextVibeClient
from nextvibe_bot.types import *

# Initialize client
client = NextVibeClient(token="your_bot_token")
```

### Basic Usage

```python
# Send message
message = await client.messages.send_message(
    chat_id="@username",
    text="Hello from NextVibeBot!",
    parse_mode=ParseMode.MARKDOWN
)

# Send inline keyboard
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Click me", callback_data="click")]
])

await client.messages.send_message(
    chat_id=chat_id,
    text="Choose an option:",
    reply_markup=keyboard
)

# Handle callback query
await client.callback.answer_callback_query(
    callback_query_id=query.id,
    text="Button clicked!",
    show_alert=True
)
```

## Client Wrapper Classes

### MessageClient
- `send_message()` - Send text messages
- `edit_message_text()` - Edit existing messages
- `delete_message()` - Delete messages
- `send_photo()` - Send images
- `send_voice()` - Send voice messages
- `send_document()` - Send files
- `send_location()` - Send location data
- `send_contact()` - Send contact info

### KeyboardClient
- `create_inline_keyboard()` - Build inline keyboards
- `create_reply_keyboard()` - Build reply keyboards
- `create_force_reply()` - Force user reply
- `remove_keyboard()` - Hide custom keyboards

### UserClient
- `get_me()` - Get bot info
- `get_chat_member()` - Get user info in chat
- `get_user_profile_photos()` - Get user photos

### ChatClient
- `get_chat()` - Get chat details
- `get_chat_administrators()` - Get chat admins
- `get_chat_member_count()` - Get member count

### CallbackClient
- `answer_callback_query()` - Answer inline queries
- `edit_message_text()` - Edit callback messages

## Configuration

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional AI services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
E2B_API_KEY=your_e2b_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/db
PGHOST=localhost
PGUSER=username
PGDATABASE=database_name
PGPASSWORD=password

# Redis
REDIS_URL=redis://localhost:6379/0

# Code execution
DOCKER_ENABLED=true
CODE_EXECUTION_TIMEOUT=30
MAX_CODE_SIZE=10000

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/nextvibe_bot.log

# Security
MAX_MESSAGES_PER_MINUTE=10
ALLOWED_USERS=user1,user2,user3
```

## Development

### Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure
4. Run the bot: `python main.py`

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_client.py

# Run with coverage
pytest --cov=nextvibe_bot
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Architecture

### Service Layer
- **CodeAnalyzer** - Analyzes and understands coding tasks
- **VoiceTranscriber** - Handles voice message transcription
- **CodeExecutor** - Safely executes and tests code
- **ResponseFormatter** - Formats responses for Telegram
- **TaskParser** - Parses and classifies user requests

### Handler Layer
- **MessageHandler** - Main message processing logic
- **CommandHandlers** - Bot command processing (/start, /help, etc.)
- **KeyboardHandlers** - Inline keyboard callback handling
- **ErrorHandler** - Centralized error handling

### Utility Layer
- **AIClient** - AI service integration (OpenAI, Anthropic)
- **RateLimiter** - Message rate limiting
- **ErrorHandling** - Error handling utilities

## API 9.2 Features

This bot utilizes the latest Telegram Bot API 9.2 features:

- **Enhanced link previews** for better code sharing
- **Message effects** for improved user experience
- **Voice message support** with transcription
- **Web app integration** capabilities
- **Direct messages in channels**
- **Checklist and suggested post handling**
- **Paid media capabilities**
- **Advanced reply parameters**

## License

This project is licensed under the MIT License - see the LICENSE file for details.