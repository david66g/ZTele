import requests
import random
import asyncio
import os
import sys
import time
import re
import logging
from time import sleep
from asyncio.exceptions import CancelledError
import telethon
from telethon import events, functions, types, Button
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.utils import get_display_name
from telethon.errors import FloodWaitError
from collections import deque
from telethon import functions
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, UserNotMutualContactError, UserPrivacyRestrictedError, YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.contacts import BlockRequest as bloock
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import KeyboardButton, ReplyKeyboardMarkup

from . import zedub
from ..Config import Config
from ..sql_helper import global_collectionjson as sql
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import reply_id

estithmar = False
ratp = False
thifts = False
bahsees = False

ZelzalCoins_cmd = (
    "[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - اوامـر تجميـع النقـاط](t.me/ZThon) .\n"
    "**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
    "**⎉╎اوامـر تجميـع نقـاط تمـويـل الخاصـه بسـورس زدثـــون ♾ :**\n\n"
    "`.المليار`  /  `.ايقاف المليار`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @EEOBot ) .. تلقـائيـاً ✓**\n\n"
    "`.العرب`  /  `.ايقاف العرب`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @xnsex21bot ) .. تلقـائيـاً ✓**\n\n"
    "`.الجوكر`  /  `.ايقاف الجوكر`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @A_MAN9300BOT ) .. تلقـائيـاً ✓**\n\n"
    "`.العقاب`  /  `.ايقاف العقاب`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @MARKTEBOT ) .. تلقـائيـاً ✓**\n\n"
    "`.المليون`  /  `.ايقاف المليون`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @qweqwe1919bot ) .. تلقـائيـاً ✓**\n\n"
    "`.برليون`  /  `.ايقاف برليون`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @Burllionbot ) .. تلقـائيـاً ✓**\n\n"
    "`.تناهيد`  /  `.ايقاف تناهيد`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @Ncoe_bot ) .. تلقـائيـاً ✓**\n\n"
    "`.اليمن`  /  `.ايقاف اليمن`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @srwry2bot ) .. تلقـائيـاً ✓**\n\n"
    "`.مهدويون`  /  `.ايقاف مهدويون`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @MHDN313bot ) .. تلقـائيـاً ✓**\n\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "**⎉╎قـائمـة بوتـات تمـويـل آخـرى تختلف عن البقيـه ♾ :** \n\n"
    "`.دعمكم`  /  `.ايقاف دعمكم`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @DamKomBot ) .. تلقـائيـاً ✓**\n\n"
    "`.نيزوكي`  /  `.ايقاف نيزوكي`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @FF4BOT ) .. تلقـائيـاً ✓**\n\n"
    "`.هايبر`  /  `.ايقاف هايبر`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت ( @ihyberbot ) .. تلقـائيـاً ✓**\n\n"
    "`.تجميع`  /  `.ايقاف تجميع`\n"
    "**⪼ لـ تجميـع النقـاط مـن البـوت المضاف لـ الفـارات .. تلقـائيـاً ✓**\n\n"
    "`.بوت التجميع`\n"
    "**⪼ لـ عـرض بوت التجميـع المضـاف لـ الفـارات ..**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "**⎉╎قـائمـة اوامــر اضافـات التجميـع الجديـدة حصريـاً ♾ :** \n\n"
    "`.لانهائي المليار` / `.لانهائي الجوكر` / `.لانهائي العقاب` / `.لانهائي العرب` / `.لانهائي المليون` / `.لانهائي برليون` / `.لانهائي تناهيد` / `.لانهائي اليمن` / `.لانهائي_دعمكم` / `.لانهائي_نيزوكي`\n"
    "**⪼ لـ تجميـع النقـاط مـن البـوت بـدون تـوقـف (لانهـائـي ♾) .. تلقـائيـاً ✓**\n\n"
    "`.اضف فار ثواني لانهائي` **بالـرد ع عـدد** / `.جلب فار ثواني لانهائي` / `.حذف فار ثواني لانهائي`\n"
    "**⪼ لـ تغييـر عـدد الثواني بين كل عملية تجميـع النقـاط لانهائـي بدلاً من الثوانـي الافتراضيـه (3600 ♾) ثانيـه ..✓**\n\n"
    "`.هدية المليار` / `.هدية الجوكر` / `.هدية العقاب` / `.هدية دعمكم` / `.هدية العرب` / `.هدية المليون` / `.هدية هايبر` / `.هدية برليون` / `.هدية تناهيد` / `.هدية اليمن` / `.هدية مهدويون` / `.هدية نيزوكي`\n"
    "**⪼ لـ تجميـع نقـاط الهديـة اليوميـة مـن البـوتات ..**\n\n"
    "`.نقاط المليار` / `.نقاط الجوكر` / `.نقاط العقاب` / `.نقاط دعمكم` / `.نقاط العرب` / `.نقاط المليون` / `.نقاط هايبر` / `.نقاط برليون` / `.نقاط تناهيد` / `.نقاط اليمن` / `.نقاط مهدويون` / `.نقاط نيزوكي`\n"
    "**⪼ لـ عـرض ومعرفـة عـدد النقـاط فـي البـوت ..**\n\n"
    "`.تحويل المليار` / `.تحويل الجوكر` / `.تحويل العقاب` / `.تحويل العرب` / `.تحويل المليون` / `.تحويل هايبر` / `.تحويل برليون` / `.تحويل تناهيد` / `.تحويل اليمن` / `.تحويل مهدويون` / `.تحويل نيزوكي`\n"
    "**⪼ الامـر + عـدد النقـاط لـ الشخـص المـراد تحويـل النقـاط اليـه**\n"
    "**⪼ لـ تحويـل النقـاط مـن حسابـك في البـوت الى شخـص عبـر عـدد النقـاط ..**\n\n"
    "`.تحويل دعمكم`\n"
    "**⪼ الامـر + ايـدي الشخـص + عـدد النقـاط لـ الشخـص المـراد تحويـل النقـاط اليـه**\n\n"
    "`.تحويل كود دعمكم`\n"
    "**⪼ الامـر + عـدد النقـاط المـراد تحويـلهـا الى كـود شحـن نقـاط**\n\n"
    "`.كود دعمكم` / `.كود هايبر`\n"
    "**⪼ الامـر + الكـود المـراد فحصـه**\n"
    "**⪼ لـ كشـط الكـود والحصـول علـى نقـاط الكـود .. تلقـائيـاً ✓**\n\n\n"
    "**- مـلاحظــه :**\n"
    "- سيتم اضـافـه المزيـد من المميـزات بالتحديثـات الجايـه ...\n"
    "\n𓆩 [𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁](t.me/ZThon) 𓆪"
)

ZelzalWaad_cmd = (
    "[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 -  اوامـر نقـاط الالعـاب](t.me/ZThon) .\n"
    "**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n\n"
    "**⎉╎قـائمـة اوامـر تجميـع نقـاط العـاب بـوت وعـد ♾ :** \n\n"
    "`.بخشيش وعد`\n"
    "`.راتب وعد`\n"
    "`.استثمار وعد`\n"
    "`.كلمات وعد`\n"
    "**⪼ لـ تجميـع نقـاط العـاب في بوت وعـد تلقائيـاً ✓ ..قم بـ اضافة البوت في مجموعة جديدة ثم ارسل**\n"
    "**الامـر + عـدد الاعـادة للامـر**\n"
    "**⪼ مثــال :**\n"
    "`.راتب وعد 50`\n\n"
    "\n𓆩 [𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁](t.me/ZThon) 𓆪"
)

bot_username0 = '@EEObot'
bot_username1 = '@A_MAN9300BOT'
bot_username2 = '@MARKTEBOT'
bot_username3 = '@xnsex21bot'
bot_username4 = '@Burllionbot'
bot_username5='@cn2bot'
bot_username6='@ihyberbot'
bot_username7='@YY8BoT'
bot_username8 = '@DamKomBot'
bot_username9 = '@qweqwe1919bot'
bot_usernamee1 = '@Ncoe_bot'
bot_usernamee2 = '@srwry2bot'
bot_usernamee3 = '@MHDN313bot'
bot_usernamee0 = '@FF4BOT'

@zedub.zed_cmd(pattern="(ايقاف المليار|ايقاف مليار)$")
async def _(event):
    await zedub(bloock(bot_username0))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع المليار .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف الجوكر|ايقاف جوكر)$")
async def _(event):
    await zedub(bloock(bot_username1))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع الجوكر .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف العرب|ايقاف عرب)$")
async def _(event):
    await zedub(bloock(bot_username3))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع العرب .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف العقاب|ايقاف الجنرال)$")
async def _(event):
    await zedub(bloock(bot_username2))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع العقاب .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف البرليون|ايقاف برليون)$")
async def _(event):
    await zedub(bloock(bot_username4))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع البرليون .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف المليون|ايقاف مليون)$")
async def _(event):
    await zedub(bloock(bot_username9))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع المليون .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف الهايبر|ايقاف هايبر)$")
async def _(event):
    await zedub(bloock(bot_username6))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع الهايبر .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف دعمكم|ايقاف دعمكمم)$")
async def _(event):
    await zedub(bloock(bot_username8))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع دعمكم .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف تناهيد|ايقاف التناهيد)$")
async def _(event):
    await zedub(bloock(bot_usernamee1))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع تناهيد .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف اليمن|ايقاف يمن)$")
async def _(event):
    await zedub(bloock(bot_usernamee2))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع اليمن .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف مهدويون|ايقاف المهدويون)$")
async def _(event):
    await zedub(bloock(bot_usernamee3))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع مهدويون .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف نيزوكي|ايقاف النيزوكي)$")
async def _(event):
    await zedub(bloock(bot_usernamee0))
    return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع نيزوكي .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(ايقاف تجميع|ايقاف التجميع)$")
async def _(event):
    zpoint = gvarstatus("Z_Point")
    if gvarstatus("Z_Point") is None:
        await edit_or_reply(event, "**⎉╎لايوجـد بوت تجميع مضاف بعـد ؟!**\n\n**⎉╎لـ اضافة بوت تجميع جديد**\n**⎉╎ارسـل**  `.اضف بوت التجميع`  **بالـرد ع معـرف البـوت**")
    else:
        await edit_or_reply(event, f"**⎉╎تم إيقـاف تجميـع من البـوت {zpoint} .. بنجـاح☑️**")

