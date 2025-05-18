import asyncio
import shutil
import contextlib
from datetime import datetime
import re
import datetime
from asyncio import sleep

from telethon import events
from telethon.utils import get_display_name

from . import zedub
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.katm_sql import (
    add_katm,
    get_katms,
    remove_all_katms,
    remove_katm,
)
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..utils import Zed_Dev
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

plugin_category = "الخدمات"
LOGS = logging.getLogger(__name__)
KTMZ = gvarstatus("Z_KTM") or "كتم"

@zedub.zed_cmd(pattern=f"{KTMZ}(?: |$)(.*)")
async def startgmute(event):
    if event.is_private:
        await asyncio.sleep(0.5)
        #userid = event.chat_id
        #reason = event.pattern_match.group(1)
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == zedub.uid:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم نفســك ؟!**")
        if user.id in Zed_Dev:
            return await edit_or_reply(event, "**- فكيـو - fuck You 😾🖕**\n**- لاتعيدهـا مـع مطـوࢪين السـورس ...🚧**")
        if user.id == 925972505 or user.id == 1895219306:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم مطـور السـورس ؟!**")
        userid = user.id 
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == zedub.uid:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم نفســك ؟!**")
        if user.id in Zed_Dev:
            return await edit_or_reply(event, "**- فكيـو - fuck You 😾🖕**\n**- لاتعيدهـا مـع مطـوࢪين السـورس ...🚧**")
        if user.id == 925972505 or user.id == 1895219306:
            return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنك كتــم مطـور السـورس ؟!**")
        userid = user.id
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنني العثــوࢪ علـى المسـتخــدم ؟!**")
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**⎉╎المستخـدم**  {_format.mentionuser(user.first_name ,user.id)} \n**⎉╎مڪتوم سابقـاً**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**- خطـأ :**\n`{e}`")
    else:
        if reason:
            if gvarstatus("PC_MUTE") is not None:
                await event.client.send_file(
                    event.chat_id,
                    gvarstatus("PC_MUTE"),
                    caption=f"**- المستخـدم :** {_format.mentionuser(user.first_name ,user.id)} .\n**- تـم كتمـه بنجـاح 🔕**\n**- السـبب :** {reason}",
                )
                await event.delete()
            else:
                await edit_or_reply(
                    event,
                    f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم كتمــه .. بنجــاح 🔕**\n**⎉╎السـبب :** {reason}",
                )
        else:
            if gvarstatus("PC_MUTE") is not None:
                await event.client.send_file(
                    event.chat_id,
                    gvarstatus("PC_MUTE"),
                    caption=f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم كتمــه .. بنجــاح 🔕**",
                )
                await event.delete()
            else:
                await edit_or_reply(
                    event,
                    f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم كتمــه .. بنجــاح 🔕**",
                )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reply:
            await reply.forward_to(BOTLOG_CHATID)
        if reason:
            if add_katm(str(zedub.uid), str(user.id), user.first_name, reason) is True:
                return await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكتــم_العـــام 🔕\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الايدي** `{user.id}`\n"
                    f"**- الســبب :** `{reason}`\n\n"
                    f"**- تم إضافة المستخدم لـ قائمة المكتوميـن ✅**\n"
                    f"**- ملاحظـه 💡:**\n"
                    f"**• قائمـة المكتوميــن هي عبارة عن إضافة جديدة وحصرية 🧾**\n"
                    f"**• غير موجودة ع سورس آخر فقط لدى سورس زدثــون¹**\n"
                    f"**• لـ تصفح قائمة المكتومين ارسـل** ( `.المكتومين` )\n"
                    f"**• لـ مسح جميع المكتومين ارسـل** ( `.مسح المكتومين` )",
                )
            else:
                remove_katm(str(zedub.uid), str(user.id))
                if add_katm(str(zedub.uid), str(user.id), user.first_name, reason) is True:
                    return await event.client.send_message(
                        BOTLOG_CHATID,
                        "#الكتــم_العـــام 🔕\n\n"
                        f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                        f"**- الايدي** `{user.id}`\n"
                        f"**- الســبب :** `{reason}`\n\n"
                        f"**- تم إضافة المستخدم لـ قائمة المكتوميـن ✅**\n"
                        f"**- ملاحظـه 💡:**\n"
                        f"**• قائمـة المكتوميــن هي عبارة عن إضافة جديدة وحصرية 🧾**\n"
                        f"**• غير موجودة ع سورس آخر فقط لدى سورس زدثــون¹**\n"
                        f"**• لـ تصفح قائمة المكتومين ارسـل** ( `.المكتومين` )\n"
                        f"**• لـ مسح جميع المكتومين ارسـل** ( `.مسح المكتومين` )",
                    )
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكتــم_العـــام 🔕\n\n"
                f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**- الســبب :** `{reason}`",
            )
        else:
            reason = "لا يوجد"
            if add_katm(str(zedub.uid), str(user.id), user.first_name, reason) is True:
                return await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكتــم_العـــام 🔕\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الايدي** `{user.id}`\n\n"
                    f"**- تم إضافة المستخدم لـ قائمة المكتوميـن ✅**\n"
                    f"**- ملاحظـه 💡:**\n"
                    f"**• قائمـة المكتوميــن هي عبارة عن إضافة جديدة وحصرية 🧾**\n"
                    f"**• غير موجودة ع سورس آخر فقط لدى سورس زدثــون¹**\n"
                    f"**• لـ تصفح قائمة المكتومين ارسـل** ( `.المكتومين` )\n"
                    f"**• لـ مسح جميع المكتومين ارسـل** ( `.مسح المكتومين` )",
                )
            else:
                remove_katm(str(zedub.uid), str(user.id))
                if add_katm(str(zedub.uid), str(user.id), user.first_name, reason) is True:
                    return await event.client.send_message(
                        BOTLOG_CHATID,
                        "#الكتــم_العـــام 🔕\n\n"
                        f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                        f"**- الايدي** `{user.id}`\n\n"
                        f"**- تم إضافة المستخدم لـ قائمة المكتوميـن ✅**\n"
                        f"**- ملاحظـه 💡:**\n"
                        f"**• قائمـة المكتوميــن هي عبارة عن إضافة جديدة وحصرية 🧾**\n"
                        f"**• غير موجودة ع سورس آخر فقط لدى سورس زدثــون¹**\n"
                        f"**• لـ تصفح قائمة المكتومين ارسـل** ( `.المكتومين` )\n"
                        f"**• لـ مسح جميع المكتومين ارسـل** ( `.مسح المكتومين` )",
                    )
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكتــم_العـــام 🔕\n"
                f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@zedub.zed_cmd(pattern="الغاء كتم(?: |$)(.*)")
