import asyncio
import math
import os
import re
import heroku3
import requests
import urllib3
import random
import string
from datetime import datetime
from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urlextract import URLExtract

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.errors.rpcerrorlist import ChatSendMediaForbiddenError
from telethon import Button, functions
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from . import zedub
from ..core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..utils import Zed_Dev
from . import BOTLOG, BOTLOG_CHATID, mention, edit_delete

plugin_category = "البوت"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER
PC_BLOCK = gvarstatus("PC_BLOCK")

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

class PMPERMIT:
    def __init__(self):
        self.TEMPAPPROVED = []

PMPERMIT_ = PMPERMIT()

async def do_pm_permit_action(event, chat):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    MAX_FLOOD_IN_PMS = 6
    try:
        ZT_WARNS = gvarstatus("MAX_FLOOD_IN_PMS")
        MAX_FLOOD_IN_PMS = int(ZT_WARNS) if gvarstatus("MAX_FLOOD_IN_PMS") else Config.MAX_FLOOD_IN_PMS
    except (ValueError, TypeError):
        MAX_FLOOD_IN_PMS = 6
    except Exception:
        MAX_FLOOD_IN_PMS = 6
    totalwarns = MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.info(str(e))
        controlmute = gvarstatus("pmute") or None
        custompmblock = gvarstatus("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
                totalwarns=totalwarns,
                warns=warns,
                remwarns=remwarns,
            )
        else:
            if controlmute is not None:
                USER_BOT_WARN_ZERO = f"**⤶ لقـد حذرتـڪ مـسـبـقـاً مـن الـتـڪـرار 📵** \n**⤶ تـم ڪتمـك تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي🔕**\n\n**⤶ تحيـاتـي** {my_mention}  🫡"
            else:
                USER_BOT_WARN_ZERO = f"**⤶ لقـد حذرتـڪ مـسـبـقـاً مـن الـتـڪـرار 📵** \n**⤶ تـم حـظـرڪ تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي🔕**\n\n**⤶ تحيـاتـي** {my_mention}  🫡"
        if controlmute is not None:
            msg = await event.reply(USER_BOT_WARN_ZERO)
            try:
                mute(event.chat_id, event.chat_id)
            except Exception as e:
                await event.reply(f"**- خطـأ **\n`{e}`")
            the_message = f"#حمـايـة_الخـاص\
                                \n** ⎉╎المستخـدم** [{get_display_name(chat)}](tg://user?id={chat.id}) .\
                                \n** ⎉╎تم كتمـه .. تلقائيـاً**\
                                \n** ⎉╎عـدد رسـائله :** {PM_WARNS[str(chat.id)]}"
            del PM_WARNS[str(chat.id)]
            sql.del_collection("pmwarns")
            sql.del_collection("pmmessagecache")
            sql.add_collection("pmwarns", PM_WARNS, {})
            sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
            try:
                return await event.client.send_message(
                    BOTLOG_CHATID,
                    the_message,
                )
            except BaseException:
                return
        else:
            msg = await event.reply(USER_BOT_WARN_ZERO)
            await event.client(functions.contacts.BlockRequest(chat.id))
            the_message = f"#حمـايـة_الخـاص\
                                \n** ⎉╎المستخـدم** [{get_display_name(chat)}](tg://user?id={chat.id}) .\
                                \n** ⎉╎تم حظـره .. تلقائيـاً**\
                                \n** ⎉╎عـدد رسـائله :** {PM_WARNS[str(chat.id)]}"
            del PM_WARNS[str(chat.id)]
            sql.del_collection("pmwarns")
            sql.del_collection("pmmessagecache")
            sql.add_collection("pmwarns", PM_WARNS, {})
            sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
            try:
                return await event.client.send_message(
                    BOTLOG_CHATID,
                    the_message,
                )
            except BaseException:
                return

    custompmpermit = gvarstatus("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(
            mention=mention,
            first=first,
            last=last,
            fullname=fullname,
            username=username,
            userid=userid,
            my_first=my_first,
            my_last=my_last,
            my_fullname=my_fullname,
            my_username=my_username,
            my_mention=my_mention,
            totalwarns=totalwarns,
            warns=warns,
            remwarns=remwarns,
        )
    elif gvarstatus("pmute") is not None:
        USER_BOT_NO_WARN = f"""ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 **- الـرد التلقـائي 〽️**
**•─────────────────•**

❞ **مرحبـاً**  {mention} ❝

**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك** {warns} **مـن** {totalwarns} **تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم ڪتمـك تلقـائياً . . .**

**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**"""
    elif gvarstatus("pmmenu") is None:
        USER_BOT_NO_WARN = f"""ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 **- الـرد التلقـائي 〽️**
**•─────────────────•**

❞ **مرحبـاً**  {mention} ❝

**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك** {warns} **مـن** {totalwarns} **تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**

**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**"""
    else:
        USER_BOT_NO_WARN = f"""ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 **- الـرد التلقـائي 〽️**
**•─────────────────•**

❞ **مرحبـاً**  {mention} ❝

**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك** {warns} **مـن** {totalwarns} **تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**

**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**"""
    addgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        if gvarstatus("pmmenu") is None:
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, "pmpermit"
            )
            msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
        else:
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                CAT = [x for x in PM_PIC.split()]
                PIC = list(CAT)
                CAT_IMG = random.choice(PIC)
            else:
                CAT_IMG = None
            if CAT_IMG is not None:
                msg = await event.client.send_file(
                    chat.id,
                    CAT_IMG,
                    caption=USER_BOT_NO_WARN,
                    reply_to=reply_to_id,
                    force_document=False,
                )
            else:
                msg = await event.client.send_message(
                    chat.id, USER_BOT_NO_WARN, reply_to=reply_to_id
                )
    except Exception as e:
        LOGS.error(e)
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@zedub.zed_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def on_new_private_message(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    zel_dev = (5176749470, 5426390871, 6269975462, 1985225531, 6550930943, 5003461173, 6227985448, 6269975462, 5746412340, 1850533212, 5616315677, 6470835326, 232499688, 6227985448, 1719023510 , 6801349110)
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if event.chat_id in zel_dev:
        reason = "**انـه احـد المطـورين المساعديـن 🥳♥️**"
        try:
            PM_WARNS = sql.get_collection("pmwarns").json
        except AttributeError:
            PM_WARNS = {}
        if not pmpermit_sql.is_approved(chat.id):
            if str(chat.id) in PM_WARNS:
                del PM_WARNS[str(chat.id)]
            start_date = str(datetime.now().strftime("%B %d, %Y"))
            pmpermit_sql.approve(
                chat.id, get_display_name(chat), start_date, chat.username, reason
            )
        return await event.client.send_message(chat, "**احد المطورين هنـا اننـي محظـوظ لقدومـك الـي 🙈♥️**")
    if chat.id in PMPERMIT_.TEMPAPPROVED:
        return
    if is_muted(event.chat_id, event.chat_id):
        return
    await do_pm_permit_action(event, chat)


@zedub.zed_cmd(outgoing=True, func=lambda e: e.is_private, edited=False, forword=None)
async def you_dm_other(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if event.text and event.text.startswith(
        (
            f"{cmdhd}بلوك",
            f"{cmdhd}رفض",
            f"{cmdhd}قبول",
            f"{cmdhd}da",
            f"{cmdhd}سماح",
            f"{cmdhd}tempapprove",
            f"{cmdhd}tempa",
            f"{cmdhd}tapprove",
            f"{cmdhd}ta",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(
            chat.id, get_display_name(chat), start_date, chat.username, "اووبس . . لـم يتـم رفضـه"
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@zedub.zed_cmd(
    pattern="الحمايه (تفعيل|تعطيل)$",
    command=("الحمايه", plugin_category),
    info={
        "header": "لـ تفعيـل/تعطيـل حمـايـة الخـاص لـ حسـابـك",
        "الاسـتخـدام": "{tr}الحمايه تفعيل/تعطيل",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmpermit."
    input_str = event.pattern_match.group(1)
    if input_str == "تفعيل":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(
                event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
            )
        else:
            await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**")
    elif gvarstatus("pmpermit") is not None:
        delgvar("pmpermit")
        await edit_delete(
            event, "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**"
        )
    else:
        await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**")
    if input_str == "تعطيل":
        if gvarstatus("pmmenu") is None:
            addgvar("pmmenu", "false")
            await edit_delete(
                event,
                "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**",
            )
        else:
            await edit_delete(
                event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**"
            )
    elif gvarstatus("pmmenu") is not None:
        delgvar("pmmenu")
        await edit_delete(
            event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
        )
    else:
        await edit_delete(
            event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**"
        )

@zedub.zed_cmd(
    pattern="الحماية (تفعيل|تعطيل)$",
    command=("الحماية", plugin_category),
    info={
        "header": "لـ تفعيـل/تعطيـل حمـايـة الخـاص لـ حسـابـك",
        "الاسـتخـدام": "{tr}الحماية تفعيل/تعطيل",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmmenu."
    input_str = event.pattern_match.group(1)
    if input_str == "تفعيل":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(
                event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
            )
        else:
            await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**")
    elif gvarstatus("pmpermit") is not None:
        delgvar("pmpermit")
        await edit_delete(
            event, "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**"
        )
    else:
        await edit_delete(event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**")
    if input_str == "تعطيل":
        if gvarstatus("pmmenu") is None:
            addgvar("pmmenu", "false")
            await edit_delete(
                event,
                "**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**",
            )
        else:
            await edit_delete(
                event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**"
            )
    elif gvarstatus("pmmenu") is not None:
        delgvar("pmmenu")
        await edit_delete(
            event, "**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**"
        )
    else:
        await edit_delete(
            event, "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل  🔐✅**"
        )


@zedub.zed_cmd(
    pattern="(قبول|سماح)(?: |$)(.*)",
    command=("سماح", plugin_category),
    info={
        "header": "لـ السمـاح لـ شخـص بمـراسلتـك خـاص اثنـاء تفعيـل الحمـايـه",
        "الاسـتخـدام": [
            "{tr}قبول/سماح + المعـرف/بالـرد + السـبب فـي الكـروب",
            "{tr}قبول/سماح + السـبب فـي الخـاص",
        ],
    },
)
async def approve_p_m(event):  # sourcery no-metrics
    "To approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"** ⎉╎لـيشتغل هذا الأمـر ...**\n** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n** ⎉╎بإرسـال** `{cmdhd}الحمايه تفعيل`",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
        if is_muted(user.id, event.chat_id):
            try:
                unmute(user.id, event.chat_id)
            except Exception as e:
                await event.edit(f"**- خطــأ **\n`{e}`")
            await event.edit("**- تـم الغــاء كتــم الشخـص هنـا .. بنجــاح ✓**")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الغــاء_كــتـم_حمـايـة_الخـاص\n"
                    f"**- الشخـص :** [{user.first_name}](tg://user?id={user.id})\n",
                )
    else:
        user, reason = await get_user_from_event(event, secondgroup=True)
        if not user:
            return
    if not reason:
        reason = "**⎉╎لـم يـذكـر 🤷🏻‍♂**"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if not pmpermit_sql.is_approved(user.id):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        pmpermit_sql.approve(
            user.id, get_display_name(user), start_date, user.username, reason
        )
        chat = user
        await edit_delete(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id})\n**⎉╎تـم السـمـاح لـه بـإرسـال الـرسـائـل 💬✓** \n **⎉╎ الـسـبـب ❔  :** {reason}",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    else:
        await edit_delete(
            event,
            f"**⎉╎المستخـدم** [{user.first_name}](tg://user?id={user.id}) \n**⎉╎هـو بـالـفـعل فـي قـائـمـة الـسـمـاح ✅**",
        )


@zedub.zed_cmd(
    pattern="t(emp)?(a|approve)(?: |$)(.*)",
    command=("tapprove", plugin_category),
    info={
        "header": "To approve user to direct message you for temporarily.",
        "note": "Heroku restarts every 24 hours so with every restart it dissapproves every temp approved user",
        "الاسـتخـدام": [
            "{tr}ta/tapprove <username/reply reason> in group",
            "{tr}ta/tapprove <reason> in pm",
        ],
    },
)
async def tapprove_pm(event):  # sourcery no-metrics
    "Temporarily approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"** ⎉╎لـيشتغل هذا الأمـر ...**\n** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n** ⎉╎بإرسـال** `{cmdhd}الحمايه تفعيل`",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(3)
    else:
        user, reason = await get_user_from_event(event, thirdgroup=True)
        if not user:
            return
    if not reason:
        reason = "**⎉╎لـم يـذكـر 🤷🏻‍♂**"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if (user.id not in PMPERMIT_.TEMPAPPROVED) and (
        not pmpermit_sql.is_approved(user.id)
    ):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        PMPERMIT_.TEMPAPPROVED.append(user.id)
        chat = user
        if str(chat.id) in sqllist.get_collection_list("pmspam"):
            sqllist.rm_from_list("pmspam", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmchat"):
            sqllist.rm_from_list("pmchat", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmrequest"):
            sqllist.rm_from_list("pmrequest", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmenquire"):
            sqllist.rm_from_list("pmenquire", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmoptions"):
            sqllist.rm_from_list("pmoptions", chat.id)
        await edit_delete(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id}) is __temporarily approved to pm__\n**Reason :** __{reason}__",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    elif pmpermit_sql.is_approved(user.id):
        await edit_delete(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id}) __is in approved list__",
        )
    else:
        await edit_delete(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id}) __is already in temporary approved list__",
        )


@zedub.zed_cmd(
    pattern="(رف|رفض)(?: |$)(.*)",
    command=("رفض", plugin_category),
    info={
        "header": "لـ رفـض الاشخـاص مـن الخـاص اثنـاء تفعيـل الحمـايـه",
        "امـر مضـاف": {"الكل": "لـ رفـض الكـل"},
        "الاسـتخـدام": [
            "{tr}رف/رفض <المعـرف/بالـرد> فـي الكـروب",
            "{tr}رف/رفض فـي الخـاص",
            "{tr}رف/رفض الكل لـ رفـض الكـل",
        ],
    },
)
async def disapprove_p_m(event):
    "To disapprove user to direct message you."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"** ⎉╎لـيشتغل هذا الأمـر ...**\n** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n** ⎉╎بإرسـال** `{cmdhd}الحمايه تفعيل`",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
    else:
        reason = event.pattern_match.group(2)
        if reason != "الكل":
            user, reason = await get_user_from_event(event, secondgroup=True)
            if not user:
                return
    if reason == "الكل":
        pmpermit_sql.disapprove_all()
        return await edit_delete(
            event, "**⎉╎حــسـنـا تــم رفـض الـجـمـيـع .. بنجـاح 💯**"
        )
    if not reason:
        reason = "**⎉╎ لـم يـذكـر 💭**"
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
        await edit_or_reply(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id})\n**⎉╎تـم رفـضـه مـن أرسـال الـرسـائـل ⚠️**\n**⎉╎ الـسـبـب ❔  :** {reason}",
        )
    elif user.id in PMPERMIT_.TEMPAPPROVED:
        PMPERMIT_.TEMPAPPROVED.remove(user.id)
        await edit_or_reply(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id})\n**⎉╎تـم رفـضـه مـن أرسـال الـرسـائـل ⚠️**\n**⎉╎ الـسـبـب ❔  :** {reason}",
        )
    else:
        await edit_delete(
            event,
            f"**⎉╎المستخـدم**  [{user.first_name}](tg://user?id={user.id})\n **⎉╎لــم تـتـم الـمـوافـقـة عـلـيـه مـسـبـقـاً ❕ **",
        )


@zedub.zed_cmd(pattern="بلوك(?: |$)(.*)")
async def block_p_m(event):
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    #if not reason:
        #reason = "**⎉╎ لـم يـذكـر 💭**"
    if user.id in Zed_Dev:
        return await edit_delete(event, "**- عـذࢪاً .. عـزيـزي ؟!**\n**- لا تستطيـع حظـࢪ مطـوࢪيـن السـوࢪس**", 10)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(user.id) in PM_WARNS:
        del PM_WARNS[str(user.id)]
    if str(user.id) in PMMESSAGE_CACHE:
        try:
            await event.client.delete_messages(user.id, PMMESSAGE_CACHE[str(user.id)])
        except Exception as e:
            LOGS.info(str(e))
        del PMMESSAGE_CACHE[str(user.id)]
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    await event.client(functions.contacts.BlockRequest(user.id))
    if reason:
        if PC_BLOCK is not None:
            await event.client.send_file(
                event.chat_id,
                PC_BLOCK,
                caption=f"**- الحيـوان :**  [{user.first_name}](tg://user?id={user.id}) 🫏\n**- تم حظـره .. بنجـاح ☑️**\n**- لايمكنـه ازعـاجـك الان 🚷**\n\n**- السـبب :** {reason}",
            )
            await event.delete()
        else:
            await edit_or_reply(
                event,
                f"**- الحيـوان :**  [{user.first_name}](tg://user?id={user.id}) 🫏\n**- تم حظـره .. بنجـاح ☑️**\n**- لايمكنـه ازعـاجـك الان 🚷**\n\n**- السـبب :** {reason}",
            )
    else:
        if PC_BLOCK is not None:
            await event.client.send_file(
                event.chat_id,
                PC_BLOCK,
                caption=f"**- الحيـوان :**  [{user.first_name}](tg://user?id={user.id}) 🫏\n**- تم حظـره .. بنجـاح ☑️**\n**- لايمكنـه ازعـاجـك الان 🚷**",
            )
            await event.delete()
        else:
            await edit_or_reply(
                event,
                f"**- الحيـوان :**  [{user.first_name}](tg://user?id={user.id}) 🫏\n**- تم حظـره .. بنجـاح ☑️**\n**- لايمكنـه ازعـاجـك الان 🚷**",
            )


@zedub.zed_cmd(pattern="الغاء بلوك(?: |$)(.*)")
async def unblock_pm(event):
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "**⎉╎ لـم يـذكـر 💭**"
    await event.client(functions.contacts.UnblockRequest(user.id))
    await edit_or_reply(
        event,
        f"**- المسـتخـدم :**  [{user.first_name}](tg://user?id={user.id}) **تم الغـاء حظـره بنجـاح .. يمكنـه التكلـم معـك الان**\n\n**- السـبب :** {reason}",
    )


@zedub.zed_cmd(pattern="المقبولين$")
async def approve_p_m(event):
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"** ⎉╎لـيشتغل هذا الأمـر ...**\n** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n** ⎉╎بإرسـال** `{cmdhd}الحمايه تفعيل`",
        )
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "**- قائمـة المسمـوح لهـم ( المقبـوليـن ) :**\n\n"
    if len(approved_users) > 0:
        for user in approved_users:
            APPROVED_PMs += f"**• 👤 الاسـم :** {_format.mentionuser(user.first_name , user.user_id)}\n**- الايـدي :** `{user.user_id}`\n**- المعـرف :** @{user.username}\n**- التـاريخ : **__{user.date}__\n**- السـبب : **__{user.reason}__\n\n"
    else:
        APPROVED_PMs = "**- انت لـم توافـق على اي شخـص بعـد**"
    await edit_or_reply(
        event,
        APPROVED_PMs,
        file_name="قائمـة الحمايـة.txt",
        caption="**- ️قائمـة المسمـوح لهـم ( المقبوليـن )**\n\n**- سـورس زدثــون** 𝙕𝙏𝙝𝙤𝙣 ",
    )

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"عقوبة الخاص (.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    vinfo = "zmute"
    zed = await edit_or_reply(event, "**⎉╎جـاري تغييـر عقـوبـة الخـاص 🚷...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "الكتم" or input_str == "بالكتم":
        variable = "pmute"
        await asyncio.sleep(1.5)
        if gvarstatus("pmute") is None:
            addgvar("pmute", vinfo)
            await zed.edit("**⎉╎تم تغييـر {} بنجـاح ☑️**\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.الحماية تفعيل`\n**⎉╎لـ تفعيـل حمايـة الخـاص . . . 🔕**".format(input_str))
        else:
            await zed.edit("**⎉╎{} مفعـله مسبقـاً ☑️**".format(input_str))
    elif input_str == "الحظر" or input_str == "بالحظر":
        variable = "pmute"
        await asyncio.sleep(1.5)
        if gvarstatus("pmute") is None:
            await zed.edit("**⎉╎{} مفعـله مسبقـاً ☑️**".format(input_str))
        else:
            delgvar("pmute")
            await zed.edit("**⎉╎تم تغييـر {} بنجـاح ☑️**\n**⎉╎الان قـم بـ ارسـال الامـر ↶** `.الحماية تفعيل`\n**⎉╎لـ تفعيـل حمايـة الخـاص . . . 🔕**".format(input_str))

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"زر حماية الخاص (.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ تغييـر زر قنـاة كليشـة حمايـة الخـاص ...**")
    if not input_str.startswith("@"):
        return await zed.edit("**⎉╎خطـأ .. قم باضافة يـوزر لـ الامـر**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    variable = "pmchannel"
    await asyncio.sleep(1.5)
    addgvar("pmchannel", input_str)
    await zed.edit("**⎉╎تم تغييـر قنـاة زر حمايـة الخـاص .. بنجـاح ☑️**\n**⎉╎يـوزر زر قنـاة حمايـة الخـاص\n{}**".format(input_str))


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="اضف صورة (الحماية|الحمايه|الفحص|الوقتي|البوت|الستارت|ستارت|الكتم|كتم|الحظر|الحضر|حظر|البلوك|بلوك) ?(.*)")
async def _(malatha):
    if malatha.fwd_from:
        return
    zed = await edit_or_reply(malatha, "**⎉╎جـاري اضـافة فـار الصـورة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await malatha.client.send_message(
            BOTLOG_CHATID,
            "**⎉╎تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**⎉╎لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = malatha.pattern_match.group(2)
    if malatha.reply_to_msg_id:
        start = datetime.now()
        r_message = await malatha.get_reply_message()
        input_str = malatha.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("pmpermit_pic", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["الفحص", "السورس"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("ALIVE_PIC", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["البوت", "الستارت", "ستارت"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("BOT_START_PIC", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["الوقتي", "البروفايل"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("DIGITAL_PIC", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["كتم", "الكتم"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("PC_MUTE", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["حظر", "الحضر","الحظر"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("PC_BANE", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["بلوك", "البلوك"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("PC_BLOCK", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
 
    else:
        await zed.edit(
            "**⎉╎بالـرد ع صـورة لتعييـن الفـار ...**",
        )




# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="اضف صوره (الحماية|الحمايه|الفحص|الوقتي|البوت|الستارت|ستارت|الكتم|كتم|الحظر|الحضر|حظر|البلوك|بلوك) ?(.*)")
async def _(malatha):
    if malatha.fwd_from:
        return
    zed = await edit_or_reply(malatha, "**⎉╎جـاري اضـافة فـار الصـورة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await malatha.client.send_message(
            BOTLOG_CHATID,
            "**⎉╎تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**⎉╎لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = malatha.pattern_match.group(2)
    if malatha.reply_to_msg_id:
        start = datetime.now()
        r_message = await malatha.get_reply_message()
        input_str = malatha.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("pmpermit_pic", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["الفحص", "السورس"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("ALIVE_PIC", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["البوت", "الستارت", "ستارت"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("BOT_START_PIC", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["الوقتي", "البروفايل"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("DIGITAL_PIC", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["كتم", "الكتم"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("PC_MUTE", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["حظر", "الحضر","الحظر"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("PC_BANE", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
        elif input_str in ["بلوك", "البلوك"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            vinfo = None
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                with open(downloaded_file_name, "rb") as f:
                    data = f.read()
                    resp = requests.post("https://envs.sh", files={"file": data})
                    if resp.status_code == 200:
                        #await zed.edit(f"https://envs.sh/{resp.text}")
                        vinfo = resp.text
                    else:
                        os.remove(downloaded_file_name)
                        return await zed.edit("**- حدث خطأ .. اثناء رفع الميديا**\n**- حاول مجدداً في وقت لاحق**")
            except Exception as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                addgvar("PC_BLOCK", vinfo)
                try:
                    await malatha.client.send_file(
                        malatha.chat_id,
                        vinfo,
                        caption="**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str),
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
                except BaseException:
                    await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str, vinfo))
 
    else:
        await zed.edit(
            "**⎉╎بالـرد ع صـورة لتعييـن الفـار ...**",
        )
