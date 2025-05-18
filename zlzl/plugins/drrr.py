import os
import re
import random
import asyncio
import base64
import contextlib
import shutil
import urllib3
import requests
import string
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from telethon.utils import get_display_name
from urlextract import URLExtract

from telethon import events, types
from telethon.utils import get_peer_id, get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl import functions, types
from telethon.tl.types import Channel, Chat, InputPhoto, User, InputMessagesFilterEmpty
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors.rpcerrorlist import ForbiddenError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetStickerSetRequest, ExportChatInviteRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, unsavegif, progress
from ..helpers.utils import _zedtools, _zedutils, _format, parse_pre, reply_id
from ..sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from ..core.data import blacklist_chats_list
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper import global_collectionjson as sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from . import *

plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)

NASHR = gvarstatus("Z_NASHR") or "(نشر عام|سوبر)"
#SPRS = gvarstatus("Z_SPRS") or "(نشر_تلقائي|نشر|تلقائي)"
#OFSPRS = gvarstatus("Z_OFSPRS") or "(ايقاف_النشر|ايقاف النشر|ستوب)"

z_super = False
client = zedub
opened = True
closed = False

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

ZelzalNSH_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - اوامـر النشـر التلقـائي](t.me/ZThon) 𓆪\n\n"
    "**- اضغـط ع الامـر للنسـخ** \n\n\n"
    "**⪼** `.السوبر` \n"
    "**- لـ عـرض اوامـر النشـر في السـوبـرات**\n\n"
    "**⪼** `.تلقائي` \n"
    "**- الامـر + (معـرف/ايـدي/رابـط) القنـاة المـراد النشـر التلقـائي منهـا** \n"
    "**- استخـدم الامـر بقنـاتـك \n\n\n"
    "**⪼** `.ايقاف النشر` \n"
    "**- الامـر + (معـرف/ايـدي/رابـط) القنـاة المـراد ايقـاف النشـر التلقـائي منهـا** \n"
    "**- استخـدم الامـر بقنـاتـك \n\n\n"
    "**- ملاحظـه :**\n"
    "**- الاوامـر صـارت تدعـم المعـرفات والروابـط الى جـانب الايـدي 🏂🎗**\n"
    "**🛃 سيتـم اضـافة المزيـد من اوامــر النشـر التلقـائي بالتحديثـات الجـايه**\n"
)

# Write Code By T.me/zzzzl1l
ZelzalSuper_cmd = (
    "[ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 النشـࢪ التڪࢪاࢪي](t.me/ZThon) .\n"
    "**⋆┄─┄─┄─┄─┄─┄─┄─┄⋆**\n"
    "**⎉╎قـائمـة اوامـر السـوبـر (النشـر التلقائي) ع سـورس زدثـــون ♾ :**\n\n"
    "`.سوبر`\n"
    "**⪼ استخـدم (الامـر + عـدد الثـوانـي)**\n"
    "**⪼ لـ النشـر بـ جميـع سوبـرات حسابك التي تشتمـل ع كلمـة سـوبر او Super ...✓**\n\n" 
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.نشر`\n"
    "**⪼ استخـدم (الامـر + عـدد الثـوانـي + يوزرات السوبـرات)**\n" 
    "**⪼ لـ النشـر بـ مجموعـة محـددة او عـدة سـوبرات ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.نشر_عام`\n"
    "**⪼ استخـدم (الامـر + عـدد الثـوانـي)**\n"
    "**⪼ لـ النشـر بـ جميـع المجموعات الموجودة ع حسابك ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.ايقاف النشر`\n"
    "**⪼ لـ إيقـاف جميـع عمليـات النشـر التلقائـي ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "**⪼ مـلاحظــات هـامــه :**\n"
    "- اوامـر النشـر صـارت بـدون تـوقف لا تتأثر باعادة التشغيـل من هيروكـو ..♾\n"
    "- إضافة جديـدة وحصريـه بسـورس زدثــون¹ فقـط 🌟\n"
    "- اوامـر النشـر راجعـة لـ إستخـدامك انت .. السـورس غيـر مسـؤول عـن أي باند او حظر لـ الحسابات المستخدمه نشـر تلقائي من قبـل تيليجـرام <=> لذلك وجب التنبيـه ⚠️\n"
    "\n𓆩 [𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁](t.me/ZThon) 𓆪"
)

async def zzz_nasher(zedub, seconds, chat, message):
    seconds = int(gvarstatus("sec_nasher"))
    ch_id = chat.id
    global z_super
    z_super = True
    while z_super:
        if gvarstatus("med_nasher") is not None:
            media_nasher = gvarstatus("med_nasher")
            caption_nasher = gvarstatus("msg_nasher")
            await zedub.send_file(ch_id, media_nasher, caption=caption_nasher)
        else:
            msg_nasher = gvarstatus("msg_nasher")
            await zedub.send_message(ch_id, msg_nasher, link_preview=False)
        await asyncio.sleep(seconds)


async def zz_nasher():
    seconds = int(gvarstatus("sec_nasher"))
    chat_usernames = gvarstatus("chat_nasher")
    list_username = re.split(r'\s+', chat_usernames)
    message = gvarstatus("msg_nasher")
    for chat_username in list_username:
        try:
            chat = await zedub.get_entity(chat_username)
            await zzz_nasher(zedub, seconds, chat, message)  # تمرير قيمة seconds هنا لكل مجموعة
        except Exception as e:
            await zedub.send_message(
                BOTLOG_CHATID, f"**⌔ لا يمكن العثور على المجموعة أو الدردشة** {chat_username}: `{str(e)}`"
            )
        await asyncio.sleep(1)