@zedub.zed_cmd(pattern="(بوت المليار|بوت مليار)$")
async def _(event):
    await edit_or_reply(event, "@EEOBot")


@zedub.zed_cmd(pattern="(المليار|تجميع المليار)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username0}**")
    try:
        channel_entity = await zedub.get_entity(bot_username0)
        await zedub.send_message(bot_username0, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username0))
        channel_entity = await zedub.get_entity(bot_username0)
        await zedub.send_message(bot_username0, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username0, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username0, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username0, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username0, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username0, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username0, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username0, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username0, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username0, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username0, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username0, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username0, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username0, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username0, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username0, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username0, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username0, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username0, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username0))


@zedub.zed_cmd(pattern="بوت العرب$")
async def _(event):
    await edit_or_reply(event, bot_username3)

@zedub.zed_cmd(pattern="(العرب|تجميع العرب)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username3}**")
    try:
        channel_entity = await zedub.get_entity(bot_username3)
        await zedub.send_message(bot_username3, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username3))
        channel_entity = await zedub.get_entity(bot_username3)
        await zedub.send_message(bot_username3, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username3, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username3, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username3, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username3, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username3, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username3, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username3, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username3, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username3, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username3, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username3, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username3, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username3, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username3, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username3, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username3, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username3, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username3, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username3))


@zedub.zed_cmd(pattern="بوت التجميع$")
async def _(event):
    zpoint = gvarstatus("Z_Point")
    if gvarstatus("Z_Point") is None:
        await edit_or_reply(event, "**⎉╎لايوجـد بوت تجميع مضاف بعـد ؟!**\n\n**⎉╎لـ اضافة بوت تجميع جديد**\n**⎉╎ارسـل**  `.اضف بوت التجميع`  **بالـرد ع معـرف البـوت**")
    else:
        await edit_or_reply(event, f"**⎉╎بوت التجميـع المضـاف حاليـاً**\n**⎉╎هـو** {zpoint}")


@zedub.zed_cmd(pattern="تجميع(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zpoint = gvarstatus("Z_Point")
    if con in ("مليار", "الجوكر", "الجنرال", "العقاب", "المليون", "هايبر", "برليون", "العرب", "دعمكم", "المليار"):
        return await edit_or_reply(event, "**⎉╎عـذراً .. عـزيـزي امـر خاطـئ .\n⎉╎لـ رؤيـة اوامـر التجميـع ارسـل**\n\n`.اوامر التجميع`")
    if gvarstatus("Z_Point") is None:
        return await edit_or_reply(event, "**⎉╎لايوجـد بـوت تجميـع مضـاف للفـارات ؟!\n⎉╎لـ اضافة بـوت تجميـع\n⎉╎ارسـل** `.اضف بوت التجميع` **بالـرد ع معـرف البـوت\n\n⎉╎او استخـدم امر تجميع** `.مليار`")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {zpoint} .**")
    try:
        channel_entity = await zedub.get_entity(zpoint)
        await zedub.send_message(zpoint, '/start')
    except YouBlockedUserError:
        await zedub(unblock(zpoint))
        channel_entity = await zedub.get_entity(zpoint)
        await zedub.send_message(zpoint, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(zpoint, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(zpoint, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(zpoint, '/start')  # إعادة إرسال "/start"
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(zpoint, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(zpoint, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(zpoint, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(zpoint, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(zpoint, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(zpoint, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(zpoint, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(zpoint, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(zpoint, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(zpoint, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(zpoint, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(zpoint, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(zpoint, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(zpoint, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(zpoint, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(zpoint))


@zedub.zed_cmd(pattern="بوت الجوكر$")
async def _(event):
    await edit_or_reply(event, bot_username1)


@zedub.zed_cmd(pattern="(الجوكر|تجميع الجوكر)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username1}**")
    try:
        channel_entity = await zedub.get_entity(bot_username1)
        await zedub.send_message(bot_username1, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username1))
        channel_entity = await zedub.get_entity(bot_username1)
        await zedub.send_message(bot_username1, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username1, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username1, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username1, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username1, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username1, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username1, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username1, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username1, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username1, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username1, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username1, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username1, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username1, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username1, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username1, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username1, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username1, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username1, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username1))


@zedub.zed_cmd(pattern="بوت الجنرال$")
async def _(event):
    await edit_or_reply(event, bot_username2)


@zedub.zed_cmd(pattern="(الجنرال|تجميع الجنرال)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username2}**")
    try:
        channel_entity = await zedub.get_entity(bot_username2)
        await zedub.send_message(bot_username2, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username2))
        channel_entity = await zedub.get_entity(bot_username2)
        await zedub.send_message(bot_username2, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username2, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username2, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username2, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username2, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username2, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username2))


@zedub.zed_cmd(pattern="بوت العقاب$")
async def _(event):
    await edit_or_reply(event, bot_username2)


@zedub.zed_cmd(pattern="(العقاب|تجميع العقاب)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username2}**")
    try:
        channel_entity = await zedub.get_entity(bot_username2)
        await zedub.send_message(bot_username2, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username2))
        channel_entity = await zedub.get_entity(bot_username2)
        await zedub.send_message(bot_username2, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username2, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username2, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username2, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username2, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username2, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username2, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username2))


@zedub.zed_cmd(pattern="بوت المليون$")
async def _(event):
    await edit_or_reply(event, bot_username9)


@zedub.zed_cmd(pattern="(المليون|تجميع المليون)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username9}**")
    try:
        channel_entity = await zedub.get_entity(bot_username9)
        await zedub.send_message(bot_username9, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username9))
        channel_entity = await zedub.get_entity(bot_username9)
        await zedub.send_message(bot_username9, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username9, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username9, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username9, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username9, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username9, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username9, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username9, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username9, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username9, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username9, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username9, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username9, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username9, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username9, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username9, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username9, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username9, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username9, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username9))


@zedub.zed_cmd(pattern="بوت هايبر$")
async def _(event):
    await edit_or_reply(event, bot_username6)

# Copyright (C) 2023 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="(هايبر|تجميع هايبر)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    await edit_or_reply(event, "**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه @ihyberbot**")
    try:
        channel_entity = await zedub.get_entity(bot_username6)
        await zedub.send_message(bot_username6, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username6))
        channel_entity = await zedub.get_entity(bot_username6)
        await zedub.send_message(bot_username6, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username6, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0= await zedub.get_messages(bot_username6, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username6, '/start')  # إعادة إرسال "/start"
    await msg0[0].click(0)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username6, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(4)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username6, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username6, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username6, limit=1)
            await msg0[0].click(0)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username6, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username6, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username6, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username6, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username6, limit=1)
            await msg0[0].click(0)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username6, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username6, limit=1)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username6, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username6, limit=1)
            await msg0[0].click(0)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username6, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username6, limit=1)
            await msg2[0].click(1)
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
        except:
            msg2 = await zedub.get_messages(bot_username6, limit=1)
            await msg2[0].click(2)
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username6))


@zedub.zed_cmd(pattern="بوت برليون$")
async def _(event):
    await edit_or_reply(event, bot_username4)

# Copyright (C) 2023 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="(برليون|تجميع برليون)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_username4}**")
    try:
        channel_entity = await zedub.get_entity(bot_username4)
        await zedub.send_message(bot_username4, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username4))
        channel_entity = await zedub.get_entity(bot_username4)
        await zedub.send_message(bot_username4, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username4, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username4, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username4, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username4, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username4, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username4, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username4, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username4, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username4, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username4, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username4, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username4, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username4, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_username4, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username4, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username4, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_username4, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_username4, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username4))


@zedub.zed_cmd(pattern="بوت دعمكم$")
async def _(event):
    await edit_or_reply(event, bot_username8)


@zedub.zed_cmd(pattern="(دعمكم|تجميع دعمكم)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, "**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه @DamKomBot**")
    try:
        channel_entity = await zedub.get_entity(bot_username8)
        await zedub.send_message(bot_username8, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username8))
        channel_entity = await zedub.get_entity(bot_username8)
        await zedub.send_message(bot_username8, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_username8, limit=1)
    for _ in range(30):
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username8, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username8, '/start')
        elif "الاشتراك بقنوات" in mss or "الاشتراك في قنوات" in mss or "الاشتراك في قنوات" in mss or "اشترك بالقنوات" in mss or "الاشتراك في القنوات" in mss or "الاشتراك في القنوات" in mss or "الأشتراك بقنوات" in mss or "الأشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الاشتراك بالقنوات" in mss:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[0]
            try:
                if msgs.reply_markup:
                    for i, row in enumerate(msgs.reply_markup.rows):
                        if row.buttons:
                            button = row.buttons[0]
                            url = msgs.reply_markup.rows[i].buttons[0].url
                            chname = msgs.reply_markup.rows[i].buttons[0].text
                            chnum = i+1
                            if "تحقق" in chname:
                                await zedub.send_message(bot_username8, '/start')
                                break
                            try:
                                try:
                                    await zedub(JoinChannelRequest(url))
                                except:
                                    bott = url.split('/')[-1]
                                    await zedub(ImportChatInviteRequest(bott))
                                msg2 = await zedub.get_messages(bot_username8, limit=1)
                                #await msg2[0].click(text='تحقق ✅')
                                await zzz.edit(f"**⎉╎تم الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. بنجاح ✓**")
                                await asyncio.sleep(2)
                                #await zedub.send_message(bot_username8, '/start')
                            except:
                                await zzz.edit(f"**⎉╎فشل الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. يمكن تبندت 🥲\n**⎉╎لذلك تم تخطيها .. بنجاح ✓**")
                                #await zedub.send_message(bot_username8, '/start')
                else:
                    await zedub.send_message(bot_username8, '/start')
                    break
            except AttributeError:
                await zedub.send_message(bot_username8, '/start')
        else:
            #await zedub.send_message(bot_username8, '/start')
            break
    await msg0[0].click(1)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_username8, limit=1)
    await msg1[0].click(1)
    chs = 1
    for i in range(100):
        await asyncio.sleep(4)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات حالياً 🤍') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_username8, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_username8, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username8, limit=1)
            await msg0[0].click(1)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username8, limit=1)
            await msg1[0].click(1)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username8, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username8, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_username8, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_username8, limit=1)
            await msg0[0].click(1)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_username8, limit=1)
            await msg1[0].click(1)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_username8, limit=1)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        msg_text = msgs.message
        if "عليك الاشتراك بقناة البوت" in msg_text:
            the_channnel = msg_text.split('@')[1].split()[0]
            try:
                entity = await zedub.get_entity(the_channnel)
                if entity:
                    await zedub(JoinChannelRequest(entity.id))
                    await asyncio.sleep(4)
                    await zedub.send_message(bot_username8, '/start')
                    await asyncio.sleep(4)
                    msg0 = await zedub.get_messages(bot_username8, limit=1)
                    await msg0[0].click(1)
                    await asyncio.sleep(4)
                    msg1 = await zedub.get_messages(bot_username8, limit=1)
                    await msg1[0].click(0)
            except:
                continue
        if "اشترك فالقناة @" in msg_text:
            the_channel = msg_text.split('@')[1].split()[0]
            try:
                entity = await zedub.get_entity(the_channel)
                if entity:
                    await zedub(JoinChannelRequest(entity.id))
                    await asyncio.sleep(4)
                    msg2 = await zedub.get_messages(bot_username8, limit=1)
                    await msg2[0].click(text='اشتركت ✅')
                    chs += 1
                    await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            except:
                continue

    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_username8))


