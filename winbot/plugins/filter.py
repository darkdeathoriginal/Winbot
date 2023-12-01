from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ParseMode as PM
from pyrogram.errors import RPCError
from winbot import LOGGER
from secrets import choice
from winbot.handler import Module, onMessage
from winbot.database.filters import Filters
from winbot.plugins.Utils.messageTypes import get_filter_type, Types
from winbot.plugins.Utils.string import (
    build_keyboard,
    parse_button,
    split_quotes,
    escape_mentions_using_curly_brackets,
)
from winbot.plugins.Utils.regex import regex_searcher
from winbot.plugins.Utils.send_cmd import send_cmd
from re import escape as re_escape


db = Filters()


async def run(app: Client, m: Message, match: str):
    all_filters = db.get_all_filters(m.chat.id)
    actual_filters = {j for i in all_filters for j in i.split("|")}

    if (len(all_filters) >= 50) and (len(actual_filters) >= 150):
        await m.reply_text(
            "Only 50 filters and 150 aliases are allowed per chat!\nTo add more filters, remove the existing ones.",
        )
        return

    if not m.reply_to_message and match == "":
        return await m.reply_text("Please read help section for how to save a filter!")

    if m.reply_to_message and match == "":
        return await m.reply_text("Please read help section for how to save a filter!")

    extracted = await split_quotes(match)
    keyword = extracted[0].lower()

    for k in keyword.split("|"):
        if k in actual_filters:
            return await m.reply_text(f"Filter <code>{k}</code> already exists!")

    if not keyword:
        return await m.reply_text(
            f"<code>{m.text}</code>\n\nError: You must give a name for this Filter!",
        )

    if keyword.startswith("<") or keyword.startswith(">"):
        return await m.reply_text("Cannot save a filter which starts with '<' or '>'")

    eee, msgtype, file_id = await get_filter_type(m)
    lol = eee if m.reply_to_message else extracted[1]
    teks = lol if msgtype == Types.TEXT else eee

    if not m.reply_to_message and msgtype == Types.TEXT and len(m.text.split()) < 3:
        return await m.reply_text(
            f"<code>{m.text}</code>\n\nError: There is no text in here!",
        )

    if not teks and not msgtype:
        return await m.reply_text(
            'Please provide keyword for this filter reply with!\nEnclose filter in <code>"double quotes"</code>',
        )

    if not msgtype:
        return await m.reply_text(
            "Please provide data for this filter reply with!",
        )

    add = db.save_filter(m.chat.id, keyword, teks, msgtype, file_id)
    LOGGER.info(f"{m.from_user.id} added new filter ({keyword}) in {m.chat.id}")
    if add:
        await m.reply_text(
            f"Saved filter for '<code>{', '.join(keyword.split('|'))}</code>' in <b>{m.chat.title}</b>!",
        )
    await m.stop_propagation()


Module({"name": "addfilter", "description": "filter message setter","group":True,"sudo":True}, run)

async def sendFilter(client: Client, m: Message):
    chat_filters = db.get_all_filters(m.chat.id)
    actual_filters = {j for i in chat_filters for j in i.split("|")}

    for trigger in actual_filters:
        pattern = r"( |^|[^\w])" + re_escape(trigger) + r"( |$|[^\w])"
        match = await regex_searcher(pattern, m.text.lower())
        if match:
            try:
                msgtype = await send_filter_reply(client, m, trigger)
                LOGGER.info(f"Replied with {msgtype} to {trigger} in {m.chat.id}")
            except Exception as ef:
                await m.reply_text(f"Error: {ef}")
                LOGGER.error(ef)
            break
        continue
    return


onMessage({"group": True}, sendFilter)


async def send_filter_reply(c: Client, m: Message, trigger: str):
    """Reply with assigned filter for the trigger"""
    getfilter = db.get_filter(m.chat.id, trigger)
    if m and not m.from_user:
        return

    if not getfilter:
        return await m.reply_text(
            "<b>Error:</b> Cannot find a type for this filter!!",
            quote=True,
        )

    msgtype = getfilter["msgtype"]
    if not msgtype:
        return await m.reply_text("<b>Error:</b> Cannot find a type for this filter!!")

    try:
        # support for random filter texts
        splitter = "%%%"
        filter_reply = getfilter["filter_reply"].split(splitter)
        filter_reply = choice(filter_reply)
    except KeyError:
        filter_reply = ""

    parse_words = [
        "first",
        "last",
        "fullname",
        "id",
        "mention",
        "username",
        "chatname",
    ]
    text = await escape_mentions_using_curly_brackets(m, filter_reply, parse_words)
    teks, button = await parse_button(text)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    textt = teks
    try:
        if msgtype == Types.TEXT:
            if button:
                try:
                    await m.reply_text(
                        textt,
                        parse_mode=PM.MARKDOWN,
                        reply_markup=button,
                        disable_web_page_preview=True,
                        quote=True,
                    )
                    return
                except RPCError as ef:
                    await m.reply_text(
                        "An error has occured! Cannot parse note.",
                        quote=True,
                    )
                    LOGGER.error(ef)
                    return
            else:
                await m.reply_text(
                    textt,
                    parse_mode=PM.MARKDOWN,
                    quote=True,
                    disable_web_page_preview=True,
                )
                return

        elif msgtype in (
            Types.STICKER,
            Types.VIDEO_NOTE,
            Types.CONTACT,
            Types.ANIMATED_STICKER,
        ):
            await (await send_cmd(c, msgtype))(
                m.chat.id,
                getfilter["fileid"],
                reply_markup=button,
                reply_to_message_id=m.id,
            )
        else:
            await (await send_cmd(c, msgtype))(
                m.chat.id,
                getfilter["fileid"],
                caption=textt,
                parse_mode=PM.MARKDOWN,
                reply_markup=button,
                reply_to_message_id=m.id,
            )
    except Exception as ef:
        await m.reply_text(f"Error in filters: {ef}")
        return msgtype

    return msgtype