# ينشر لمجموعات محددة فقط بالامر
@zedub.zed_cmd(pattern="نشر")
async def _(event): # .نشر + عدد الثواني الفاصله + يوزرات المجموعات بالرد ع الرسالة
    if gvarstatus("status_nasher") or gvarstatus("status_allnasher") or gvarstatus("status_nsuper"):
        return await edit_or_reply(event, "**⎉╎عـذراً .. عـزيـزي ✖️**\n**⎉╎هناك عملية نشر سابقـه مفعله**\n**⎉╎ارسـل** ( `.ايقاف النشر` ) ** لـ إيقافها اولاً**")
    await event.delete()
    #input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    parameters = re.split(r'\s+', event.text.strip(), maxsplit=2)
    if len(parameters) != 3:
        return await edit_delete(event, "**- امـر خاطـىء .. ارسـل ( .النشر ) لـ تصفح اوامـر النشـر التلقائي**")
    #zzz = await edit_or_reply(event, "**⎉╎جـاري بـدء النشـر في المجموعـات ...الرجـاء الانتظـار**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    seconds = int(parameters[1])
    chat_usernames = parameters[2].split()
    #seconds = int(input_str[0])
    #chat_usernames = input_str[1:]
    chat_usernames_str = " ".join(chat_usernames)
    addgvar("sec_nasher", seconds)
    addgvar("chat_nasher", chat_usernames_str)
    zedub = event.client
    global z_super
    z_super = True
    message = await event.get_reply_message()
    if message.media:
        downloaded_file_name = await malatha.client.download_media(
            message, Config.TEMP_DIR
        )
        r_caption = message.text
        if r_caption:
            addgvar("msg_nasher", r_caption)
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            start = datetime.now()
            media_urls = upload_file(downloaded_file_name)
        except exceptions.TelegraphException as exc:
            #await zed.edit("**⎉╎خطا : **" + str(exc))
            os.remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms_two = (end - start).seconds
            os.remove(downloaded_file_name)
            vinfo = ("https://graph.org{}".format(media_urls[0]))
            addgvar("med_nasher", vinfo)
    elif message.text:
        addgvar("msg_nasher", message.text)
    else:
        return
    rsr = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 <b>النشــࢪ التڪـࢪاࢪي</b>\n<b>⋆┄─┄─┄─┄─┄─┄─┄─┄⋆</b>"
    rsr += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
    if message.media:
        rsr += f"\n<b>• نـوع الرسـالة :</b>\n ميديـا 🏕️"
    else:
        rsr += f"\n<b>• نـوع الرسـالة :</b>\n نـص 📝"
    rsr += f"\n<b>• المجموعـات :</b>\n{chat_usernames_str}"
    rsr += f"\n<b>• نشـر تلقائـي .. بلا توقف ♾</b>"
    rsr += f"\n<b>• بـ تأخيـر</b> {seconds} <b>ثانيـه ⏳</b>"
    rsr += f"\n\n<b>• لـ عـرض اوامـر النشـر ارسـل</b> ( <code>.النشر</code> )"
    rsr += f"\n<b>• لـ ايقاف النشـر ارسـل</b> ( <code>.ايقاف النشر</code> )"
    await event.client.send_message(event.chat_id, rsr, parse_mode="html", link_preview=False)
    addgvar("status_nasher", True)
    if BOTLOG:
        rss = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 <b>النشــࢪ التڪـࢪاࢪي</b>\n<b>⋆┄─┄─┄─┄─┄─┄─┄─┄⋆</b>"
        rss += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
        if message.text:
            rss += f"\n<b>• الرسـالة المنشـورة :</b>\n<code>{message.text}</code>"
        rss += f"\n<b>• المجموعـات :</b>\n{chat_usernames_str}"
        rss += f"\n<b>• نشـر تلقائـي .. بلا توقف ♾</b>"
        rss += f"\n<b>• بـ تأخيـر</b> {seconds} <b>ثانيـه ⏳</b>"
        rss += f"\n\n<b>• لـ عـرض اوامـر النشـر ارسـل</b> ( <code>.النشر</code> )"
        rss += f"\n<b>• لـ ايقاف النشـر ارسـل</b> ( <code>.ايقاف النشر</code> )"
        await event.client.send_message(
            BOTLOG_CHATID,
            rss,
            parse_mode="html",
            link_preview=False,
        )
    await zz_nasher()


async def zzz_all_nasher(zedub, sleeptimet, message):
    global z_super
    z_super = True
    zzz_chats = await zedub.get_dialogs()
    while z_super:
        for chat in zzz_chats:
            if chat.is_group:
                if chat.title != "⎉ 𝗭𝗧𝗵𝗼𝗻 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 ⎉":
                    try:
                        if gvarstatus("med_allnasher") is not None:
                            media_nasher = gvarstatus("med_allnasher")
                            caption_nasher = gvarstatus("msg_allnasher")
                            await zedub.send_file(chat.id, media_nasher, caption=caption_nasher)
                        else:
                            caption_nasher = gvarstatus("msg_allnasher")
                            await zedub.send_message(chat.id, caption_nasher, link_preview=False)
                    except Exception:
                        #print(f"Error in sending message to chat {chat.id}: {e}")
                        pass
                        await asyncio.sleep(2)
        await asyncio.sleep(sleeptimet)


