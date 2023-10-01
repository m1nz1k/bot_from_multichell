from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_cancel = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                                InlineKeyboardButton(text="Отменить", callback_data="cancel")
                                           ],
                                       ])