import asyncio
import json
from datetime import datetime
from html import escape
from math import floor, ceil
from random import choice
import heroku3
import re
import sys
import typing
from string import ascii_letters, ascii_uppercase, ascii_lowercase
import time
from uuid import uuid4
from bs4 import BeautifulSoup
from cachetools import cached
from emoji import replace_emoji
from markdown.core import markdown
import os.path
import subprocess
from functools import partial
import aiofiles
import aiohttp
import telegraph
import html
from cachetools import cached, LRUCache
from heroku3 import from_key
from contextlib import suppress
from datetime import datetime, timezone
from functools import wraps
from functools import reduce
from inspect import stack
from io import BytesIO
from pathlib import Path
from traceback import format_exc
from telethon import hints, events
from telethon.errors.rpcerrorlist import (
    AuthKeyDuplicatedError,
    ChatSendGifsForbiddenError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    ChatWriteForbiddenError,
    FloodWaitError,
    MessageDeleteForbiddenError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)
from telethon.tl import types as typ

from . import zedub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import get_readable_time
from . import StartTime, BOTLOG, BOTLOG_CHATID
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY

zz_pic = "https://graph.org/file/6c21b5221a7e53c69014b.jpg"

class Heroku:
    def __init__(self) -> None:
        self.name: str = HEROKU_APP_NAME
        self.api: str = HEROKU_API_KEY

    def heroku(self) -> typing.Any:
        _conn = None
        try:
            if self.is_heroku:
                _conn = from_key(self.api)
        except BaseException as err:
            LOGS.exception(err)
        return _conn

    @property
    @cached(LRUCache(maxsize=512))
    def stack(self) -> str:
        try:
            app = self.heroku().app(self.name)
            stack = app.info.stack.name
        except BaseException:
            stack = "none"
        return stack

    @property
    def is_heroku(self) -> bool:
        return bool(self.api and self.name)

hk = Heroku()



def mask_email(email: str) -> str:
    at = email.find("@")
    return email[0] + "*" * int(at - 2) + email[at - 1 :]

def humanbytes(size: typing.Union[int, float]) -> str:
    if not size:
        return "0 B"
    power = 1024
    pos = 0
    power_dict = {
        0: "",
        1: "K",
        2: "M",
        3: "G",
        4: "T",
        5: "P",
        6: "E",
        7: "Z",
        8: "Y",
    }
    while size > power:
        size /= power
        pos += 1
    return "{:.2f}{}B".format(size, power_dict[pos])


def to_dict(
    obj: typing.Any,
    classkey: typing.Optional[str] = None,
) -> typing.Any:
    if isinstance(obj, dict):
        data = {}
        for k, v in obj.items():
            data[k] = to_dict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return to_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(_, classkey) for _ in obj]
    elif hasattr(obj, "__dict__"):
        data = dict(
            [(k, to_dict(v, classkey)) for k, v in obj.__dict__.items() if not callable(v) and not k.startswith("_")]
        )
        if classkey and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    return obj

async def Fetch(
    url: str,
    post: bool = None,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    data: dict = None,
    ssl: typing.Any = None,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
    statuses: typing.Optional[typing.Set[int]] = None,
    *args,
    **kwargs,
) -> typing.Any:
    statuses = statuses or {}
    if not headers:
        headers = {
            "User-Agent": "Python/{0[0]}.{0[1]} aiohttp/{1} getter/{2}".format(
                sys.version_info,
                aiohttp.__version__,
                __version__,
            )
        }
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            if post:
                resp = await session.post(
                    url=url,
                    json=json,
                    data=data,
                    ssl=ssl,
                    raise_for_status=False,
                    *args,
                    **kwargs,
                )
            else:
                resp = await session.get(
                    url=url,
                    params=params,
                    ssl=ssl,
                    raise_for_status=False,
                    *args,
                    **kwargs,
                )
        except BaseException:
            return None
        if resp.status not in {*{200, 201}, *statuses}:
            return None
        if re_json:
            return await resp.json(content_type=None)
        if re_content:
            return await resp.read()
        if real:
            return resp
        return await resp.text()