@zedub.zed_cmd(pattern="(بوت التناهيد|بوت تناهيد)$")
async def _(event):
    await edit_or_reply(event, "@Ncoe_bot")

@zedub.zed_cmd(pattern="(تناهيد|تجميع تناهيد)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_usernamee1}**")
    try:
        channel_entity = await zedub.get_entity(bot_usernamee1)
        await zedub.send_message(bot_usernamee1, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee1))
        channel_entity = await zedub.get_entity(bot_usernamee1)
        await zedub.send_message(bot_usernamee1, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_usernamee1, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_usernamee1, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee1, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_usernamee1, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_usernamee1, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee1, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_usernamee1, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_usernamee1, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_usernamee1, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee1, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_usernamee1, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_usernamee1))


@zedub.zed_cmd(pattern="(بوت اليمن|بوت يمن)$")
async def _(event):
    await edit_or_reply(event, "@srwry2bot")

@zedub.zed_cmd(pattern="(اليمن|تجميع اليمن)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_usernamee2}**")
    try:
        channel_entity = await zedub.get_entity(bot_usernamee2)
        await zedub.send_message(bot_usernamee2, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee2))
        channel_entity = await zedub.get_entity(bot_usernamee2)
        await zedub.send_message(bot_usernamee2, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_usernamee2, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_usernamee2, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee2, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_usernamee2, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_usernamee2, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_usernamee2, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_usernamee2, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_usernamee2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee2, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_usernamee2, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_usernamee2))


@zedub.zed_cmd(pattern="(مهدويون|تجميع مهدويون)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    if con == "ايقاف":
        return await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_usernamee3}**")
    try:
        channel_entity = await zedub.get_entity(bot_usernamee3)
        await zedub.send_message(bot_usernamee3, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee3))
        channel_entity = await zedub.get_entity(bot_usernamee3)
        await zedub.send_message(bot_usernamee3, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_usernamee3, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_usernamee3, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee3, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_usernamee3, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_usernamee3, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee3, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_usernamee3, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(2)
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await msg2[0].click(text='استمرار التجميع')
            await asyncio.sleep(2)
            msg2 = await zedub.get_messages(bot_usernamee3, limit=1)
            mas = msg2[0].text
            await asyncio.sleep(4)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_usernamee3, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        try:
            url = msgs.reply_markup.rows[0].buttons[0].url
        except AttributeError:
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee3, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg0[0].click(2)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            await asyncio.sleep(2)
        except:
            msg2 = await zedub.get_messages(bot_usernamee3, limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await zzz.edit(f"**⎉╎القنـاة رقـم {chs} .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_usernamee3))



@zedub.zed_cmd(pattern="نقاط هايبر(?: |$)(.*)")
async def ZelzalStart(event):
    zzz = await edit_or_reply(event, "**⎉╎جـارِ جمـع المعلومـات مـن بـوت هايبر ...✓**")
    try:
        send = await zedub.send_message(bot_username6, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username6))
        send = await zedub.send_message(bot_username6, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username6, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username6, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username6, '/start')
    await msg1[0].click(4)
    sleep(2)
    msg = await zedub.get_messages(boto, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(boto))


@zedub.zed_cmd(pattern="نقاط (.*)")
async def ZelzalStart(event):
    malak = event.pattern_match.group(1)
    if malak == "مليار" or malak == "المليار":
        boto = '@EEObot'
    elif malak == "الجوكر" or malak == "جوكر":
        boto = '@A_MAN9300BOT'
    elif malak == "العقاب" or malak == "عقاب" or malak == "الجنرال" or malak == "جنرال":
        boto = '@MARKTEBOT'
    elif malak == "المليون" or malak == "مليون":
        boto = '@qweqwe1919bot'
    elif malak == "عرب" or malak == "العرب":
        boto = '@xnsex21bot'
    elif malak == "برليون" or malak == "البرليون":
        boto = '@Burllionbot'
    elif malak == "تناهيد" or malak == "التناهيد":
        boto = '@Ncoe_bot'
    elif malak == "اليمن" or malak == "تمويل اليمن":
        boto = '@srwry2bot'
    elif malak == "مهدويون" or malak == "مهدويين" or malak == "مهدوين":
        boto = '@MHDN313bot'
    elif malak == "دعمكم" or malak == "هايبر" or malak == "نيزوكي":
        return
    else:
        return await edit_or_reply(event, "**⎉╎عـذراً الامـر خاطـئ ♾ ؟!\n⎉╎ارسـل (.اوامر النقاط) لعـرض الاوامـر**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ جمـع المعلومـات مـن بـوت {boto} ...✓**")
    try:
        send = await zedub.send_message(boto, '/start')
    except YouBlockedUserError:
        await zedub(unblock(boto))
        send = await zedub.send_message(boto, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(boto, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(boto, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(boto, '/start')
    await msg1[0].click(5)
    sleep(2)
    msg = await zedub.get_messages(boto, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(boto))


@zedub.zed_cmd(pattern="تحويل دعمكم (.*) (.*)")
async def ZelzalStart(event):
    pt = event.pattern_match.group(1)
    pt1= event.pattern_match.group(2) 
    zzz = await edit_or_reply(event, "**⎉╎جـارِ تحويـل النقـاط مـن بـوت دعمكـم ...✓**")
    try:
        send = await zedub.send_message(bot_username8, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username8))
        send = await zedub.send_message(bot_username8, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username8, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username8, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username8, '/start')
    await msg1[0].click(4)
    sleep(4)
    msgt = await zedub.get_messages(bot_username8, limit=1)
    await msgt[0].click(0)
    sleep(4)
    await zedub.send_message(bot_username8, pt)
    sleep(4)
    await zedub.send_message(bot_username8, pt1)
    sleep(4)
    msg = await zedub.get_messages(bot_username8, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username8))


@zedub.zed_cmd(pattern="تحويل كود دعمكم (.*)")
async def ZelzalStart(event):
    pt = event.pattern_match.group(1)
    zzz = await edit_or_reply(event, "**⎉╎جـارِ تحويـل النقـاط مـن بـوت دعمكـم ...✓**")
    try:
        send = await zedub.send_message(bot_username8, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username8))
        send = await zedub.send_message(bot_username8, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username8, limit=1)
    for _ in range(30):
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username8, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username8, '/start')
        elif "الاشتراك بقنوات" in mss or "الاشتراك في قنوات" in mss or "الاشتراك في قنوات" in mss or "اشترك بالقنوات" in mss or "الاشتراك في القنوات" in mss or "الاشتراك في القنوات" in mss or "الأشتراك بقنوات" in mss or "الأشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الاشتراك بالقنوات" in mss:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[0]
            try:
                if msgs.reply_markup:
                    for i, row in enumerate(msgs.reply_markup.rows):
                        if row.buttons:
                            button = row.buttons[0]
                            url = msgs.reply_markup.rows[i].buttons[0].url
                            chname = msgs.reply_markup.rows[i].buttons[0].text
                            chnum = i+1
                            if "تحقق" in chname:
                                await zedub.send_message(bot_username8, '/start')
                                break
                            try:
                                try:
                                    await zedub(JoinChannelRequest(url))
                                except:
                                    bott = url.split('/')[-1]
                                    await zedub(ImportChatInviteRequest(bott))
                                msg2 = await zedub.get_messages(bot_username8, limit=1)
                                #await msg2[0].click(text='تحقق ✅')
                                await event.edit(f"**⎉╎تم الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. بنجاح ✓**")
                                await asyncio.sleep(2)
                                #await zedub.send_message(bot_username8, '/start')
                            except:
                                await event.edit(f"**⎉╎فشل الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. يمكن تبندت 🥲\n**⎉╎لذلك تم تخطيها .. بنجاح ✓**")
                                #await zedub.send_message(bot_username8, '/start')
                else:
                    await zedub.send_message(bot_username8, '/start')
                    break
            except AttributeError:
                await zedub.send_message(bot_username8, '/start')
        else:
            #await zedub.send_message(bot_username8, '/start')
            break
    await msg1[0].click(4)
    sleep(4)
    msgt = await zedub.get_messages(bot_username8, limit=1)
    await msgt[0].click(1)
    sleep(4)
    await zedub.send_message(bot_username8, pt)
    sleep(4)
    msg = await zedub.get_messages(bot_username8, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username8))


