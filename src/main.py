import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_carts = {}

products = {
    "t-shirts": {
        "name": "Футболки",
        "items": [
            {
                "id": 1,
                "name": "Футболка черная",
                "price": 2690,
                "description": "Хлопковая футболка черного цвета",
                "image_url": "https://avatars.mds.yandex.net/get-mpic/1865219/2a000001904ac03b511361955534d6e77eea/optimize",
                "sizes": ["M", "L", "XL"]
            },
{
                "id": 2,
                "name": "Футболка белая",
                "price": 990,
                "description": "Белая базовая футболка. 100% хлопок",
                "image_url": "https://yandex-images.clstorage.net/ik55f1h48/820b8dZF/0YoNEutyVEspEfIAE-7qScYmuZqYZKH01HdF1ZTQlfoc7lqmhD5B7e50qmhztlil6lT3_8vZopoLoDsNYaGGZKSueBbO5hGvWRGjRKNKK-kHJ-1bTFX11UQ3MEVU5lZNDplsYfIchr8p0KpopoNcBF5l8Rm6nHJ6TnQbr3AzMOOg-68gq5EG_mjj4LdR_JrJZDQuWCrFJXdS1YWh48U1T--L3VMSHSRviXOKu-XhvtIdtJAq3m6S2YwlyZxAoSAhEAv_M2vANvxaUIPkg9wYu2cVvmooFPY3Uuc3MiLn5U2O6BzykD5mD9uzqGkEsFwQPzYjmc3-IKt8NPh9wPOw00PZP2Ha4zdP-bLydLBuS8rX9n5YiqdUhRNHF3LzJ7ecLJgsE8INJB4aomjpVCBNYm40wpr9rqBo_DQbvBKxMYAz6l2ze8I232rz8QbB_ZqZZQVN6xlWhZSy16bSUqfU3_xqb1OhzGWtyfPYycZxnOKMJzAaXhxy2h6kyS1gAXMwsBvvUiuxxH6b89JUggzYuZVlzwk65xcUE8blMjJF9--MaQ7xwh8F78hSOvtnQhzwzicwaq0-0vhPRhn_gQHAU1CKP9K5Ugf_CpARZdMPuIkFJQwZG1VGJdKn9WLClzdf3wsesyN-B41Z4Qj49lB_szzngqguLOKIbXbbnXExcqIxKi-hClJGPTpTgxfD7CkrBPXNOtgnR2fgt4Uwgke1LF0oTbPzjTZdWeNpeWSTPuJ91LFIvH-w-OynCgzQcZHzsjgsEIlxJ764sVMmMI_puPdELwv7Z1ZE4Ma3YKDG5U0_-3wDs87EbjuDewsGAjzj_XQCSR5M0ZhulhkcUrGAMDNIHbOIMaYfuzPyV2C8e-vmZ34oqac1poN1ZdFClSfsPmjvsoMcNF6oslgaNGNNQk7kkeiPDmO4Pae4H_CiUPMxq32h6SJlTksjYSSR_amIF_Z_6us1tkXglNVAwxYnk",
                "sizes": ["M", "L", "XL"]
            },
        ]
    },
    "hoodies": {
        "name": "Лонгсливы",
        "items": [
            {
                "id": 3,
                "name": "Белый лонгслив",
                "price": 2490,
                "description": "Утепленная толстовка с капюшоном",
                "image_url": "https://mir-s3-cdn-cf.behance.net/project_modules/1400/2963a834267299.56cab65d3d56a.jpg",
                "sizes": ["S", "M", "L"]
            },
            {
                "id": 4,
                "name": "Лонгслив брауни",
                "price": 2990,
                "description": "Свободная толстовка oversize",
                "image_url": "https://sun9-55.userapi.com/impg/nebGToOIDGANtDPza_RweKlKno2ATlRzMTr5TQ/Um4FrTKrz0M.jpg?size=798x883&quality=95&sign=45ce4576f181061a95e2ddefd50e4b89&type=album",
                "sizes": ["L", "XL", "XXL"]
            },
        ]
    }
}


async def safe_delete_message(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id, message_id)
    except TelegramBadRequest as e:
        logger.warning(f"Не удалось удалить сообщение: {e}")


