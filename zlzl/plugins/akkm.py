import os
import io
import random
import asyncio
import math
import requests
import json
import urllib3
from asyncio import sleep
from datetime import datetime
from pathlib import Path
from telethon import events, types
from telethon.tl import functions, types
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest
from telethon.tl.types import MessageEntityMentionName, InputMessagesFilterPhotos
from telethon.errors.rpcerrorlist import MessageIdInvalidError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from ..Config import Config
from ..core.logger import logging
from ..helpers.tools import media_type
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import _zedutils, reply_id
from . import BOTLOG, BOTLOG_CHATID, mention, zedub
LOGS = logging.getLogger(__name__)


@zedub.zed_cmd(pattern="احكام(?: |$)(.*)")
async def zed(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    userz = zedub.uid
    zed_chat = event.chat_id
    if gvarstatus("Z_AKM") is None:
        delgvar("Z_EKB")
        delgvar("Z_AK")
        delgvar("Z_A2K")
        delgvar("Z_A3K")
        delgvar("Z_A4K")
        delgvar("Z_A5K")
        delgvar("A_CHAT")
        addgvar("Z_AKM", "true")
        addgvar("Z_AK", userz)
        addgvar("A_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا` ", link_preview=False)
    else:
        delgvar("Z_EKB")
        delgvar("Z_AK")
        delgvar("Z_A2K")
        delgvar("Z_A3K")
        delgvar("Z_A4K")
        delgvar("Z_A5K")
        delgvar("Z_AKM")
        delgvar("A_CHAT")
        addgvar("Z_AKM", "true")
        addgvar("Z_AK", userz)
        addgvar("A_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ. 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا` ", link_preview=False)



@zedub.on(events.NewMessage(pattern=".انا"))
async def _(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    if gvarstatus("Z_AKM") is not None and event.chat_id == int(gvarstatus("A_CHAT")):
        if user.id == zedub.uid:
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- انت منضم مسبقـاً ؟!**", link_preview=False)
        if gvarstatus("Z_AK") is None:
            addgvar("Z_AK", user.id)
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 2⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is None:
            addgvar("Z_A2K", user.id)
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 3⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is None:
            addgvar("Z_A3K", user.id)
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 4⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is None:
            addgvar("Z_A4K", user.id)
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 5⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is None:
            addgvar("Z_A5K", user.id)
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم انضمـام**   [{user.first_name}](tg://user?id={user.id})  ** ☑️**\n\n**- اصبح عـدد اللاعبيـن 6⃣**\n**- على صاحب اللعبـة ان يرسـل**  `.تم`", link_preview=False)
        elif gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is not None:
            return await event.reply(f"**- عـذراً عـزيـزي**   [{user.first_name}](tg://user?id={user.id})  \n\n**- لقـد اكتمـل عـدد اللاعبيــن . . انتظـر بـدء اللعبـة من جديـد**", link_preview=False)



@zedub.zed_cmd(pattern="تم(?: |$)(.*)")
async def zed(event): # Code by t.me/zzzzl1l
    ZZZZ = gvarstatus("Z_AKM")
    AKM = gvarstatus("Z_AK")
    AK2M = gvarstatus("Z_A2K")
    AK3M = gvarstatus("Z_A3K")
    AK4M = gvarstatus("Z_A4K")
    AK5M = gvarstatus("Z_A5K")
# Code by t.me/zzzzl1l
    zana2 = [f"{AKM}", f"{AK2M}"]
    zaza2 = [x for x in zana2 if x is not None]
    zana3 = [f"{AKM}", f"{AK2M}", f"{AK3M}"]
    zaza3 = [x for x in zana3 if x is not None]
    zana4 = [f"{AKM}", f"{AK2M}", f"{AK3M}", f"{AK4M}"]
    zaza4 = [x for x in zana4 if x is not None]
    zana5 = [f"{AKM}", f"{AK2M}", f"{AK5M}", f"{AK3M}", f"{AK4M}"]
    zaza5 = [x for x in zana5 if x is not None]
# Code by t.me/zzzzl1l
    zed2 = random.choice(zana2)
    zee2 = random.choice([x for x in zaza2 if x != zed2])
    zed3 = random.choice(zana3)
    zee3 = random.choice([x for x in zaza3 if x != zed3])
    zed4 = random.choice(zana4)
    zee4 = random.choice([x for x in zaza4 if x != zed4])
    zed5 = random.choice(zana5)
    zee5 = random.choice([x for x in zaza5 if x != zed5])
    if gvarstatus("Z_AKM") is None:
        return await edit_or_reply(event, "**- انت لم تبـدأ اللعبـه بعـد ؟!\n- لـ بـدء لعبـة جديـدة ارسـل** `.احكام`")
    if gvarstatus("Z_AK") is None:
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is None and gvarstatus("Z_A4K") is None and gvarstatus("Z_A5K") is None:
       
        zelzal = int(zed2)
        zilzal = int(zee2)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed2})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee2}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is None and gvarstatus("Z_A5K") is None:
        zelzal = int(zed3)
        zilzal = int(zee3)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed3})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee3}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is None:
        zelzal = int(zed4)
        zilzal = int(zee4)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed4})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee4}) ", link_preview=False)
        delgvar("Z_AKM")
        return
    if gvarstatus("Z_AK") is not None and gvarstatus("Z_A2K") is not None and gvarstatus("Z_A3K") is not None and gvarstatus("Z_A4K") is not None and gvarstatus("Z_A5K") is not None:
        zelzal = int(zed5)
        zilzal = int(zee5)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
        except ValueError:
            return
        name_zed = user_zed.first_name
        name_zee = user_zee.first_name
        await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة أحكـام](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تـم اختيـار المتهـم ⇠**  [{name_zed}](tg://user?id={zed5})  \n**- ليتـم الحكـم عليـه ⇠ ⚖**\n**- الحاكـم 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee5}) ", link_preview=False)
        delgvar("Z_AKM")
        return


""" وصـف الملـف : لعبـة عقـاب الشهيـرة تقبـل ( 2 او 3 او 4 او 5 ... الـخ ) لاعبيـن
الملـف كتـابه من الصفـر 🤘
حقـوق للتـاريخ : @ZThon
@zzzzl1l - كتـابـة الملـف :  زلــزال الهيبــه
.. تخمـط تعبي اطشك للناس
"""
#                                        تـاريـخ كتابـة الكـود - 7 يوليو/2022 مدفـوع                                   #
#                                       تـاريـخ كتابـة الكـود - 24 ابريل/2023 مجاني                                  #
#                                            الملف كتابتي من الصفر ومتعوب عليه                                          #
#                                     مامسموحلك تخمـط So تخمـط = اهينك وافضحك                             #

@zedub.zed_cmd(pattern="عقاب(?: |$)(.*)")
async def zed(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    userz = user.id
    zed_chat = event.chat_id
    if gvarstatus("Z_EKB") is None:
        delgvar("Z_EKM")
        delgvar("Z_EK")
        delgvar("Z_E2K")
        delgvar("Z_E3K")
        delgvar("Z_E4K")
        delgvar("Z_E5K")
        delgvar("Z_E6K")
        delgvar("E_CHAT")
        addgvar("Z_EKB", "true")
        addgvar("Z_EK", userz)
        addgvar("E_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا` ", link_preview=False)
    else:
        delgvar("Z_EKM")
        delgvar("Z_EK")
        delgvar("Z_E2K")
        delgvar("Z_E3K")
        delgvar("Z_E4K")
        delgvar("Z_E5K")
        delgvar("Z_E6K")
        delgvar("Z_EKB")
        delgvar("E_CHAT")
        addgvar("Z_EKB", "true")
        addgvar("Z_EK", userz)
        addgvar("E_CHAT", zed_chat)
        return await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم بـدء اللعبـة وتـم إنضمـامي**  [{user.first_name}](tg://user?id={user.id})  **بنجـاح ☑️**\n\n**- اللي بيلعـب يرسل**  `.انا` ", link_preview=False)

@zedub.zed_cmd(pattern="(ايقاف عقاب|انهاء عقاب)$")
async def zed(event): # Code by t.me/zzzzl1l
    if gvarstatus("Z_EKB") is None:
        delgvar("Z_EKM")
        delgvar("Z_EK")
        delgvar("Z_E2K")
        delgvar("Z_E3K")
        delgvar("Z_E4K")
        delgvar("Z_E5K")
        delgvar("Z_E6K")
        delgvar("E_CHAT")
        return await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم إيقـاف اللعبـه .. بنجـاح ☑️**\n**- لبـدء لعبـه جديـدة ارسـل**  `.انا` ", link_preview=False)
    else:
        delgvar("Z_EKM")
        delgvar("Z_EK")
        delgvar("Z_E2K")
        delgvar("Z_E3K")
        delgvar("Z_E4K")
        delgvar("Z_E5K")
        delgvar("Z_E6K")
        delgvar("Z_EKB")
        delgvar("E_CHAT")
        return await edit_or_reply(event, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم إيقـاف اللعبـه .. بنجـاح ☑️**\n**- لبـدء لعبـه جديـدة ارسـل**  `.انا` ", link_preview=False)


@zedub.on(events.NewMessage(pattern=".انا"))
async def _(event): # Code by t.me/zzzzl1l
    user = await event.get_sender()
    if gvarstatus("Z_EKB") is not None and event.chat_id == int(gvarstatus("E_CHAT")):
        if user.id == zedub.uid:
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- انت منضم مسبقـاً ؟!**", link_preview=False)
        if gvarstatus("Z_E2K") is None:
            addgvar("Z_E2K", user.id)
            zzz1 = int(zedub.uid)
            try:
                u1 = await event.client.get_entity(zzz1)
            except ValueError:
                u1 = await zedub(GetUsersRequest(zzz1))
            zillzall = f"[{user.first_name}](tg://user?id={user.id})"
            zilzal1 = f"[{u1.first_name}](tg://user?id={u1.id})"
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**• تم انضمـام اللاعـب .. بنجـاح ☑️**\n**• قائمـة اللاعبيـن حتـى الان 2⃣:**\n{zillzall}\n{zilzal1}\n**- على صاحب اللعبـة ان يرسـل**  `.نعم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_E2K") is not None and gvarstatus("Z_E3K") is None:
            addgvar("Z_E3K", user.id)
            zzz1 = int(zedub.uid)
            zzz2 = int(gvarstatus("Z_E2K"))
            try:
                u1 = await event.client.get_entity(zzz1)
            except ValueError:
                u1 = await zedub(GetUsersRequest(zzz1))
            try:
                u2 = await event.client.get_entity(zzz2)
            except ValueError:
                u2 = await zedub(GetUsersRequest(zzz2))
            zillzall = f"[{user.first_name}](tg://user?id={user.id})"
            zilzal1 = f"[{u1.first_name}](tg://user?id={u1.id})"
            zilzal2 = f"[{u2.first_name}](tg://user?id={u2.id})"
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**• تم انضمـام اللاعـب .. بنجـاح ☑️**\n**• قائمـة اللاعبيـن حتـى الان 3⃣:**\n{zillzall}\n{zilzal1}\n{zilzal2}\n**- على صاحب اللعبـة ان يرسـل**  `.نعم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_E3K") is not None and gvarstatus("Z_E4K") is None:
            addgvar("Z_E4K", user.id)
            zzz1 = int(zedub.uid)
            zzz2 = int(gvarstatus("Z_E2K"))
            zzz3 = int(gvarstatus("Z_E3K"))
            try:
                u1 = await event.client.get_entity(zzz1)
            except ValueError:
                u1 = await zedub(GetUsersRequest(zzz1))
            try:
                u2 = await event.client.get_entity(zzz2)
            except ValueError:
                u2 = await zedub(GetUsersRequest(zzz2))
            try:
                u3 = await event.client.get_entity(zzz3)
            except ValueError:
                u3 = await zedub(GetUsersRequest(zzz3))
            zillzall = f"[{user.first_name}](tg://user?id={user.id})"
            zilzal1 = f"[{u1.first_name}](tg://user?id={u1.id})"
            zilzal2 = f"[{u2.first_name}](tg://user?id={u2.id})"
            zilzal3 = f"[{u3.first_name}](tg://user?id={u3.id})"
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**• تم انضمـام اللاعـب .. بنجـاح ☑️**\n**• قائمـة اللاعبيـن حتـى الان 4⃣:**\n{zillzall}\n{zilzal1}\n{zilzal2}\n{zilzal3}\n**- على صاحب اللعبـة ان يرسـل**  `.نعم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_E4K") is not None and gvarstatus("Z_E5K") is None:
            addgvar("Z_E5K", user.id)
            zzz1 = int(zedub.uid)
            zzz2 = int(gvarstatus("Z_E2K"))
            zzz3 = int(gvarstatus("Z_E3K"))
            zzz4 = int(gvarstatus("Z_E4K"))
            try:
                u1 = await event.client.get_entity(zzz1)
            except ValueError:
                u1 = await zedub(GetUsersRequest(zzz1))
            try:
                u2 = await event.client.get_entity(zzz2)
            except ValueError:
                u2 = await zedub(GetUsersRequest(zzz2))
            try:
                u3 = await event.client.get_entity(zzz3)
            except ValueError:
                u3 = await zedub(GetUsersRequest(zzz3))
            try:
                u4 = await event.client.get_entity(zzz4)
            except ValueError:
                u4 = await zedub(GetUsersRequest(zzz4))
            zillzall = f"[{user.first_name}](tg://user?id={user.id})"
            zilzal1 = f"[{u1.first_name}](tg://user?id={u1.id})"
            zilzal2 = f"[{u2.first_name}](tg://user?id={u2.id})"
            zilzal3 = f"[{u3.first_name}](tg://user?id={u3.id})"
            zilzal4 = f"[{u4.first_name}](tg://user?id={u4.id})"
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**• تم انضمـام اللاعـب .. بنجـاح ☑️**\n**• قائمـة اللاعبيـن حتـى الان 5⃣:**\n{zillzall}\n{zilzal1}\n{zilzal2}\n{zilzal3}\n{zilzal4}\n**- على صاحب اللعبـة ان يرسـل**  `.نعم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_E4K") is not None and gvarstatus("Z_E5K") is not None and gvarstatus("Z_E6K") is None:
            addgvar("Z_E6K", user.id)
            zzz1 = int(zedub.uid)
            zzz2 = int(gvarstatus("Z_E2K"))
            zzz3 = int(gvarstatus("Z_E3K"))
            zzz4 = int(gvarstatus("Z_E4K"))
            zzz5 = int(gvarstatus("Z_E5K"))
            try:
                u1 = await event.client.get_entity(zzz1)
            except ValueError:
                u1 = await zedub(GetUsersRequest(zzz1))
            try:
                u2 = await event.client.get_entity(zzz2)
            except ValueError:
                u2 = await zedub(GetUsersRequest(zzz2))
            try:
                u3 = await event.client.get_entity(zzz3)
            except ValueError:
                u3 = await zedub(GetUsersRequest(zzz3))
            try:
                u4 = await event.client.get_entity(zzz4)
            except ValueError:
                u4 = await zedub(GetUsersRequest(zzz4))
            try:
                u5 = await event.client.get_entity(zzz5)
            except ValueError:
                u5 = await zedub(GetUsersRequest(zzz5))
            zillzall = f"[{user.first_name}](tg://user?id={user.id})"
            zilzal1 = f"[{u1.first_name}](tg://user?id={u1.id})"
            zilzal2 = f"[{u2.first_name}](tg://user?id={u2.id})"
            zilzal3 = f"[{u3.first_name}](tg://user?id={u3.id})"
            zilzal4 = f"[{u4.first_name}](tg://user?id={u4.id})"
            zilzal5 = f"[{u5.first_name}](tg://user?id={u5.id})"
            return await event.reply(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖🧑🏻‍⚖ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**• تم انضمـام اللاعـب .. بنجـاح ☑️**\n**• قائمـة اللاعبيـن حتـى الان 6⃣:**\n{zillzall}\n{zilzal1}\n{zilzal2}\n{zilzal3}\n{zilzal4}\n{zilzal5}\n**- على صاحب اللعبـة ان يرسـل**  `.نعم`\n**- او ينتظـر انضمـام لاعبيـن 🛗**", link_preview=False)
        elif gvarstatus("Z_E3K") is not None and gvarstatus("Z_E4K") is not None and gvarstatus("Z_E5K") is not None and gvarstatus("Z_E6K") is not None:
            return await event.reply(f"**- عـذراً عـزيـزي**   [{user.first_name}](tg://user?id={user.id})  \n\n**- لقـد اكتمـل عـدد اللاعبيــن . . انتظـر بـدء اللعبـة من جديـد**", link_preview=False)



@zedub.zed_cmd(pattern="نعم(?: |$)(.*)")
async def zed(event): # Code by t.me/zzzzl1l
    ZZZZ = gvarstatus("Z_EKM")
    EKB = gvarstatus("Z_EK")
    EK2B = gvarstatus("Z_E2K")
    EK3B = gvarstatus("Z_E3K")
    EK4B = gvarstatus("Z_E4K")
    EK5B = gvarstatus("Z_E5K")
    EK6B = gvarstatus("Z_E6K")
# Code by t.me/zzzzl1l
    zana2 = [f"{EKB}", f"{EK2B}"]
    zaza2 = [x for x in zana2 if x is not None]
    zana3 = [f"{EKB}", f"{EK2B}", f"{EK3B}"]
    zaza3 = [x for x in zana3 if x is not None]
    zana4 = [f"{EKB}", f"{EK2B}", f"{EK3B}", f"{EK4B}"]
    zaza4 = [x for x in zana4 if x is not None]
    zana5 = [f"{EKB}", f"{EK2B}", f"{EK5B}", f"{EK3B}", f"{EK4B}"]
    zaza5 = [x for x in zana5 if x is not None]
    zana6 = [f"{EKB}", f"{EK2B}", f"{EK5B}", f"{EK3B}", f"{EK4B}", f"{EK6B}"]
    zaza6 = [x for x in zana6 if x is not None]
# Code by t.me/zzzzl1l
    zed2 = random.choice(zana2)
    zee2 = random.choice([x for x in zaza2 if x != zed2])
    zed3 = random.choice(zana3)
    zee3 = random.choice([x for x in zaza3 if x != zed3])
    zed4 = random.choice(zana4)
    zee4 = random.choice([x for x in zaza4 if x != zed4])
    zed5 = random.choice(zana5)
    zee5 = random.choice([x for x in zaza5 if x != zed5])
    zed6 = random.choice(zana6)
    zee6 = random.choice([x for x in zaza6 if x != zed6])
    if gvarstatus("Z_EKB") is None:
        return await edit_or_reply(event, "**- انت لم تبـدأ اللعبـه بعـد ؟!\n- لـ بـدء لعبـة جديـدة ارسـل** `.عقاب`")
    if gvarstatus("Z_EK") is None:
        return
    if gvarstatus("Z_EK") is not None and gvarstatus("Z_E2K") is not None and gvarstatus("Z_E3K") is None and gvarstatus("Z_E4K") is None and gvarstatus("Z_E5K") is None and gvarstatus("Z_E6K") is None:
        zelzal = int(zed2)
        zilzal = int(zee2)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
            name_zed = user_zed.first_name
            name_zee = user_zee.first_name
            messages = await event.client.get_messages("@VVVYVV4", filter=InputMessagesFilterPhotos)
            zedph = [message for message in messages]
            aing = await event.client.get_me()
            chosen_photo = random.sample(zedph, 1)[0]
            await event.client.send_file(
                event.chat_id,
                file=chosen_photo,
                caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖⛓ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم تحديـد المجـرم 🥷 ⇠**  [{name_zed}](tg://user?id={zed2})  \n**- الجـلاد 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee2}) \n**- العقاب : تغيير صورة حسابك بالصورة اعلاه والاسم والبايو يحددهم الجلاد ⚖**",
            )
            await event.delete()
            delgvar("Z_EKB")
            return
        except (Exception, ValueError):
            return
    if gvarstatus("Z_EK") is not None and gvarstatus("Z_E2K") is not None and gvarstatus("Z_E3K") is not None and gvarstatus("Z_E4K") is None and gvarstatus("Z_E5K") is None and gvarstatus("Z_E6K") is None:
        zelzal = int(zed3)
        zilzal = int(zee3)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
            name_zed = user_zed.first_name
            name_zee = user_zee.first_name
            messages = await event.client.get_messages("@VVVYVV4", filter=InputMessagesFilterPhotos)
            zedph = [message for message in messages]
            aing = await event.client.get_me()
            chosen_photo = random.sample(zedph, 1)[0]
            await event.client.send_file(
                event.chat_id,
                file=chosen_photo,
                caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖⛓ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم تحديـد المجـرم 🥷 ⇠**  [{name_zed}](tg://user?id={zed3})  \n**- الجـلاد 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee3}) \n**- العقاب : تغيير صورة حسابك بالصورة اعلاه والاسم والبايو يحددهم الجلاد ⚖**",
            )
            await event.delete()
            delgvar("Z_EKB")
            return
        except (Exception, ValueError):
            return
    if gvarstatus("Z_EK") is not None and gvarstatus("Z_E2K") is not None and gvarstatus("Z_E3K") is not None and gvarstatus("Z_E4K") is not None and gvarstatus("Z_E5K") is None and gvarstatus("Z_E6K") is None:
        zelzal = int(zed4)
        zilzal = int(zee4)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
            name_zed = user_zed.first_name
            name_zee = user_zee.first_name
            messages = await event.client.get_messages("@VVVYVV4", filter=InputMessagesFilterPhotos)
            zedph = [message for message in messages]
            aing = await event.client.get_me()
            chosen_photo = random.sample(zedph, 1)[0]
            await event.client.send_file(
                event.chat_id,
                file=chosen_photo,
                caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖⛓ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم تحديـد المجـرم 🥷 ⇠**  [{name_zed}](tg://user?id={zed4})  \n**- الجـلاد 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee4}) \n**- العقاب : تغيير صورة حسابك بالصورة اعلاه والاسم والبايو يحددهم الجلاد ⚖**",
            )
            await event.delete()
            delgvar("Z_EKB")
            return
        except (Exception, ValueError):
            return
    if gvarstatus("Z_EK") is not None and gvarstatus("Z_E2K") is not None and gvarstatus("Z_E3K") is not None and gvarstatus("Z_E4K") is not None and gvarstatus("Z_E5K") is not None and gvarstatus("Z_E6K") is None:
        zelzal = int(zed5)
        zilzal = int(zee5)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
            name_zed = user_zed.first_name
            name_zee = user_zee.first_name
            messages = await event.client.get_messages("@VVVYVV4", filter=InputMessagesFilterPhotos)
            zedph = [message for message in messages]
            aing = await event.client.get_me()
            chosen_photo = random.sample(zedph, 1)[0]
            await event.client.send_file(
                event.chat_id,
                file=chosen_photo,
                caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖⛓ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم تحديـد المجـرم 🥷 ⇠**  [{name_zed}](tg://user?id={zed5})  \n**- الجـلاد 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee5}) \n**- العقاب : تغيير صورة حسابك بالصورة اعلاه والاسم والبايو يحددهم الجلاد ⚖**",
            )
            await event.delete()
            delgvar("Z_EKB")
            return
        except (Exception, ValueError):
            return
    if gvarstatus("Z_EK") is not None and gvarstatus("Z_E2K") is not None and gvarstatus("Z_E3K") is not None and gvarstatus("Z_E4K") is not None and gvarstatus("Z_E5K") is not None and gvarstatus("Z_E6K") is not None:
        zelzal = int(zed6)
        zilzal = int(zee6)
        try:
            user_zed = await event.client.get_entity(zelzal)
            user_zee = await event.client.get_entity(zilzal)
            name_zed = user_zed.first_name
            name_zee = user_zee.first_name
            messages = await event.client.get_messages("@VVVYVV4", filter=InputMessagesFilterPhotos)
            zedph = [message for message in messages]
            aing = await event.client.get_me()
            chosen_photo = random.sample(zedph, 1)[0]
            await event.client.send_file(
                event.chat_id,
                file=chosen_photo,
                caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 - ⚖⛓ لعبـة عقـاب](t.me/ZThon)\n⋆──┄─┄─┄───┄─┄─┄──⋆\n**- تم تحديـد المجـرم 🥷 ⇠**  [{name_zed}](tg://user?id={zed5})  \n**- الجـلاد 👨🏻‍⚖⇠**  [{name_zee}](tg://user?id={zee5}) \n**- العقاب : تغيير صورة حسابك بالصورة اعلاه والاسم والبايو يحددهم الجلاد ⚖**",
            )
            await event.delete()
            delgvar("Z_EKB")
            return
        except (Exception, ValueError):
            return


@zedub.zed_cmd(pattern="ذاتي (\\d*) ([\\s\\S]*)")
async def selfdestruct(destroy):
    zzz = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = zzz[1]
    ttl = int(zzz[0])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, message)
    await sleep(ttl)
    await smsg.delete()

@zedub.zed_cmd(pattern="ذااتي (\\d*) ([\\s\\S]*)")
async def selfdestruct(destroy):
    zzz = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = zzz[1]
    ttl = int(zzz[0])
    text = f"{message}\n\n\n`هذه الرسالة سوف يتم حذفها تلقائياً بعد {ttl} ثانية`"

    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(ttl)
    await smsg.delete()

@zedub.on(admin_cmd(pattern="(خط الغامق|خط غامق|تفعيل غامق|تفعيل الغامق)"))
async def _(event):
    is_thin = gvarstatus("thin")
    if not is_thin:
        addgvar ("thin", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل الخـط الغامـق .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل غامق) **")
        return
    if is_thin:
        await edit_delete(event, "**⎉╎الخـط الغامـق مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل غامق) **")
        return

@zedub.on(admin_cmd(pattern="(تعطيل غامق|تعطيل الغامق)"))
async def _(event):
    is_thin = gvarstatus("thin")
    if is_thin:
        delgvar("thin")
        await edit_delete(event, "**⎉╎تم تعطيـل الخـط الغامـق .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل غامق) **")
        return
    if not is_thin:
        await edit_delete(event, "**⎉╎الخـط الغامـق مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل غامق) **")
        return

@zedub.on(admin_cmd(pattern="(خط المائل|خط مائل|تفعيل مائل|تفعيل المائل)"))
async def _(event):
    is_mael = gvarstatus("mael")
    if not is_mael:
        addgvar ("mael", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل الخـط المائـل .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل مائل) **")
        return
    if is_mael:
        await edit_delete(event, "**⎉╎الخـط المائـل مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل مائل) **")
        return

@zedub.on(admin_cmd(pattern="(تعطيل مائل|تعطيل المائل)"))
async def _(event):
    is_mael = gvarstatus("mael")
    if is_mael:
        delgvar("mael")
        await edit_delete(event, "**⎉╎تم تعطيـل الخـط المائـل .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل مائل) **")
        return
    if not is_mael:
        await edit_delete(event, "**⎉╎الخـط المائـل مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل مائل) **")
        return

# خط تشويش منقول لملف الايدي

@zedub.on(admin_cmd(pattern="(خط النسخ|خط نسخ|تفعيل نسخ|تفعيل النسخ)"))
async def _(event):
    is_cood = gvarstatus("cood")
    if not is_cood:
        addgvar ("cood", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل خـط النسـخ .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل نسخ) **")
        return
    if is_cood:
        await edit_delete(event, "**⎉╎خـط النسـخ مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل نسخ) **")
        return

@zedub.on(admin_cmd(pattern="(تعطيل نسخ|تعطيل النسخ)"))
async def _(event):
    is_cood = gvarstatus("cood")
    if is_cood:
        delgvar("cood")
        await edit_delete(event, "**⎉╎تم تعطيـل خـط النسـخ .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل نسخ) **")
        return
    if not is_cood:
        await edit_delete(event, "**⎉╎خـط النسـخ مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل نسخ) **")
        return

@zedub.on(admin_cmd(pattern="(خط الاقتباس|خط اقتباس|تفعيل اقتباس|تفعيل الاقتباس)"))
async def _(event):
    is_qood = gvarstatus("qood")
    if not is_qood:
        addgvar ("qood", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل خـط الاقتبـاس .. بنجـاح ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل اقتباس) **")
        return
    if is_qood:
        await edit_delete(event, "**⎉╎خـط الاقتبـاس مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل اقتباس) **")
        return

@zedub.on(admin_cmd(pattern="(تعطيل اقتباس|تعطيل الاقتباس)"))
async def _(event):
    is_qood = gvarstatus("qood")
    if is_qood:
        delgvar("qood")
        await edit_delete(event, "**⎉╎تم تعطيـل خـط الاقتبـاس .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل اقتباس) **")
        return
    if not is_qood:
        await edit_delete(event, "**⎉╎خـط الاقتبـاس مغعـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل اقتباس) **")
        return

@zedub.on(events.NewMessage(outgoing=True))
async def comming(event):
    if event.message.text and not event.message.media and "." not in event.message.text:
        is_thin = gvarstatus("thin")
        is_mael = gvarstatus("mael")
        is_cood = gvarstatus("cood")
        is_qood = gvarstatus("qood")
        #is_cllear = gvarstatus("cllear")
        if is_thin:
            try:
                await event.edit(f"**{event.message.text}**")
            except MessageIdInvalidError:
                pass
        if is_mael:
            try:
                await event.edit(f"__{event.message.text}__")
            except MessageIdInvalidError:
                pass
        if is_cood:
            try:
                await event.edit(f"`{event.message.text}`")
            except MessageIdInvalidError:
                pass
        if is_qood:
            try:
                await event.edit(f"```{event.message.text}```")
            except MessageIdInvalidError:
                pass
        #if is_cllear:
            #try:
                #await event.edit(f"<tg-spoiler>{event.message.text}</tg-spoiler>", parse_mode="html")
            #except MessageIdInvalidError:
                #pass


#Code by T.me/zzzzl1l
headers = {
    'authority': 'www.fancytextpro.com',
    'accept': 'text/plain, */*; q=0.01',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.fancytextpro.com',
    'referer': 'https://www.fancytextpro.com/',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

#Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="زخرفه(?: |$)(.*)")
async def zelzal_gif(event):
    namz = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not namz and reply:
        return await edit_delete(event, "**- ارسـل (.زخرفه) + اسمـك بالانكلـش**", 10)
    if not namz:
        return await edit_delete(event, "**- ارسـل (.زخرفه) + اسمـك بالانكلـش**", 10)
    data = {
        'text': namz,
        '_csrf': '',
        'pages[]': [
            'New',
            'Unique',
            'CoolText',
        ],
    }
    response = requests.post('https://www.fancytextpro.com/generate', headers=headers, data=data)
    data = json.loads(response.content)
    #s1 = data['MusicalMap']
    s2 = data['neonCharMap']
    s3 = data['boldCharMap']
    s4 = data['EmojiMap']
    s4 = data['italicCharMap']
    s5 = data['AncientMap']
    s6 = data['Ladyleo']
    if "💋" in s6:
        s6 = s6.replace("💋 ", "").replace(" 💋", "")
    s7 = data['boldItalicCharMap']
    s8 = data['SinoTibetan']
    s9 = data['monospaceCharMap']
    s10 = data['weirdChar']
    s11 = data['BoldFloara']
    if "🌸" in s11:
        s11 = s11.replace("🌸ꗥ～ꗥ🌸 ", "ꗥ～").replace(" 🌸ꗥ～ꗥ🌸", "～ꗥ")
    s12 = data['upperAnglesCharMap']
    s13 = data['BuzzChar']
    s14 = data['greekCharMap']
    s15 = data['SunnyDay']
    s16 = data['invertedSquaresCharMap']
    if "🅰" in s16:
        s16 = s16.replace("🅰", "🅐")
    if "🅱" in s16:
        s16 = s16.replace("🅱", "🅑")
    if "🅿" in s16:
        s16 = s16.replace("🅿", "🅟")
    if "🅾" in s16:
        s16 = s16.replace("🅾", "🅞")
    s17 = data['TextDecorated']
    s18 = data['doubleStruckCharMap']
    s19 = data['Dessert']
    s20 = data['oldEnglishCharMap']
    s21 = data['taiVietCharMap']
    s22 = data["oldEnglishCharBoldMap"]
    s23 = data['oldItalicText']
    s24 = data['cursiveLetters']
    s25 = data['cursiveLettersBold']
    s26 = data['BoldJavaneseText']
    s27 = data['wideTextCharMap']
    s28 = data['subscriptCharMap']
    s29 = data['GunText']
    s30 = data['superscriptCharMap']
    s31 = data['ak47GunText']
    zz = "ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - زخرفـه انكلـش\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
    aa = f"`{s2}`\n`{s3}`\n`{s4}`\n`{s5}`\n`{s6}`\n`{s7}`\n`{s8}`\n`{s9}`\n`{s10}`\n`{s11}`\n`{s12}`\n`{s13}`\n`{s14}`\n`{s15}`\n`{s16}`\n`{s17}`\n`{s18}`\n`{s19}`\n`{s20}`\n`{s21}`\n`{s22}`\n`{s23}`\n`{s24}`\n`{s25}`\n`{s26}`\n`{s27}`\n`{s28}`\n`{s29}`\n`{s30}`\n`{s31}`"
    dd = "࿐  𖣳  𓃠  𖡟  𖠜  ‌♡⁩  ‌༗  ‌𖢖  ❥  ‌ঌ  𝆹𝅥𝅮  𖠜\n𖠲  𖤍  𖠛  𝅘𝅥𝅮  ‌༒  ‌ㇱ  ߷  メ 〠  𓃬  𖠄\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\nl⌭l♥️🧸 زخرفـة انكلـش 30 نـوع تمبلـر -\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆"
    await edit_or_reply(event, f"**{zz}**\n{aa}\n\n**{dd}**")

###########################################################
from telethon import events
from telethon.tl.types import InputMediaDice
from random import randint
from . import zedub
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# قاموس لحفظ نتائج اللاعبين
#player_scores = {}
games = {}
#player_end = {}

@zedub.on(events.NewMessage(pattern='.لعبة النرد'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال /start_game.
    يحفظ معرف الدردشة الحالية كدلالة على بدء اللعبة في هذه الدردشة
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🎲 لعبـة رمـي النـرد")
    global player_scores
    #player_scores = {}
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎲 لعبـة رمـي النـرد](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة رمـي النـرد .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع النـرد بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🎲"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@zedub.on(events.NewMessage(pattern='.لعبة السهام'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال /start_game.
    يحفظ معرف الدردشة الحالية كدلالة على بدء اللعبة في هذه الدردشة
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🎯 لعبـة رمـي السهـام")
    global player_scores
    #player_scores = {}
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎯 لعبـة رمـي السهـام](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة رمـي السهـام .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع السهم بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🎯"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@zedub.on(events.NewMessage(pattern='.لعبة السلة'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال /start_game.
    يحفظ معرف الدردشة الحالية كدلالة على بدء اللعبة في هذه الدردشة
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🏀 لعبـة كـرة السلـة")
    global player_scores
    #player_scores = {}
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🏀 لعبـة كـرة السلـة](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة كـرة السلـة .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع السلة بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🏀"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@zedub.on(events.NewMessage(pattern='.لعبة الكرة'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال /start_game.
    يحفظ معرف الدردشة الحالية كدلالة على بدء اللعبة في هذه الدردشة
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "⚽️ لعبـة كـرة القـدم")
    global player_scores
    #player_scores = {}
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 ⚽️ لعبـة كـرة القـدم](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة كـرة القـدم .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع الكـرة بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "⚽️"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@zedub.on(events.NewMessage(pattern='.لعبة البولينج'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال /start_game.
    يحفظ معرف الدردشة الحالية كدلالة على بدء اللعبة في هذه الدردشة
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🎳 لعبـة كـرة البولينـج")
    global player_scores
    #player_scores = {}
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎳 لعبـة كـرة البولينـج](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة كـرة البولينـج .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع البولينـج بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🎳"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@zedub.on(events.NewMessage(pattern='.لعبة الحظ'))
async def start_game(event):
    """
    تبدأ اللعبة عند إرسال /start_game.
    يحفظ معرف الدردشة الحالية كدلالة على بدء اللعبة في هذه الدردشة
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    global games
    chat_id = event.chat_id
    games[chat_id] = {
        "players": {} 
    }
    if gvarstatus("dice_game"):
        delgvar("dice_game")
    if gvarstatus("name_game"):
        delgvar("name_game")
    addgvar("name_game", "🎰 لعبـة الحـظ")
    global player_scores
    #player_scores = {}
    addgvar("dice_game", True)
    await event.reply("[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎰 لعبـة الحـظ](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─⋆\n**- تم بـدء لعبـة الحـظ .. بنجـاح ☑️\n- اللي بيلعـب يضغـط ع عجلة الحظ بالاسفـل **", link_preview=False)
    await event.delete()
    emoticon = "🎰"
    r = await event.reply(file=InputMediaDice(emoticon=emoticon))

@zedub.on(events.NewMessage())
async def handle_dice(event):
    """
     يتفاعل مع رمي النرد في الدردشة التي بدأت فيها لعبة.
    """
    global games
    chat_id = event.chat_id
    #  التحقق من وجود لعبة في هذه الدردشة 
    if chat_id in games:
        sender = await event.get_sender()
        user_id = sender.id
        sender_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
        #  للتأكد من أن الرسالة تحتوي على رمي نرد 
        if event.dice and event.dice.emoticon == '🎲':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            #  حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                elif dice_value == 6:
                    dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• رمى النرد وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()
        if event.dice and event.dice.emoticon == '🎯':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            #  حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                elif dice_value == 6:
                    dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• رمى السهم وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()
        if event.dice and event.dice.emoticon == '🏀':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            #  حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                #elif dice_value == 6:
                    #dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• رمى كرة السلة وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()
        if event.dice and event.dice.emoticon == '⚽️':
            if gvarstatus("dice_game") is None:
                return
            await asyncio.sleep(2)
            dice_value = event.dice.value
            #  حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                #elif dice_value == 6:
                    #dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• سدد كرة القدم وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()
        if event.dice and event.dice.emoticon == '🎳':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            #  حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                if dice_value == 1:
                    dice_value = "❶"
                elif dice_value == 2:
                    dice_value = "❷"
                elif dice_value == 3:
                    dice_value = "❸"
                elif dice_value == 4:
                    dice_value = "❹"
                elif dice_value == 5:
                    dice_value = "❺"
                elif dice_value == 6:
                    dice_value = "❻"
                else:
                    pass
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• رمى كرة البولينج وحصل على ⇐ ** {dice_value} **نقاط**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()
        if event.dice and event.dice.emoticon == '🎰':
            if gvarstatus("dice_game") is None:
                return
            dice_value = event.dice.value
            #  حفظ نتيجة اللاعب 
            if user_id not in games[chat_id]["players"]:
                games[chat_id]["players"][user_id] = 0
                games[chat_id]["players"][user_id] += dice_value
                await event.reply(f"**• اللاعب ⇐**  {sender_name}\n**• حرك عجلة الحظ وحصل على ⇐ ** {dice_value} **نقطه**\n\n**• انتظـر لـ حتى يتم إنهاء اللعبـه واختيار الفائـز**\n**• لـ إنهـاء اللعبـه ارسـل الامـر** ( `.النتيجه` )")
            else:
                await event.delete()


@zedub.on(events.NewMessage(pattern='.النتيجه'))
async def end_game(event):
    """
    ينهي اللعبة الحالية في الدردشة ويعرض النتائج.
    """
    user = await event.get_sender()
    if user.id != zedub.uid:
        return
    if gvarstatus("dice_game") is None:
        return
    global games
    chat_id = event.chat_id

    # التحقق من وجود لعبة في هذه الدردشة
    if chat_id in games:
        if not games[chat_id]["players"]:
            await event.reply("**- لم يشارك أحد في اللعبة بعد.**")
            return

        #  إيجاد أعلى نتيجة 
        max_score = max(games[chat_id]["players"].values())

        #  إيجاد جميع الفائزين (الذين حصلوا على أعلى نتيجة)
        winners = [user_id for user_id, score in games[chat_id]["players"].items() if score == max_score]

        #  بناء رسالة النتائج 
        name_game = gvarstatus("name_game") if gvarstatus("name_game") else "🕹 العـاب المشاركـة الجماعيـة"
        results_message = f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 {name_game}\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆\n"
        for user_id, score in games[chat_id]["players"].items():
            user_entity = (await zedub.get_entity(user_id))
            user_name = f"{user_entity.first_name} {user_entity.last_name}" if user_entity.last_name else user_entity.first_name
            #score = str(score)  #  لا حاجة للتحويل  إلى  رموز  هنا
            if score == 1:
                score = "❶"
            elif score == 2:
                score = "❷"
            elif score == 3:
                score = "❸"
            elif score == 4:
                score = "❹"
            elif score == 5:
                score = "❺"
            elif score == 6:
                score = "❻"
            else:
                pass
            results_message += f"**• اللاعب ⇐**  {user_name} | **عـدد النقـاط ⇐** {score}\n"

        #  إضافة  أسماء  الفائزين 
        if len(winners) == 1:
            winner_entity = (await zedub.get_entity(winners[0]))
            winner_name = f"{winner_entity.first_name} {winner_entity.last_name}" if winner_entity.last_name else winner_entity.first_name
            if max_score == 1:
                max_score = "❶"
            elif max_score == 2:
                max_score = "❷"
            elif max_score == 3:
                max_score = "❸"
            elif max_score == 4:
                max_score = "❹"
            elif max_score == 5:
                max_score = "❺"
            elif max_score == 6:
                max_score = "❻"
            else:
                pass
            results_message += f"\n\n**• الفـائـز هـو ⇐** {winner_name} | **بمجمـوع نقـاط ⇐** {max_score} 🏆"
        else:
            results_message += f"\n\n**• الفائـزيـن هـم:** "
            for winner_id in winners:
                winner_entity = (await zedub.get_entity(winner_id))
                winner_name = f"**• الفائـز ⇐** {winner_entity.first_name} {winner_entity.last_name}" if winner_entity.last_name else winner_entity.first_name
                results_message += f"\n{winner_name}"
            #results_message = results_message[:-2]  #  إزالة  الفاصلة  والفراغ  الإضافيين  في  النهاية
            if max_score == 1:
                max_score = "❶"
            elif max_score == 2:
                max_score = "❷"
            elif max_score == 3:
                max_score = "❸"
            elif max_score == 4:
                max_score = "❹"
            elif max_score == 5:
                max_score = "❺"
            elif max_score == 6:
                max_score = "❻"
            else:
                pass
            results_message += f"\n**• نقـاط الفائـزيـن ⇐** {max_score} **نقطـه** 🏆"

        # إزالة اللعبة من القائمة بعد نهايتها
        del games[chat_id]
        delgvar("dice_game")
        delgvar("name_game")
        await event.reply(results_message, link_preview=False)
        await event.delete()
    else:
        await event.reply("**- لا يوجد لعبة جماعيه في هذه الدردشة ❌**\n**- لـ بـدء لعبـة جماعية جديـدة 🎮**\n**- ارسـل الامـر** ( `.العاب الجماعي` ) 🕹")


ZelzalGM_cmd = (
"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗮𝗺𝗲 🎮 العـاب المشاركـة الجماعيـة](t.me/ZThon)\n"
"**⋆─┄─┄─┄─┄•┄─┄─┄─┄─⋆**\n"
"**⌖ قائمـة 6 العـاب مشاركـة جماعيـة ممطروقـه 🪁**\n"
"**⌖ تقبـل مشاركـة عـدد لامحـدود مـن اللاعبيـن 🤼‍♀**\n"
"**⌖ لـ اول مـرة ع سـورس يـوزر بـوت 🥇**\n"
"**⌖ تستطيـع لعبها فـي الخاص او المجموعـات مـع أصدقائـك 🕹**\n\n"
"  ❶ **⪼**  `.لعبة النرد`\n"
"**⪼ لعبـة رمـي النـرد 🎲 الجديـدة اكثـر نقطـه 6 ⛳️**\n\n"
"  ❷ **⪼**  `.لعبة السهام`\n"
"**⪼ لعبـة رمـي السهـام 🎯 أعلـى نقطـه فيها 5 نقـاط 🏹**\n\n"
"  ❸ **⪼**  `.لعبة الكرة`\n"
"**⪼ لعبـة تسديـد كـرة القـدم ⚽️ أعلـى نقطـه فيها 5 نقـاط 🥅**\n\n"
"  ❹ **⪼**  `.لعبة السلة`\n"
"**⪼ لعبـة رمـي كـرة السلة 🏀 أعلـى نقطـه فيها 5 نقـاط ⛹🏻‍♂**\n\n"
"  ❺ **⪼**  `.لعبة البولينج`\n"
"**⪼ لعبـة رمـي كـرة البولينـج 🎳 أعلـى نقطـه فيها 6 نقـاط 🤽‍♀**\n\n"
"  ❻ **⪼**  `.لعبة الحظ`\n"
"**⪼ لعبـة الحـظ 🎰 أعلـى نقطـه فيها 64 نقطـه 🎟**\n\n"
)

@zedub.zed_cmd(pattern="العاب المشاركة")
async def ganez(event):
    await edit_or_reply(event, ZelzalGM_cmd, link_preview=False)