async def zz_all_nasher():
    sleeptimet = int(gvarstatus("sec_allnasher"))
    message = gvarstatus("msg_allnasher")
    await zzz_all_nasher(zedub, sleeptimet, message)


# ينشر لجميع المجموعات
@zedub.zed_cmd(pattern="(نشر_كروبات|نشر_عام)")
async def _(event): # .نشر_كروبات + عدد الثواني بالرد ع الرسالة
    if gvarstatus("status_nasher") or gvarstatus("status_allnasher") or gvarstatus("status_nsuper"):
        return await edit_or_reply(event, "**⎉╎عـذراً .. عـزيـزي ✖️**\n**⎉╎هناك عملية نشر سابقـه مفعله**\n**⎉╎ارسـل** ( `.ايقاف النشر` ) ** لـ إيقافها اولاً**")
    await event.delete()
    seconds = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = int(seconds[0])
        addgvar("sec_allnasher", sleeptimet)
    except Exception:
        return await edit_delete(
            event, "**- امـر خاطـىء .. ارسـل ( .النشر ) لـ تصفح اوامـر النشـر التلقائي**"
        )
    #zzz = await edit_or_reply(event, "**⎉╎جـاري بـدء النشـر في المجموعـات ...الرجـاء الانتظـار**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    message =  await event.get_reply_message()
    if message.media:
        downloaded_file_name = await malatha.client.download_media(
            message, Config.TEMP_DIR
        )
        r_caption = message.text
        if r_caption:
            addgvar("msg_allnasher", r_caption)
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            start = datetime.now()
            media_urls = upload_file(downloaded_file_name)
        except exceptions.TelegraphException as exc:
            #await zed.edit("**⎉╎خطا : **" + str(exc))
            os.remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms_two = (end - start).seconds
            os.remove(downloaded_file_name)
            vinfo = ("https://graph.org{}".format(media_urls[0]))
            addgvar("med_allnasher", vinfo)
    elif message.text:
        addgvar("msg_allnasher", message.text)
    else:
        return

    zedub = event.client
    global z_super
    z_super = True
    rsr = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 <b>النشــࢪ التڪـࢪاࢪي</b>\n<b>⋆┄─┄─┄─┄─┄─┄─┄─┄⋆</b>"
    rsr += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
    if message.media:
        rsr += f"\n<b>• نـوع الرسـالة :</b>\n ميديـا 🏕️"
    else:
        rsr += f"\n<b>• نـوع الرسـالة :</b>\n نـص 📝"
    rsr += f"\n<b>• المجموعـات :</b> جميـع مجموعات الحسـاب"
    rsr += f"\n<b>• نشـر تلقائـي .. بلا توقف ♾</b>"
    rsr += f"\n<b>• بـ تأخيـر</b> {seconds} <b>ثانيـه ⏳</b>"
    rsr += f"\n\n<b>• لـ عـرض اوامـر النشـر ارسـل</b> ( <code>.النشر</code> )"
    rsr += f"\n<b>• لـ ايقاف النشـر ارسـل</b> ( <code>.ايقاف النشر</code> )"
    await event.client.send_message(event.chat_id, rsr, parse_mode="html", link_preview=False)
    addgvar("status_allnasher", True)
    if BOTLOG:
        rss = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 <b>النشــࢪ التڪـࢪاࢪي</b>\n<b>⋆┄─┄─┄─┄─┄─┄─┄─┄⋆</b>"
        rss += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
        if message.text:
            rss += f"\n<b>• الرسـالة المنشـورة :</b>\n<code>{message.text}</code>"
        rss += f"\n<b>• المجموعـات :</b> جميـع مجموعات الحسـاب"
        rss += f"\n<b>• نشـر تلقائـي .. بلا توقف ♾</b>"
        rss += f"\n<b>• المجموعـات الهـدف:</b> جميـع مجموعات الحسـاب التي يشتمل اسمها على كلمة (سوبر/Super)""\n<b>• بـ تأخيـر</b> {seconds} <b>ثانيـه ⏳</b>"
        rss += f"\n\n<b>• لـ عـرض اوامـر النشـر ارسـل</b> ( <code>.النشر</code> )"
        rss += f"\n<b>• لـ ايقاف النشـر ارسـل</b> ( <code>.ايقاف النشر</code> )"
        await event.client.send_message(
            BOTLOG_CHATID,
            rss,
            parse_mode="html",
            link_preview=False,
        )
    await zz_all_nasher()


super_groups = ["super", "سوبر"]
async def zzz_supers(zedub, sleeptimet, message):
    global z_super
    z_super = True
    zzz_chats = await zedub.get_dialogs()
    while z_super:
        for chat in zzz_chats:
            chat_title_lower = chat.title.lower()
            if chat.is_group and any(keyword in chat_title_lower for keyword in super_groups):
                try:
                    if gvarstatus("med_nsuper") is not None:
                        media_nasher = gvarstatus("med_nsuper")
                        caption_nasher = gvarstatus("msg_nsuper")
                        await zedub.send_file(chat.id, media_nasher, caption=caption_nasher)
                    else:
                        caption_nasher = gvarstatus("msg_nsuper")
                        await zedub.send_message(chat.id, caption_nasher, link_preview=False)
                except Exception:
                    #print(f"Error in sending message to chat {chat.id}: {e}")
                    pass
                    await asyncio.sleep(1)
        await asyncio.sleep(sleeptimet)


async def zz_supers():
    sleeptimet = int(gvarstatus("sec_nsuper"))
    message = gvarstatus("msg_nsuper")
    await zzz_supers(zedub, sleeptimet, message)


