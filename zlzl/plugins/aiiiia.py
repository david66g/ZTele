import contextlib
import base64
import asyncio
import io
import re
import time
from asyncio import sleep
from datetime import datetime
from math import sqrt

from telethon.events import InlineQuery, callbackquery
from telethon import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest, EditBannedRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

from telethon import events, functions, types
from telethon.tl.types import Channel, Chat, User, ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantsKicked,
    ChatBannedRights,
    MessageActionChannelMigrateFrom,
    MessageEntityCustomEmoji,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
    InputPeerChat,
)
from telethon.errors import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
    FloodWaitError,
    MessageNotModifiedError,
)
from . import zedub
from ..utils import is_admin
from ..sql_helper.locks_sql import get_locks, is_locked, update_lock
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import reply_id, _format
from ..sql_helper.fsub_sql import *
from ..helpers import readable_time
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

ANTI_DDDD_ZEDTHON_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_media=True, send_stickers=True, send_gifs=True
)
from ..Config import Config
zed_dev = (925972505, 1895219306, 5280339206)
kicked_count = 0
The_Premium = False
activated = []
admins_out = {}
plugin_category = "الادمن"

async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod

@zedub.zed_cmd(
    pattern="قفل(?: |$)(.*)",
    command=("قفل", plugin_category),
    info={
        "header": "اوامــر قفـل الحمـاية الخـاصه بـ المجمـوعـات",
        "الوصـف": "اوامـر ذكيـه لـ قفـل / فتـح حمـاية المجمـوعـات بالمسـح والطـرد والتقييـد لـ اول مـره فقـط ع سـورس زدثــون",
        "الاوامـر": {
            "الدردشه": "- لـ قفـل ارسـال الرسـائل فقـط",
            "الميديا": "- لـ قفـل ارسـال الوسـائط",
            "الدخول": "- لـ قفـل دخـول الاعضـاء",
            "الفارسيه": "- لـ قفـل الفـارسيـه",
            "الفشار": "- لـ قفـل الفشـار والسـب",
            "المعرفات": "- لـ قفـل ارسـال المعـرفات",
            "الانلاين": "- لـ قفـل انـلاين البـوتـات",
            "البوتات": "- لـ قفـل اضـافة البـوتـات",
            "الاضافه": "- لـ قفـل اضـافة الاعضـاء",
            "التوجيه": "- لـ قفـل التـوجيـه",
            "الروابط": "- لـ قفـل ارسـال الروابـط",
            "الكل": "- لـ قفـل كـل الاوامـر",
        },
        "الاسـتخـدام": "{tr}قفل + الامــر",
    },
    #groups_only=True,
    require_admin=True,
)
async def _(event):
    if not event.is_group:
        return #await edit_or_reply(event, "**ايا مطـي! ، هـذه ليست مجموعـة لقفـل الأشيـاء**")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    zed_id = event.chat_id
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str in ("الدردشه", "الدردشة", "الصور", "الملصقات", "المتحركه", "المتحركة", "المتحركات" "الفيديو", "الصوت", "البصمات", "الكل"):
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        embed_link = chat_per.embed_links
        gpoll = chat_per.send_polls
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "الدردشة" or input_str == "الدردشه":
            if msg:
                return await edit_or_reply(event, "**⎉╎الدردشـة مغلقـه بالفعـل سابقـاً ☑️ •**")
            msg = True
            what = "الدردشـه"
        elif input_str == "الصور" or input_str == "الفيديو" or input_str == "الصوت" or input_str == "البصمات":
            if media:
                return await edit_or_reply(event, "**⎉╎الوسائـط مغلقـه بالفعـل سابقـاً ☑️ •**")
            media = True
            what = "الصـور والفيديـو والصـوت"
        elif input_str == "الملصقات":
            if sticker:
                return await edit_or_reply(event, "**⎉╎الملصقـات مغلقـه بالفعـل سابقـاً ☑️ •**")
            sticker = True
            what = "الملصقـات"
        elif input_str == "المتحركه":
            if gif:
                return await edit_or_reply(event, "**⎉╎المتحركـات مغلقـه بالفعـل سابقـاً ☑️ •**")
            gif = True
            what = "المتحركـات"
        elif input_str == "الكل":
            msg = None
            media = True
            sticker = True
            gif = True
            what = "الكـل"
            update_lock(zed_id, "bots", True)
            update_lock(zed_id, "game", True)
            update_lock(zed_id, "forward", True)
            update_lock(zed_id, "egame", True)
            update_lock(zed_id, "rtl", True)
            update_lock(zed_id, "url", True)
            update_lock(zed_id, "contact", True)
            update_lock(zed_id, "location", True)
            update_lock(zed_id, "button", True)
            update_lock(zed_id, "inline", True)
            update_lock(zed_id, "video", True)
            update_lock(zed_id, "sticker", True)
            update_lock(zed_id, "voice", True)
            update_lock(zed_id, "audio", True)
        lock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            embed_links=embed_link,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights))
            return await edit_or_reply(event, f"**⎉╎تـم قفـل {what} بنجـاح ✅ •**")
        except BaseException as e:
            return await edit_or_reply(event, f"**⎉╎عـذࢪاً  عـزيـزي ..**\n**⎉╎لا املك صـلاحيات هنـا**")
    if input_str == "البوتات":
        update_lock(zed_id, "bots", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة الطـرد والتحذيـر •**".format(input_str))
    if input_str == "المعرفات":
        update_lock(zed_id, "button", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الدخول":
        update_lock(zed_id, "location", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة الطـرد والتحذيـر •**".format(input_str))
    if input_str == "الفارسيه" or input_str == "دخول الايران":
        update_lock(zed_id, "egame", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الاضافه":
        update_lock(zed_id, "contact", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة الطـرد والتحذيـر •**".format(input_str))
    if input_str == "التوجيه":
        update_lock(zed_id, "forward", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الميديا":
        update_lock(zed_id, "game", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح بالتقييـد والتحذيـر •**".format(input_str))
    if input_str == "تعديل الميديا":
        update_lock(zed_id, "document", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح بالتقييـد والتحذيـر •**".format(input_str))
    if input_str == "الانلاين":
        update_lock(zed_id, "inline", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الفشار":
        update_lock(zed_id, "rtl", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "الروابط":
        update_lock(zed_id, "url", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
    if input_str == "التفليش" or input_str == "الخيانه" or input_str == "الخيانة":
        update_lock(zed_id, "audio", True)
        return await edit_or_reply(event, "**⎉╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة تنزيـل المشـرف الخـائن •**".format(input_str))
    if input_str == "المميز":
        return
    else:
        if input_str:
            return await edit_or_reply(event, f"**⎉╎عذراً لايـوجـد امـر بـ اسـم :** `{input_str}`\n**⎉╎لعـرض اوامـر القفـل والفتـح ارسـل** `.م4`")

        return await edit_or_reply(event, "**⎉╎عـذࢪاً عـزيـزي .. لايمكنك قفـل اي شي هنـا ...𓆰**")

@zedub.zed_cmd(
    pattern="فتح(?: |$)(.*)",
    command=("فتح", plugin_category),
    info={
        "header": "اوامــر فتـح الحمـاية الخـاصه بـ المجمـوعـات",
        "الوصـف": "اوامـر ذكيـه لـ قفـل / فتـح حمـاية المجمـوعـات بالمسـح والطـرد والتقييـد لـ اول مـره فقـط ع سـورس زدثــون",
        "الاوامـر": {
            "الدردشه": "- لـ فتـح ارسـال الرسـائل فقـط",
            "الميديا": "- لـ فتـح ارسـال الوسـائط",
            "الدخول": "- لـ فتـح دخـول الاعضـاء",
            "الفارسيه": "- لـ فتـح الفـارسيـه",
            "الفشار": "- لـ فتـح الفشـار والسـب",
            "المعرفات": "- لـ فتـح ارسـال المعـرفات",
            "الانلاين": "- لـ فتـح انـلاين البـوتـات",
            "البوتات": "- لـ فتـح اضـافة البـوتـات",
            "الاضافه": "- لـ فتـح اضـافة الاعضـاء",
            "التوجيه": "- لـ فتـح التـوجيـه",
            "الروابط": "- لـ فتـح ارسـال الروابـط",
            "الكل": "- لـ فتـح كـل الاوامـر",
        },
        "الاسـتخـدام": "{tr}فتح + الامــر",
    },
    #groups_only=True,
    require_admin=True,
)
async def _(event):
    if not event.is_group:
        return #await edit_or_reply(event, "**ايا مطـي! ، هـذه ليست مجموعـة لقفـل الأشيـاء**")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    zed_id = event.chat_id
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str in ("الدردشه", "الدردشة", "الصور", "الملصقات", "المتحركه", "المتحركة", "المتحركات" "الفيديو", "الصوت", "البصمات", "الكل"):
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        gpoll = chat_per.send_polls
        embed_link = chat_per.embed_links
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "الدردشة" or input_str == "الدردشه":
            if not msg:
                return await edit_or_reply(event, "**⎉╎الدردشـة غيـر مغلقـه اسـاسـاً ☑️ •**")
            msg = False
            what = "الدردشـه"
        elif input_str == "الصور" or input_str == "الفيديو" or input_str == "الصوت" or input_str == "البصمات":
            if not media:
                return await edit_or_reply(event, "**⎉╎الوسائـط غيـر مغلقـه اسـاسـاً ☑️ •**")
            media = False
            what = "الصـور والفيديـو والصـوت"
        elif input_str == "الملصقات":
            if not sticker:
                return await edit_or_reply(event, "**⎉╎الملصقـات غيـر مغلقـه اسـاسـاً ☑️ •**")
            sticker = False
            what = "الملصقـات"
        elif input_str == "المتحركه":
            if not gif:
                return await edit_or_reply(event, "**⎉╎المتحركـات غيـر مغلقـه اسـاسـاً ☑️ •**")
            gif = False
            what = "المتحركـات"
        elif input_str == "الكل":
            msg = False
            media = False
            sticker = False
            gif = False
            what = "الكـل"
            update_lock(zed_id, "bots", False)
            update_lock(zed_id, "game", False)
            update_lock(zed_id, "forward", False)
            update_lock(zed_id, "egame", False)
            update_lock(zed_id, "rtl", False)
            update_lock(zed_id, "url", False)
            update_lock(zed_id, "contact", False)
            update_lock(zed_id, "location", False)
            update_lock(zed_id, "button", False)
            update_lock(zed_id, "inline", False)
            update_lock(zed_id, "video", False)
            update_lock(zed_id, "sticker", False)
            update_lock(zed_id, "voice", False)
            update_lock(zed_id, "audio", False)
        unlock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            embed_links=embed_link,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=unlock_rights))
            return await edit_or_reply(event, f"**⎉╎تـم فتـح {what} بنجـاح ✅ •**")
        except BaseException as e:
            return await edit_or_reply(event, f"**⎉╎عـذࢪاً  عـزيـزي ..**\n**⎉╎لا املك صـلاحيات هنـا**")
    if input_str == "البوتات":
        update_lock(zed_id, "bots", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الدخول":
        update_lock(zed_id, "location", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الاضافه":
        update_lock(zed_id, "contact", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "التوجيه":
        update_lock(zed_id, "forward", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الفارسيه" or input_str == "دخول الايران":
        update_lock(zed_id, "egame", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الفشار":
        update_lock(zed_id, "rtl", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الروابط":
        update_lock(zed_id, "url", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الميديا":
        update_lock(zed_id, "game", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "تعديل الميديا":
        update_lock(zed_id, "document", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "المعرفات":
        update_lock(zed_id, "button", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "الانلاين":
        update_lock(zed_id, "inline", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    if input_str == "التفليش" or input_str == "الخيانه" or input_str == "الخيانة":
        update_lock(zed_id, "audio", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح {} بنجـاح ✅ •**\n\n**⎉╎وتعطيـل مانـع التفليـش •**".format(input_str))
    if input_str == "المميز":
        return
    if input_str == "الفارسيه":
        update_lock(zed_id, "egame", False)
        return await edit_or_reply(event, "**⎉╎تـم فتـح** {} **بنجـاح ✅ 𓆰•**".format(input_str))
    else:
        if input_str:
            return await edit_or_reply(event, f"**⎉╎عذراً لايـوجـد امـر بـ اسـم :** `{input_str}`\n**⎉╎لعـرض اوامـر القفـل والفتـح ارسـل** `.م4`")

        return await edit_or_reply(event, "**⎉╎عـذࢪاً عـزيـزي .. لايمكنك اعـادة فتـح اي شي هنـا ...𓆰**")

@zedub.zed_cmd(pattern="(المميز تفعيل|قفل المميز)")
async def lock_premium(event):
    global The_Premium
    The_Premium = True
    activated.append(event.chat_id)
    return await edit_or_reply(event, "**⎉╎تم قفـل الايمـوجي المميـز .. بنجاح ✓**")

@zedub.zed_cmd(pattern="(المميز تعطيل|فتح المميز)")
async def unlock_premium(event):
    global The_Premium
    The_Premium = False
    activated.remove(event.chat_id)
    return await edit_or_reply(event, "**⎉╎تم فتـح الايمـوجي المميـز .. بنجاح ✓**")

@zedub.zed_cmd(
    pattern="الاعدادات$",
    command=("الاعدادات", plugin_category),
    info={
        "header": "لـ عـرض اعـدادات حمـاية المجمـوعـة الخـاصـه ببـوت زدثــون",
        "الاسـتخـدام": "{tr}الاعدادات",
    },
    #groups_only=True,
)
async def _(event):
    if not event.is_group:
        return #await edit_or_reply(event, "**ايا مطـي! ، هـذه ليست مجموعـة لقفـل الأشيـاء**")
    if event.fwd_from:
        return
    res = "**- فيمـا يلـي إعـدادات حمـاية المجمـوعـة :**\n**- الخاصـه بـ سـورس زدثــون**\n\n"
    ubots = "✅" if is_locked(event.chat_id, "bots") else "❌"
    uegame = "✅" if is_locked(event.chat_id, "egame") else "❌"
    urtl = "✅" if is_locked(event.chat_id, "rtl") else "❌"
    uforward = "✅" if is_locked(event.chat_id, "forward") else "❌"
    ubutton = "✅" if is_locked(event.chat_id, "button") else "❌"
    uurl = "✅" if is_locked(event.chat_id, "url") else "❌"
    ugame = "✅" if is_locked(event.chat_id, "game") else "❌"
    udocument = "✅" if is_locked(event.chat_id, "document") else "❌"
    ulocation = "✅" if is_locked(event.chat_id, "location") else "❌"
    ucontact = "✅" if is_locked(event.chat_id, "contact") else "❌"
    ubutton = "✅" if is_locked(event.chat_id, "button") else "❌"
    uinline = "✅" if is_locked(event.chat_id, "inline") else "❌"
    uaudio = "✅" if is_locked(event.chat_id, "audio") else "❌"
    res += f"**⎉╎ البوتات :** {ubots}\n"
    res += f"**⎉╎ الدخول :** {ulocation}\n"
    res += f"**⎉╎ دخول الايران :** {uegame}\n"
    res += f"**⎉╎ الاضافه :** {ucontact}\n"
    res += f"**⎉╎ التوجيه :** {uforward}\n"
    res += f"**⎉╎ الميديا :** {ugame}\n"
    res += f"**⎉╎ تعديـل الميديـا :** {udocument}\n"
    res += f"**⎉╎ المعرفات :** {ubutton}\n"
    res += f"**⎉╎ الفارسيه :** {uegame}\n"
    res += f"**⎉╎ الفشار :** {urtl}\n"
    res += f"**⎉╎ الروابط :** {uurl}\n"
    res += f"**⎉╎ الانلاين :** {uinline}\n"
    res += f"**⎉╎ التفليش :** {uaudio}\n"
    await edit_or_reply(event, res)


@zedub.zed_cmd(incoming=True, forword=None)
async def check_incoming_messages(event):
    if not event.is_group:
        return
    try:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    except Exception:
        return
    zed_dev = (925972505, 1895219306, 5280339206)
    zelzal = event.sender_id
    zelzal_by = event.sender_id
    malath = zedub.uid
    hhh = event.message.text
    ttt = gvarstatus("ANTI_THIFT")
    zed_id = event.chat_id
    user = await event.get_sender()
    try:
        zelzal_by = user.id
    except AttributeError:
        zelzal_by = event.sender_id
    except Exception:
        return
    if ttt is not None:
        first = zelzal.first_name
        last = zelzal.last_name
        if ttt in first:
            if zelzal == malath or await is_admin(event, zelzal) or not await is_admin(event, malath):
                return
            try:
                await event.delete()
                await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - كاشـف الانتحـال ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**الحيـوان** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**ليه منتحـل اسمـي ياورع 😡⚠️•**", link_preview=False)
            except Exception as e:
                return
            if BOTLOG:
                await event.client.send_message(BOTLOG_CHATID,
                    "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎بانتحـال اسمـك**\n**⎉╎تم تحذيـر الشخـص وكتمـه .. بنجـاح ✓𓆰**".format(
                        zelzal
                    )
                )
    if is_locked(zed_id, "rtl") and ("خرا" in hhh or "كسها" in hhh or "كسمك" in hhh or "كسختك" in hhh or "عيري" in hhh or "كسخالتك" in hhh or "خرا بالله" in hhh or "عير بالله" in hhh or "كسخواتكم" in hhh or "اختك" in hhh or "بڪسسخخت" in hhh or "كحاب" in hhh or "مناويج" in hhh or "كحبه" in hhh or " كواد " in hhh or "كواده" in hhh or "تبياته" in hhh or "تبياتة" in hhh or "فرخ" in hhh or "كحبة" in hhh or "فروخ" in hhh or "طيز" in hhh or "آإيري" in hhh or "اختج" in hhh or "سالب" in hhh or "موجب" in hhh or "فحل" in hhh or "كسي" in hhh or "كسك" in hhh or "كسج" in hhh or "مكوم" in hhh or "نيج" in hhh or "نتنايج" in hhh or "مقاطع" in hhh or "ديوث" in hhh or "دياث" in hhh or "اديث" in hhh or "محارم" in hhh or "سكس" in hhh or "مصي" in hhh or "اعرب" in hhh or "أعرب" in hhh or "قحب" in hhh or "قحاب" in hhh or "عراب" in hhh or "مكود" in hhh or "عربك" in hhh or "مخنث" in hhh or "مخنوث" in hhh or "فتال" in hhh or "زاني" in hhh or "زنا" in hhh or "لقيط" in hhh or "بنات شوارع" in hhh or "بنت شوارع" in hhh or "نيك" in hhh or "منيوك" in hhh or "منيوج" in hhh or "نايك" in hhh or "قواد" in hhh or "زبي" in hhh or "ايري" in hhh or "ممحو" in hhh or "بنت شارع" in hhh or " است " in hhh or "اسات" in hhh or "زوب" in hhh or "عيير" in hhh or "املس" in hhh or "مربرب" in hhh or " خول " in hhh or "عرص" in hhh or "قواد" in hhh or "اهلاتك" in hhh or "جلخ" in hhh or "شرمو" in hhh or "فرك" in hhh or "رهط" in hhh):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع الفشـار والسب هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "rtl", False)
    if is_locked(zed_id, "game") and event.message.media:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع ارسـال الوسائـط هنـا 🚸•**\n\n⌔╎**تـم تقييدك مـن ارسـال الوسائط 📵**\n⌔╎**التـزم الهـدوء .. تستطـيع ارسـال الرسـائل فقـط..**", link_preview=False)
	            await event.client(
	                EditBannedRequest(
	                    event.chat_id, event.sender_id, ANTI_DDDD_ZEDTHON_MODE
	                )
	            )
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "game", False)
    if is_locked(zed_id, "forward") and event.fwd_from:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع التوجيـه هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "forward", False)
    if is_locked(zed_id, "button") and "@" in hhh:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع ارسـال المعـرفـات هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "button", False)
    if is_locked(zed_id, "egame") and ("فارسى" in hhh or "خوببی" in hhh or "میخوام" in hhh or "کی" in hhh or "پی" in hhh or "گ" in hhh or "خسته" in hhh or "صكص" in hhh or "راحتی" in hhh or "بیام" in hhh or "بپوشم" in hhh or "گرمه" in hhh or "چ" in hhh or "چه" in hhh or "ڬ" in hhh or "ٺ" in hhh or "چ" in hhh or "ڿ" in hhh or "ڇ" in hhh or "ڀ" in hhh or "ڎ" in hhh or "ݫ" in hhh or "ژ" in hhh or "ڟ" in hhh or "۴" in hhh or "زدن" in hhh or "دخترا" in hhh or "كسى" in hhh or "مک" in hhh or "خالى" in hhh or "ݜ" in hhh or "ڸ" in hhh or "پ" in hhh or "بند" in hhh or "عزيزم" in hhh or "برادر" in hhh or "باشى" in hhh or "ميخوام" in hhh or "خوبى" in hhh or "ميدم" in hhh or "كى اومدى" in hhh or "خوابيدين" in hhh):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع التحـدث بالفارسيـه هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "egame", False)
    if is_locked(zed_id, "url") and "http" in hhh:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع ارسـال الروابـط هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "url", False)
    if is_locked(zed_id, "inline") and event.message.via_bot:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع استخـدام الانلايـن في هذه المجموعـة ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "inline", False)

@zedub.on(events.NewMessage(incoming=True))
async def Premiumz(event):
    if not The_Premium:
        return
    if not event.is_group:
        return
    if event.is_private or event.chat_id not in activated:
        return
    sender_id = event.sender_id
    malath = zedub.uid
    if sender_id == malath or await is_admin(event, sender_id) or not await is_admin(event, malath):
        return
    if sender_id not in zed_dev:
        if isinstance(event.message.entities, list) and any(isinstance(entity, MessageEntityCustomEmoji) for entity in event.message.entities):
            try:
                await event.delete()
                sender = await event.get_sender()
                usr_entity = await zedub.get_entity(sender.id)
                usr_profile = f"[{usr_entity.first_name}](tg://user?id={usr_entity.id})"
                await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** {usr_profile} .\n⌔╎**يُمنـع ارسـال الايمـوجي المميـز هنـا ⚠️•**", link_preview=False)
            except Exception as e:
                return


@zedub.on(events.MessageEdited)
async def check_edit_media(event):
    if not is_locked(event.chat_id, "document"):
        return
    if not event.is_group:
        return
    if event.is_group:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (925972505, 1895219306, 5280339206) 
    zelzal = event.sender_id
    malath = zedub.uid
    hhh = event.message.text
    zed_id = event.chat_id
    user = await event.get_sender()
    if is_locked(zed_id, "document") and event.message.media:
        if zelzal == malath or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع تعديـل الميديـا هنـا 🚫**\n⌔╎**تم حـذف التعديـل .. بنجـاح ☑️**", link_preview=False)
	            await event.client(
	                EditBannedRequest(
	                    event.chat_id, event.sender_id, ANTI_DDDD_ZEDTHON_MODE
	                )
	            )
	        except Exception: 
	            update_lock(zed_id, "document", False)


@zedub.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "contact"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (925972505, 1895219306, 5280339206)
    malath = zedub.uid
    if event.user_added:
        zedy = await event.client.get_entity(event.user_id)
        zelzal_by = event.action_message.sender_id
        zed = await event.client.get_permissions(event.chat_id, zelzal_by)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if event.user_added:
                is_ban_able = True
                if zelzal_by == malath or zed.is_admin or zelzal_by in zed_dev:
                    return
                else:
	                try:
	                    await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, user_obj, rights
	                        )
	                    )
	                    await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع اضـافة الاعضـاء لـ هـذه المجموعـة ⚠️•**\n\n⌔╎**تـم حظـࢪ العضـو المضـاف .. بنجـاح ☑️**", link_preview=False)
	                except Exception as e:
	                    await event.reply(
	                        "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(
	                            str(e)
	                        )
	                    )
	                    update_lock(event.chat_id, "contact", False)
	                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎باضافـة اشخـاص للمجمـوعـة**\n**⎉╎تم تحذيـر الشخـص وطـرد الاعضـاء المضافيـن .. بنجـاح ✓𓆰**".format(
                    zelzal_by
                )
            )

@zedub.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "egame"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (1895219306, 925972505)
    if event.user_joined: 
        a_user = await event.get_user()
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        zedy = await event.client.get_entity(event.user_id)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        if event.user_joined and ("ژ" in first or "چ" in first or "۴" in first or "مهسا" in first or "sara" in first or "گ" in first or "نازنین" in first or "آسمان" in first or "ڄ" in first or "پ" in first or "Sanaz" in first or "𝓈𝒶𝓇𝒶" in first or "سارة" in first or "GIRL" in first or " Lady " in first or "فتاة" in first or "👅" in first or "سمانه" in first or "بهار" in first or "maryam" in first or "👙" in first or "هانیه" in first or "هستی" in first or "💋" in first or "ندا" in first or "Mina" in first or "خانم" in first or "ایناز" in first or "مبینا" in first or "امینی" in first or "سرنا" in first or "اندیشه" in first or "لنتكلم" in first or "دریا" in first or "زاده" in first or "نااز" in first or "ناز" in first or "بیتا" in first or "سكس" in first or "💄" in first or "اعرب" in first or "أعرب" in first or "قحب" in first or "قحاب" in first or "عراب" in first or "مكود" in first or "عربك" in first or "مخنث" in first or "مخنوث" in first or "فتال" in first or "زاني" in first or "زنا" in first or "لقيط" in first or "بنات شوارع" in first or "بنت شوارع" in first or "نيك" in first or "منيوك" in first or "منيوج" in first or "نايك" in first or "قواد" in first or "زبي" in first or "ايري" in first or "ممحو" in first or "بنت شارع" in first or " است " in first or "اسات" in first or "زوب" in first or "عيير" in first or "املس" in first or "مربرب" in first or " خول " in first or "عرص" in first or "قواد" in first or "اهلاتك" in first or "جلخ" in first or "شرمو" in first or "فرك" in first or "رهط" in first):
            is_ban_able = True
            if zedy.id in zed_dev:
                return
            else:
	            try:
	                await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, zedy.id, rights
	                        )
	                    )
	                await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً**  [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع انضمـام الايـࢪان هنـا 🚷•**\n\n⌔╎**تـم حظـࢪه .. بنجـاح ☑️**", link_preview=False)
	            except Exception as e:
	                await event.reply(
	                    "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(
	                        str(e)
	                    )
	                )
	                update_lock(event.chat_id, "egame", False)
	                return
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**⎉╎** [عـزيـزي](tg://user?id={}) **يمنـع دخـول الايـران لهـذه المجمـوعـة 𓆰•**".format(
                    zedy.id
                )
            )

@zedub.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "location"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (925972505, 1895219306, 5280339206)
    if event.user_joined: 
        zedy = await event.client.get_entity(event.user_id)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        if event.user_joined:
            is_ban_able = True
            if zedy.id in zed_dev:
                return
            else:
	            try:
	                await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, zedy.id, rights
	                        )
	                    )
	                await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع الانضمـام لـ هـذه المجموعـة 🚷•**\n⌔╎**تـم حظـࢪه .. بنجـاح ☑️**", link_preview=False)
	            except Exception as e:
	                await event.reply(
	                    "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(
	                        str(e)
	                    )
	                )
	                update_lock(event.chat_id, "location", False)
	                return
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎بالانضمـام للمجمـوعـة**\n**⎉╎تم تحذيـر الشخـص وطـرده .. بنجـاح ✓𓆰**".format(
                    zedy.id
                )
            )


@zedub.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "bots"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (925972505, 1895219306, 5280339206)
    malath = zedub.uid
    if event.user_added:
        zedy = await event.client.get_entity(event.user_id)
        zelzal_by = event.action_message.sender_id
        zed = await event.client.get_permissions(event.chat_id, zelzal_by)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                if zelzal_by == malath or zelzal_by in zed_dev:
                    return
                else:
	                try:
	                    await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, user_obj, rights
	                        )
	                    )
	                    await event.reply(f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع اضـافة البـوتـات لـ هـذه المجمـوعـة 🚫•**", link_preview=False)
	                except Exception as e:
	                    await event.reply(
	                        "**⎉╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا 𓆰** \n`{}`".format(
	                            str(e)
	                        )
	                    )
	                    update_lock(event.chat_id, "bots", False)
	                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**⎉╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎باضـافة بـوت للمجمـوعـة**\n**⎉╎تم تحذيـر الشخـص وطـرد البـوت .. بنجـاح ✓𓆰**".format(
                    zelzal_by
                )
            )


