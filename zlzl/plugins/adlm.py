import re
import os
import typing
import asyncio
from pytz import timezone
from random import choice
import asyncio
import csv
from pathlib import Path
from datetime import datetime
from time import time
import aiofiles

try:
    from aiocsv import AsyncDictReader, AsyncWriter
except ModuleNotFoundError:
    os.system("pip3 install aiocsv")
    from aiocsv import AsyncDictReader, AsyncWriter

from telethon.errors.rpcerrorlist import (
    ChannelPrivateError,
    FloodWaitError,
    InputUserDeactivatedError,
    UserAlreadyParticipantError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
    UserKickedError,
    UserChannelsTooMuchError,
)
from telethon.tl import functions as fun, types as typ
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from . import zedub
from ..Config import Config
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from . import BOTLOG, BOTLOG_CHATID

invite_text = """
<b>ᯓ <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻 𝗩𝗶𝗽 🚹 إضـافـة الأعضـاء</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ <b>إنتهـت الإضافـة .. بنجـاح</b> ✅
⌔ <b>تـم إضافـة :</b> <code>{}</code>
⌔ <b>خطـأ بـ إضافـة :</b> <code>{}</code>
⌔ <b>آخـر خطـأ :</b> <code>{}</code>
"""
done_text = """
<b>ᯓ <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻 𝗩𝗶𝗽 🚹 إضـافـة الأعضـاء</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ <b>إنتهـت الإضافـة .. بنجـاح</b> ✅
⌔ <b>تـم إضافـة :</b> <code>{}</code>
⌔ <b>خطـأ بـ إضافـة :</b> <code>{}</code>
⌔ <b>الوقـت المستغـرق :</b> <code>{}</code> ⌛️
⌔ <b>المجموعـة الهـدف :</b> <code>{}</code>
⌔ <b>الوقـت :</b> <code>{}</code> ⏰
"""
done_limit_text = """
<b>ᯓ <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻 𝗩𝗶𝗽 🚹 إضـافـة الأعضـاء</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ <b>انتهـت الإضـافـه مـع حـدود تيليجـرام</b> ✅
<b><u>ملاحظــه هامــه :</u></b>
<pre>لقـد تجـاوزت حـدود الاضـافة حـاول مـرة آخـرى بعـد {}</pre>

<b><u>معلومـات الخطـأ :</u></b>
<pre>{}</pre>

⌔ <b>تـم إضافـة :</b> <code>{}</code>
⌔ <b>خطـأ بـ إضافـة :</b> <code>{}</code>
⌔ <b>الوقـت المستغـرق :</b> <code>{}</code> ⌛️
⌔ <b>المجموعـة الهـدف :</b> <code>{}</code>
⌔ <b>الوقـت :</b> <code>{}</code> ⏰
"""
done_error_text = """
<b>ᯓ <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻 𝗩𝗶𝗽 🚹 إضـافـة الأعضـاء</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ <b>اووبـسس .. لقـد حـدث خطـأ</b> ⚠️

<b><u>معلومـات الخطـأ :</u></b>
<pre>{}</pre>

⌔ <b>تـم إضافـة :</b> <code>{}</code>
⌔ <b>خطـأ بـ إضافـة :</b> <code>{}</code>
⌔ <b>الوقـت المستغـرق :</b> <code>{}</code> ⌛️
⌔ <b>المجموعـة الهـدف :</b> <code>{}</code>
⌔ <b>الوقـت :</b> <code>{}</code> ⏰
"""
getmembers_text = """
<b>ᯓ <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻 𝗩𝗶𝗽 🚹 تجميـع الأعضـاء</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ <b>إنتهـت العمليـة .. بنجـاح</b> ✅
⌔ <b>نـوع عمليـة السحب :</b> <code>{}</code>
⌔ <b>المستغـرق الوقـت :</b> <code>{}</code> ⏳

⌔ <b>الايـدي :</b> <code>{}</code>
⌔ <b>الاسـم :</b> <code>{}</code>
⌔ <b>اليـوزر :</b> {}
⌔ <b>إجمالي الاعضـاء :</b> <code>{}</code>
⌔ <b>تم سحـب ({}) بنجـاح :</b> <code>{}</code>
⌔ <b>الوقـت :</b> <code>{}</code> ⏰
"""
no_process_text = "**- عـذراً .. لايوجـد عمليـة إضافـة جاريـه الان**"
cancelled_text = """
<b>ᯓ <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻 𝗩𝗶𝗽 🚹 إضـافـة الأعضـاء</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
⌔ <b>تم إيقـاف عمليـة الإضافـة .. بنجـاح</b> ✅

⌔ <b>نـوع العمليـة :</b> <code>{}</code>
⌔ <b>المجموعـة الهـدف :</b> <code>{}</code>
⌔ <b>تـم إضافـة :</b> <code>{}</code>
⌔ <b>الوقـت المستغـرق :</b> <code>{}</code> ⌛️
"""
_INVITING_LOCK = asyncio.Lock()
_SCRAPING_LOCK = asyncio.Lock()
_ADDING_LOCK = asyncio.Lock()