async def show_main_menu(chat_id: int, message_id: int = None):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👕 Футболки", callback_data="category_t-shirts"),
        InlineKeyboardButton(text="🧥 Лонгсливы", callback_data="category_hoodies")
    )
    builder.row(
        InlineKeyboardButton(text="🛒 Корзина", callback_data="view_cart"),
        InlineKeyboardButton(text="ℹ️ О магазине", callback_data="about")
    )

    text = "Добро пожаловать в наш магазин одежды! Выберите категорию:"

    try:
        if message_id:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=builder.as_markup()
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                photo="https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_666c3d5dbdac467014320755_666c426761a30954faafcb95/scale_1200",
                caption=text,
                reply_markup=builder.as_markup()
            )
    except TelegramBadRequest as e:
        logger.error(f"Ошибка при отображении главного меню: {e}")
        await bot.send_message(chat_id, text, reply_markup=builder.as_markup())


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await show_main_menu(message.chat.id)


@dp.callback_query(lambda c: c.data.startswith('category_'))
async def process_category(callback_query: CallbackQuery):
    try:
        category = callback_query.data.split('_')[1]
        category_data = products.get(category)

        if not category_data:
            await callback_query.answer("Категория не найдена")
            return

        await safe_delete_message(callback_query.message.chat.id, callback_query.message.message_id)

        first_item = category_data['items'][0]
        await callback_query.message.answer_photo(
            photo=first_item['image_url'],
            caption=f"Категория: {category_data['name']}\n\nВыберите товар:"
        )

        builder = InlineKeyboardBuilder()
        for item in category_data['items']:
            builder.row(InlineKeyboardButton(
                text=f"{item['name']} - {item['price']}₽",
                callback_data=f"item_{item['id']}"
            ))
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))

        await callback_query.message.answer(
            text="Доступные товары:",
            reply_markup=builder.as_markup()
        )

    except Exception as e:
        logger.error(f"Ошибка в process_category: {e}")
        await callback_query.answer("Произошла ошибка, попробуйте позже")


@dp.callback_query(lambda c: c.data.startswith('item_'))
async def process_item(callback_query: CallbackQuery):
    try:
        item_id = int(callback_query.data.split('_')[1])
        item = None

        for category in products.values():
            for product in category['items']:
                if product['id'] == item_id:
                    item = product
                    break
            if item:
                break

        if not item:
            await callback_query.answer("Товар не найден")
            return

        await safe_delete_message(callback_query.message.chat.id, callback_query.message.message_id)

        await callback_query.message.answer_photo(
            photo=item['image_url'],
            caption=f"<b>{item['name']}</b>\n\n{item['description']}\n\nЦена: <b>{item['price']}₽</b>\n\nДоступные размеры: {', '.join(item['sizes'])}",
            parse_mode="HTML"
        )

        builder = InlineKeyboardBuilder()
        for size in item['sizes']:
            builder.add(InlineKeyboardButton(
                text=size,
                callback_data=f"add_{item['id']}_{size}"
            ))
        builder.row(InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"category_{next(k for k, v in products.items() if any(p['id'] == item_id for p in v['items']))}"
        ))

        await callback_query.message.answer(
            text="Выберите размер:",
            reply_markup=builder.as_markup()
        )

    except Exception as e:
        logger.error(f"Ошибка в process_item: {e}")
        await callback_query.answer("Произошла ошибка, попробуйте позже")


@dp.callback_query(lambda c: c.data.startswith('add_'))
async def add_to_cart(callback_query: CallbackQuery):
    try:
        _, item_id, size = callback_query.data.split('_')
        item_id = int(item_id)

        item = None
        for category in products.values():
            for product in category['items']:
                if product['id'] == item_id:
                    item = product
                    break
            if item:
                break

        if not item:
            await callback_query.answer("Товар не найден")
            return

        user_id = callback_query.from_user.id
        if user_id not in user_carts:
            user_carts[user_id] = []

        user_carts[user_id].append({
            "id": item['id'],
            "name": item['name'],
            "price": item['price'],
            "size": size,
            "image": item['image_url']
        })

        await callback_query.answer(f"Добавлено: {item['name']} (размер {size})")

    except Exception as e:
        logger.error(f"Ошибка в add_to_cart: {e}")
        await callback_query.answer("Не удалось добавить в корзину")


