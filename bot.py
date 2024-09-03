from aiogram import executor
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp, channel

from keyboards import menu_keyboard, back_btn
from states import Form
import texts


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await message.answer(texts.welcome_text,
                         reply_markup=menu_keyboard())


@dp.callback_query_handler(Text(startswith="select_"))
async def handle_menu(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]

    if action == "one":
        message = await call.message.edit_text(texts.selected_one, reply_markup=back_btn())
        await state.update_data(response_message_id=message.message_id)
        await Form.photo.set()
    elif action == "two":
        await call.message.edit_text(texts.selected_two, reply_markup=back_btn())
    elif action == "three":
        message = await call.message.edit_text(texts.selected_three, reply_markup=back_btn())
        await state.update_data(response_message_id=message.message_id)
        await Form.message.set()

    await call.answer()


@dp.message_handler(state=Form.message, content_types=[ContentType.TEXT, ContentType.PHOTO])
async def process_response(message: Message, state: FSMContext):
    data = await state.get_data()
    response_message_id = data.get("response_message_id")

    if message.content_type == ContentType.TEXT:
        await dp.bot.send_message(
            channel,
            texts.notify_sended.format(
                user_link=texts.user_link.format(user_id=message.from_user.id,
                                                 name=message.from_user.full_name,
                                                 username=message.from_user.username),
                message=message.text
            ),
            disable_web_page_preview=True
        )

    elif message.content_type == ContentType.PHOTO:
        photo_id = message.photo[-1].file_id
        await dp.bot.send_photo(channel,
                                photo=photo_id,
                                caption=texts.notify_sended.format(user_link=texts.user_link.format(user_id=message.from_user.id,
                                                                                                    name=message.from_user.full_name,
                                                                                                    username=message.from_user.username),
                                                                   caption_text=message.caption if message.caption else ''))

    await dp.bot.delete_message(chat_id=message.chat.id, message_id=response_message_id,)

    await message.answer_sticker(texts.sticker_id)
    await message.answer(texts.message_send_admin,
                         reply_markup=back_btn())

    await state.finish()


@dp.message_handler(state=Form.photo, content_types=[ContentType.PHOTO])
async def process_screenshot_review(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    await dp.bot.send_photo(
        channel,
        photo=photo_id,
        caption=texts.review_send_admin.format(user_link=texts.user_link.format(user_id=message.from_user.id,
                                                                                name=message.from_user.full_name,
                                                                                username=message.from_user.username)))

    await message.answer_sticker(texts.sticker_id)
    await message.answer(texts.screenshot_send_user,
                         reply_markup=back_btn())

    await state.finish()


@dp.callback_query_handler(lambda call: call.data == "back_menu", state='*')
async def back_menu(call: CallbackQuery, state=FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await call.message.edit_text(texts.welcome_text,
                                 reply_markup=menu_keyboard())

    await call.answer()


if __name__ == '__main__':
    print('Bot Started')
    executor.start_polling(dp, skip_updates=True)