INVITE_WORKER: typing.Dict[str, typing.Any] = {}
DEVS = (5176749470, 1895219306, 925972505)
tz = timezone(Config.TZ)
hl = Config.COMMAND_HAND_LER
Root: Path = Path(__file__).parent.parent

TELEGRAM_LINK_RE = r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/)([\w-]+)$"
USERNAME_RE = r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)?(?:/)?(.*?))"
MSG_ID_RE = r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/)(?:c\/|)(.*)\/(.*)|(?:tg//openmessage\?)?(?:user_id=(.*))?(?:\&message_id=(.*))"


def is_telegram_link(url: str) -> bool:
    # TODO: support for username.t.me
    return bool(re.match(TELEGRAM_LINK_RE, url, flags=re.I))


def get_username(url: str) -> str:
    # TODO: support for username.t.me
    return "".join(re.sub(USERNAME_RE, "@", url, flags=re.I).split("/")[:1])

def normalize_chat_id(chat_id: typing.Union[int, str]) -> typing.Union[int, str]:
    if str(chat_id).startswith(("-100", "-")) and str(chat_id)[1:].isdecimal():
        chat_id = int(str(chat_id).replace("-100", "").replace("-", ""))
    elif str(chat_id).isdecimal():
        chat_id = int(chat_id)
    return chat_id

def get_user_status(user: typ.User) -> str:
    if user.bot or user.support:
        status = "none"
    if isinstance(user.status, typ.UserStatusOnline):
        status = "online"
    elif isinstance(user.status, typ.UserStatusOffline):
        status = "offline"
    elif isinstance(user.status, typ.UserStatusRecently):
        status = "recently"
    elif isinstance(user.status, typ.UserStatusLastWeek):
        status = "within_week"
    elif isinstance(user.status, typ.UserStatusLastMonth):
        status = "within_month"
    else:
        status = "long_time_ago"
    return status

def time_formatter(ms: typing.Union[int, float]) -> str:
    minutes, seconds = divmod(int(ms / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w, ") if weeks else "")
        + ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
    )
    return tmp and tmp[:-2] or "0s"


@zedub.zed_cmd(pattern="ضيف(?: |$)(.*)")
async def _(zelzal):
    if not zelzal.is_group:
        return await edit_delete(zelzal, "**ايا مطـي .. هـذه ليست مجموعـة ؟!**")
    chat_id = normalize_chat_id(zelzal.chat_id)
    if INVITE_WORKER.get(chat_id) or _INVITING_LOCK.locked():
        await edit_delete(zelzal, "**- عـذراً .. هناك عمليـة إضافـة جاريـه الان**", time=5)
        return
    async with _INVITING_LOCK:
        ga = zelzal.client
        yy = await edit_or_reply(zelzal, "**╮  جـاري الاضـافه .. الࢪجـاء الانتظـار ...𓅫╰**")
        target = await get_chat_info(zelzal, yy)
        if not target:
            return
        target_id = target.full_chat.id
        args = zelzal.pattern_match.group(1).split(" ")
        is_active = bool(
            len(args) > 1
            and args[1].lower()
            in (
                "active",
                "a",
            )
        )
        is_online = bool(
            len(args) > 1
            and args[1].lower()
            in (
                "online",
                "on",
            )
        )
        if is_active:
            filters = (
                "within_week",
                "within_month",
                "long_time_ago",
            )
        elif is_online:
            filters = (
                "recently",
                "offline",
                "within_week",
                "within_month",
                "long_time_ago",
            )
        else:
            filters = ("long_time_ago",)
        start_time = time()
        local_now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        max_success, success, failed, error = 300, 0, 0, "لايوجـد"
        chat = await zelzal.get_chat()
        INVITE_WORKER[chat_id] = {
            "mode": "invite",
            "msg_id": yy.id,
            "current": chat.title,
            "success": success,
            "now": local_now,
        }
        try:
            await edit_or_reply(yy, "**- جـاري جـمع معـلومات الاعضـاء ...⏳**")
            async for x in ga.iter_participants(target_id):
                if not INVITE_WORKER.get(chat_id):
                    break
                if (
                    not (x.deleted or x.bot or x.is_self or hasattr(x.participant, "admin_rights"))
                    and get_user_status(x) not in filters
                ):
                    try:
                        if error.lower().startswith(("Too many", "a wait of")) or success > max_success:
                            if INVITE_WORKER.get(chat_id):
                                INVITE_WORKER.pop(chat_id)
                            taken = time_formatter((time() - start_time) * 1000)
                            try:
                                waitfor = int("".join(filter(str.isdigit, error.lower())))
                            except ValueError:
                                waitfor = 0
                            flood = time_formatter(waitfor * 1000)
                            done_limit = done_limit_text.format(
                                flood,
                                error,
                                success,
                                failed,
                                taken,
                                zelzal.pattern_match.group(1),
                                local_now,
                            )
                            await edit_or_reply(yy, done_limit, parse_mode="html")
                            return await zedub.send_message(BOTLOG_CHATID, done_limit, parse_mode="html")
                        await ga(
                            fun.channels.InviteToChannelRequest(
                                chat_id,
                                users=[x.id],
                            )
                        )
                        success += 1
                        INVITE_WORKER[chat_id].update({"success": success})
                        await edit_or_reply(yy, 
                            invite_text.format(
                                success,
                                failed,
                                error,
                            ),
                            parse_mode="html",
                        )
                        await asyncio.sleep(3)
                    except (
                        InputUserDeactivatedError,
                        UserAlreadyParticipantError,
                        UserNotMutualContactError,
                        UserPrivacyRestrictedError,
                        UserKickedError,
                        UserChannelsTooMuchError,
                    ):
                        failed += 1
                    except ChannelPrivateError as err:
                        if INVITE_WORKER.get(chat_id):
                            INVITE_WORKER.pop(chat_id)
                        taken = time_formatter((time() - start_time) * 1000)
                        done_error = done_error_text.format(
                            str(err),
                            success,
                            failed,
                            taken,
                            zelzal.pattern_match.group(1),
                            local_now,
                        )
                        await edit_or_reply(yy, done_error, parse_mode="html")
                        return await zedub.send_message(BOTLOG_CHATID, done_error, parse_mode="html")
                    except Exception as err:
                        error = str(err)
                        failed += 1
        except BaseException:
            pass
        if INVITE_WORKER.get(chat_id):
            INVITE_WORKER.pop(chat_id)
        taken = time_formatter((time() - start_time) * 1000)
        done = done_text.format(
            success,
            failed,
            taken,
            zelzal.pattern_match.group(1),
            local_now,
        )
        await edit_or_reply(yy, done, parse_mode="html")
        await zedub.send_message(BOTLOG_CHATID, done, parse_mode="html")


@zedub.zed_cmd(pattern="سحب?(?: |$)(.*)")
async def _(zelzal):
    chat_id = normalize_chat_id(zelzal.chat_id)
    if _SCRAPING_LOCK.locked():
        await edit_delete(zelzal, "**- عـذراً .. هناك عمليـة سحب جاريـه الان**", time=5)
        return
    async with _SCRAPING_LOCK:
        ga = zelzal.client
        yy = await edit_or_reply(zelzal, "**╮  جـاري تجميـع الاعضـاء .. الࢪجـاء الانتظـار ...𓅫╰**")
        target = await get_chat_info(zelzal, yy)
        if not target:
            return
        target_id = target.full_chat.id
        if chat_id == target_id:
            return await yy.try_delete()
        args = zelzal.pattern_match.group(1).split(" ")
        is_append = bool(len(args) > 1 and args[1].lower() in ("-a", "a", "append"))
        start_time = time()
        local_now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        members, admins, bots = 0, 0, 0
        members_file = "members_list.csv"
        admins_file = "admins_list.csv"
        bots_file = "bots_list.csv"
        await edit_or_reply(yy, "**- جـاري جـمع معـلومات الاعضـاء ...⏳**")
        members_exist = bool(is_append and (Root / members_file).exists())
        if members_exist:
            with open(members_file, "r") as f:
                rows = [int(x[0]) for x in csv.reader(f) if str(x[0]).isdecimal()]
            members = len(rows)
            async with aiofiles.open(members_file, mode="a") as f:
                writer = AsyncWriter(f, delimiter=",")
                # aggressive=True : telethon.errors.common.MultiError: ([None, None, None, FloodWaitError('A wait of 11 seconds is required (caused by GetParticipantsRequest)'),
                try:
                    async for x in ga.iter_participants(target_id):
                        if (
                            not (x.deleted or x.bot or x.is_self or hasattr(x.participant, "admin_rights"))
                            and get_user_status(x) != "long_time_ago"
                            and x.id not in rows
                        ):
                            try:
                                await writer.writerow([x.id, x.access_hash, x.username])
                                members += 1
                            except BaseException:
                                pass
                except BaseException:
                    pass
        else:
            async with aiofiles.open(members_file, mode="w") as f:
                writer = AsyncWriter(f, delimiter=",")
                await writer.writerow(["user_id", "hash", "username"])
                try:
                    async for x in ga.iter_participants(target_id):
                        if (
                            not (x.deleted or x.bot or x.is_self or hasattr(x.participant, "admin_rights"))
                            and get_user_status(x) != "long_time_ago"
                        ):
                            try:
                                await writer.writerow([x.id, x.access_hash, x.username])
                                members += 1
                            except BaseException:
                                pass
                except BaseException:
                    pass
        await edit_or_reply(yy, "**- جـاري جمع معلومـات الادمنيـه ...⏳**")
        async with aiofiles.open(admins_file, mode="w") as f:
            writer = AsyncWriter(f, delimiter=",")
            await writer.writerow(["user_id", "hash", "username"])
            try:
                async for x in ga.iter_participants(
                    target_id,
                    filter=typ.ChannelParticipantsAdmins,
                ):
                    if not (x.deleted or x.bot or x.is_self):
                        try:
                            await writer.writerow([x.id, x.access_hash, x.username])
                            admins += 1
                        except BaseException:
                            pass
            except BaseException:
                pass
        await edit_or_reply(yy, "**- جـاري جمع معلومـات البوتـات ...⏳**")
        async with aiofiles.open(bots_file, mode="w") as f:
            writer = AsyncWriter(f, delimiter=",")
            await writer.writerow(["user_id", "hash", "username"])
            try:
                async for x in ga.iter_participants(
                    target_id,
                    filter=typ.ChannelParticipantsBots,
                ):
                    if not x.deleted:
                        try:
                            await writer.writerow([x.id, x.access_hash, x.username])
                            bots += 1
                        except BaseException:
                            pass
            except BaseException:
                pass
        taken = time_formatter((time() - start_time) * 1000)
        await edit_or_reply(yy, "**- جـاري رفـع ملف الاعضـاء CSV ...📁**")
        await zelzal.client.send_file(
            zelzal.chat_id,
            getmembers_text.format(
                "اعضـاء فقـط",
                taken,
                target_id,
                target.chats[0].title,
                "@" + target.chats[0].username if target.chats[0].username else "لايوجـد",
                target.full_chat.participants_count,
                members,
                "باستثنـاء حسابك, المشرفين, البوتات, الحسابات المحذوفه, الاعضاء طويلة الظهور",
                local_now,
            ),
            file=members_file,
            parse_mode="html",
            force_document=True,
        )
        await zelzal.client.send_file(
            zelzal.chat_id,
            getmembers_text.format(
                "مشرفيـن فقـط",
                taken,
                target_id,
                target.chats[0].title,
                "@" + target.chats[0].username if target.chats[0].username else "لايوجـد",
                target.full_chat.participants_count,
                admins,
                "باستثنـاء حسابك, البوتات, الحسابات المحذوفه",
                local_now,
            ),
            file=admins_file,
            parse_mode="html",
            force_document=True,
        )
        await zelzal.client.send_file(
            zelzal.chat_id,
            getmembers_text.format(
                "بوتـات فقـط",
                taken,
                target_id,
                target.chats[0].title,
                "@" + target.chats[0].username if target.chats[0].username else "لايوجـد",
                target.full_chat.participants_count,
                bots,
                "باستثنـاء البـوتات المحذوفـه",
                local_now,
            ),
            file=bots_file,
            parse_mode="html",
            force_document=True,
        )


@zedub.zed_cmd(pattern="ضف (الاعضاء|المشرفين|البوتات)?$")
async def _(zelzal):
    if not zelzal.is_group:
        return await edit_delete(zelzal, "**ايا مطـي .. هـذه ليست مجموعـة ؟!**")
    chat_id = normalize_chat_id(zelzal.chat_id)
    if INVITE_WORKER.get(chat_id) or _ADDING_LOCK.locked():
        await edit_delete(zelzal, "**- عـذراً .. هناك عمليـة سحب جاريـه الان**", time=5)
        return
    async with _ADDING_LOCK:
        ga = zelzal.client
        yy = await edit_or_reply(zelzal, "**- جـارِ نقـل الاعضـاء المسحوبيـن ...**")
        users = []
        mode = None
        args = zelzal.pattern_match.group(1).lower()
        if args.startswith("الاعضاء"):
            mode = "members"
        elif args.startswith("المشرفين"):
            mode = "admins"
        elif args.startswith("البوتات"):
            mode = "bots"
        csv_file = mode + "_list.csv"
        start_time = time()
        local_now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        try:
            await edit_or_reply(yy, f"`Reading {csv_file} file...`")
            async with aiofiles.open(csv_file, mode="r") as f:
                async for row in AsyncDictReader(f, delimiter=","):
                    user = {"user_id": int(row["user_id"]), "hash": int(row["hash"])}
                    users.append(user)
        except FileNotFoundError:
            await edit_or_reply(yy, 
                f"File `{csv_file}` not found.\nPlease run `{hl}getmembers [username/link/id]/[reply]` and try again!"
            )
            return
        success = 0
        chat = await zelzal.get_chat()
        INVITE_WORKER[chat_id] = {
            "mode": "add",
            "msg_id": yy.id,
            "current": chat.title,
            "success": success,
            "now": local_now,
        }
        for user in users:
            if not INVITE_WORKER.get(chat_id):
                break
            if success == 50:
                await edit_or_reply(yy, f"`🔄 Reached 50 members, wait until {900/60} minutes...`")
                await asyncio.sleep(900)
            try:
                adding = typ.InputPeerUser(user["user_id"], user["hash"])
                await ga(
                    fun.channels.InviteToChannelRequest(
                        chat_id,
                        users=[adding],
                    )
                )
                success += 1
                INVITE_WORKER[chat_id].update({"success": success})
                await edit_or_reply(yy, f"`Adding {success} {mode}...`")
            except FloodWaitError as fw:
                await asyncio.sleep(fw.seconds + 10)
                try:
                    adding = typ.InputPeerUser(user["user_id"], user["hash"])
                    await ga(
                        fun.channels.InviteToChannelRequest(
                            chat_id,
                            users=[adding],
                        )
                    )
                    success += 1
                    INVITE_WORKER[chat_id].update({"success": success})
                    await edit_or_reply(yy, f"`Adding {success} {mode}...`")
                except ChannelPrivateError:
                    break
                except BaseException:
                    pass
            except ChannelPrivateError:
                break
            except BaseException:
                pass
        if INVITE_WORKER.get(chat_id):
            INVITE_WORKER.pop(chat_id)
        taken = time_formatter((time() - start_time) * 1000)
        await edit_or_reply(yy, f"`✅ Completed adding {success} {mode} in {taken}` at `{local_now}`")


@zedub.zed_cmd(pattern="ايقاف الاضافه$")
async def _(zelzal):
    if not zelzal.is_group:
        return await edit_or_reply(zelzal, "**ايا مطـي .. هـذه ليست مجموعـة ؟!**")
    chat_id = normalize_chat_id(zelzal.chat_id)
    if not INVITE_WORKER.get(chat_id):
        return await edit_or_reply(zelzal, no_process_text)
    _worker = INVITE_WORKER.get(chat_id)
    if INVITE_WORKER.get(chat_id):
        INVITE_WORKER.pop(chat_id)
    await edit_or_reply(
        zelzal,
        cancelled_text.format(
            "الإضافـه" if _worker.get("mode") == "invite" else "تجميـع الاعضـاء",
            _worker.get("current"),
            _worker.get("success"),
            _worker.get("now"),
        ),
        parse_mode="html",
        reply_to=_worker.get("msg_id"),
    )


async def get_chat_info(zelzal, yy):
    info = None
    target = zelzal.pattern_match.group(1)
    if not target:
        await edit_delete(yy, "**╮  ارسـل (.ضيف) + رابـط/يـوزر/ايـدي المجمـوعـة ...𓅫╰**")
        return None
    target = normalize_chat_id(target)
    if isinstance(target, str) and is_telegram_link(target):
        target = get_username(target)
    try:
        info = await zelzal.client(fun.messages.GetFullChatRequest(target))
    except BaseException:
        try:
            info = await zelzal.client(fun.channels.GetFullChannelRequest(target))
        except ValueError:
            await edit_delete(yy, "**╮  يجب ان تكـون عضـو فـي المجمـوعـة الهـدف ...𓅫╰**")
            return None
        except BaseException:
            await edit_delete(yy, "**╮  رابـط غيـر صالـح - تحـقق مـن الرابـط ...𓅫╰**")
            return None
    return info


@zedub.zed_cmd(pattern="انضم(?: |$)(.*)")
async def zelzal_join(event): #Code by T.me/zzzzl1l
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    sweetie = "- جـارِ الانضمـام انتظـر قليـلاً . . ."
    zzz = await edit_or_reply(event, sweetie, parse_mode=None, link_preview=None)
    if not link and reply: #Code by T.me/zzzzl1l
        link = reply.text
    if not link: #Code by T.me/zzzzl1l
        return await edit_or_reply(event, "**- ارسـل الامـر بالـرد ع رابـط او يوزر**\n**- او بـ إضافة رابـط او يـوزر لـ الامـر**")
    if link.startswith('https://t.me/+'):
        try:
            link = link.replace('https://t.me/+', '')
            result = await zedub(ImportChatInviteRequest(link.strip()))
            return await zzz.edit("**- تم الانضمـام .. بنجـاح  ✓**")
        except Exception as e:
            return await zzz.edit("**- خطـأ:**\n" + str(e))
    elif link.startswith('@'):
        try:
            get_entity_must_join = await zedub.get_entity(link)
            result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            return await zzz.edit("**- تم الانضمـام .. بنجـاح  ✓**")
        except Exception as e:
            return await zzz.edit("**- خطـأ:**\n" + str(e))
    elif link.startswith('https://t.me/'):
        try:
            link = link.replace('https://t.me/', '')
            get_entity_must_join = await zedub.get_entity(link)
            result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            return await zzz.edit("**- تم الانضمـام .. بنجـاح  ✓**")
        except Exception as e:
            return await zzz.edit("**- خطـأ:**\n" + str(e))
    else:
        return await edit_or_reply(event, "**- ارسـل الامـر بالـرد ع رابـط او يوزر**\n**- او بـ إضافة رابـط او يـوزر لـ الامـر**")


#Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="غادر(?: |$)(.*)")
async def zelzal_leave(event): #Code by T.me/zzzzl1l
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    sweetie = "- جـارِ المغـادرة انتظـر قليـلاً . . ."
    zzz = await edit_or_reply(event, sweetie, parse_mode=None, link_preview=None)
    if not link and reply: #Code by T.me/zzzzl1l
        link = reply.text
    if not link: #Code by T.me/zzzzl1l
        return await edit_or_reply(event, "**- ارسـل الامـر بالـرد ع رابـط او يوزر**\n**- او بـ إضافة رابـط او يـوزر لـ الامـر**")
    if link.startswith('https://t.me/+'):
        try:
            link = link.replace('https://t.me/+', '')
            result = await zedub(ImportChatInviteRequest(link.strip()))
            return await zzz.edit("**- تم المغـادرة .. بنجـاح  ✓**")
        except Exception as e:
            return await zzz.edit("**- خطـأ:**\n" + str(e))
    elif link.startswith('@'):
        try:
            get_entity_must_join = await zedub.get_entity(link)
            result = await zedub(LeaveChannelRequest(get_entity_must_join.id))
            return await zzz.edit("**- تم المغـادرة .. بنجـاح  ✓**")
        except Exception as e:
            return await zzz.edit("**- خطـأ:**\n" + str(e))
    elif link.startswith('https://t.me/'):
        try:
            link = link.replace('https://t.me/', '')
            get_entity_must_join = await zedub.get_entity(link)
            result = await zedub(LeaveChannelRequest(get_entity_must_join.id))
            return await zzz.edit("**- تم المغـادرة .. بنجـاح  ✓**")
        except Exception as e:
            return await zzz.edit("**- خطـأ:**\n" + str(e))
    else:
        return await edit_or_reply(event, "**- ارسـل الامـر بالـرد ع رابـط او يوزر**\n**- او بـ إضافة رابـط او يـوزر لـ الامـر**")


@zedub.zed_cmd(pattern="اضافه(?: |$)(.*)")
async def _(event):
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    fun.messages.AddChatUserRequest(
                        chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{str(e)}`", 5)
    else:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    fun.channels.InviteToChannelRequest(
                        channel=event.chat_id, users=[user_id]
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{e}`", 5)

    await edit_or_reply(event, f"**{to_add_users} تم اضافته بنجاح ✓**")