# ينشر لمجموعات يوجد ع اسمها كلمة سوبر او super
@zedub.zed_cmd(pattern="سوبر")
async def _(event):
    if gvarstatus("status_nasher") or gvarstatus("status_allnasher") or gvarstatus("status_nsuper"):
        return await edit_or_reply(event, "**⎉╎عـذراً .. عـزيـزي ✖️**\n**⎉╎هناك عملية نشر سابقـه مفعله**\n**⎉╎ارسـل** ( `.ايقاف النشر` ) ** لـ إيقافها اولاً**")
    await event.delete()
    await event.delete()
    #zzz = await edit_or_reply(event, "**⎉╎جـاري بـدء النشـر في المجموعـات ...الرجـاء الانتظـار**")
    seconds = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    #addgvar("sec_nsuper", seconds)
    try:
        sleeptimet = int(seconds[0])
        addgvar("sec_nsuper", sleeptimet)
    except Exception:
        return await edit_delete(
            event, "**- امـر خاطـىء .. ارسـل ( .النشر ) لـ تصفح اوامـر النشـر التلقائي**"
        )
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    message =  await event.get_reply_message()
    if message.media:
        downloaded_file_name = await malatha.client.download_media(
            message, Config.TEMP_DIR
        )
        r_caption = message.text
        if r_caption:
            addgvar("msg_nsuper", r_caption)
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            start = datetime.now()
            media_urls = upload_file(downloaded_file_name)
        except exceptions.TelegraphException as exc:
            #await zed.edit("**⎉╎خطا : **" + str(exc))
            os.remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms_two = (end - start).seconds
            os.remove(downloaded_file_name)
            vinfo = ("https://graph.org{}".format(media_urls[0]))
            addgvar("med_nsuper", vinfo)
    elif message.text:
        addgvar("msg_nsuper", message.text)
    else:
        return

    zedub = event.client
    global z_super
    z_super = True
    rsr = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 <b>النشــࢪ التڪـࢪاࢪي</b>\n<b>⋆┄─┄─┄─┄─┄─┄─┄─┄⋆</b>"
    rsr += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
    if message.media:
        rsr += f"\n<b>• نـوع الرسـالة :</b>\n ميديـا 🏕️"
    else:
        rsr += f"\n<b>• نـوع الرسـالة :</b>\n نـص 📝"
    rsr += f"\n<b>• المجموعـات :</b> جميـع مجموعات الحسـاب التي يشتمل اسمها على كلمة (سوبر/Super)"
    rsr += f"\n<b>• نشـر تلقائـي .. بلا توقف ♾</b>"
    rsr += f"\n<b>• بـ تأخيـر</b> {seconds} <b>ثانيـه ⏳</b>"
    rsr += f"\n\n<b>• لـ عـرض اوامـر النشـر ارسـل</b> ( <code>.النشر</code> )"
    rsr += f"\n<b>• لـ ايقاف النشـر ارسـل</b> ( <code>.ايقاف النشر</code> )"
    await event.client.send_message(event.chat_id, rsr, parse_mode="html", link_preview=False)
    addgvar("status_nsuper", True)
    if BOTLOG:
        rss = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 🎡 <b>النشــࢪ التڪـࢪاࢪي</b>\n<b>⋆┄─┄─┄─┄─┄─┄─┄─┄⋆</b>"
        rss += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
        if message.text:
            rss += f"\n<b>• الرسـالة المنشـورة :</b>\n<code>{message.text}</code>"
        rss += f"\n<b>• المجموعـات :</b> جميـع مجموعات الحسـاب التي يشتمل اسمها على كلمة (سوبر/Super)"
        rss += f"\n<b>• نشـر تلقائـي .. بلا توقف ♾</b>"
        rss += f"\n<b>• بـ تأخيـر</b> {seconds} <b>ثانيـه ⏳</b>"
        rss += f"\n\n<b>• لـ عـرض اوامـر النشـر ارسـل</b> ( <code>.النشر</code> )"
        rss += f"\n<b>• لـ ايقاف النشـر ارسـل</b> ( <code>.ايقاف النشر</code> )"
        await event.client.send_message(
            BOTLOG_CHATID,
            rss,
            parse_mode="html",
            link_preview=False,
        )
    await zzz_supers(zedub, sleeptimet, message)


@zedub.zed_cmd(pattern="ايقاف (النشر|نشر|السوبر|سوبر)")
async def stop_super(event):
    global z_super
    z_super = False
    if gvarstatus("status_nasher") is not None:
        delgvar("status_nasher")
    if gvarstatus("status_allnasher") is not None:
        delgvar("status_allnasher")
    if gvarstatus("status_nsuper") is not None:
        delgvar("status_nsuper")
    if gvarstatus("sec_nasher") is not None:
        delgvar("sec_nasher")
    if gvarstatus("sec_allnasher") is not None:
        delgvar("sec_allnasher")
    if gvarstatus("sec_nsuper") is not None:
        delgvar("sec_nsuper")
    if gvarstatus("med_nasher") is not None:
        delgvar("med_nasher")
    if gvarstatus("med_allnasher") is not None:
        delgvar("med_allnasher")
    if gvarstatus("med_nsuper") is not None:
        delgvar("med_nsuper")
    await event.edit("**- تم إيقاف النشر التلقائي .. بنجاح ✅**")


