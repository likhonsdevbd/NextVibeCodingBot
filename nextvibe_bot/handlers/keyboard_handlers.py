"""
Keyboard handlers for NextVibeCodingBot
Implements various types of inline keyboards and their callback handlers
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from typing import List, Dict, Any

# Define callback data patterns
class CallbackPatterns:
    TASK_TYPE = "task_{type}"
    LANGUAGE = "lang_{code}"
    CONFIRM = "confirm_{action}"
    PAGE = "page_{num}"

async def create_task_type_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for task type selection"""
    keyboard = [
        [
            InlineKeyboardButton("🐛 Bug Fix", callback_data=CallbackPatterns.TASK_TYPE.format(type="bug")),
            InlineKeyboardButton("✨ New Feature", callback_data=CallbackPatterns.TASK_TYPE.format(type="feature"))
        ],
        [
            InlineKeyboardButton("🔍 Code Review", callback_data=CallbackPatterns.TASK_TYPE.format(type="review")),
            InlineKeyboardButton("🔧 Debug", callback_data=CallbackPatterns.TASK_TYPE.format(type="debug"))
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def create_language_keyboard(page: int = 0, items_per_page: int = 6) -> InlineKeyboardMarkup:
    """Create paginated keyboard for programming language selection"""
    languages = {
        "python": "🐍 Python",
        "javascript": "💛 JavaScript",
        "typescript": "💙 TypeScript",
        "java": "☕ Java",
        "cpp": "⚡ C++",
        "go": "🔵 Go",
        "rust": "🦀 Rust",
        "php": "🐘 PHP",
        "ruby": "💎 Ruby"
    }
    
    # Calculate pagination
    total_items = len(languages)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    # Create language buttons for current page
    items = list(languages.items())[start_idx:end_idx]
    keyboard = [
        [InlineKeyboardButton(
            text=label,
            callback_data=CallbackPatterns.LANGUAGE.format(code=code)
        )] for code, label in items
    ]
    
    # Add navigation buttons if needed
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton("◀️ Previous", callback_data=f"page_{page-1}")
        )
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton("Next ▶️", callback_data=f"page_{page+1}")
        )
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(keyboard)

async def create_confirmation_keyboard(action: str) -> InlineKeyboardMarkup:
    """Create confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=CallbackPatterns.CONFIRM.format(action=f"confirm_{action}")),
            InlineKeyboardButton("❌ Cancel", callback_data=CallbackPatterns.CONFIRM.format(action=f"cancel_{action}"))
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def handle_task_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle task type selection callback"""
    query = update.callback_query
    await query.answer()
    
    # Extract task type from callback data
    task_type = query.data.split("_")[1]
    
    # Store task type in user data
    context.user_data["task_type"] = task_type
    
    # Show language selection keyboard
    await query.message.edit_text(
        f"You selected: {task_type}\nNow, choose the programming language:",
        reply_markup=await create_language_keyboard()
    )

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle programming language selection callback"""
    query = update.callback_query
    await query.answer()
    
    # Extract language from callback data
    language = query.data.split("_")[1]
    
    # Store language in user data
    context.user_data["language"] = language
    
    # Show confirmation with task details
    task_type = context.user_data.get("task_type", "unknown")
    await query.message.edit_text(
        f"Please confirm your selection:\n"
        f"Task Type: {task_type}\n"
        f"Language: {language}\n\n"
        f"Ready to proceed?",
        reply_markup=await create_confirmation_keyboard("task")
    )

async def handle_confirmation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle confirmation callback"""
    query = update.callback_query
    await query.answer()
    
    action = query.data.split("_")[1]
    if action.startswith("confirm"):
        # Process the confirmed task
        await query.message.edit_text(
            "Task confirmed! Please provide your code or describe your issue in detail."
        )
    else:
        # Reset and show task type selection again
        context.user_data.clear()
        await query.message.edit_text(
            "Task cancelled. What would you like to do?",
            reply_markup=await create_task_type_keyboard()
        )

async def handle_pagination_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle pagination callback"""
    query = update.callback_query
    await query.answer()
    
    # Extract page number from callback data
    page = int(query.data.split("_")[1])
    
    # Update message with new page of languages
    await query.message.edit_text(
        "Choose the programming language:",
        reply_markup=await create_language_keyboard(page)
    )

# Callback handler mapping
callback_handlers = [
    CallbackQueryHandler(handle_task_callback, pattern=r"^task_"),
    CallbackQueryHandler(handle_language_callback, pattern=r"^lang_"),
    CallbackQueryHandler(handle_confirmation_callback, pattern=r"^confirm_"),
    CallbackQueryHandler(handle_pagination_callback, pattern=r"^page_")
]