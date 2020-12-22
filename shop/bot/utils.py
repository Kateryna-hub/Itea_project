import json

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_kb_from_iterable(
        tag,
        iterable,
        id_field='id',
        text_field='title',

):
    buttons = []

    for i in iterable:
        json_data = json.dumps({
            id_field: str(getattr(i, id_field)),
            'tag': tag
        })
        buttons.append(
            InlineKeyboardButton(
                text=getattr(i, text_field),
                callback_data=json_data
            )
        )
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(*buttons)
    return kb


def inline_kb_from_list(
        tag,
        text_buttons,
        id_field
    ):
    buttons = []

    for i in text_buttons:
        json_data = json.dumps({
            'id': str(id_field),
            'tag': tag
        })
        buttons.append(
            InlineKeyboardButton(
                text=text_buttons[i],
                callback_data=json_data
            )
        )
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(*buttons)
    return kb

