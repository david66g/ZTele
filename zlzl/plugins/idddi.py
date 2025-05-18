import asyncio
import contextlib
import re
import html
import shutil
import os
import base64
import requests
from requests import get

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import MessageEntityMentionName, EmojiStatusEmpty
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon import events, types
from telethon.extensions import markdown, html
#from .xtelethonimport CustomParseMode  # TODO: Call the class from custom module
from . import zedub
from ..Config import Config
from ..utils import Zed_Vip, Zed_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from . import BOTLOG, BOTLOG_CHATID, spamwatch

plugin_category = "العروض"
LOGS = logging.getLogger(__name__)

zed_dev = (5176749470, 1895219306, 925972505, 5280339206, 5426390871, 6269975462, 1985225531)
zel_dev = (5176749470, 5426390871, 6269975462, 1985225531)
zelzal = (925972505, 1895219306, 5280339206)
ZIDA = gvarstatus("Z_ZZID") or "zvhhhclc"
Zel_Uid = zedub.uid
#zedub.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode

ZED_BLACKLIST = [
    -1001935599871,
    ]


class InvalidFormatException(Exception):
    pass


class CustomParseMode:
    """
    Example using Markdown:

    - client.send_message('me', 'hello this is a [Text](spoiler), with custom emoji [❤️](emoji/10002345) !')

    Example using HTML:

    - client.send_message('me', 'hello this is a <a href="spoiler">Text</a>, with custom emoji <a href="emoji/10002345">❤️</a> !')

    `Sending spoilers and custom emoji <https://github.com/LonamiWebs/Telethon/wiki/Sending-more-than-just-messages#sending-spoilers-and-custom-emoji>`_
    :param parse_mode: The format to use for parsing text.
                       Can be either 'markdown' for Markdown formatting
                       or 'html' for HTML formatting.
    """
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'markdown':
            text, entities = markdown.parse(text)
        elif self.parse_mode == 'html':
            text, entities = html.parse(text)
        else:
            raise InvalidFormatException("Invalid parse mode. Choose either Markdown or HTML.")

        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return html.unparse(text, entities)


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object