@dp.callback_query(lambda c: c.data == "view_cart")
async def view_cart(callback_query: CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        cart = user_carts.get(user_id, [])

        if not cart:
            await callback_query.answer("🛒 Ваша корзина пуста")
            return

        total = sum(item['price'] for item in cart)
        cart_text = "\n".join(
            f"{i + 1}. {item['name']} (размер: {item['size']}) - {item['price']}₽"
            for i, item in enumerate(cart)
        )

        await safe_delete_message(callback_query.message.chat.id, callback_query.message.message_id)

        await callback_query.message.answer_photo(
            photo=cart[0]['image'],
            caption=f"🛒 Ваша корзина:\n\n{cart_text}\n\nИтого: {total}₽"
        )

        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout"),
            InlineKeyboardButton(text="❌ Очистить корзину", callback_data="clear_cart")
        )
        builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))

        await callback_query.message.answer(
            text="Выберите действие:",
            reply_markup=builder.as_markup()
        )

    except Exception as e:
        logger.error(f"Ошибка в view_cart: {e}")
        await callback_query.answer("Не удалось открыть корзину")

@dp.callback_query(lambda c: c.data == "about")
async def process_about(callback_query: CallbackQuery):
    try:
        about_text = (
            "🛍️ <b>О нашем магазине</b>\n\n"
            "Этот чат-бот создан, чтобы сделать ваши покупки максимально простыми и удобными!\n\n"
            "• 🔍 Легкий поиск товаров по категориям\n"
            "• 🛒 Удобное управление корзиной\n"
            "• 💳 Быстрое оформление заказа\n"
            "• 📦 Отслеживание статуса заказа\n\n"
            "Мы предлагаем качественную одежду по доступным ценам с быстрой доставкой.\n\n"
            "Приятных покупок! 😊"
        )

        await callback_query.message.answer(
            text=about_text,
            parse_mode="HTML"
        )
        await callback_query.answer()

    except Exception as e:
        logger.error(f"Ошибка в process_about: {e}")
        await callback_query.answer("Не удалось загрузить информацию")

@dp.callback_query(lambda c: c.data == "clear_cart")
async def clear_cart(callback_query: CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        if user_id in user_carts:
            del user_carts[user_id]
        await callback_query.answer("Корзина очищена")
        await show_main_menu(callback_query.message.chat.id, callback_query.message.message_id)
    except Exception as e:
        logger.error(f"Ошибка в clear_cart: {e}")
        await callback_query.answer("Не удалось очистить корзину")


@dp.callback_query(lambda c: c.data == "checkout")
async def checkout(callback_query: CallbackQuery):
    try:
        user_id = callback_query.from_user.id
        cart = user_carts.get(user_id, [])

        if not cart:
            await callback_query.answer("Корзина пуста")
            return

        total = sum(item['price'] for item in cart)
        order_details = "\n".join(
            f"{item['name']} (размер: {item['size']})"
            for item in cart
        )

        await callback_query.message.answer(
            text=f"✅ Ваш заказ оформлен!\n\n{order_details}\n\nИтого: {total}₽\n\nСпасибо за покупку!",
        )

        if user_id in user_carts:
            del user_carts[user_id]

    except Exception as e:
        logger.error(f"Ошибка в checkout: {e}")
        await callback_query.answer("Не удалось оформить заказ")


@dp.message(Command("about"))
async def about_command(message: types.Message):
    about_text = """
<b>🏪 О нашем магазине</b>

Мы - современный онлайн-магазин модной одежды, предлагающий:
• Качественные материалы (100% хлопок, премиальные ткани)
• Стильные и актуальные модели
• Доступные цены и регулярные скидки
• Быструю доставку по всей России

<b>📅 Год основания:</b> 2020
<b>⭐ Довольных клиентов:</b> более 10 000

<b>📱 Контакты:</b>
Телефон: +7 (XXX) XXX-XX-XX
Адрес: г. Москва, ул. ПК, 123
Часы работы: Пн-Пт 10:00-20:00, Сб-Вс 11:00-18:00

Для возврата в меню нажмите /start"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 В меню", callback_data="main_menu")],
        [InlineKeyboardButton(text="📞 Связаться", url="https://t.me/tabo0oo")],
        [InlineKeyboardButton(text="🛒 Перейти к покупкам", callback_data="category_t-shirts")]
    ])

    await message.answer_photo(
        photo="https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_666c3d5dbdac467014320755_666c426761a30954faafcb95/scale_1200",
        caption=about_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "main_menu")
async def process_back_to_main(callback_query: CallbackQuery):
    try:
        await show_main_menu(callback_query.message.chat.id, callback_query.message.message_id)
    except Exception as e:
        logger.error(f"Ошибка в process_back_to_main: {e}")
        await callback_query.answer("Не удалось вернуться в меню")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())