dyno_text = """
<b>⌔ تطبيـق هيروكـو 📦</b>
<b>• الاسـم :</b> <code>{}</code>
<b>• نظـام التشغيـل :</b> <code>{}</code>
<b>• السيرفـر :</b> <code>{}</code>
<b>• تاريـخ الانشـاء :</b> <code>{}</code>
<b>• آخـر تحـديث :</b> <code>{}</code>
<b>• الايميـل :</b> <code>{}</code>

<b>⌔ هيـروكـو داينـو ⚙️</b>
<b>- الساعات المستخدمه :</b>
    •  <code>{}ساعة  {}دقيقه  ⪼  {}%</code>
<b>- ساعات الداينو المتبقية لك هذا الشهر :</b>
    •  <code>{}ساعة  {}دقيقه  ⪼  {}%</code>
"""
usage_text = """
<b>ᯓ <a href = https//t.me/ZThon>𝗭𝗧𝗵𝗼𝗻 𝗛𝗲𝗿𝗼𝗸𝘂 🌐 استخـدام هيـروكـو</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔ وقت التشغيـل 🖥️</b>
<b>• التطبيـق :</b> <code>{}</code>
<b>• النظـام :</b> <code>{}</code>

<b>⌔ استخدام البيانات 📊</b>
<b>• الرفـع :</b> <code>{}</code>
<b>• التحميـل :</b> <code>{}</code>

<b>⌔ مساحة القرص 💾</b>
<b>• الكليـه :</b> <code>{}</code>
<b>• المستخدمـه :</b> <code>{}</code>
<b>• المتبقيـه :</b> <code>{}</code>

<b>⌔ استخدام الذاكرة 📈</b>
<b>• المعالـج :</b> <code>{}</code>
<b>• الـرام :</b> <code>{}</code>
<b>• القـرص :</b> <code>{}</code>
<b>• التبديـل :</b> <code>{}</code>
"""
info_text = """
<b>ᯓ <a href = https//t.me/ZThon>𝗭𝗧𝗵𝗼𝗻 𝗛𝗲𝗿𝗼𝗸𝘂 🌐 معلومـات هيـروكـو</a> </b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔ معلومـات حسـاب هيـروكـو 🚹:</b>
<b>• الاسـم ⤎ </b> <code>{}</code>
<b>• البريـد ⤎ </b> <code>{}</code>
<b>• تاريـخ الإنشـاء ⤎ </b> <code>{}</code>
<b>• آخـر دخـول ⤎ </b> <code>{}</code>
<b>• آخـر تحـديث ⤎ </b> <code>{}</code>
<b>• التـوثيـق ⤎ </b> {}

<b>⌔ معلومـات تطبيـق هيروكـو الخـاص بـك 🅿️:</b>
<b>• اسـم التطبيـق ⤎ </b> <code>{}</code>
<b>• رابـط التطبيـق ⤎ </b> <a href = {}>اضغـط هنـا</a>
<b>• تاريـخ الإنشـاء ⤎ </b> <code>{}</code>
<b>• آخـر تحـديث ⤎ </b> <code>{}</code>
<b>• التيـم ⤎ </b> {}
<b>• السيـرفـر ⤎ </b> {}
<b>• نظـام التشغيـل ⤎ </b> {}
<b>• نـوع الداينـو ⤎ </b> {}
"""


@zedub.zed_cmd(pattern="استخدامي$")
async def _(zelzal):
    yy = await edit_or_reply(zelzal, "**⌔ جـارِ جلـب المعلومـات . . .**")
    if hk.is_heroku:
        usage = default_usage() + await heroku_usage()
    else:
        usage = default_usage()
    await edit_or_reply(yy, usage, parse_mode="html")


@zedub.zed_cmd(pattern="(هيروكو|حسابي)$")
async def _(zelzal):
    yy = await edit_or_reply(zelzal, "**⌔ جـارِ جلـب المعلومـات . . .**")
    if not hk.api:
        return await edit_or_reply(yy, "**⎉╎اضبط فـار مفتـاح هيروكـو\n⎉╎الشـرح هنـا\nhttps://t.me/heroku_error/31**")
    if not hk.name:
        return await edit_or_reply(yy, "**⎉╎اضبط فـار اسـم تطبيـق هيروكـو\n⎉╎الشـرح هنـا\nhttps://t.me/heroku_error/31\n⎉╎نفـس الطريقـه لـكن للفـار HEROKU_APP_NAME**")
    try:
        conn = hk.heroku()
        app = conn.app(hk.name)
    except Exception as err:
        return await edit_or_reply(yy, err, parse_mode="html")
    account = json.dumps(to_dict(conn.account()), indent=1, default=str)
    capp = json.dumps(to_dict(app.info), indent=1, default=str)
    dyno = json.dumps(to_dict(app.dynos()), indent=1, default=str)
    addons = json.dumps(to_dict(app.addons()), indent=1, default=str)
    buildpacks = json.dumps(to_dict(app.buildpacks()), indent=1, default=str)
    configs = json.dumps(app.config().to_dict(), indent=1, default=str)
    account_info = json.loads(account)
    acc_name = account_info["name"]
    acc_email = account_info["email"]
    acc_cd = account_info["created_at"]
    acc_log = account_info["last_login"]
    acc_up = account_info["updated_at"]
    acc_vd = account_info["verified"]
    if acc_vd == True:
        acc_vd = "☑️"
    else:
        acc_vd = "✖️"
    app_info = json.loads(capp)
    name_app = app_info["name"]
    owner_email = app_info["owner"]["email"]
    web_url = app_info["web_url"]
    created_at = app_info["created_at"]
    released_at = app_info["released_at"]
    team_is = app_info["team"]
    if team_is is None:
        team_name = "لايوجـد"
    else:
        team_name = app_info["team"]
    name_reg = app_info["region"]["name"]
    if name_reg == "us":
        name_region = "الولايـات المتحـدة 🇺🇸"
    else:
        name_region = "اوروبـا 🇪🇺"
    stack_app = app_info["stack"]["name"]
    dyno_info = json.loads(dyno)
    dyno_is = dyno_info[0]["size"]
    if dyno_is == "Basic":
        dyno_size = "أسـاسـي"
    elif dyno_is == "Eco" or dyno_is == "eco":
        dyno_size = "إيكـو"
    else:
        dyno_size = "إحتـرافـي"
    zelzal_heroku = info_text.format(acc_name, acc_email, acc_cd, acc_log, acc_up, acc_vd, name_app, web_url, created_at, released_at, team_name, name_region, stack_app, dyno_size)
    await asyncio.sleep(1)
    await zedub.send_file(zelzal.chat_id, zz_pic, caption=zelzal_heroku, parse_mode="html")
    await yy.delete()

