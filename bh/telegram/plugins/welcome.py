from bh.helpers import Common
from pyrogram import Client, filters, emoji
from pyrogram.types import Message


@Client.on_message(filters.new_chat_members & filters.chat(Common().bot_dustbin), group=1)
async def new_chat_members(c: Client, m: Message):
    mentions = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
    welcome_msg = "{} Welcome to Vakkaru Falcon Headquarters! Keep your " \
                  "calm, be respectful and enjoy the discussion within the group. \n" \
                  "I will be your butler for the services that are given here."

    new_members = [mentions.format(i.first_name, i.id) for i in m.new_chat_members]
    text = welcome_msg.format(emoji.MAN_RAISING_HAND_DARK_SKIN_TONE, ", ".join(new_members))

    await m.reply_text(
        text=text,
        parse_mode="html",
        disable_web_page_preview=True
    )

