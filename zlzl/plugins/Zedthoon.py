import json
import math
import os
import random
import re
import time
from pathlib import Path
from uuid import uuid4

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from youtubesearchpython import VideosSearch

from . import zedub
from ..Config import Config
from ..helpers.functions import rand_key
from ..helpers.functions.utube import (
    download_button,
    get_yt_video_id,
    get_ytthumb,
    result_formatter,
    ytsearch_data,
)
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)
BTN_URL_REGEX = re.compile(r"(([^]+?)\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
MEDIA_PATH_REGEX = re.compile(r"(:?\<\bmedia:(:?(?:.*?)+)\>)")
tr = Config.COMMAND_HAND_LER

def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb

@zedub.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text.strip()
    query_user_id = event.query.user_id

    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        str_y = query.split(" ", 1)
        if str_y[0].lower() == "ytdl" and len(str_y) == 2:
            try:
                search_text = str_y[1].strip()
                link = get_yt_video_id(search_text)
                found_ = True
                if link is None:
                    search = VideosSearch(search_text, limit=15)
                    resp = (search.result()).get("result", [])
                    if len(resp) == 0:
                        found_ = False
                    else:
                        outdata = await result_formatter(resp)
                        if len(outdata) < 2:
                            found_ = False
                        else:
                            key_ = rand_key()
                            ytsearch_data.store_(key_, outdata)
                            buttons = [
                                Button.inline(f"1 / {len(outdata)}", data=f"ytdl_next_{key_}_1"),
                                Button.inline("القائمـة 📜", data=f"ytdl_listall_{key_}_1"),
                                Button.inline("⬇️  تحميـل", data=f'ytdl_download_{outdata[1]["video_id"]}_0'),
                            ]
                            caption = outdata[1]["message"]
                            photo = await get_ytthumb(outdata[1]["video_id"])
                else:
                    caption, buttons = await download_button(link, body=True)
                    photo = await get_ytthumb(link)

                if found_:
                    markup = event.client.build_reply_markup(buttons)
                    photo = types.InputWebDocument(
                        url=photo, size=0, mime_type="image/jpeg", attributes=[]
                    )
                    text, msg_entities = await event.client._parse_message_text(caption, "html")
                    result = types.InputBotInlineResult(
                        id=str(uuid4()),
                        type="photo",
                        title=link if link else "YouTube Video",
                        description="⬇️ اضغـط للتحميـل",
                        thumb=photo,
                        content=photo,
                        send_message=types.InputBotInlineMessageMediaAuto(
                            reply_markup=markup, message=text, entities=msg_entities
                        ),
                    )
                else:
                    result = builder.article(
                        title="لم يتم العثور على نتائج",
                        text=f"No results found for `{search_text}`",
                        description="INVALID",
                    )
            except Exception as e:
                LOGS.error(f"خطأ أثناء معالجة ytdl: {e}")
                result = builder.article(
                    title="حدث خطأ",
                    text="تعذر معالجة الطلب.",
                    description="Error",
                )

            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="خطأ في الاستعلام",
                            text="حدثت مشكلة أثناء تنفيذ الطلب.",
                            description="QueryIdInvalid",
                        )
                    ]
                )
        elif query.lower() == "pmpermit":
            controlpmch = gvarstatus("pmchannel") or None
            if controlpmch is not None:
                zchannel = controlpmch.replace("@", "")
                buttons = [[Button.url("⌔ قنـاتـي ⌔", f"https://t.me/{zchannel}")]]
            else:
                buttons = [[Button.url("𝗭𝗧𝗵𝗼𝗻", "https://t.me/ZThon")]]

            PM_PIC = gvarstatus("pmpermit_pic")
            ZZZ_IMG = random.choice(PM_PIC.split()) if PM_PIC else None
            query_text = gvarstatus("pmpermit_text") or "مرحبًا! كيف يمكنني مساعدتك؟"

            if ZZZ_IMG and ZZZ_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(ZZZ_IMG, text=query_text, buttons=buttons)
            elif ZZZ_IMG:
                result = builder.document(ZZZ_IMG, title="Alive zzz", text=query_text, buttons=buttons)
            else:
                result = builder.article(title="Alive zzz", text=query_text, buttons=buttons)

            await event.answer([result] if result else None)