def default_usage() -> str:
    import psutil
    uptime = get_readable_time((time.time() - StartTime))
    try:
        UPLOAD = humanbytes(psutil.net_io_counters().bytes_sent)
    except BaseException:
        UPLOAD = 0
    try:
        DOWN = humanbytes(psutil.net_io_counters().bytes_recv)
    except BaseException:
        DOWN = 0
    try:
        workdir = psutil.disk_usage(".")
        TOTAL = humanbytes(workdir.total)
        USED = humanbytes(workdir.used)
        FREE = humanbytes(workdir.free)
    except BaseException:
        TOTAL = 0
        USED = 0
        FREE = 0
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = "{}GHz".format(round(cpu_freq / 1000, 2))
        else:
            cpu_freq = "{}MHz".format(round(cpu_freq, 2))
        CPU = "{}% ({}) {}".format(psutil.cpu_percent(), psutil.cpu_count(), cpu_freq)
    except BaseException:
        try:
            CPU = "{}%".format(psutil.cpu_percent())
        except BaseException:
            CPU = "0%"
    try:
        RAM = "{}%".format(psutil.virtual_memory().percent)
    except BaseException:
        RAM = "0%"
    try:
        DISK = "{}%".format(psutil.disk_usage("/").percent)
    except BaseException:
        DISK = "0%"
    try:
        swap = psutil.swap_memory()
        SWAP = "{} | {}%".format(humanbytes(swap.total), swap.percent or 0)
    except BaseException:
        SWAP = "0 | 0%"
    return usage_text.format(
        uptime,
        datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        UPLOAD,
        DOWN,
        TOTAL,
        USED,
        FREE,
        CPU,
        RAM,
        DISK,
        SWAP,
    )


async def heroku_usage() -> str:
    try:
        conn = hk.heroku()
        user = conn.account().id
        app = conn.app(hk.name)
    except Exception as err:
        return f"<b>ERROR:</b>\n<code>{err}</code>"
    USERAGENTS = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": choice(USERAGENTS),
        "Authorization": f"Bearer {hk.api}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    url = f"https://api.heroku.com/accounts/{user}/actions/get-quota"
    res = await Fetch(url, headers=headers, re_json=True)
    if not res:
        return "<code>Try again now!</code>"
    if app.region.name == "us":
        name_region = "الولايـات المتحـدة 🇺🇸"
    else:
        name_region = "اوروبـا 🇪🇺"
    quota = res["account_quota"]
    quota_used = res["quota_used"]
    remaining_quota = quota - quota_used
    percentage = floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = floor(minutes_remaining / 60)
    minutes = floor(minutes_remaining % 60)
    Apps = res["apps"]
    try:
        Apps[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = Apps[0]["quota_used"] / 60
        AppPercentage = floor(Apps[0]["quota_used"] * 100 / quota)
    AppHours = floor(AppQuotaUsed / 60)
    AppMinutes = floor(AppQuotaUsed % 60)
    return dyno_text.format(
        app.name,
        app.stack.name,
        name_region,
        app.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        app.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        mask_email(app.owner.email),
        AppHours,
        AppMinutes,
        AppPercentage,
        hours,
        minutes,
        percentage,
    )