@zedub.zed_cmd(pattern="(اوامر السوبرات|اوامر السوبر|السوبر|السوبرات)")
async def cmd_super(zelzallll):
    await edit_or_reply(zelzallll, ZelzalSuper_cmd)


@zedub.zed_cmd(pattern="(النشر|اوامر النشر)")
async def cmd_nasher(zilzallll):
    await edit_or_reply(zilzallll, ZelzalNSH_cmd)


@zedub.zed_cmd(pattern="(نشر تلقائي|تلقائي)(?: |$)(.*)")
async def _(event):
    if event.is_private:
        return await edit_or_reply(event, "**⎉╎عـذراً .. النشر التلقائي خـاص بالقنـوات/المجموعات فقـط\n⎉╎قم باستخـدام الامـر داخـل القنـاة/المجموعة الهـدف**")
    if input_str := event.pattern_match.group(2):
        try:
            zch = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
        try:
            if is_post(zch.id , event.chat_id):
                return await edit_or_reply(event, "**⎉╎النشـر التلقـائي مفعـل مسبقـاً ✓**")
            if zch.first_name:
                await asyncio.sleep(1.5)
                add_post(zch.id, event.chat_id)
                await edit_or_reply(event, "**⎉╎تم تفعيـل النشـر التلقـائي من القنـاة .. بنجـاح ✓**")
        except Exception:
            try:
                if is_post(zch.id , event.chat_id):
                    return await edit_or_reply(event, "**⎉╎النشـر التلقـائي مفعـل مسبقـاً ✓**")
                if zch.title:
                    await asyncio.sleep(1.5)
                    add_post(zch.id, event.chat_id)
                    return await edit_or_reply(event, "**⎉╎تم تفعيـل النشـر التلقـائي من القنـاة .. بنجـاح ✓**")
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")


@zedub.zed_cmd(pattern="(ايقاف النشر|ستوب)(?: |$)(.*)")
async def _(event):
    if event.is_private:
        return await edit_or_reply(event, "**⎉╎عـذراً .. النشر التلقائي خـاص بالقنـوات/المجموعات فقـط\n⎉╎قم باستخـدام الامـر داخـل القنـاة/المجموعة الهـدف**")
    if input_str := event.pattern_match.group(2):
        try:
            zch = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
        try:
            if not is_post(zch.id, event.chat_id):
                return await edit_or_reply(event, "**⎉╎عـذراً .. النشـر التلقـائي غير مفعـل اسـاسـاً ؟!**")
            if zch.first_name:
                await asyncio.sleep(1.5)
                remove_post(zch.id, event.chat_id)
                await edit_or_reply(event, "**⎉╎تم تعطيـل النشر التلقـائي هنـا .. بنجـاح ✓**")
        except Exception:
            try:
                if not is_post(zch.id, event.chat_id):
                    return await edit_or_reply(event, "**⎉╎عـذراً .. النشـر التلقـائي غير مفعـل اسـاسـاً ؟!**")
                if zch.title:
                    await asyncio.sleep(1.5)
                    remove_post(zch.id, event.chat_id)
                    return await edit_or_reply(event, "**⎉╎تم تعطيـل النشر التلقـائي هنـا .. بنجـاح ✓**")
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")


blocked_word = ["sex", "سكس", "نيك", "نيج", "كحاب", "سحاق", "porn"]
blocked_channels = ["ZlZZll7", "M_iaar_M", "RS_F_Z", "LL_7L", "OoO15", "JO6JJ", "ZlZZl771", "zzzzl1l1", "ZedThon1", "EARCXb", "zzzzl1lj", "Dakson_SDR12", "w352xd", "AAffoopp12", "Slomsfr", "BT224"]


@zedub.zed_cmd(pattern="تلي (.*)")
async def _(event): # Code by t.me/zzzzl1l
    search = event.pattern_match.group(1)
    if "sex" in search or "porn" in search or "سكس" in search or "نيك" in search or "نيج" in search or "سحاق" in search or "كحاب" in search or "تبياته" in search:
        return await edit_delete(event, "**- البحث عـن قنـوات غيـر اخلاقيـه محظـور 🔞؟!**", 5)
    l = 'qwertyuiopasdfghjklxcvbnmz'
    result = await zedub(functions.contacts.SearchRequest(
        q=search,
        limit=20
    ))
    json = result.to_dict()
    i = str(''.join(random.choice(l) for i in range(3))) + '.txt'
    counter = 0
    for item in json['chats']:
        channel_id = item["username"]
        if channel_id not in blocked_channels:
            links = f'https://t.me/{channel_id}'
            counter += 1
            open(i, 'a').write(f"{counter}• {links}\n")
    link = open(i, 'r').read()
    if not link:
        await event.edit("**- لا توجد نتائج في البحث**")
    else:
        await event.edit(f'''
ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **بـحـث تيليـجـࢪام**
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
l {search} l  **🔎 نتائـج البحث عـن -**
l قنوات + مجموعات l **يشمـل -**

{link}
        ''')


@zedub.zed_cmd(pattern="كلمه (.*)")
async def _(event): # Code by t.me/zzzzl1l
    search_word = event.pattern_match.group(1)
    chat = await event.get_chat()
    chat_name = chat.title
    l = 'qwertyuiopasdfghjklxcvbnmz'
    messages = await zedub.get_messages(chat, filter=InputMessagesFilterEmpty(), limit=100)
    i = str(''.join(random.choice(l) for i in range(3))) + '.txt'
    counter = 0
    for message in messages:
        if message.message and search_word in message.message:
            links = f'https://t.me/c/{chat.id}/{message.id}'
            counter += 1
            open(i, 'a').write(f"{counter}• {links}\n")
    link = open(i, 'r').read()
    if not link:
        await event.edit("**- لا توجد نتائج في البحث**")
    else:
        await event.edit(f'''
ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **بـحـث تيليـجـࢪام**
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
l {search_word} l  **نتائـج البحث عـن -**
l {chat_name} l  **فـي المجموعـة -**

{link}
        ''')