@zedub.on(events.ChatAction())
async def handle_event(event):
    global kicked_count
    if not is_locked(event.chat_id, "bots"):
        return
    if not event.is_group:
        return
    zedy = await event.client.get_entity(event.user_id)
    if event.user_id in await zedub.get_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        if "kicked" in event.raw_text:
            zedy = await event.client.get_entity(event.user_id)
            kicked_count += 1
            if kicked_count == 3:
                await zedub(EditAdminRequest(event.chat_id, zedy.id, change_info=False,
                                              post_messages=False, edit_messages=False,
                                              delete_messages=False, ban_users=False,
                                              invite_users=False, pin_messages=False,
                                              add_admins=False))
                await zedub(EditAdminRequest(event.chat_id, zedy.id, rank=''))
                kicked_count = 0
                await edit_or_reply(event, f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**مشرف خاين** [{zedy.first_name}](tg://user?id={zedy.id}) .\n⌔╎**حاول تفليش المجموعـة•**\n⌔╎**تم تنزيلـه .. بنجـاح ✅**", link_preview=False)


@zedub.zed_cmd(pattern=f"البوتات ?(.*)")
async def zelzal(zed):
    con = zed.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**⎉╎مجمـوعتك/قناتـك في أمـان ✅.. لاتوجـد بوتـات في هذه المجمـوعـة ༗**"
    if con != "طرد":
        event = await edit_or_reply(zed, "**⎉╎جـاري البحـث عن بوتات في هـذه المجمـوعـة ...🝰**")
        async for user in zed.client.iter_participants(zed.chat_id):
            if user.bot:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"🛂**┊كشـف البـوتات -** 𝙎𝙊𝙐𝙍𝘾𝞝 𝙕𝙏𝙃𝙊𝙉\
                           \n\n**⎉╎تم العثور على** **{del_u}**  **بـوت**\
                           \n**⎉╎لطـرد البوتات استخدم الامـر التالي ⩥** `.البوتات طرد`"
        await event.edit(del_status)
        return
    chat = await zed.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(zed, "**⎉╎عـذࢪاً .. احتـاج الى صلاحيـات المشـرف هنـا**")
        return
    event = await edit_or_reply(zed, "**⎉╎جـارِ طـرد البوتـات من هنـا ...⅏**")
    del_u = 0
    del_a = 0
    async for user in zed.client.iter_participants(zed.chat_id):
        if user.bot:
            try:
                await zed.client.kick_participant(zed.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_or_reply(event, "**⎉╎اووبس .. ليس لدي صلاحيـات حظـر هنـا**")
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**⎉╎تم طـرد  {del_u}  بـوت .. بنجـاح🚮**"
    if del_a > 0:
        del_status = f"❇️**┊طـرد البـوتات -** 𝙎𝙊𝙐𝙍𝘾𝞝 𝙕𝙏𝙃𝙊𝙉\
                           \n\n**⎉╎تم طـرد  {del_u}  بـوت بنجـاح ✓** 🚮 \
                           \n**⎉╎لـم يتـم طـرد  {del_a}  بـوت لانـها اشـراف ..⅏** \
                           \n\n**⎉╎الان لـ الحفـاظ علـى كروبك/قناتك من التصفيـر ارسـل ⩥** `.قفل البوتات`"
    await edit_or_reply(event, del_status)
    if BOTLOG:
        await zed.client.send_message(
            BOTLOG_CHATID,
            f"#طـرد_البوتـات\
            \n ⎉╎{del_status}\
            \n ⎉╎الدردشه: {zed.chat.title}(`{zed.chat_id}`)",
        )