@zedub.zed_cmd(pattern="كود دعمكم (.*)")
async def ZelzalStart(event):
    pt = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, '**⎉╎جـارِ فحـص الكـود في بـوت دعمـكـم ...✓**')
    try:
        send = await zedub.send_message(bot_username8, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username8))
        send = await zedub.send_message(bot_username8, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username8, limit=1)
    for _ in range(30):
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username8, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username8, '/start')
        elif "الاشتراك بقنوات" in mss or "الاشتراك في قنوات" in mss or "الاشتراك في قنوات" in mss or "اشترك بالقنوات" in mss or "الاشتراك في القنوات" in mss or "الاشتراك في القنوات" in mss or "الأشتراك بقنوات" in mss or "الأشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الاشتراك بالقنوات" in mss:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[0]
            try:
                if msgs.reply_markup:
                    for i, row in enumerate(msgs.reply_markup.rows):
                        if row.buttons:
                            button = row.buttons[0]
                            url = msgs.reply_markup.rows[i].buttons[0].url
                            chname = msgs.reply_markup.rows[i].buttons[0].text
                            chnum = i+1
                            if "تحقق" in chname:
                                await zedub.send_message(bot_username8, '/start')
                                break
                            try:
                                try:
                                    await zedub(JoinChannelRequest(url))
                                except:
                                    bott = url.split('/')[-1]
                                    await zedub(ImportChatInviteRequest(bott))
                                msg2 = await zedub.get_messages(bot_username8, limit=1)
                                #await msg2[0].click(text='تحقق ✅')
                                await event.edit(f"**⎉╎تم الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. بنجاح ✓**")
                                await asyncio.sleep(2)
                                #await zedub.send_message(bot_username8, '/start')
                            except:
                                await event.edit(f"**⎉╎فشل الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. يمكن تبندت 🥲\n**⎉╎لذلك تم تخطيها .. بنجاح ✓**")
                                #await zedub.send_message(bot_username8, '/start')
                else:
                    await zedub.send_message(bot_username8, '/start')
                    break
            except AttributeError:
                await zedub.send_message(bot_username8, '/start')
        else:
            #await zedub.send_message(bot_username8, '/start')
            break
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_username8, pt)
    sleep(4)
    msg = await zedub.get_messages(bot_username8, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username8))


@zedub.zed_cmd(pattern="نقاط دعمكم$")
async def ZelzalStart(event):
    zzz = await edit_or_reply(event, '**⎉╎جـارِ حسـاب نقاطـك في بـوت دعمـكـم ...✓**')
    try:
        send = await zedub.send_message(bot_username8, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username8))
        send = await zedub.send_message(bot_username8, '/start')
    sleep(3)
    msg1 = await zedub.get_messages(bot_username8, limit=1)
    for _ in range(30):
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username8, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username8, '/start')
        elif "الاشتراك بقنوات" in mss or "الاشتراك في قنوات" in mss or "الاشتراك في قنوات" in mss or "اشترك بالقنوات" in mss or "الاشتراك في القنوات" in mss or "الاشتراك في القنوات" in mss or "الأشتراك بقنوات" in mss or "الأشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الاشتراك بالقنوات" in mss:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[0]
            try:
                if msgs.reply_markup:
                    for i, row in enumerate(msgs.reply_markup.rows):
                        if row.buttons:
                            button = row.buttons[0]
                            url = msgs.reply_markup.rows[i].buttons[0].url
                            chname = msgs.reply_markup.rows[i].buttons[0].text
                            chnum = i+1
                            if "تحقق" in chname:
                                await zedub.send_message(bot_username8, '/start')
                                break
                            try:
                                try:
                                    await zedub(JoinChannelRequest(url))
                                except:
                                    bott = url.split('/')[-1]
                                    await zedub(ImportChatInviteRequest(bott))
                                msg2 = await zedub.get_messages(bot_username8, limit=1)
                                #await msg2[0].click(text='تحقق ✅')
                                await event.edit(f"**⎉╎تم الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. بنجاح ✓**")
                                await asyncio.sleep(2)
                                #await zedub.send_message(bot_username8, '/start')
                            except:
                                await event.edit(f"**⎉╎فشل الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. يمكن تبندت 🥲\n**⎉╎لذلك تم تخطيها .. بنجاح ✓**")
                                #await zedub.send_message(bot_username8, '/start')
                else:
                    await zedub.send_message(bot_username8, '/start')
                    break
            except AttributeError:
                await zedub.send_message(bot_username8, '/start')
        else:
            #await zedub.send_message(bot_username8, '/start')
            break
    await msg1[0].click(2)
    sleep(4)
    msg = await zedub.get_messages(bot_username8, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username8))


@zedub.zed_cmd(pattern="هدية دعمكم$")
async def ZelzalStart(event):
    zzz = await edit_or_reply(event, '**⎉╎جـارِ جمـع الهديـه مـن بـوت دعمـكـم ...✓**')
    try:
        send = await zedub.send_message(bot_username8, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username8))
        send = await zedub.send_message(bot_username8, '/start')
    sleep(3)
    msg1 = await zedub.get_messages(bot_username8, limit=1)
    for _ in range(30):
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_username8, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username8, '/start')
        elif "الاشتراك بقنوات" in mss or "الاشتراك في قنوات" in mss or "الاشتراك في قنوات" in mss or "اشترك بالقنوات" in mss or "الاشتراك في القنوات" in mss or "الاشتراك في القنوات" in mss or "الأشتراك بقنوات" in mss or "الأشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الاشتراك بالقنوات" in mss:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[0]
            try:
                if msgs.reply_markup:
                    for i, row in enumerate(msgs.reply_markup.rows):
                        if row.buttons:
                            button = row.buttons[0]
                            url = msgs.reply_markup.rows[i].buttons[0].url
                            chname = msgs.reply_markup.rows[i].buttons[0].text
                            chnum = i+1
                            if "تحقق" in chname:
                                await zedub.send_message(bot_username8, '/start')
                                break
                            try:
                                try:
                                    await zedub(JoinChannelRequest(url))
                                except:
                                    bott = url.split('/')[-1]
                                    await zedub(ImportChatInviteRequest(bott))
                                msg2 = await zedub.get_messages(bot_username8, limit=1)
                                #await msg2[0].click(text='تحقق ✅')
                                await event.edit(f"**⎉╎تم الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. بنجاح ✓**")
                                await asyncio.sleep(2)
                                #await zedub.send_message(bot_username8, '/start')
                            except:
                                await event.edit(f"**⎉╎فشل الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. يمكن تبندت 🥲\n**⎉╎لذلك تم تخطيها .. بنجاح ✓**")
                                #await zedub.send_message(bot_username8, '/start')
                else:
                    await zedub.send_message(bot_username8, '/start')
                    break
            except AttributeError:
                await zedub.send_message(bot_username8, '/start')
        else:
            #await zedub.send_message(bot_username8, '/start')
            break
    await msg1[0].click(2)
    sleep(4)
    msg2 = await zedub.get_messages(bot_username8, limit=1)
    await msg2[0].click(1)
    sleep(4)
    msg = await zedub.get_messages(bot_username8, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username8))


@zedub.zed_cmd(pattern="هدية (.*)")
async def ZelzalStart(event): #by T.me/zzzzl1l
    malak = event.pattern_match.group(1)
    if malak == "مليار" or malak == "المليار":
        boto = '@EEObot'
    elif malak == "الجوكر" or malak == "جوكر":
        boto = '@A_MAN9300BOT'
    elif malak == "العقاب" or malak == "عقاب" or malak == "الجنرال" or malak == "جنرال":
        boto = '@MARKTEBOT'
    elif malak == "المليون" or malak == "مليون":
        boto = '@qweqwe1919bot'
    elif malak == "عرب" or malak == "العرب":
        boto = '@xnsex21bot'
    elif malak == "برليون" or malak == "البرليون":
        boto = '@Burllionbot'
    elif malak == "تناهيد" or malak == "التناهيد":
        boto = '@Ncoe_bot'
    elif malak == "اليمن" or malak == "تمويل اليمن":
        boto = '@srwry2bot'
    elif malak == "مهدويون" or malak == "مهدويين" or malak == "مهدوين":
        boto = '@MHDN313bot'
    elif malak == "دعمكم" or malak == "هايبر" or malak == "نيزوكي":
        return
    else:
        return await edit_or_reply(event, "**⎉╎عـذراً الامـر خاطـئ ♾ ؟!\n⎉╎ارسـل (.اوامر النقاط) لعـرض الاوامـر**")
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ جمـع الهديـه مـن بـوت {malak} ...✓**")
    try:
        send = await zedub.send_message(boto, '/start')
    except YouBlockedUserError:
        await zedub(unblock(boto))
        send = await zedub.send_message(boto, '/start')
    sleep(4)
    msg1 = await zedub.get_messages(boto, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(boto, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(boto, '/start')
    await msg1[0].click(6)
    sleep(4)
    msg = await zedub.get_messages(boto, limit=1)
    await msg[0].forward_to(event.chat_id)
    await zzz.delete()


@zedub.zed_cmd(pattern="تحويل المليار (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username0} ...✓**")
    try:
        send = await zedub.send_message(bot_username0, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username0))
        send = await zedub.send_message(bot_username0, '/start')
    await asyncio.sleep(2)
    msg1 = await zedub.get_messages(bot_username0, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username0, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username0, '/start')
    await msg1[0].click(3)
    await asyncio.sleep(4)
    await zedub.send_message(bot_username0, pts)
    await asyncio.sleep(4)
    msg = await zedub.get_messages(bot_username0, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username0))


@zedub.zed_cmd(pattern="تحويل الجوكر (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username1} ...✓**")
    try:
        send = await zedub.send_message(bot_username1, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username1))
        send = await zedub.send_message(bot_username1, '/start')
    await asyncio.sleep(2)
    msg1 = await zedub.get_messages(bot_username1, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username1, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username1, '/start')
    await msg1[0].click(3)
    await asyncio.sleep(4)
    await zedub.send_message(bot_username1, pts)
    await asyncio.sleep(4)
    msg = await zedub.get_messages(bot_username1, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username1))


@zedub.zed_cmd(pattern="تحويل العقاب (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username2} ...✓**")
    try:
        send = await zedub.send_message(bot_username2, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username2))
        send = await zedub.send_message(bot_username2, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username2, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username2, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username2, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_username2, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_username2, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username2))


@zedub.zed_cmd(pattern="تحويل الجنرال (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username2} ...✓**")
    try:
        send = await zedub.send_message(bot_username2, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username2))
        send = await zedub.send_message(bot_username2, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username2, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username2, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username2, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_username2, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_username2, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username2))