Z = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⣾⣿⠁⢸⣿⣧⠀⣿⣿⠉⠹⣿⣆⠉⠉⠉⠉⣿⣿⠟⠀⠀⠀\n"
    "⣿⣿⠀⠘⠛⠛⠀⣿⣿⠀⠀⣿⣿⠀⠀⠀⣼⣿⡟⠀⠀⠀⠀\n"
    "⣿⣿⠀⠀⠀⠀⠀⣿⣿⣤⣾⡿⠃⠀⠀⣼⣿⡟⠀⠀⠀⠀⠀\n"
    "⣿⣿⠀⠀⠀⠀⠀⣿⣿⢻⣿⣇⠀⠀⠀⣿⣿⠁⠀⠀⠀⠀⠀\n"
    "⣿⣿⠀⢸⣿⣷⠀⣿⣿⠀⣿⣿⡄⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⢻⣿⣦⣼⣿⠏⠀⣿⣿⠀⢸⣿⣧⠀⢀⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⠈⠛⠛⠛⠋⠀⠀⠛⠛⠀⠀⠛⠛⠀⠸⠛⠛⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⣴⣿⢿⣷⠒⠲⣾⣾⣿⣿⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⣴⣿⠟⠁⠀⢿⣿⠁⣿⣿⣿⠻⣿⣄⠀⠀⠀⠀⠀\n"
    "⠀⠀⣠⡾⠟⠁⠀⠀⠀⢸⣿⣸⣿⣿⣿⣆⠙⢿⣷⡀⠀⠀⠀\n"
    "⣰⡿⠋⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠉⠻⣿⡀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣆⠂⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠿⠟⠀⠀⠻⣿⣿⡇⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⢀⣾⡿⠃⠀⠀⠀⠀⠀⠘⢿⣿⡀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⣰⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀\n"
    "⠀⠀⠀⠀⢠⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣧⠀⠀⠀\n"
    "⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣆⠀⠀\n"
    "⠀⠀⠠⢾⠇⠀⠀⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡤.\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀sɪɪɪɪᴜᴜᴜᴜ⠀⠀ ⠀⠀⠀⠀⠀⠀\n"
)




@zedub.zed_cmd(pattern="كريس")
async def cr7(crr): # Code by t.me/zzzzl1l
    await crr.edit(Z)
    


@zedub.zed_cmd(pattern="ماريو")
async def mario(mario):
    await mario.edit(f'''
➖➖➖🟥🟥🟥🟥🟥🟥
➖➖🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥
➖➖🟫🟫🟫🟨🟨🟨⬛🟨
➖🟫🟨🟫🟨🟨🟨🟨⬛🟨🟨🟨
➖🟫🟨🟫🟫🟨🟨🟨🟨⬛🟨🟨
➖🟫🟫🟨🟨🟨🟨🟨⬛⬛⬛⬛
➖➖➖🟨🟨🟨🟨🟨🟨🟨🟨
➖➖🟥🟥🟦🟥🟥🟥🟥
➖🟥🟥🟥🟦🟥🟥🟦🟥🟥🟥
🟥🟥🟥🟥🟦🟦🟦🟦🟥🟥🟥🟥
🟨🟨🟥🟦🟨🟦🟦🟨🟦🟥🟨🟨
🟨🟨🟨🟦🟦🟦🟦🟦🟦🟨🟨🟨
🟨🟨🟦🟦🟦🟦🟦🟦🟦🟦🟨🟨
➖➖🟦🟦🟦➖➖🟦🟦🟦
➖🟫🟫🟫➖➖➖➖🟫🟫🟫
🟫🟫🟫🟫➖➖➖➖🟫🟫🟫🟫
    ''')



@zedub.zed_cmd(pattern="ضفدع")
async def frog(frog):
    await frog.edit(f'''
⬜️⬜️🟩🟩⬜️🟩🟩
⬜️🟩🟩🟩⬜️🟩🟩🟩
🟩🟩🟩🟩🟩🟩🟩🟩🟩
🟩⬜️⬛️⬜️🟩⬜️⬛️⬜️🟩
🟩🟩🟩🟩🟩🟩🟩🟩
🟩🟩🟥🟥🟥🟥🟥🟥🟥
🟩??🟥🟥🟥🟥🟥🟥🟥
🟩🟩🟩🟩🟩🟩🟩🟩
    ''')


