"""Private long-polling only after an explicitly authorized invocation."""

import argparse
import asyncio
import json
import logging
import os

import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from citysense.telegram_demo import DemoSettings, OperatorHTTPBackend, TelegramDemo


def build_application(
    token: str, demo: TelegramDemo, client: httpx.AsyncClient | None = None
) -> Application:
    async def dispatch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.effective_user or not update.effective_message or not update.effective_chat:
            return
        # No persistence, context.user_data, raw-content logs or arbitrary intent parsing.
        text = update.effective_message.text or "/help"
        try:
            reply = await asyncio.wait_for(
                demo.handle(
                    update.effective_user.id, text, private=update.effective_chat.type == "private"
                ),
                timeout=20,
            )
        except TimeoutError:
            reply = demo.banner + "\nRequest timed out. No result."
        await update.effective_message.reply_text(reply, disable_web_page_preview=True)

    async def safe_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.getLogger("citysense.telegram").warning(
            "Telegram transport failure; details redacted"
        )

    async def shutdown(application: Application) -> None:
        if client is not None:
            await client.aclose()

    app = (
        Application.builder()
        .token(token)
        .concurrent_updates(False)
        .update_queue(asyncio.Queue(maxsize=100))
        .connect_timeout(5)
        .read_timeout(5)
        .get_updates_connect_timeout(5)
        .get_updates_read_timeout(20)
        .post_shutdown(shutdown)
        .build()
    )
    for name in ("start", "help", "needs", "places", "evaluate", "near", "sports"):
        app.add_handler(CommandHandler(name, dispatch))
    app.add_handler(MessageHandler(filters.LOCATION | (filters.TEXT & ~filters.COMMAND), dispatch))
    app.add_error_handler(safe_error)
    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorize-telegram", action="store_true")
    args = parser.parse_args()
    if not args.authorize_telegram:
        raise SystemExit("Polling requires explicit authorization and a private operator allowlist")
    token = os.environ.get("CITYSENSE_TELEGRAM_TOKEN", "")
    if not token:
        raise SystemExit("CITYSENSE_TELEGRAM_TOKEN is required")
    settings = DemoSettings.model_validate(
        {
            "mode": os.environ.get("CITYSENSE_TELEGRAM_MODE", "real"),
            "allowed_users": json.loads(os.environ.get("CITYSENSE_TELEGRAM_ALLOWED_USERS", "[]")),
            "place_ids": json.loads(os.environ.get("CITYSENSE_TELEGRAM_PLACE_IDS", "[]")),
        }
    )
    # HTTPX request URLs contain the Telegram token: disable library logs before startup.
    for name in ("httpx", "httpcore", "telegram", "apscheduler"):
        logger = logging.getLogger(name)
        logger.handlers = [logging.NullHandler()]
        logger.setLevel(logging.CRITICAL + 1)
        logger.disabled = True
        logger.propagate = False
    client = httpx.AsyncClient(trust_env=False)
    demo = TelegramDemo(
        settings,
        OperatorHTTPBackend(
            os.environ.get("CITYSENSE_OPERATOR_URL", "http://127.0.0.1:8000"),
            os.environ.get("CITYSENSE_API_KEY", ""),
            client,
        ),
    )
    build_application(token, demo, client).run_polling(
        allowed_updates=["message"], drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