@zedub.zed_cmd(pattern="تحويل العرب (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username3} ...✓**")
    try:
        send = await zedub.send_message(bot_username3, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username3))
        send = await zedub.send_message(bot_username3, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username3, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username3, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username3, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_username3, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_username3, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username3))


@zedub.zed_cmd(pattern="تحويل برليون (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username4} ...✓**")
    try:
        send = await zedub.send_message(bot_username4, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username4))
        send = await zedub.send_message(bot_username4, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username4, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username4, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username4, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_username4, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_username4, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username4))


@zedub.zed_cmd(pattern="تحويل المليون (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username9} ...✓**")
    try:
        send = await zedub.send_message(bot_username9, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username9))
        send = await zedub.send_message(bot_username9, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_username9, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_username9, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_username9, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_username9, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_username9, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username9))

@zedub.zed_cmd(pattern="تحويل تناهيد (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_usernamee1} ...✓**")
    try:
        send = await zedub.send_message(bot_usernamee1, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee1))
        send = await zedub.send_message(bot_usernamee1, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_usernamee1, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_usernamee1, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee1, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_usernamee1, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_usernamee1, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_usernamee1))

@zedub.zed_cmd(pattern="تحويل اليمن (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_usernamee2} ...✓**")
    try:
        send = await zedub.send_message(bot_usernamee2, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee2))
        send = await zedub.send_message(bot_usernamee2, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_usernamee2, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_usernamee2, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee2, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_usernamee2, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_usernamee2, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_usernamee2))

@zedub.zed_cmd(pattern="تحويل مهدويون (.*)")
async def ZelzalStart(event):
    pts = event.pattern_match.group(1) 
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_usernamee3} ...✓**")
    try:
        send = await zedub.send_message(bot_usernamee3, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee3))
        send = await zedub.send_message(bot_usernamee3, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_usernamee3, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_usernamee3, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee3, '/start')
    await msg1[0].click(3)
    sleep(4)
    await zedub.send_message(bot_usernamee3, pts)
    sleep(4)
    msg = await zedub.get_messages(bot_usernamee3, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_usernamee3))


@zedub.zed_cmd(pattern="تحويل هايبر (.*)")
async def ZelzalStart(event):
       pts = event.pattern_match.group(1) 
       zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username6} ...✓**")
       try:
           send = await zedub.send_message(bot_username6, '/start')
       except YouBlockedUserError:
           await zedub(unblock(bot_username6))
           send = await zedub.send_message(bot_username6, '/start')
       sleep(2)
       msg1 = await zedub.get_messages(bot_username6, limit=1)
       for _ in range(7):
           await asyncio.sleep(1.5)
           msg1 = await zedub.get_messages(bot_username6, limit=1)
           mss = msg1[0].text
           if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
               link_pattern = re.compile(r'(https?://\S+|@\w+)')
               link = re.search(link_pattern, mss).group(1)
               if link.startswith('https://t.me/+'):
                   link = link.replace('https://t.me/+', '')
                   result = await zedub(ImportChatInviteRequest(link.strip()))
               elif link.startswith('@'):
                   get_entity_must_join = await zedub.get_entity(link)
                   result = await zedub(JoinChannelRequest(get_entity_must_join.id))
               else:
                   get_entity_must_join = await zedub.get_entity(link)
                   result = await zedub(JoinChannelRequest(get_entity_must_join.id))
               await asyncio.sleep(3)
               await zedub.send_message(bot_username6, '/start')
       await msg1[0].click(2)
       sleep(4)
       await zedub.send_message(bot_username6, pts)
       sleep(4)
       msg = await zedub.get_messages(bot_username6, limit=1)
       await msg[0].forward_to(event.chat_id)
       await asyncio.sleep(4)
       await zzz.delete()
       await zedub(bloock(bot_username6))


@zedub.zed_cmd(pattern="كود هايبر$")
async def ZelzalStart(event):
       pt = event.pattern_match.group(1) 
       zzz = await edit_or_reply(event, '**⎉╎جـارِ فحـص الكـود في بـوت هايبـر ...✓**')
       try:
           send = await zedub.send_message(bot_username6, '/start')
       except YouBlockedUserError:
           await zedub(unblock(bot_username6))
           send = await zedub.send_message(bot_username6, '/start')
       sleep(2)
       msg1 = await zedub.get_messages(bot_username6, limit=1)
       for _ in range(7):
           await asyncio.sleep(1.5)
           msg1 = await zedub.get_messages(bot_username6, limit=1)
           mss = msg1[0].text
           if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
               link_pattern = re.compile(r'(https?://\S+|@\w+)')
               link = re.search(link_pattern, mss).group(1)
               if link.startswith('https://t.me/+'):
                   link = link.replace('https://t.me/+', '')
                   result = await zedub(ImportChatInviteRequest(link.strip()))
               elif link.startswith('@'):
                   get_entity_must_join = await zedub.get_entity(link)
                   result = await zedub(JoinChannelRequest(get_entity_must_join.id))
               else:
                   get_entity_must_join = await zedub.get_entity(link)
                   result = await zedub(JoinChannelRequest(get_entity_must_join.id))
               await asyncio.sleep(3)
               await zedub.send_message(bot_username6, '/start')
       await msg1[0].click(5)
       sleep(4)
       await zedub.send_message(bot_username6, pt)
       sleep(4)
       msg = await zedub.get_messages(bot_username6, limit=1)
       await msg[0].forward_to(event.chat_id)
       await asyncio.sleep(4)
       await event.delete()
       await zedub(bloock(bot_username6))


@zedub.zed_cmd(pattern="هدية هايبر$")
async def ZelzalStart(event):
    zzz = await edit_or_reply(event, '**⎉╎جـارِ جمـع الهديـه مـن بـوت هايبـر ...✓**')
    try:
        send = await zedub.send_message(bot_username6, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_username6))
        send = await zedub.send_message(bot_username6, '/start')
    sleep(3)
    msg1 = await zedub.get_messages(bot_username6, limit=1)
    for _ in range(7):
         await asyncio.sleep(1.5)
         msg1 = await zedub.get_messages(bot_username6, limit=1)
         mss = msg1[0].text
         if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
              link_pattern = re.compile(r'(https?://\S+|@\w+)')
              link = re.search(link_pattern, mss).group(1)
              if link.startswith('https://t.me/+'):
                    link = link.replace('https://t.me/+', '')
                    result = await zedub(ImportChatInviteRequest(link.strip()))
              elif link.startswith('@'):
                    get_entity_must_join = await zedub.get_entity(link)
                    result = await zedub(JoinChannelRequest(get_entity_must_join.id))
              else:
                    get_entity_must_join = await zedub.get_entity(link)
                    result = await zedub(JoinChannelRequest(get_entity_must_join.id))
              await asyncio.sleep(3)
              await zedub.send_message(bot_username6, '/start')
    await msg1[0].click(4)
    sleep(4)
    msg2 = await zedub.get_messages(bot_username6, limit=1)
    await msg2[0].click(1)
    sleep(4)
    msg = await zedub.get_messages(bot_username6, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_username6))


@zedub.zed_cmd(pattern="تحويل برليون (.*)")
async def ZelzalStart(event):
       pts = event.pattern_match.group(1) 
       zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_username4} ...✓**")
       try:
           send = await zedub.send_message(bot_username4, '/start')
       except YouBlockedUserError:
           await zedub(unblock(bot_username4))
           send = await zedub.send_message(bot_username4, '/start')
       sleep(2)
       msg1 = await zedub.get_messages(bot_username4, limit=1)
       for _ in range(7):
           await asyncio.sleep(1.5)
           msg1 = await zedub.get_messages(bot_username4, limit=1)
           mss = msg1[0].text
           if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
               link_pattern = re.compile(r'(https?://\S+|@\w+)')
               link = re.search(link_pattern, mss).group(1)
               if link.startswith('https://t.me/+'):
                   link = link.replace('https://t.me/+', '')
                   result = await zedub(ImportChatInviteRequest(link.strip()))
               elif link.startswith('@'):
                   get_entity_must_join = await zedub.get_entity(link)
                   result = await zedub(JoinChannelRequest(get_entity_must_join.id))
               else:
                   get_entity_must_join = await zedub.get_entity(link)
                   result = await zedub(JoinChannelRequest(get_entity_must_join.id))
               await asyncio.sleep(3)
               await zedub.send_message(bot_username4, '/start')
       await msg1[0].click(3)
       sleep(4)
       await zedub.send_message(bot_username4, pts)
       sleep(4)
       msg = await zedub.get_messages(bot_username4, limit=1)
       await msg[0].forward_to(event.chat_id)
       await asyncio.sleep(4)
       await zzz.delete()
       await zedub(bloock(bot_username4))


