from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from perfumeProject import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, ContextTypes, CommandHandler, ApplicationBuilder
from telegram.constants import ParseMode
from perfumeApp.models import PendingOrders, Product
import logging
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
GROUP_ID = os.getenv('GROUP_ID')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")


@sync_to_async
def save_pending_order(message_id, username, phone_number, product_name):
    PendingOrders.objects.create(
        message_id=message_id,
        username=username,
        phone_number=phone_number,
        slug=product_name
    )


async def send_order_to_group(username, phone_number, product_name):
    slug = await get_product_slug(product_name)

    text = (
        f"📦 <b>Новый заказ</b>\n"
        f"👤 Имя: <code>{username}</code>\n"
        f"📱 Телефон: <code>{phone_number}</code>\n"
        f"🛍️ Продукт: <a href='http://127.0.0.1:8000/ru/api/product/{slug}/'><b>{product_name}</b></a>"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Одобрить", callback_data="approve"),
            InlineKeyboardButton("❌ Отклонить", callback_data="reject")
        ]
    ])

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    message = await application.bot.send_message(
        chat_id=GROUP_ID,
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    await save_pending_order(message.id, username, phone_number, product_name)


@sync_to_async
def get_pending_order_by_message_id(message_id):
    return PendingOrders.objects.get(message_id=message_id)


@sync_to_async
def get_product_slug(name):
    product = Product.objects.get(name=name)
    return product.slug


@sync_to_async
def delete_pending_order(order):
    order.delete()


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    moderator = update.effective_user

    await query.answer()

    message_id = query.message.message_id
    order_data = await get_pending_order_by_message_id(message_id)

    if not order_data:
        await query.edit_message_text("⛔ Заказ не найден или уже обработан.")
        return

    await delete_pending_order(order=order_data)

    if query.data == "approve":
        status = "✅ Одобрено"
    else:
        status = "❌ Отклонено"

    slug = await get_product_slug(order_data.slug)

    text = (
        f"📦 <b>Заказ</b>\n"
        f"👤 Имя: <code>{order_data.username}</code>\n"
        f"📱 Телефон: <code>{order_data.phone_number}</code>\n"
        f"🛍️ Продукт: <a href='http://127.0.0.1:8000/ru/api/product/{slug}/'><b>{order_data.slug}</b></a>\n\n"
        f"<b>{status}</b> модератором: "
        f"<a href='tg://user?id={moderator.id}'>{moderator.full_name}</a>"
    )

    await query.edit_message_text(text=text, parse_mode="HTML")


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        app = Application.builder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler('start', start))
        app.add_handler(CallbackQueryHandler(handle_callback))

        self.stdout.write(self.style.SUCCESS("Telegram-бот запущен"))
        app.run_polling()
