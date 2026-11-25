import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/your_channel")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "@your_channel")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with a button to the channel."""
    keyboard = [
        [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user = update.effective_user
    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        "Thanks for reaching out. Please join our official channel "
        "for updates, news and exclusive content."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Redirect any text message to the channel."""
    keyboard = [
        [InlineKeyboardButton("📢 Go to Channel", url=CHANNEL_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "You can find everything on our channel 👇", reply_markup=reply_markup
    )


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