async def fetch_zelzal(user_id):
    headers = {
        'Host': 'restore-access.indream.app',
        'Connection': 'keep-alive',
        'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
        'Accept': '*/*',
        'Accept-Language': 'ar',
        'Content-Length': '25',
        'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"telegramId":' + str(user_id) + '}'
    response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
    zelzal_date = response['data']['date']
    return zelzal_date


async def zzz_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    zelzal_sinc = await fetch_zelzal(user_id)
    username = zthon_user.username
    verified = zthon_user.verified
    zilzal = (await event.client.get_entity(user_id)).premium
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    zzzsinc = zelzal_sinc if zelzal_sinc else ("غيـر معلـوم")
################# Dev ZilZal #################
    ZThon = f'<a href="T.me/ZThon">ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟</a>'
    ZThon += f"\n<b>⋆─┄─┄─┄─┄─┄─┄─⋆</b>\n\n"
    ZThon += f"<b>• معلومـات إنشـاء حسـاب تيليجـرام 📑 :</b>\n"
    ZThon += f"<b>- الاسـم    ⤎ </b> "
    ZThon += f'<a href="tg://user?id={user_id}">{full_name}</a>'
    ZThon += f"\n<b>- الايــدي   ⤎ </b> <code>{user_id}</code>"
    ZThon += f"\n<b>- اليـوزر    ⤎  {username}</b>\n"
    if zilzal == True or user_id in zelzal: 
        ZThon += f"<b>- الحساب  ⤎  بـريميـوم</b> "
        ZThon += f'<a href="emoji/5834880210268329130">❤️</a> \n'
    ZThon += f"<b>- الإنشـاء   ⤎</b>  {zzzsinc}  🗓" 
    return ZThon

async def fetch_info(replied_user, event):
    """Get details from the User object."""
    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
    dc_id = "Can't get dc id"
    with contextlib.suppress(AttributeError):
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
    user_id = replied_user.id
    zelzal_sinc = await fetch_zelzal(user_id)
    first_name = replied_user.first_name
    last_name = replied_user.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    common_chat = FullUser.common_chats_count
    username = replied_user.username
    user_bio = FullUser.about
    is_bot = replied_user.bot
    restricted = replied_user.restricted
    verified = replied_user.verified
    zilzal = (await event.client.get_entity(user_id)).premium
    mypremium = (await event.client.get_entity(Zel_Uid)).premium
    #zid = int(gvarstatus("ZThon_Vip"))
    if zilzal == True or user_id in zelzal:
        zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
    else:
        zpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    if user_id in Zed_Dev:
        zvip = "𝕍𝕀ℙ 💎"
    elif gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip")):
        zvip = "𝕍𝕀ℙ 💎"
    else:
        zvip = "ℕ𝕆ℕ𝔼"
    if (zilzal == True and mypremium == True):
        emoji_status = (await event.client.get_entity(user_id)).emoji_status
        if isinstance(emoji_status, EmojiStatusEmpty): 
            emoji_id = 5834880210268329130
        else:
            try:
                emoji_id = emoji_status.document_id
                if emoji_id is None:
                    emoji_id = 5834880210268329130
            except Exception:
                    emoji_id = 5834880210268329130
    photo = await event.client.download_profile_photo(
        user_id,
        Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
        download_big=True,
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    #full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    user_bio = "لا يـوجـد" if not user_bio else user_bio
    zzzsinc = zelzal_sinc if zelzal_sinc else ("غيـر معلـوم")
    zmsg = await bot.get_messages(event.chat_id, 0, from_user=user_id) 
    zzz = zmsg.total
    if zzz < 100: 
        zelzzz = "غير متفاعل  🗿"
    elif zzz > 200 and zzz < 500:
        zelzzz = "ضعيف  🗿"
    elif zzz > 500 and zzz < 700:
        zelzzz = "شد حيلك  🏇"
    elif zzz > 700 and zzz < 1000:
        zelzzz = "ماشي الحال  🏄🏻‍♂"
    elif zzz > 1000 and zzz < 2000:
        zelzzz = "ملك التفاعل  🎖"
    elif zzz > 2000 and zzz < 3000:
        zelzzz = "امبراطور التفاعل  🥇"
    elif zzz > 3000 and zzz < 4000:
        zelzzz = "غنبله  💣"
    else:
        zelzzz = "نار وشرر  🏆"
################# Dev ZilZal #################
    if user_id in zelzal: 
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id in zel_dev:
        rotbat = "مـطـور 𐏕" 
    elif user_id == (await event.client.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
################# Dev ZilZal #################
    #zid = int(gvarstatus("ZThon_Vip"))
    ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن بـوت زدثــون"  
    ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ " 
    ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ᶻᵗʰᵒᶰ ─┄─┄─┄─⋆" 
    if gvarstatus("ZID_TEMPLATE") is None:
        if Zel_Uid in Zed_Dev or (gvarstatus("ZThon_Vip") and Zel_Uid == int(gvarstatus("ZThon_Vip"))):
            if mypremium == True:
                caption = f"<b>✦ مـعلومـات المسـتخـدم سـورس زدثــون </b>"
                caption += f'<a href="emoji/5812307593032372545">❤️</a>\n'
                caption += f"ٴ<b>⋆┄─┄─┄─┄─</b>"
                caption += f'<a href="emoji/5809662223890518926">❤️</a>'
                caption += f"<b>─┄─┄─┄─┄⋆</b>\n"
                caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
                caption += f'<a href="tg://user?id={user_id}">{full_name}</a> '
                if zilzal == True:
                    caption += f'<a href="emoji/{emoji_id}">❤️</a>'
                caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
                caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
                caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
                if zilzal == True:
                    caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم</b>"
                    caption += f'<a href="emoji/5832422209074762334">❤️</a>\n'
                if user_id in Zed_Dev or (gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip"))):
                    if zilzal == True or user_id in zelzal:
                        caption += f"<b>{ZEDM}الاشتراك ⤎ </b>"
                        caption += f'<a href="emoji/5832653669157310552">❤️</a> \n'
                caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
                caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz} "
                caption += f'<a href="emoji/5253742260054409879">❤️</a>\n'
                caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
                if user_id != (await event.client.get_me()).id: 
                    caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
                caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
                caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
                caption += f"ٴ<b>⋆┄─┄─┄─┄─</b>"
                caption += f'<a href="emoji/5809662223890518926">❤️</a>'
                caption += f"<b>─┄─┄─┄─┄⋆</b>\n"
            else:
                caption = f"<b> {ZED_TEXT} </b>\n"
                caption += f"ٴ<b>{ZEDF}</b>\n"
                caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
                caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
                caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
                caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
                caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
                if zilzal == True:
                    caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
                if user_id in Zed_Dev or (gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip"))):
                    if zilzal == True or user_id in zelzal:
                        caption += f"<b>{ZEDM}الاشتراك  ⤎  𝕍𝕀ℙ</b>\n"
                caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
                caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
                caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
                if user_id != (await event.client.get_me()).id: 
                    caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
                caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
                caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
                caption += f"ٴ<b>{ZEDF}</b>"
        else:
            caption = f"<b> {ZED_TEXT} </b>\n"
            caption += f"ٴ<b>{ZEDF}</b>\n"
            caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
            caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
            caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
            caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
            caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
            if zilzal == True:
                caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
            if user_id in Zed_Dev or (gvarstatus("ZThon_Vip") and user_id == int(gvarstatus("ZThon_Vip"))):
                if zilzal == True or user_id in zelzal:
                    caption += f"<b>{ZEDM}الاشتراك  ⤎  𝕍𝕀ℙ</b>\n"
            caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
            caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
            caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" 
            if user_id != (await event.client.get_me()).id: 
                caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
            caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" 
            caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
            caption += f"ٴ<b>{ZEDF}</b>"
    else:
        zzz_caption = gvarstatus("ZID_TEMPLATE")
        caption = zzz_caption.format(
            znam=full_name,
            zusr=username,
            zidd=user_id,
            zrtb=rotbat,
            zpre=zpre,
            zvip=zvip,
            zpic=replied_user_profile_photos_count,
            zmsg=zzz,
            ztmg=zelzzz,
            zcom=common_chat,
            zsnc=zzzsinc,
            zbio=user_bio,
        )
    return photo, caption


@zedub.zed_cmd(
    pattern="ايدي(?: |$)(.*)",
    command=("ايدي", plugin_category),
    info={
        "header": "لـ عـرض معلومـات الشخـص",
        "الاستـخـدام": " {tr}ايدي بالـرد او {tr}ايدي + معـرف/ايـدي الشخص",
    },
)
async def who(event):
    "Gets info of an user"
    #if gvarstatus("ZThon_Vip") is not None or Zel_Uid in Zed_Dev:
        #input_str = event.pattern_match.group(1)
        #reply = event.reply_to_msg_id
        #if not input_str and not reply:
            #return
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    #except (AttributeError, TypeError):
        #return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    except AttributeError as e:
        return await edit_or_reply(zed, str(e))
    except TypeError as e:
        return await edit_or_reply(zed, str(e))
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if gvarstatus("ZID_TEMPLATE") is None:
        #event.client.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(caption, parse_mode=CustomParseMode("html"))
    else:
        #event.client.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(caption, parse_mode=CustomParseMode("markdown"))


@zedub.zed_cmd(
    pattern="ا(?: |$)(.*)",
    command=("ا", plugin_category),
    info={
        "header": "امـر مختصـر لـ عـرض معلومـات الشخـص",
        "الاستـخـدام": " {tr}ا بالـرد او {tr}ا + معـرف/ايـدي الشخص",
    },
)
async def who(event):
    "Gets info of an user"
    #if gvarstatus("ZThon_Vip") is not None or Zel_Uid in Zed_Dev:
        #input_str = event.pattern_match.group(1)
        #reply = event.reply_to_msg_id
        #if not input_str and not reply:
            #return
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if gvarstatus("ZID_TEMPLATE") is None:
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(caption, parse_mode=CustomParseMode("html"))
    else:
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except (TypeError, ChatSendMediaForbiddenError):
            await zed.edit(caption, parse_mode=CustomParseMode("markdown"))


@zedub.zed_cmd(pattern="الانشاء(?: |$)(.*)")
async def zelzalll(event):
    zed = await edit_or_reply(event, "**- جـارِ جلب المعلومـات . . .**")
    zthon_user = await get_user_from_event(event)
    try:
        ZThon = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    #zedub.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
    try:
        await event.client.send_message(
            event.chat_id,
            ZThon,
            link_preview=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        await zed.delete()
    except:
        await zed.edit("**- غيـر معلـوم او هنـاك خطـأ ؟!**", parse_mode="html")


@zedub.zed_cmd(pattern=f"{ZIDA}(?: |$)(.*)")
async def hwo(event):
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Vip):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            os.remove(photo)
        await zed.delete()
    except TypeError:
        await zed.edit(caption, parse_mode="html")


@zedub.zed_cmd(
    pattern="صورته(?:\\s|$)([\\s\\S]*)",
    command=("صورته", plugin_category),
    info={
        "header": "لـ جـلب بـروفـايـلات الشخـص",
        "الاستـخـدام": [
            "{tr}صورته + عدد",
            "{tr}صورته الكل",
            "{tr}صورته",
        ],
    },
)
async def potocmd(event):
    "To get user or group profile pic"
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Vip):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user and user.sender:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "الكل":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await edit_or_reply(
                    event, "**- رقـم خـاطـئ . . .**"
                )
                return
        except BaseException:
            await edit_or_reply(event, "**- رقـم خـاطـئ . . .**")
            return
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()


@zedub.zed_cmd(
    pattern="(الايدي|id)(?:\\s|$)([\\s\\S]*)",
    command=("id", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get id of the group or user."
    if input_str := event.pattern_match.group(2):
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"**⎉╎ايـدي المستخـدم**  `{input_str}` **هـو** `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"**⎉╎ايـدي المستخـدم**  `{p.title}` **هـو** `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎أدخل إما اسم مستخدم أو الرد على المستخدم**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**⎉╎ايـدي الدردشـه : **`{event.chat_id}`\n\n**⎉╎ايـدي المستخـدم : **`{r_msg.sender_id}`\n\n**⎉╎ايـدي الميديـا : **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                event,
                f"**⎉╎ايـدي الدردشـه : **`{event.chat_id}`\n\n**⎉╎ايـدي المستخـدم : **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(event, f"**⎉╎ايـدي الدردشـه : **`{event.chat_id}`")


@zedub.zed_cmd(
    pattern="رابطه(?:\\s|$)([\\s\\S]*)",
    command=("رابطه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.رابطه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}رابطه <username/userid/reply>",
    },
)
async def permalink(event):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(pattern="اسمي$")
async def permalink(event):
    user = await event.client.get_me()
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(
    pattern="اسمه(?:\\s|$)([\\s\\S]*)",
    command=("اسمه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.اسمه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}اسمه <username/userid/reply>",
    },
)
async def permalink(event):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(pattern="الصور(?:\\s|$)([\\s\\S]*)")
async def potocmd(event):
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await get_user_from_event(event)
    rser = await event.get_reply_message()
    chat = event.input_chat
    if rser and ser.sender:
        photos = await event.client.get_profile_photos(rser.sender)
    else:
        photos = await event.client.get_profile_photos(user.id)
    if uid.strip() == "":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if rser:
                    photo = await event.client.download_profile_photo(rser.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **")
    else:
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                photo = await event.client.download_profile_photo(user.id)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! ")
    await event.delete()


@zedub.zed_cmd(pattern="معنى(?: |$)(.*)")
async def get_name_meaning(event):
    nms = event.pattern_match.group(1)
    if not nms:
        return await edit_or_reply(event, "**- ارسـل (.معنى) + الاسـم**\n**- مثـال :**\n.معنى محمد")
    zzz = await edit_or_reply(event, "**⎉╎جـارِ البحث عـن معنـى الاسـم ...**")
    url = "https://meaningnames.net/mean.php"
    headers = {
        'authority': 'meaningnames.net',
        'accept': '*/*',
        'referer': 'https://meaningnames.net/',
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': 'PHPSESSID=7uoau0rn3ud96s7nhc684aatf1',
    }
    if nms == "عائشه" or nms == "عائشة":
        caption=f"**- معنى اسم ( عائشة ) :**\nمعناه: الحياة، المأمولُ بطول عمرها، ذات الحياة، المرتاحة في حياتها...\nوهو اسم ام المؤمنين عائشة احب زوجات رسول الله (صلى الله عليه وسلم) اليه وابنة أبي بكر الصديق، وبها يتحبَّبون الناس تسمية بناتهم."
        return await edit_or_reply(event, caption)
    data = {'name': nms, 'ajax': 'TRUE'}
    response = requests.post(url, headers=headers, data=data).text
    try:
        ma = re.findall(r'<h3 style="line-height: 215%;">(.*?)<h3>', response)[0]
        photo = f"https://meaning-names.net/images-{nms}"
        caption=f"**- معنى اسم ( {nms} )** :\n{ma}"
        await edit_or_reply(event, caption)
    except:
        await zzz.edit("**- لم يتم العثـور على معنى الاسم ؟!\n- جرب الكتابة بدون اخطاء املائيـه**")


@zedub.zed_cmd(pattern="حساب(?: |$)(.*)")
async def openacc(event):
    acc = event.pattern_match.group(1)
    if not acc:
        return await edit_or_reply(event, "**- ارسـل الامـر والايـدي فقـط**")
    zzz = await edit_or_reply(event, "**⎉╎جـارِ صنـع رابـط دخـول لـ الحسـاب ▬▭ ...**")
    caption=f"**- رابـط صاحب الايدي ( {acc} )** :\n**- الرابـط ينفتـح عبـر تطبيـق تيليكرام بلاس فقـط**\n\n[اضـغـط هـنـا](tg://openmessage?user_id={acc})"
    await edit_or_reply(event, caption)


@zedub.zed_cmd(pattern="اضف كليشة (الايدي|ايدي|الفحص|فحص|الحماية|الحمايه|الخاص) ?(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vinfo = reply.text
    zed = await edit_or_reply(event, "**⎉╎جـاري اضـافة الكليشـة الـى بـوتك ...**")
    if input_str == "الايدي" or input_str == "ايدي":
        variable = "ZID_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ZID_TEMPLATE") is None:
            await zed.edit("**⎉╎تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة الجـديده** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉╎تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة المضـافه** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ZID_TEMPLATE", vinfo)
    elif input_str == "الفحص" or input_str == "فحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await zed.edit("**⎉╎تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة الجـديده** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉╎تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة المضـافه** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ALIVE_TEMPLATE", vinfo)
    elif input_str == "الحماية" or input_str == "الحمايه" or input_str == "الخاص":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
            await zed.edit("**⎉╎تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة الجـديده** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉╎تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة المضـافه** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmpermit_txt", vinfo)
    else:
        if input_str:
            return await zed.edit("**⎉╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


@zedub.zed_cmd(pattern="اضف كليشه (الايدي|ايدي|الفحص|فحص|الحماية|الحمايه|الخاص) ?(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vinfo = reply.text
    zed = await edit_or_reply(event, "**⎉╎جـاري اضـافة الكليشـة الـى بـوتك ...**")
    if input_str == "الايدي" or input_str == "ايدي":
        variable = "ZID_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ZID_TEMPLATE") is None:
            await zed.edit("**⎉╎تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة الجـديده** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉╎تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة المضـافه** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ZID_TEMPLATE", vinfo)
    elif input_str == "الفحص" or input_str == "فحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await zed.edit("**⎉╎تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة الجـديده** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉╎تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة المضـافه** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ALIVE_TEMPLATE", vinfo)
    elif input_str == "الحماية" or input_str == "الحمايه" or input_str == "الخاص":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
            await zed.edit("**⎉╎تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة الجـديده** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉╎تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉╎الكليشـة المضـافه** \n {} \n\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmpermit_txt", vinfo)
    else:
        if input_str:
            return await zed.edit("**⎉╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


@zedub.on(admin_cmd(pattern="(خط التشويش|خط تشويش|تفعيل تشويش|تفعيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if not is_cllear:
        addgvar ("cllear", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
        return
    if is_cllear:
        await edit_delete(event, "**⎉╎خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل تشويش) **")
        return

@zedub.on(admin_cmd(pattern="(تعطيل تشويش|تعطيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if is_cllear:
        delgvar("cllear")
        await edit_delete(event, "**⎉╎تم تعطيـل خـط التشـويش .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
        return
    if not is_cllear:
        await edit_delete(event, "**⎉╎خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل تشويش) **")
        return


@zedub.on(events.NewMessage(outgoing=True))
async def comming(event):
    if event.message.text and not event.message.media and "." not in event.message.text:
        is_cllear = gvarstatus("cllear")
        if is_cllear:
            try:
                await event.edit(f"[{event.message.text}](spoiler)", parse_mode=CustomParseMode("markdown"))
            except MessageIdInvalidError:
                pass