async def endgmute(event):
    if event.is_private:
        await asyncio.sleep(0.5)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == zedub.uid:
            return await edit_or_reply(event, "**- عــذࢪاً .. انت غيـر مكتـوم يامطــي ؟!**")
        userid = user.id
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(event, "**- عــذࢪاً .. لايمكــنني العثــوࢪ علـى المسـتخــدم ؟!**")
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n\n**⎉╎غيـر مكتـوم عــام ✓**"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**- خطـأ :**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n**⎉╎تم الغـاء كتمــه .. بنجــاح 🔔**\n**⎉╎السـبب :** {reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"**⎉╎المستخـدم :** {_format.mentionuser(user.first_name ,user.id)}\n\n**⎉╎تم الغـاء كتمــه .. بنجــاح 🔔**",
            )
    if BOTLOG:
        if not remove_katm(str(zedub.uid), str(user.id)):
            if reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الغـــاء_الكتــم_العـــام 🔔\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الســبب :** `{reason}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الغـــاء_الكتــم_العـــام 🔔\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n",
                )
        else:
            if reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الغـــاء_الكتــم_العـــام 🔔\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الايدي** `{user.id}`\n"
                    f"**- الســبب :** `{reason}`\n\n"
                    f"**- تم إزالة المستخدم من قائمة المكتوميـن ✅**\n"
                    f"**- ملاحظـه 💡:**\n"
                    f"**• قائمـة المكتوميــن هي عبارة عن إضافة جديدة وحصرية 🧾**\n"
                    f"**• غير موجودة ع سورس آخر فقط لدى سورس زدثــون¹**\n"
                    f"**• لـ تصفح قائمة المكتومين ارسـل** ( `.المكتومين` )\n"
                    f"**• لـ مسح جميع المكتومين ارسـل** ( `.مسح المكتومين` )",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الغـــاء_الكتــم_العـــام 🔔\n\n"
                    f"**- المُستخدِم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                    f"**- الايدي** `{user.id}`\n\n"
                    f"**- تم إزالة المستخدم من قائمة المكتوميـن ✅**\n"
                    f"**- ملاحظـه 💡:**\n"
                    f"**• قائمـة المكتوميــن هي عبارة عن إضافة جديدة وحصرية 🧾**\n"
                    f"**• غير موجودة ع سورس آخر فقط لدى سورس زدثــون¹**\n"
                    f"**• لـ تصفح قائمة المكتومين ارسـل** ( `.المكتومين` )\n"
                    f"**• لـ مسح جميع المكتومين ارسـل** ( `.مسح المكتومين` )",
                )


@zedub.zed_cmd(incoming=True, forword=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@zedub.zed_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@zedub.zed_cmd(pattern="المكتومين$")
async def on_mute_list(event):
    OUT_STR = "**- لايــوجـد لديــك أي مكتوميــن بعــد 🔔**"
    count = 1
    mktoms = get_katms(zedub.uid)
    for mktoom in mktoms:
        if OUT_STR == "**- لايــوجـد لديــك أي مكتوميــن بعــد 🔔**":
            OUT_STR = f"𓆩 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - **قائمـة المكتوميــن** 🔕𓆪\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n**• إجمالي عـدد المكتوميـن {count}**\n"
        OUT_STR += "\n**• الاسم:** [{}](tg://user?id={})\n**• السبب:** {}".format(mktoom.f_name, mktoom.ktm_id, mktoom.f_reason)
        count += 1
    await edit_or_reply(
        event,
        OUT_STR,
        caption="**⧗╎قائمـة المكتوميــن 🔕**",
        file_name="mktoms.text",
    )


@zedub.zed_cmd(pattern="مسح المكتومين$")
async def on_all_muted_delete(event):
    mktomers = get_katms(zedub.uid)
    count = 1
    if mktomers:
        zed = await edit_or_reply(event, "**⪼ جـارِ مسـح المكتوميـن .. انتظـر ⏳**")
        for mktoom in mktomers:
            unmute(mktoom.ktm_id, "gmute")
            count += 1
        remove_all_katms(zedub.uid)
        await zed.edit("**⪼ تم حـذف جميـع المكتوميـن .. بنجـاح ✅**")
    else:
        OUT_STR = "**- لايــوجـد لديــك أي مكتوميــن بعــد 🔔**"
        await edit_or_reply(event, OUT_STR)


# ================================================================================================ #
# ================================================================================================ #
# ================================================================================================ #
import asyncio
from telethon import utils
from telethon.tl import functions, types
from telethon.tl.types import InputUser
from telethon.tl.types import InputFile
from . import zedub

@zedub.zed_cmd(pattern="ستوري جهاتي(?: |$)(.*)")
async def story_upload(event):
    reply = await event.get_reply_message()
    r_caption = reply.text if reply.text else ""
    command_caption = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ رفـع الستوري (القصه) ع حسابك ...** ")
    if not reply:
        return await zed.edit("**⎉╎بالـرد ع صـورة او فيـديـو او اكثـر**\n**⎉╎لـ رفعهـا ستـوري ع حسابك ...**")
    if not reply.media:
        return await zed.edit("**⎉╎بالـرد ع صـورة او فيـديـو او اكثـر**\n**⎉╎لـ رفعهـا ستـوري ع حسابك ...**")
    # الحصول على التعليق من الرسالة الأصلية إن لم يكن هناك تعليق مع الأمر
    if command_caption: # Write Code by T.me/zzzzl1l
        final_caption = command_caption
    else:
        final_caption = r_caption
    media_files = []
    if reply.media:
        media_files.append(reply.media)
    # جمع الوسائط في المجموعة إذا كانت موجودة
    if hasattr(reply, 'media_group_id'):
        if reply.video or (reply.document and reply.document.mime_type.startswith('video')):  # التحقق من الفيديو
            async for message in zedub.iter_messages(reply.chat_id, filter=types.InputMessagesFilterDocument, grouped=reply.grouped_id):
                if message.grouped_id == reply.grouped_id and (message.video or message.document):
                    media_files.append(message.media)
        elif reply.photo:  # التحقق من الصورة
            async for message in zedub.iter_messages(reply.chat_id, filter=types.InputMessagesFilterPhotos, grouped=reply.grouped_id):
                if message.grouped_id == reply.grouped_id and message.photo:
                    media_files.append(message.media)
        else: #  في حالة كان الملف ليس صورة او فيديو
            return await zed.edit("⎉╎نوع الوسائط غير  مدعوم, الرجاء اختيار صورة او فيديو ❌")
    if not media_files:
        return await zed.edit("**⎉╎لم يتم العثور على وسائط ❌**\n**⎉╎حاول مرة اخرى في وقت لاحق ...⏳**")
    for media in media_files:
        try:
            file_path = await zedub.download_media(media, file="./downloaded_media/")
            await zed.edit(f"**⎉╎تم تحميل الميديا إلى** `{file_path}` ☑️\n**⎉╎جـارِ الرفـع الآن .. انتظر قليلاً ▬▭**")
            try:
                file = await zedub.upload_file(file_path)
                input_file = InputFile(
                    id=file.id,
                    parts=file.parts,
                    name=file.name,
                    md5_checksum=file.md5_checksum
                )
                try:
                    if media.video and reply.video:
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type='video/mp4',
                            attributes=[
                                types.DocumentAttributeVideo(duration=0, w=0, h=0),
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    elif media.photo and reply.photo:
                        input_media = types.InputMediaUploadedPhoto(file=input_file)
                    elif media.document: # إضافة شرط للتحقق من نوع "مستند"
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type=media.document.mime_type, #  الحصول على نوع الملف من الخصائص 
                            attributes=[
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    else:
                        await zed.edit("**- وسائط غيـر مدعومـه ❌**")
                        continue
                except Exception as e:
                    if media.photo and reply.photo:
                        input_media = types.InputMediaUploadedPhoto(file=input_file)
                    elif media.video and reply.video:
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type='video/mp4',
                            attributes=[
                                types.DocumentAttributeVideo(duration=0, w=0, h=0),
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    elif media.document: # إضافة شرط للتحقق من نوع "مستند"
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type=media.document.mime_type, #  الحصول على نوع الملف من الخصائص 
                            attributes=[
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    else:
                        await zed.edit("**- وسائط غيـر مدعومـه ❌**")
                        continue
                result = await zedub(functions.stories.SendStoryRequest(
                    media=input_media,
                    caption=final_caption,
                    privacy_rules=[types.InputPrivacyValueAllowContacts()],
                    peer='me'
                ))
                if hasattr(result, 'updates') and result.updates:
                    if hasattr(result.updates[0], 'id'):
                        story_id = result.updates[0].id
                        zuz = zedub.me.username if zedub.me.username else ""
                        story_link = f"https://t.me/{zuz}/s/{story_id}"
                        await zed.edit(f"**⎉╎تم رفـع القصة لحسابك .. بنجـاح ☑️**\n**⎉╎مسار الملف:** `{file_path}`\n**⎉╎رابـط الستوري: {story_link}**")
                    else:
                        await zed.edit(f"**⎉╎تم رفـع القصة لحسابك .. بنجـاح ☑️**\n**⎉╎مسار الملف:** `{file_path}`")
                else:
                    await zed.edit(f"**⎉╎تم رفـع القصة لحسابك .. بنجـاح ☑️**\n**⎉╎مسار الملف:** `{file_path}`")
                media_files.remove(reply.media)
            except Exception as e:
                if "STORIES_TOO_MUCH" in str(e):
                    return await zed.edit(f"**- اووبـس .. لقد تجاوزت الحد الأقصى ❌**\n**- لعدد القصص المسموح بها على تيليجرام 🚸**")
                elif "A premium account is required to execute this action" in str(e):
                    return await zed.edit(f"**- حسابك لا يدعم رفع القصص ❌**\n**- قم بالترقيه الى البريميوم 🌟**")
                else:
                    return await zed.edit(f"**- اووبـس .. حدث خطأ اثناء رفع القصة ❌**\n**- الخطـأ:**\n{str(e)}")
        except Exception as e:
            return await zed.edit(f"**- اووبـس .. حدث خطأ اثناء رفع القصة ❌**\n**- الخطـأ:**\n{str(e)}")


@zedub.zed_cmd(pattern="ستوري عام(?: |$)(.*)")
async def story_upload(event):
    reply = await event.get_reply_message()
    r_caption = reply.text if reply.text else ""
    command_caption = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ رفـع الستوري (القصه) ع حسابك ...** ")
    if not reply:
        return await zed.edit("**⎉╎بالـرد ع صـورة او فيـديـو او اكثـر**\n**⎉╎لـ رفعهـا ستـوري ع حسابك ...**")
    if not reply.media:
        return await zed.edit("**⎉╎بالـرد ع صـورة او فيـديـو او اكثـر**\n**⎉╎لـ رفعهـا ستـوري ع حسابك ...**")
    # الحصول على التعليق من الرسالة الأصلية إن لم يكن هناك تعليق مع الأمر
    if command_caption: # Write Code by T.me/zzzzl1l
        final_caption = command_caption
    else:
        final_caption = r_caption
    media_files = []
    if reply.media:
        media_files.append(reply.media)
    # جمع الوسائط في المجموعة إذا كانت موجودة
    if hasattr(reply, 'media_group_id'):
        if reply.video or (reply.document and reply.document.mime_type.startswith('video')):  # التحقق من الفيديو
            async for message in zedub.iter_messages(reply.chat_id, filter=types.InputMessagesFilterDocument, grouped=reply.grouped_id):
                if message.grouped_id == reply.grouped_id and (message.video or message.document):
                    media_files.append(message.media)
        elif reply.photo:  # التحقق من الصورة
            async for message in zedub.iter_messages(reply.chat_id, filter=types.InputMessagesFilterPhotos, grouped=reply.grouped_id):
                if message.grouped_id == reply.grouped_id and message.photo:
                    media_files.append(message.media)
        else: #  في حالة كان الملف ليس صورة او فيديو
            return await zed.edit("⎉╎نوع الوسائط غير  مدعوم, الرجاء اختيار صورة او فيديو ❌")
    if not media_files:
        return await zed.edit("**⎉╎لم يتم العثور على وسائط ❌**\n**⎉╎حاول مرة اخرى في وقت لاحق ...⏳**")
    for media in media_files:
        try:
            file_path = await zedub.download_media(media, file="./downloaded_media/")
            await zed.edit(f"**⎉╎تم تحميل الميديا إلى** `{file_path}` ☑️\n**⎉╎جـارِ الرفـع الآن .. انتظر قليلاً ▬▭**")
            try:
                file = await zedub.upload_file(file_path)
                input_file = InputFile(
                    id=file.id,
                    parts=file.parts,
                    name=file.name,
                    md5_checksum=file.md5_checksum
                )
                try:
                    if media.video and reply.video:
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type='video/mp4',
                            attributes=[
                                types.DocumentAttributeVideo(duration=0, w=0, h=0),
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    elif media.photo and reply.photo:
                        input_media = types.InputMediaUploadedPhoto(file=input_file)
                    elif media.document: # إضافة شرط للتحقق من نوع "مستند"
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type=media.document.mime_type, #  الحصول على نوع الملف من الخصائص 
                            attributes=[
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    else:
                        await zed.edit("**- وسائط غيـر مدعومـه ❌**")
                        continue
                except Exception as e:
                    if media.photo and reply.photo:
                        input_media = types.InputMediaUploadedPhoto(file=input_file)
                    elif media.video and reply.video:
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type='video/mp4',
                            attributes=[
                                types.DocumentAttributeVideo(duration=0, w=0, h=0),
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    elif media.document: # إضافة شرط للتحقق من نوع "مستند"
                        input_media = types.InputMediaUploadedDocument(
                            file=input_file,
                            mime_type=media.document.mime_type, #  الحصول على نوع الملف من الخصائص 
                            attributes=[
                                types.DocumentAttributeFilename(file.name)
                            ]
                        )
                    else:
                        await zed.edit("**- وسائط غيـر مدعومـه ❌**")
                        continue
                result = await zedub(functions.stories.SendStoryRequest(
                    media=input_media,
                    caption=final_caption,
                    privacy_rules=[types.InputPrivacyValueAllowAll()],
                    peer='me'
                ))
                if hasattr(result, 'updates') and result.updates:
                    if hasattr(result.updates[0], 'id'):
                        story_id = result.updates[0].id
                        zuz = zedub.me.username if zedub.me.username else ""
                        story_link = f"https://t.me/{zuz}/s/{story_id}"
                        await zed.edit(f"**⎉╎تم رفـع القصة لحسابك .. بنجـاح ☑️**\n**⎉╎مسار الملف:** `{file_path}`\n**⎉╎رابـط الستوري: {story_link}**")
                    else:
                        await zed.edit(f"**⎉╎تم رفـع القصة لحسابك .. بنجـاح ☑️**\n**⎉╎مسار الملف:** `{file_path}`")
                else:
                    await zed.edit(f"**⎉╎تم رفـع القصة لحسابك .. بنجـاح ☑️**\n**⎉╎مسار الملف:** `{file_path}`")
                media_files.remove(reply.media)
            except Exception as e:
                if "STORIES_TOO_MUCH" in str(e):
                    return await zed.edit(f"**- اووبـس .. لقد تجاوزت الحد الأقصى ❌**\n**- لعدد القصص المسموح بها على تيليجرام 🚸**")
                elif "A premium account is required to execute this action" in str(e):
                    return await zed.edit(f"**- حسابك لا يدعم رفع القصص ❌**\n**- قم بالترقيه الى البريميوم 🌟**")
                else:
                    return await zed.edit(f"**- اووبـس .. حدث خطأ اثناء رفع القصة ❌**\n**- الخطـأ:**\n{str(e)}")
        except Exception as e:
            return await zed.edit(f"**- اووبـس .. حدث خطأ اثناء رفع القصة ❌**\n**- الخطـأ:**\n{str(e)}")


async def download_all_stories(event, user_id):
    stories = await zedub(functions.stories.GetPeerStoriesRequest(
        peer=user_id
    ))
    
    for story in stories.stories.stories:
        file = await zedub.download_media(story.media)
        caption = story.caption if story.caption else "" # Get caption if exists
        yield file, caption 

@zedub.zed_cmd(pattern="ستوريات(?: |$)(.*)")
async def story_upload(event):
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    if input_str and not reply_message:
        if input_str.isnumeric():
            username = input_str
        if input_str.startswith("@"):
            username = input_str
    if input_str and reply_message:
        if input_str.isnumeric():
            username = input_str
        if input_str.startswith("@"):
            username = input_str
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        username = user.id
    zed = await edit_or_reply(event, f"**⎉╎جـارِ تحميـل ستوريات المستخدم {username}**\n**⎉╎الرجاء الانتظار لحظات ...⏳**")
    try:
        user = await event.client.get_entity(username)
    except Exception:
        return await zed.edit("**- عــذࢪاً .. لايمكــنني العثــوࢪ علـى المسـتخــدم ؟!**")
    user_id = user.id
    try:
        async for story, caption in download_all_stories(event, user_id):
            captioon=f"<b>{caption}\n\n• تم تحميـل الستوري .. بنجـاح 🪁\n• بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
            await zedub.send_file(event.chat_id, story, caption=captioon, parse_mode="html")
    except Exception as e:
        await zed.edit(f"- اووبـس .. حدث خطأ اثناء تحميل القصص ❌\n- الخطـأ:\n{str(e)}")
    await zed.delete()