@zedub.zed_cmd(pattern="اجري$")
async def _(kst):
    chars = (
        "🏃                        🦖",
        "🏃                       🦖",
        "🏃                      🦖",
        "🏃                     🦖",
        "🏃                    🦖",
        "🏃                   🦖",
        "🏃                  🦖",
        "🏃                 🦖",
        "🏃                🦖",
        "🏃               🦖",
        "🏃              🦖",
        "🏃             🦖",
        "🏃            🦖",
        "🏃           🦖",
        "🏃          🦖",
        "🏃           🦖",
        "🏃            🦖",
        "🏃             🦖",
        "🏃              🦖",
        "🏃               🦖",
        "🏃                🦖",
        "🏃                 🦖",
        "🏃                  🦖",
        "🏃                   🦖",
        "🏃                    🦖",
        "🏃                     🦖",
        "🏃                    🦖",
        "🏃                   🦖",
        "🏃                  🦖",
        "🏃                 🦖",
        "🏃                🦖",
        "🏃               🦖",
        "🏃              🦖",
        "🏃             🦖",
        "🏃            🦖",
        "🏃           🦖",
        "🏃          🦖",
        "🏃         🦖",
        "🏃        🦖",
        "🏃       🦖",
        "🏃      🦖",
        "🏃     🦖",
        "🏃    🦖",
        "🏃   🦖",
        "🏃  🦖",
        "🏃 🦖",
        "🧎🦖",
    )
    for char in chars:
        await asyncio.sleep(0.3)
        await edit_or_reply(kst, char)


@zedub.zed_cmd(pattern="(كلبي|فكيو|ورده|سوفيت|كلوك|تحبني)$")
async def _(kst):
    cmd = kst.pattern_match.group(1)
    if cmd == "كلبي":
        art = r"""
ㅤ
┈┈┈┈╱▏┈┈┈┈┈╱▔▔▔▔╲┈┈┈┈
┈┈┈┈▏▏┈┈┈┈┈▏╲▕▋▕▋▏┈┈┈
┈┈┈┈╲╲┈┈┈┈┈▏┈▏┈▔▔▔▆┈┈
┈┈┈┈┈╲▔▔▔▔▔╲╱┈╰┳┳┳╯┈┈
┈┈╱╲╱╲▏┈┈┈┈┈┈▕▔╰━╯┈┈┈
┈┈▔╲╲╱╱▔╱▔▔╲╲╲╲┈┈┈┈┈┈
┈┈┈┈╲╱╲╱┈┈┈┈╲╲▂╲▂┈┈┈┈
┈┈┈┈┈┈┈┈┈┈┈┈┈╲╱╲╱┈┈┈┈
ㅤ
"""
    elif cmd == "فكيو":
        art = """
ㅤ
⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣴⠏⠁⠙ ⡄
⠀⠀⠀⠀⠀⠀⠀⠀   ⡾     ⠀⠀ ⢷
⠀⠀⠀⠀⠀⠀   ⠀⠀⣾  ⠀  ⠀  ⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿  ⠀⠀⠀ ⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿  ⠀⠀ ⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿  ⠀⠀⠀ ⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿      ⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠀⠀⠀⠀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⣾⠏⣿⠀⠀⠀⠀⣿⣷⣦⣄⡀
⠀⠀⠀⠀⠀⠀⣼⡿⠀⣿⠀⠀⠀⠀⣿⠇⠀⠉⢷⡀
⠀⠀⠀⠀⣠⡾⢿⠇⠀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠸⡷⠤⣄⡀
⠀⠀⢠⡾⠋⣾⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⣧⠀⠀⠹⡄
⠀⣰⠏⠀⠀⣿⠀⠀⠀⠉⠀⠀⠀⠀⠈⠁⠀⠀⠀⢹⡄⠀⠀⢹⡄
⡾⡏⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠇⠀⠀⠀⢻⡄
⡾⣿⡀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷
⠀⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀  ⠀فكيو⠀⠀⠀⠀           ⠀⢠⣿
⠀⠀⠀⠹⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟
⠀⠀⠀⠀⠈⠻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟
⠀⠀⠀⠀⠀⠀⠈⠻⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏
ㅤ
"""
    elif cmd == "ورده":
        art = """
ㅤ
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀
⠀⠀⠀⠀⠀⠀⠀⡠⠖⠋⠉⠉⠳⡴⠒⠒⠒⠲⠤⢤⣀
⠀⠀⠀⠀⠀⣠⠊⠀⠀⡴⠚⡩⠟⠓⠒⡖⠲⡄⠀⠀⠈⡆
⠀⠀⠀⢀⡞⠁⢠⠒⠾⢥⣀⣇⣚⣹⡤⡟⠀⡇⢠⠀⢠⠇
⠀⠀⠀⢸⣄⣀⠀⡇⠀⠀⠀⠀⠀⢀⡜⠁⣸⢠⠎⣰⣃
⠀⠀⠸⡍⠀⠉⠉⠛⠦⣄⠀⢀⡴⣫⠴⠋⢹⡏⡼⠁⠈⠙⢦⡀
⠀⠀⣀⡽⣄⠀⠀⠀⠀⠈⠙⠻⣎⡁⠀⠀⣸⡾⠀⠀⠀⠀⣀⡹⠂
⢀⡞⠁⠀⠈⢣⡀⠀⠀⠀⠀⠀⠀⠉⠓⠶⢟⠀⢀⡤⠖⠋⠁
⠀⠉⠙⠒⠦⡀⠙⠦⣀⠀⠀⠀⠀⠀⠀⢀⣴⡷⠋
⠀⠀⠀⠀⠀⠘⢦⣀⠈⠓⣦⣤⣤⣤⢶⡟⠁
⢤⣤⣤⡤⠤⠤⠤⠤⣌⡉⠉⠁⠀⢸⢸⠁⡠⠖⠒⠒⢒⣒⡶⣶⠤
⠉⠲⣍⠓⠦⣄⠀⠀⠙⣆⠀⠀⠀⡞⡼⡼⢀⣠⠴⠊⢉⡤⠚⠁
⠀⠀⠈⠳⣄⠈⠙⢦⡀⢸⡀⠀⢰⢣⡧⠷⣯⣤⠤⠚⠉
⠀⠀⠀⠀⠈⠑⣲⠤⠬⠿⠧⣠⢏⡞
⠀⠀⢀⡴⠚⠉⠉⢉⣳⣄⣠⠏⡞
⣠⣴⣟⣒⣋⣉⣉⡭⠟⢡⠏⡼
⠉⠀⠀⠀⠀⠀⠀⠀⢀⠏⣸⠁
⠀⠀⠀⠀⠀⠀⠀⠀⡞⢠⠇
⠀⠀⠀⠀⠀⠀⠀⠘⠓⠚
ㅤ
"""
    elif cmd == "سوفيت":
        art = """
ㅤ
⠀⠀⠀⠀⠀⠀⢀⣤⣀⣀⣀⠀⠻⣷⣄
⠀⠀⠀⠀⢀⣴⣿⣿⣿⡿⠋⠀⠀⠀⠹⣿⣦⡀
⠀⠀⢀⣴⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠀⢹⣿⣧
⠀⠀⠙⢿⣿⡿⠋⠻⣿⣿⣦⡀⠀⠀⠀⢸⣿⣿⡆
⠀⠀⠀⠀⠉⠀⠀⠀⠈⠻⣿⣿⣦⡀⠀⢸⣿⣿⡇
⠀⠀⠀⠀⢀⣀⣄⡀⠀⠀⠈⠻⣿⣿⣶⣿⣿⣿⠁
⠀⠀⠀⣠⣿⣿⢿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⡁
⢠⣶⣿⣿⠋⠀⠀⠉⠛⠿⠿⠿⠿⠿⠛⠻⣿⣿⣦⡀
⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡿
ㅤ
"""
    elif cmd == "كلوك":
        art = """
ㅤ
⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⢀⣀⣀⣀⣀⣀⣤⣤
⠀⢶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠛⠋⠉
⠀⠀⢹⣿⣿⣿⣿⣿⠏    ⣿   ⠀ ⢹⡟
⠀⢠⣿⣿⣿⣿⣿⣿⣦⣀⣀⣙⣂⣠⠼⠃
⠀⣾⣿⣿⣿⣿⣿⠁
⢠⣿⣿⣿⣿⣿⡟
⢸⣿⣿⣿⣿⣿⡅
⠀⠛⠛⠛⠛⠛⠃
ㅤ
"""
    elif cmd == "تحبني":
        art = """
ㅤ
⠀⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀
⠀⠀⠀⣴⠿⠏⠀⠀⠀⠀⠀⠀⢳⡀⠀⡏⠀⠀⠀⠀ ⠀⢷
⠀⠀⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀⠀ ⠀ ⡇
⠀⠀⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿⠀⣸⠀تحبني؟   ⡇
⠀⠀⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀⣿⠀⢹⠀⠀⠀ ⠀⠀ ⡇
⠀⠀⠙⢿⣯⠄⠀⠀⠀⢀⡀⠀⠀⡿⠀⠀⡇⠀⠀⠀⠀⡼
⠀⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀⠀⠘⠤⣄⣠⠞
⠀⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁
⠀⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀
⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿
⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀⠀⣄⢸
⣿⣿⣧⣀⣿.........⣀⣰⣏⣘⣆⣀
ㅤ
"""
    await kst.edit(art, parse_mode=parse_pre)