@zedub.zed_cmd(pattern="لانهائي (.*)")
async def ZelzalStart(event):
    while True:
        try:
           malak = event.pattern_match.group(1)
           if malak == "مليار" or malak == "المليار":
               pot = '@EEObot'
           elif malak == "الجوكر" or malak == "جوكر":
               pot = '@A_MAN9300BOT'
           elif malak == "العقاب" or malak == "عقاب" or malak == "الجنرال" or malak == "جنرال":
               pot = '@MARKTEBOT'
           elif malak == "المليون" or malak == "مليون":
               pot = '@qweqwe1919bot'
           elif malak == "عرب" or malak == "العرب":
               pot = '@xnsex21bot'
           elif malak == "برليون" or malak == "البرليون":
               pot = '@Burllionbot'
           elif malak == "تناهيد" or malak == "التناهيد":
               pot = '@Ncoe_bot'
           elif malak == "اليمن" or malak == "تمويل اليمن":
               pot = '@srwry2bot'
           elif malak == "مهدويون" or malak == "مهدويين" or malak == "مهدوين":
               pot = '@MHDN313bot'
           elif malak == "دعمكم":
               return edit_or_reply(event, "**⎉╎عـذراً .. لانهائي دعمكم يختلف عن البقية ♾ ؟!\n⎉╎الامـر الصحيـح** ( `.لانهائي_دعمكم` )")
           elif malak == "نيزوكي":
               return edit_or_reply(event, "**⎉╎عـذراً .. لانهائي نيزوكي يختلف عن البقية ♾ ؟!\n⎉╎الامـر الصحيـح** ( `.لانهائي_نيزوكي` )")
           else:
               return edit_or_reply(event, "**⎉╎عـذراً الامـر خاطـئ ♾ ؟!\n⎉╎ارسـل (.اوامر النقاط) لعـرض الاوامـر**")
           numw = int(3600) if gvarstatus("SEC_LAN") is None else int(gvarstatus("SEC_LAN"))
           await edit_or_reply(event, f"**⎉╎تم بـدء التمويـل بـدون توقـف (لانهائي) ♾\n⎉╎عـدد الثـواني الفاصلـه : {numw} ⏳\n⎉╎من البـوت : {pot} 🤖\n\n⎉╎لـ الايقـاف ارسـل :** ( `.اعاده تشغيل` )")
           try:
               channel_entity = await zedub.get_entity(pot)
               await zedub.send_message(pot, '/start')
           except YouBlockedUserError:
               await zedub(unblock(pot))
               channel_entity = await zedub.get_entity(pot)
               await zedub.send_message(pot, '/start')
           await asyncio.sleep(4)
           msg0 = await zedub.get_messages(pot, limit=1)
           for _ in range(7):
               await asyncio.sleep(3)
               msg0 = await zedub.get_messages(pot, limit=1)
               mss = msg0[0].text
               if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
                   link_pattern = re.compile(r'(https?://\S+|@\w+)')
                   link = re.search(link_pattern, mss).group(1)
                   if link.startswith('https://t.me/+'):
                       link = link.replace('https://t.me/+', '')
                       result = await zedub(ImportChatInviteRequest(link.strip()))
                   elif link.startswith('@'):
                       get_entity_must_join = await zedub.get_entity(link)
                       result = await zedub(JoinChannelRequest(get_entity_must_join.id))
                   else:
                       get_entity_must_join = await zedub.get_entity(link)
                       result = await zedub(JoinChannelRequest(get_entity_must_join.id))
                   await asyncio.sleep(4)
                   await zedub.send_message(pot, '/start')
           await msg0[0].click(2)
           await asyncio.sleep(4)
           msg1 = await zedub.get_messages(pot, limit=1)
           await msg1[0].click(0)
           chs = 0
           for i in range(100):
               await asyncio.sleep(4)
               list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
               msgs = list.messages[0]
               if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
                   await zedub.send_message(event.chat_id, f"**⎉╎تم بـدء التمويـل بـدون توقـف (لانهائي) ♾\n⎉╎عـدد الثـواني الفاصلـه : {numw} ⏳\n⎉╎من البـوت : {pot} 🤖**")
                   break
               if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
                   await asyncio.sleep(2)
                   await msg2[0].click(text='استمرار التجميع')
                   await asyncio.sleep(2)
                   await zedub.send_message(pot, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(pot, limit=1)
                   await msg0[0].click(2)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(pot, limit=1)
                   await msg1[0].click(0)
                   await asyncio.sleep(2)
                   msg2 = await zedub.get_messages(pot, limit=1)
                   mas = msg2[0].text
                   await asyncio.sleep(2)
               if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
                   await asyncio.sleep(2)
                   await msg2[0].click(text='استمرار التجميع')
                   await asyncio.sleep(2)
                   msg2 = await zedub.get_messages(pot, limit=1)
                   mas = msg2[0].text
                   await asyncio.sleep(4)

               if "بسبب التكرار" in mas or "تم حظرك" in mas:
                   await asyncio.sleep(65)
                   await zedub.send_message(pot, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(pot, limit=1)
                   await msg0[0].click(2)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(pot, limit=1)
                   await msg1[0].click(0)
                   await asyncio.sleep(2)
               try:
                   url = msgs.reply_markup.rows[0].buttons[0].url
               except AttributeError:
                   await asyncio.sleep(4)
                   await zedub.send_message(pot, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(pot, limit=1)
                   await msg0[0].click(2)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(pot, limit=1)
                   await msg1[0].click(0)
                   await asyncio.sleep(2)
               try:
                   try:
                       await zedub(JoinChannelRequest(url))
                   except:
                       syth = url.split('/')[-1]
                       await zedub(ImportChatInviteRequest(syth))
                   msg2 = await zedub.get_messages(pot, limit=1)
                   await msg2[0].click(text='تحقق')
                   chs += 10
                   await edit_or_reply(event, f"**⎉╎عدد النقاط في هذه المحاولة {chs} .**")
                   await asyncio.sleep(2)
               except:
                   msg2 = await zedub.get_messages(pot, limit=1)
                   await msg2[0].click(text='التالي')
                   chs += 0
                   await edit_or_reply(event, f"**⎉╎عـذراً لم تحصل على نقاط في هذه المحاولة\n⎉╎لأنني وجدت قناة خاصة وقمت بتخطيها\n⎉╎البوت الذي حدث فيه الخطأ: {pot}**")
           await zedub.send_message(event.chat_id, f"**⎉╎عذرا نفذت قنوات البوت \n⎉╎لكن سوف اعاود المحاولة بعد {numw} ثانية**")
           await zedub(bloock(pot))
           await asyncio.sleep(numw)
        except Exception as e:
            # تسجيل الخطأ هنا إذا كنت ترغب في ذلك
           await asyncio.sleep(numw)

@zedub.zed_cmd(pattern="لانهائي_دعمكم$")
async def ZelzalStart(event):
    while True:
        try:
           malak = event.pattern_match.group(1)
           pot = '@DamKomBot'
           numw = int(3600) if gvarstatus("SEC_LAN") is None else int(gvarstatus("SEC_LAN"))
           await edit_or_reply(event, f"**⎉╎تم بـدء التمويـل بـدون توقـف (لانهائي) ♾\n⎉╎عـدد الثـواني الفاصلـه : {numw} ⏳\n⎉╎من البـوت : {pot} 🤖\n\n⎉╎لـ الايقـاف ارسـل :** ( `.اعاده تشغيل` )")
           try:
               channel_entity = await zedub.get_entity(pot)
               await zedub.send_message(pot, '/start')
           except YouBlockedUserError:
               await zedub(unblock(pot))
               channel_entity = await zedub.get_entity(pot)
               await zedub.send_message(pot, '/start')
           await asyncio.sleep(4)
           msg0 = await zedub.get_messages(pot, limit=1)
           for _ in range(30):
                await asyncio.sleep(1.5)
                msg0 = await zedub.get_messages(bot_username8, limit=1)
                mss = msg0[0].text
                if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "الأشتراك بقناة" in mss or "الأشتراك بقناه" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
                    link_pattern = re.compile(r'(https?://\S+|@\w+)')
                    link = re.search(link_pattern, mss).group(1)
                    if link.startswith('https://t.me/+'):
                        link = link.replace('https://t.me/+', '')
                        result = await zedub(ImportChatInviteRequest(link.strip()))
                    elif link.startswith('@'):
                        get_entity_must_join = await zedub.get_entity(link)
                        result = await zedub(JoinChannelRequest(get_entity_must_join.id))
                    else:
                        get_entity_must_join = await zedub.get_entity(link)
                        result = await zedub(JoinChannelRequest(get_entity_must_join.id))
                    await asyncio.sleep(3)
                    await zedub.send_message(bot_username8, '/start')
                elif "الاشتراك بقنوات" in mss or "الاشتراك في قنوات" in mss or "الاشتراك في قنوات" in mss or "اشترك بالقنوات" in mss or "الاشتراك في القنوات" in mss or "الاشتراك في القنوات" in mss or "الأشتراك بقنوات" in mss or "الأشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الإشتراك بقنوات" in mss or "الاشتراك بالقنوات" in mss:
                    list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
                    msgs = list.messages[0]
                    try:
                        if msgs.reply_markup:
                            for i, row in enumerate(msgs.reply_markup.rows):
                                if row.buttons:
                                    button = row.buttons[0]
                                    url = msgs.reply_markup.rows[i].buttons[0].url
                                    chname = msgs.reply_markup.rows[i].buttons[0].text
                                    chnum = i+1
                                    if "تحقق" in chname:
                                        await zedub.send_message(bot_username8, '/start')
                                        break
                                    try:
                                        try:
                                            await zedub(JoinChannelRequest(url))
                                        except:
                                            bott = url.split('/')[-1]
                                            await zedub(ImportChatInviteRequest(bott))
                                        msg2 = await zedub.get_messages(bot_username8, limit=1)
                                        #await msg2[0].click(text='تحقق ✅')
                                        await event.edit(f"**⎉╎تم الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. بنجاح ✓**")
                                        await asyncio.sleep(2)
                                        #await zedub.send_message(bot_username8, '/start')
                                    except:
                                        await event.edit(f"**⎉╎فشل الاشتـراك في قناة الاشتراك الاجباري** {chname}\n**⎉╎رقم {chnum} .. يمكن تبندت 🥲\n**⎉╎لذلك تم تخطيها .. بنجاح ✓**")
                                        #await zedub.send_message(bot_username8, '/start')
                        else:
                            await zedub.send_message(bot_username8, '/start')
                            break
                    except AttributeError:
                        await zedub.send_message(bot_username8, '/start')
                else:
                    #await zedub.send_message(bot_username8, '/start')
                    break
           await msg0[0].click(1)
           await asyncio.sleep(4)
           msg1 = await zedub.get_messages(pot, limit=1)
           await msg1[0].click(1)
           chs = 0
           for i in range(100):
               await asyncio.sleep(4)
               list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
               msgs = list.messages[0]
               if msgs.message.find('لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه') != -1:
                   await zedub.send_message(event.chat_id, f"**⎉╎تم بـدء التمويـل بـدون توقـف (لانهائي) ♾\n⎉╎عـدد الثـواني الفاصلـه : {numw} ⏳\n⎉╎من البـوت : {pot} 🤖**")
                   break
               if "أدوات تجميع" in msgs.message or "ادوات " in msgs.message:
                   await asyncio.sleep(2)
                   await msg2[0].click(text='استمرار التجميع')
                   await asyncio.sleep(2)
                   await zedub.send_message(bot_username8, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(bot_username8, limit=1)
                   await msg0[0].click(1)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(bot_username8, limit=1)
                   await msg1[0].click(1)
                   await asyncio.sleep(2)
                   msg2 = await zedub.get_messages(bot_username8, limit=1)
                   mas = msg2[0].text
                   await asyncio.sleep(2)
               if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
                   await asyncio.sleep(2)
                   await msg2[0].click(text='استمرار التجميع')
                   await asyncio.sleep(2)
                   msg2 = await zedub.get_messages(bot_username8, limit=1)
                   mas = msg2[0].text
                   await asyncio.sleep(4)
               if "بسبب التكرار" in mas or "تم حظرك" in mas:
                   await asyncio.sleep(65)
                   await zedub.send_message(pot, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(pot, limit=1)
                   await msg0[0].click(1)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(pot, limit=1)
                   await msg1[0].click(0)
                   await asyncio.sleep(2)
               msg_text = msgs.message
               if "عليك الاشتراك بقناة البوت" in msg_text:
                   the_channnel = msg_text.split('@')[1].split()[0]
                   try:
                       entity = await zedub.get_entity(the_channnel)
                       if entity:
                           await zedub(JoinChannelRequest(entity.id))
                           await asyncio.sleep(4)
                           await zedub.send_message(pot, '/start')
                           await asyncio.sleep(4)
                           msg0 = await zedub.get_messages(pot, limit=1)
                           await msg0[0].click(1)
                           await asyncio.sleep(4)
                           msg1 = await zedub.get_messages(pot, limit=1)
                           await msg1[0].click(0)
                   except:
                       continue
               if "اشترك فالقناة @" in msg_text:
                   the_channel = msg_text.split('@')[1].split()[0]
                   try:
                       entity = await zedub.get_entity(the_channel)
                       if entity:
                           await zedub(JoinChannelRequest(entity.id))
                           await asyncio.sleep(4)
                           msg2 = await zedub.get_messages(pot, limit=1)
                           await msg2[0].click(text='اشتركت ✅')
                           chs += 10
                           await edit_or_reply(event, f"**⎉╎عدد النقاط في هذه المحاولة {chs} .**")
                           await asyncio.sleep(2)
                   except:
                       await edit_or_reply(event, f"**⎉╎عـذراً لم تحصل على نقاط في هذه المحاولة\n⎉╎لأنني وجدت قناة خاصة وقمت بتخطيها\n⎉╎البوت الذي حدث فيه الخطأ: {pot}**")
                       continue
           await zedub.send_message(event.chat_id, f"**⎉╎عذرا نفذت قنوات البوت \n⎉╎لكن سوف اعاود المحاولة بعد {numw} ثانية**")
           await zedub(bloock(pot))
           await asyncio.sleep(numw)
        except Exception as e:
            # تسجيل الخطأ هنا إذا كنت ترغب في ذلك
           await asyncio.sleep(numw)


@zedub.zed_cmd(pattern="(بوت النيزوكي|بوت نيزوكي)$")
async def _(event):
    await edit_or_reply(event, "@FF4BOT")

@zedub.zed_cmd(pattern="(نيزوكي|تجميع نيزوكي)(?: |$)(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ الاشتـراك بـ قنـوات الاشتـراك الاجبـاري .. انتظـر دقيقـه {bot_usernamee0}**")
    try:
        channel_entity = await zedub.get_entity(bot_usernamee0)
        await zedub.send_message(bot_usernamee0, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee0))
        channel_entity = await zedub.get_entity(bot_usernamee0)
        await zedub.send_message(bot_usernamee0, '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages(bot_usernamee0, limit=1)
    for _ in range(7):  # تكرار الإجراءات 3 مرات كحد أقصى
        await asyncio.sleep(1.5)
        msg0 = await zedub.get_messages(bot_usernamee0, limit=1)
        mss = msg0[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "في قناه البوت" in mss or "في قناة البوت" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            await zedub(JoinChannelRequest(channel="@Niyzokybots"))
            await zedub(JoinChannelRequest(channel="@XX4CH"))
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee0, '/start')  # إعادة إرسال "/start"
    await asyncio.sleep(3)
    await msg0[0].click(0)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
    await msg1[0].click(0)
    chs = 1
    for i in range(100):
        await asyncio.sleep(4)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('لا يوجد قنوات') != -1:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        msg2 = await zedub.get_messages(bot_usernamee0, limit=1)
        mas = msg2[0].text
        if "في الوقت الحالي" in mas or "لا يوجد قنوات" in mas:
            await zedub.send_message(event.chat_id, "**⎉╎مـافي قنـوات بالبـوت حاليـاً ...**")
            break
        if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
            await asyncio.sleep(2)
            await zedub.send_message(bot_usernamee0, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee0, limit=1)
            await msg0[0].click(0)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if "بسبب التكرار" in mas or "تم حظرك" in mas:
            await asyncio.sleep(65)
            await zedub.send_message(bot_usernamee0, '/start')
            await asyncio.sleep(4)
            msg0 = await zedub.get_messages(bot_usernamee0, limit=1)
            await msg0[0].click(0)
            await asyncio.sleep(4)
            msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
            await msg1[0].click(0)
            await asyncio.sleep(2)
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, "**⎉╎تم إيقـاف تجميـع النقـاط .. بنجـاح☑️**")
            break
        #try:
            #url = msgs.reply_markup.rows[0].buttons[0].url
        #except AttributeError:
            #await asyncio.sleep(2)
            #await zedub.send_message(bot_usernamee0, '/start')
            #await asyncio.sleep(4)
            #msg0 = await zedub.get_messages(bot_usernamee0, limit=1)
            #await msg0[0].click(0)
            #await asyncio.sleep(4)
            #msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
            #await msg1[0].click(0)
            #await asyncio.sleep(2)
        msg_text = msgs.message
        if "انضم ب" in msg_text:
            the_channel = msg_text.split('@')[1].split()[0]
            try:
                entity = await zedub.get_entity(the_channel)
                if entity:
                    await zedub(JoinChannelRequest(entity.id))
                    await asyncio.sleep(4)
                    msg2 = await zedub.get_messages(bot_usernamee0, limit=1)
                    await msg2[0].click(text='💰 تحقق من الانضمام 💰')
                    await asyncio.sleep(1.5)
                    chs += 1
                    await zzz.edit(f"**⎉╎تم الاشتـراك في القنـاة  {chs} ...✓**")
            except:
                continue

    await zedub.send_message(event.chat_id, "**⎉╎تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    await zedub(bloock(bot_usernamee0))


@zedub.zed_cmd(pattern="هدية نيزوكي$")
async def ZelzalStart(event): #by T.me/zzzzl1l
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ جمـع الهديـه مـن بـوت {bot_usernamee0} ...✓**")
    try:
        send = await zedub.send_message(bot_usernamee0, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee0))
        send = await zedub.send_message(bot_usernamee0, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "في قناه البوت" in mss or "في قناة البوت" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            await zedub(JoinChannelRequest(channel="@Niyzokybots"))
            await zedub(JoinChannelRequest(channel="@XX4CH"))
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee0, '/start')
    await msg1[0].click(0)
    await asyncio.sleep(2)
    msg2 = await zedub.get_messages(bot_usernamee0, limit=1)
    await msg2[0].click(6)
    msg = await zedub.get_messages(bot_usernamee0, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(2)
    await zzz.delete()
    await zedub(bloock(bot_usernamee0))


@zedub.zed_cmd(pattern="تحويل نيزوكي (.*)")
async def ZelzalStart(event):
    ptss = event.pattern_match.group(1)
    if not ptss.isnumeric():
        return await edit_or_reply(event, "**⎉╎باضافة ايـدي الشخص لـ الامـر**")
    pts = f"#{ptss}"
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ تحويـل النقـاط مـن بـوت {bot_usernamee0} ...✓**")
    try:
        send = await zedub.send_message(bot_usernamee0, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee0))
        send = await zedub.send_message(bot_usernamee0, '/start')
    sleep(2)
    msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "في قناه البوت" in mss or "في قناة البوت" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            await zedub(JoinChannelRequest(channel="@Niyzokybots"))
            await zedub(JoinChannelRequest(channel="@XX4CH"))
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee0, '/start')
    await msg1[0].click(7)
    sleep(4)
    msg2 = await zedub.get_messages(bot_usernamee0, limit=1)
    mss = msg2[0].text
    if "وجب التنبيه" in mss or "لضمان حقك" in mss:
        await msg2[0].click(0)
        msg2 = await zedub.get_messages(bot_usernamee0, limit=1)
    await zedub.send_message(bot_usernamee0, pts)
    sleep(4)
    msg3 = await zedub.get_messages(bot_usernamee0, limit=1)
    mss = msg3[0].text
    if "نقاطك انت" in mss or "صديقك" in mss:
        await msg3[0].click(0)
        sleep(4)
    if "تعذر العثور" in mss:
        return await msg3.forward_to(event.chat_id)
    msg = await zedub.get_messages(bot_usernamee0, limit=1)
    await msg[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_usernamee0))

@zedub.zed_cmd(pattern="نقاط نيزوكي$")
async def ZelzalStart(event):
    boto = '@FF4BOT'
    zzz = await edit_or_reply(event, f"**⎉╎جـارِ جمـع المعلومـات مـن بـوت {boto} ...✓**")
    try:
        send = await zedub.send_message(bot_usernamee0, '/start')
    except YouBlockedUserError:
        await zedub(unblock(bot_usernamee0))
        send = await zedub.send_message(bot_usernamee0, '/start')
    sleep(1)
    msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
    for _ in range(7):
        await asyncio.sleep(1.5)
        msg1 = await zedub.get_messages(bot_usernamee0, limit=1)
        mss = msg1[0].text
        if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "في قناه البوت" in mss or "في قناة البوت" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
            await zedub(JoinChannelRequest(channel="@Niyzokybots"))
            await zedub(JoinChannelRequest(channel="@XX4CH"))
            link_pattern = re.compile(r'(https?://\S+|@\w+)')
            link = re.search(link_pattern, mss).group(1)
            if link.startswith('https://t.me/+'):
                link = link.replace('https://t.me/+', '')
                result = await zedub(ImportChatInviteRequest(link.strip()))
            elif link.startswith('@'):
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            else:
                get_entity_must_join = await zedub.get_entity(link)
                result = await zedub(JoinChannelRequest(get_entity_must_join.id))
            await asyncio.sleep(3)
            await zedub.send_message(bot_usernamee0, '/start')
    sleep(1)
    await msg1[0].forward_to(event.chat_id)
    await asyncio.sleep(4)
    await zzz.delete()
    await zedub(bloock(bot_usernamee0))

@zedub.zed_cmd(pattern="لانهائي_نيزوكي$")
async def ZelzalStart(event):
    while True:
        try:
           malak = event.pattern_match.group(1)
           pot = '@FF4BOT'
           numw = int(3600) if gvarstatus("SEC_LAN") is None else int(gvarstatus("SEC_LAN"))
           await edit_or_reply(event, f"**⎉╎تم بـدء التمويـل بـدون توقـف (لانهائي) ♾\n⎉╎عـدد الثـواني الفاصلـه : {numw} ⏳\n⎉╎من البـوت : {pot} 🤖\n\n⎉╎لـ الايقـاف ارسـل :** ( `.اعاده تشغيل` )")
           try:
               channel_entity = await zedub.get_entity(pot)
               await zedub.send_message(pot, '/start')
           except YouBlockedUserError:
               await zedub(unblock(pot))
               channel_entity = await zedub.get_entity(pot)
               await zedub.send_message(pot, '/start')
           await asyncio.sleep(4)
           msg0 = await zedub.get_messages(pot, limit=1)
           for _ in range(7):
               await asyncio.sleep(3)
               msg0 = await zedub.get_messages(pot, limit=1)
               mss = msg0[0].text
               if "الاشتراك بقناة" in mss or "الاشتراك في قناه" in mss or "الاشتراك في قناة" in mss or "اشترك بالقناة" in mss or "الاشتراك في القناه" in mss or "الاشتراك في القناة" in mss or "في قناه البوت" in mss or "في قناة البوت" in mss or "الإشتراك بقناة" in mss or "الإشتراك بقناه" in mss:
                   await zedub(JoinChannelRequest(channel="@Niyzokybots"))
                   await zedub(JoinChannelRequest(channel="@XX4CH"))
                   link_pattern = re.compile(r'(https?://\S+|@\w+)')
                   link = re.search(link_pattern, mss).group(1)
                   if link.startswith('https://t.me/+'):
                       link = link.replace('https://t.me/+', '')
                       result = await zedub(ImportChatInviteRequest(link.strip()))
                   elif link.startswith('@'):
                       get_entity_must_join = await zedub.get_entity(link)
                       result = await zedub(JoinChannelRequest(get_entity_must_join.id))
                   else:
                       get_entity_must_join = await zedub.get_entity(link)
                       result = await zedub(JoinChannelRequest(get_entity_must_join.id))
                   await asyncio.sleep(4)
                   await zedub.send_message(pot, '/start')
           await msg0[0].click(0)
           await asyncio.sleep(4)
           msg1 = await zedub.get_messages(pot, limit=1)
           await msg1[0].click(0)
           chs = 0
           for i in range(100):
               await asyncio.sleep(4)
               list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
               msgs = list.messages[0]
               if msgs.message.find('لا يوجد قنوات') != -1:
                   await zedub.send_message(event.chat_id, f"**⎉╎تم بـدء التمويـل بـدون توقـف (لانهائي) ♾\n⎉╎عـدد الثـواني الفاصلـه : {numw} ⏳\n⎉╎من البـوت : {pot} 🤖**")
                   break
               if "أدوات تجميع" in mas or "ادوات تجميع" in mas:
                   await asyncio.sleep(2)
                   await zedub.send_message(pot, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(pot, limit=1)
                   await msg0[0].click(1)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(pot, limit=1)
                   await msg1[0].click(0)
                   await asyncio.sleep(2)
               if "بسبب التكرار" in mas or "تم حظرك" in mas:
                   await asyncio.sleep(65)
                   await zedub.send_message(pot, '/start')
                   await asyncio.sleep(4)
                   msg0 = await zedub.get_messages(pot, limit=1)
                   await msg0[0].click(0)
                   await asyncio.sleep(4)
                   msg1 = await zedub.get_messages(pot, limit=1)
                   await msg1[0].click(0)
                   await asyncio.sleep(2)
               msg_text = msgs.message
               if "انضم ب" in msg_text:
                   the_channel = msg_text.split('@')[1].split()[0]
                   try:
                       entity = await zedub.get_entity(the_channel)
                       if entity:
                           await zedub(JoinChannelRequest(entity.id))
                           await asyncio.sleep(4)
                           msg2 = await zedub.get_messages(pot, limit=1)
                           await msg2[0].click(text='💰 تحقق من الانضمام 💰')
                           chs += 2.3
                           await edit_or_reply(event, f"**⎉╎عدد النقاط في هذه المحاولة {chs} .**")
                           await asyncio.sleep(2)
                   except:
                       await edit_or_reply(event, f"**⎉╎عـذراً لم تحصل على نقاط في هذه المحاولة\n⎉╎لأنني وجدت قناة خاصة وقمت بتخطيها\n⎉╎البوت الذي حدث فيه الخطأ: {pot}**")
                       continue
           await zedub.send_message(event.chat_id, f"**⎉╎عذرا نفذت قنوات البوت \n⎉╎لكن سوف اعاود المحاولة بعد {numw} ثانية**")
           await zedub(bloock(pot))
           await asyncio.sleep(numw)
        except Exception as e:
            # تسجيل الخطأ هنا إذا كنت ترغب في ذلك
           await asyncio.sleep(numw)


@zedub.zed_cmd(pattern="بخشيش وعد(?: |$)(.*)")
async def baqshis(event):
    global bahsees
    await event.delete()
    if not bahsees:
        bahsees = True
        if event.is_group:
            await the_bahsees(event)
        else:
            await edit_or_reply(event, "**⎉╎ الامـر خاص بـ المجموعات فقـط ؟!**")
async def the_bahsees(event):
    await event.respond('بخشيش')
    await asyncio.sleep(660)
    global bahsees
    if bahsees:
        await the_bahsees(event)  
@zedub.zed_cmd(pattern="ايقاف بخشيش وعد(?: |$)(.*)")
async def baqshis(event):
    global bahsees
    bahsees = False
    await edit_or_reply(event, "**⎉╎تم إيقـاف تجميـع البخشيش  .. بنجـاح ✓** ")

@zedub.zed_cmd(pattern="سرقة وعد(?: |$)(.*)")
async def thift(event):
    global thifts
    await event.delete()
    if not thifts:
        thifts = True
        if event.is_group:
            message = event.pattern_match.group(1).strip()
            if message:
                await send_message(event, message)
            else:
                await edit_or_reply(event, "**⎉╎قم بكتابة ايدي الشخص مع الامـر ؟!**")

async def send_message(event, message):
    await event.respond(f"زرف {message}")
    await asyncio.sleep(660)
    global thifts
    if thifts:
        await send_message(event, message)

@zedub.zed_cmd(pattern="ايقاف سرقة وعد(?: |$)(.*)")
async def _(event):
    global thifts
    thifts = False
    await edit_or_reply(event, "**⎉╎تم إيقـاف السرقة  .. بنجـاح ✓**")
client = zedub


@zedub.zed_cmd(pattern="راتب وعد(?: |$)(.*)")
async def thift(event):
    global ratp
    await event.delete()
    if not ratp:
        ratp = True
        if event.is_group:
            await the_ratp(event)
        else:
            await edit_or_reply(event, "**⎉╎ الامـر خاص بـ المجموعات فقـط ؟!**")

async def the_ratp(event):
    await event.respond('راتب')
    await asyncio.sleep(660)
    global ratp
    if ratp:
        await the_ratp(event)  
@zedub.zed_cmd(pattern="ايقاف راتب وعد(?: |$)(.*)")
async def thift(event):
    global ratp
    ratp = False
    await edit_or_reply(event, "**تم تعطيل راتب وعد بنجاح ✅**")


@zedub.zed_cmd(pattern="كلمات وعد (.*)")
async def waorwaad(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await zedub.send_message(chat, "كلمات")
        await asyncio.sleep(0.5)
        masg = await zedub.get_messages(chat, limit=1)
        masg = masg[0].message
        masg = ("".join(masg.split(maxsplit=3)[3:])).split(" ", 2)
        if len(masg) == 2:
            msg = masg[0]
            await zedub.send_message(chat, msg)
        else:
            msg = masg[0] + " " + masg[1]
            await zedub.send_message(chat, msg)


@zedub.zed_cmd(pattern="استثمار وعد")
async def _(event):
    await event.delete()
    global estithmar
    estithmar = True
    while estithmar:
        if event.is_group:
            await event.client.send_message(event.chat_id, "فلوسي")
            await asyncio.sleep(4)
            zzzthon = await event.client.get_messages(event.chat_id, limit=1)
            zzzthon = zzzthon[0].message
            zzzthon = ("".join(zzzthon.split(maxsplit=2)[2:])).split(" ", 2)
            zedub = zzzthon[0]
            if zedub.isdigit() and int(zedub) > 500000000:
                await event.client.send_message(event.chat_id,f"استثمار {zedub}")
                await asyncio.sleep(5)
                zzthon = await event.client.get_messages(event.chat_id, limit=1)
                await zzthon[0].click(text="اي ✅")
            else:
                await event.client.send_message(event.chat_id, f"استثمار {zedub}")
            await asyncio.sleep(1210)
        
        else:
            await edit_or_reply(event, "**⎉╎امر الاستثمار يمكنك استعماله في المجموعات فقط 🖤**")
@zedub.zed_cmd(pattern="ايقاف استثمار وعد")
async def stop_wad(event):
    global estithmar
    estithmar = False
    await edit_or_reply(event, "**⎉╎تم إيقـاف استثمار وعـد  .. بنجـاح ✓**")


@zedub.zed_cmd(pattern="اوامر النقاط")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalCoins_cmd)

@zedub.zed_cmd(pattern="اوامر التجميع")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalCoins_cmd)

@zedub.zed_cmd(pattern="اوامر وعد")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalWaad_cmd)