@zedub.zed_cmd(pattern="(شبح|دعبل)$")
async def _(kst):
    cmd = kst.pattern_match.group(1)
    if cmd == "شبح":
        expr = """
┻┳|
┳┻| _
┻┳| •.•)  **lشبحl**
┳┻|⊂ﾉ
┻┳|
"""
    elif cmd == "دعبل":
        expr = """
○
く|)へ
    〉
 ￣￣┗┓             __lدعبل مناl__
 　 　   ┗┓　     ヾ○ｼ
  　　        ┗┓   ヘ/
 　                 ┗┓ノ
　 　 　 　 　   ┗┓
"""
    await kst.edit(expr)


if gvarstatus("status_nasher") and gvarstatus("status_nasher") != "false":

    async def szz_nasher():
        seconds = int(gvarstatus("sec_nasher"))
        chat_usernames = gvarstatus("chat_nasher")
        list_username = re.split(r'\s+', chat_usernames)
        message = gvarstatus("msg_nasher")
        for chat_username in list_username:
            try:
                chat = await zedub.get_entity(chat_username)
                await zzz_nasher(zedub, seconds, chat.id, message)  # تمرير قيمة seconds هنا لكل مجموعة
            except Exception as e:
                await zedub.send_message(
                    BOTLOG_CHATID, f"**⌔ لا يمكن العثور على المجموعة أو الدردشة** {chat_username}: `{str(e)}`"
                )
            await asyncio.sleep(1)

    zedub.loop.create_task(szz_nasher())


if gvarstatus("status_allnasher") and gvarstatus("status_allnasher") != "false":

    async def szz_all_nasher():
        sleeptimet = int(gvarstatus("sec_allnasher"))
        message = gvarstatus("msg_allnasher")
        await zzz_all_nasher(zedub, sleeptimet, message)

    zedub.loop.create_task(szz_all_nasher())


if gvarstatus("status_nsuper") and gvarstatus("status_nsuper") != "false":

    async def szz_supers():
        sleeptimet = int(gvarstatus("sec_nsuper"))
        message = gvarstatus("msg_nsuper")
        await zzz_supers(zedub, sleeptimet, message)

    zedub.loop.create_task(szz_supers())

