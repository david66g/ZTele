import asyncio
import math
import os
import io
import sys
import re
import urllib.request
import requests
import urllib3
import aiohttp
import random
import string
import time
import json
import shutil
import base64
import contextlib
from urllib.parse import quote
from datetime import datetime
from time import sleep
from googletrans import LANGUAGES, Translator
from PIL import Image
from io import BytesIO
from validators.url import url
from urlextract import URLExtract
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from telethon import events, types, functions, sync
from telethon.utils import get_peer_id, get_display_name
from telethon.tl.types import MessageService, MessageEntityMentionName, MessageActionChannelMigrateFrom, MessageEntityMentionName, InputPhoneContact, DocumentAttributeFilename
from telethon.errors import FloodWaitError, ChatForwardsRestrictedError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest, DeleteHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, GetAdminedPublicChannelsRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.contacts import BlockRequest as bloock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import InputSingleMedia, InputMediaPhoto

from . import zedub
from ..Config import Config
from ..utils import Zed_Vip
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers import media_type, progress, thumb_from_audio, sanga_seperator
from ..helpers.functions import convert_toimage, convert_tosticker, vid_to_gif
from ..helpers.utils import _zedtools, _zedutils, _format, parse_pre, reply_id
from . import BOTLOG, BOTLOG_CHATID, mention, deEmojify

extractor = URLExtract()

plugin_category = "الادوات"
ZGIF = gvarstatus("Z_GIF") or "(لمتحركه|لمتحركة|متحركه|متحركة)"
if not os.path.isdir("./temp"):
    os.makedirs("./temp")
gpsbb = '@openmap_bot'
storyz = '@tgstories_dl_bot'
ppdf = '@Photo22pdfbot'
LOGS = logging.getLogger(__name__)
Zel_Uid = zedub.uid
thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
cancel_process = False

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

def get_random_cat():
    api_url = 'https://api.thecatapi.com/v1/images/search'
    try:
        response = requests.get(api_url)
        cat_url = response.json()[0]['url']
        return cat_url
    except:
        return None

async def get_chatgpt_response(question):
    url = f"https://tbcai.flashninja000.workers.dev/?question={question}&state=omega"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["answer"]
    else:
        return None


lastResponse = None

async def process_gpt(question):
    global lastResponse
    if lastResponse is None:
        lastResponse = []
    url = "https://chat-gpt.hazex.workers.dev/"
    data = {
        "gpt": lastResponse,
        "user": str(question)
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                try:
                    get = await response.json()
                    print(get)
                    ans = get['answer']
                    return ans
                except Exception as e:
                    return False
            else:
                return False

async def dark_response(query):
    url = f'https://dark-gpt-v1.vercel.app/ai?query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data.get('response')
    else:
        return "Error fetching response."

async def gpt3_response(query):
    url = f'https://api-1stclass-hashierholmes.vercel.app/gpt/ada?question={query}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data.get('message')
    else:
        return "Error fetching response."

async def ai_img_gen(prompt):
    #image_url = 'https://img.hazex.workers.dev/?prompt={prompt}&improve=true&format=tall&random=Hj6Fq19j'
    # تعريف الباراميترات المطلوبة من ال API
    params = {
        'prompt': prompt,
        'improve': 'true',  # true or false the best is true
        'format': 'square',   # wide or tall or square
        'random': 'Hj6Fq19j'  # Replace with your random string
    }
    url = 'https://img.hazex.workers.dev/'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    else:
        return False

async def gemini_response(query):
    url = f'https://gemini.hazex.workers.dev/?ques={query}'
    response = requests.get(url)
    if response.status_code == 200:
        #data = json.loads(response.text)
        data = response.json()
        #print(data)
        return data["text"]
    else:
        return None
        #if not data.get("error"):
            #return data.get("text")
    #return None

async def geminiiii_response(query):
    url = f'https://gemini.hazex.workers.dev/?ques={query}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if not data.get("error"):
                    return data.get("text")
    return None

async def gemini_images(query):
    """
    البحث عن صور باستخدام Gemini AI API.

    Args:
        query: نص البحث.

    Returns:
        قائمة بعناوين URL للصور، أو  None  إذا لم يتم العثور على نتائج أو حدث خطأ.
Ex:
{"error":false,"text":null,"images":["https://i.imgur.com/123456.jpg"],"join":"@HazexAPI on Telegram","support":"@MrHazex"}
    """
    url = f"https://gemini.hazex.workers.dev/?ques={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if not data.get("error"):
            return data.get("images")
    return None

# Global variables to store image URLs
target_img = None
face_img = None

# Function to create a task
async def create_swap_task(target_img, face_img):
    # Face Swap API URL
    api_url = "https://face-swap.hazex.workers.dev/"
    params = {
        "function": "create_task",
        "target_img": target_img,
        "face_img": face_img
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("task_id")
    else:
        return None

# Function to check task status
async def check_swap_task(task_id):
    # Face Swap API URL
    api_url = "https://face-swap.hazex.workers.dev/"
    params = {
        "function": "check_task",
        "task_id": task_id
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("error") == False and data.get("result_img"):
            return data.get("result_img")
        else:
            return None
    else:
        return None

async def convert_webp_to_jpg(webp_url):
    response = requests.get(webp_url)
    webp_image = Image.open(BytesIO(response.content))
    jpg_image = webp_image.convert("RGB")
    jpg_image_path = "converted.jpg"
    jpg_image.save(jpg_image_path, "JPEG")
    return jpg_image_path


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

async def get_names(phone_number):
    try:
        contact = InputPhoneContact(client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = await zedub(functions.contacts.ImportContactsRequest([contact]))
        user = contacts.to_dict()['users'][0]
        username = user['username']
        if not username:
            username = "لايوجد"
        user_id = user['id']
        return username, user_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


@zedub.zed_cmd(pattern="اضف وسائط (الحماية|الحمايه|الفحص|فحص) ?(.*)")
async def _(malatha):
    if malatha.fwd_from:
        return
    zed = await edit_or_reply(malatha, "**⎉╎جـاري اضـافة فـار الكليشـة الكاملـة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    optional_title = malatha.pattern_match.group(2)
    if malatha.reply_to_msg_id:
        start = datetime.now()
        r_message = await malatha.get_reply_message()
        r_caption = r_message.text
        input_str = malatha.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            if r_caption:
                addgvar("pmpermit_txt", r_caption)
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
                await zed.edit("**⎉╎تم تعييـن الكليشـة الكاملـة لـ {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶ ميديـا + كليشـة**\n**⎉╎ارسـل الان الامـر : ↶** `.الحماية تفعيل`\n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str))
        elif input_str in ["الفحص", "فحص"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            if r_caption:
                addgvar("ALIVE_TEMPLATE", r_caption)
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
                await zed.edit("**⎉╎تم تعييـن الكليشـة الكاملـة لـ {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶ ميديـا + كليشـة**\n**⎉╎ارسـل الان الامـر : ↶** `.فحص`\n\n**⎉╎قنـاة السـورس : @ZThon**".format(input_str))
    else:
        await zed.edit("**⎉╎بالـرد ع صـورة او ميديـا لتعييـن الفـار ...**")

@zedub.zed_cmd(pattern=r"حفظ (.+)")
async def save_post(event):
    post_link = event.pattern_match.group(1)
    if not post_link:
        return await edit_or_reply(event, "**- يرجـى إدخـال رابـط المنشـور المقيـد بعـد الامـر ؟!**")
    save_dir = "media"
    os.makedirs(save_dir, exist_ok=True)
    if post_link.startswith("https://t.me/c/"):
        try:
            post_id = post_link.split("/")
            if len(post_id) >= 2:
                channel_username_or_id = int(post_id[-2])
                message_id = int(post_id[-1])
            else:
                return
        except Exception as e:
            return await edit_or_reply(event, f"**- اووبـس .. حدث خطأ أثناء حفظ الرسالة\n- تفاصيل الخطأ :**\n {str(e)}\n\n**- استخـدم الامـر الآخـر لـ حفـظ الملفـات المقيـده 🔳:\n- ارسـل** ( .احفظ ) **+ رابـط او بالـرد ع رابـط مقيـد**")
    else:
        try:
            post_id = post_link.split("/")
            if len(post_id) >= 2:
                channel_username_or_id = post_id[-2]
                message_id = int(post_id[-1])
            else:
                return await edit_or_reply(event, "**- رابـط غيـر صالـح ؟!**")
        except Exception as e:
            return await edit_or_reply(event, f"**- اووبـس .. حدث خطأ أثناء حفظ الرسالة\n- تفاصيل الخطأ :**\n {str(e)}\n\n**- استخـدم الامـر الآخـر لـ حفـظ الملفـات المقيـده 🔳:\n- ارسـل** ( .احفظ ) **+ رابـط او بالـرد ع رابـط مقيـد**")
    try:
        message = await zedub.get_messages(channel_username_or_id, ids=message_id)
        if not message:
            return await edit_or_reply(event, "**- رابـط غيـر صالـح ؟!**")
        if message.media:
            file_ext = ""
            if message.photo:
                file_ext = ".jpg"
            elif message.video:
                file_ext = ".mp4"
            elif message.document:
                if hasattr(message.document, "file_name") and message.document.file_name:
                    file_ext = os.path.splitext(message.document.file_name)[1]
                else:
                    for attr in message.document.attributes:
                        if isinstance(attr, DocumentAttributeFilename):
                            file_ext = os.path.splitext(attr.file_name)[1]
            file_path = os.path.join(save_dir, f"media_{message.id}{file_ext}")
            await zedub.download_media(message, file=file_path)
            if message.text:
                ahmed = await zedub.send_file(event.chat_id, file=file_path, caption=f"{message.text}")
                await zedub.send_message(event.chat_id, f"ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - حـفـظ المـحتـوى 🧧\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎ تـم جلب المنشـور المقيـد .. بنجـاح ☑️** ❝\n**⌔╎رابـط المنشـور** {post_link} .", reply_to=ahmed)
                os.remove(file_path)
                await event.delete()
            else:
                await zedub.send_file(event.chat_id, file=file_path, caption=f"[ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - حـفـظ المـحتـوى 🧧](t.me/ZThon) .\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎ تـم جلب المنشـور المقيـد .. بنجـاح ☑️** ❝\n**⌔╎رابـط المنشـور** {post_link} .")
                os.remove(file_path)
                await event.delete()
        else:
            if message.text:
                ali = await zedub.send_message(event.chat_id, f"{message.text}")
                await zedub.send_message(event.chat_id, f"ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - حـفـظ المـحتـوى 🧧\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎ تـم جلب المنشـور المقيـد .. بنجـاح ☑️** ❝\n**⌔╎رابـط المنشـور** {post_link} .", reply_to=ali)
                await event.delete()
            else:
                await edit_or_reply(event, "**- الرابط لا يحتوي على ميديا أو نص ؟!**")
    except Exception as e:
        return await edit_or_reply(event, f"**- اووبـس .. حدث خطأ أثناء حفظ الرسالة\n- تفاصيل الخطأ :**\n {str(e)}\n\n**- استخـدم الامـر الآخـر لـ حفـظ الملفـات المقيـده 🔳:\n- ارسـل** ( .احفظ ) **+ رابـط او بالـرد ع رابـط مقيـد**")

@zedub.zed_cmd(
    pattern="(الغاء محتوى|الغاء المحتوى)$",
    command=("الغاء المحتوى", plugin_category),
    info={
        "header": "إلغاء عملية حفظ الميديا.",
        "description": "يقوم بإلغاء العملية الجارية لحفظ الميديا من القنوات.",
        "usage": "{tr}الغاء المحتوى",
    },
)
async def save_posts(event):
    "إلغاء عملية حفظ الميديا."
    global cancel_process
    cancel_process = True
    await event.edit("**- تم إلغـاء عمليـة حفـظ الميـديا .. بنجـاح✅**")

@zedub.on(events.NewMessage(incoming=True))
async def check_cancel(event):
    global cancel_process
    if isinstance(event.message, MessageService) and event.message.action and isinstance(event.message.action, MessageActionChannelMigrateFrom):
        cancel_process = True

@zedub.zed_cmd(
    pattern="محتوى(?: |$)(.*) (\\d+)",
    command=("محتوى", plugin_category),
    info={
        "header": "حفظ الميديا من القنوات ذات تقييد المحتوى.",
        "description": "يقوم بحفظ الميديا (الصور والفيديوهات والملفات) من القنوات ذات تقييد المحتوى.",
        "usage": "{tr}محتوى + يـوزر القنـاة + عـدد الميديـا (الحـد)",
    },
)
async def save_posts(event):
    "حفظ الميديا من القنوات ذات تقييد المحتوى."
    global cancel_process
    channel_username = event.pattern_match.group(1)
    limit = int(event.pattern_match.group(2))
    if not channel_username:
        return await event.edit("**- يرجـى إدخـال يـوزر القنـاة بعـد الامـر ؟!**\n**- مثــال :**\n**. محتوى + يـوزر القنـاة + عـدد الميديـا التي تريـد جلبهـا (الحـد)**")
    if channel_username.startswith("@"):
        channel_username = channel_username.replace("@", "")
    save_dir = "media"
    os.makedirs(save_dir, exist_ok=True)
    try:
        channel_entity = await zedub.get_entity(channel_username)
        messages = await zedub.get_messages(channel_entity, limit=limit)
    except Exception as e:
        return await event.edit(f"**- اووبـس .. حدث خطأ أثناء جلب الرسـائل مـن القنـاة**\n**- تفاصيـل الخطـأ:**\n{str(e)}")
    for message in messages:
        try:
            if message.media:
                file_ext = ""
                if message.photo:
                    file_ext = ".jpg"
                elif message.video:
                    file_ext = ".mp4"
                elif message.document:
                    if hasattr(message.document, "file_name"):
                        file_ext = os.path.splitext(message.document.file_name)[1]
                    else:
                        # Handle documents without file_name attribute
                        file_ext = ""
                if not file_ext:
                    continue
                file_path = os.path.join(save_dir, f"media_{message.id}{file_ext}")
                await message.download_media(file=file_path)
                await zedub.send_file("me", file=file_path)
                os.remove(file_path)
            if cancel_process:
                await event.edit("**- تم إلغـاء عمليـة حفـظ الميـديا .. بنجـاح✅**")
                cancel_process = False
                return
        except Exception as e:
            print(f"حدث خطأ أثناء حفظ الرسالة {message.id}. الخطأ: {str(e)}")
            continue
    await event.edit(f"تم حفظ الميديا من القناة {channel_username} بنجاح.")

@zedub.zed_cmd(pattern="متحركات ?(.*)")
async def gifs(ult):
    get = ult.pattern_match.group(1)
    xx = random.randint(0, 5)
    n = 0
    if not get:
        return await edit_or_reply(ult, "**-ارسـل** `.متحركات` **+ نـص لـ البحـث**\n**- او** `.متحركات عدد` **+ العـدد**")
    if "عدد" in get:
        try:
            n = int(get.split("عدد")[-1])
        except BaseException:
            pass
    m = await edit_or_reply(ult, "**╮ جـارِ ﮼ البحـث ؏ الـمتحـركھہ 𓅫🎆╰**")
    gifs = await ult.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            ult.chat.id, reply_to=ult.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                ult.chat.id, reply_to=ult.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()

@zedub.zed_cmd(pattern="متحركاات(?: |$)(.*)")
async def some(event):
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not inpt:
        return await edit_or_reply(event, "**-ارسـل** `.متحركات` **+ نـص لـ البحـث**\n**- او** `.متحركات عدد` **+ العـدد**")
    count = 1
    if "عدد" in inpt:
        inpt, count = inpt.split("عدد")
    if int(count) < 0 and int(count) > 20:
        await edit_delete(event, "`Give value in range 1-20`")
    zedevent = await edit_or_reply(event, "**╮ جـارِ ﮼ البحـث ؏ الـمتحـركھہ 𓅫🎆╰**")
    res = requests.get("https://giphy.com/")
    res = res.text.split("GIPHY_FE_WEB_API_KEY =")[1].split("\n")[0]
    api_key = res[2:-1]
    r = requests.get(
        f"https://api.giphy.com/v1/gifs/search?q={inpt}&api_key={api_key}&limit=50"
    ).json()
    list_id = [r["data"][i]["id"] for i in range(len(r["data"]))]
    rlist = random.sample(list_id, int(count))
    for items in rlist:
        nood = await event.client.send_file(
            event.chat_id,
            f"https://media.giphy.com/media/{items}/giphy.gif",
            reply_to=reply_to_id,
        )
        await _zedutils.unsavegif(event, nood)
    await zedevent.delete()

@zedub.zed_cmd(pattern="(لمتحركه|لمتحركة|متحركه|متحركة)$")
async def zelzal_gif(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**╮ بالـرد ﮼؏ فيديـو للتحـويـل لمتحركـه ...𓅫╰**\n\n**-لـ البحث عن متحركـات :**\n**-ارسـل** `.متحركه` **+ نـص لـ البحـث**\n**- او** `.متحركه عدد` **+ العـدد**")
    chat = "@VideoToGifConverterBot"
    zed = await edit_or_reply(event, "**╮ جـارِ تحويـل الفيديـو لـ متحركـه ...𓅫╰**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_file(reply_message)
            await conv.get_response()
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await zed.delete()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎تم التحويل لمتحركه .. بنجاح 🎆</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zed.delete()
            await asyncio.sleep(3)
            await event.client(DeleteHistoryRequest(1125181695, max_id=0, just_clear=True))
        except YouBlockedUserError:
            await zedub(unblock("VideoToGifConverterBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_file(reply_message)
            await conv.get_response()
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎تم التحويل لمتحركه .. بنجاح 🎆</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zed.delete()
            await asyncio.sleep(3)
            await event.client(DeleteHistoryRequest(1125181695, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="(معالجه|تنقيه|تحسين|توضيح)$")
async def zelzal_ai(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لمعالجتهـا**")
    chat = "@PhotoFixerBot"
    zzz = await edit_or_reply(event, "**- جـارِ معالجـة الصـورة بالذكـاء الاصطناعـي ...💡╰**\n**- الرجاء الانتظار دقيقـه كاملـه لـ التحسيـن ..... 🍧╰**")
    await zedub(JoinChannelRequest(channel="@NeuralZone"))
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        except YouBlockedUserError:
            await zedub(unblock("PhotoFixerBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        zedthon1 = None
        response = await conv.get_response()
        await asyncio.sleep(1.5)
        if response.media:
            zedthon1 = response.media
        else:
            zedthon1 = await conv.get_response()
        response = await conv.get_response()
        if response.media:
            zedthon1 = response.media
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم معالجـة الصـورة .. بنجـاح 🎆</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        else:
            zedthon1 = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم معالجـة الصـورة .. بنجـاح 🎆</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(6314982389, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern=f"s(?: |$)(.*)")
async def zelzal_ss(event):
    malath = event.pattern_match.group(1)
    zilzal = None
    if malath:
        zelzal = malath
        zilzal = zelzal
    elif event.is_reply:
        zelzal = await event.get_reply_message()
        zilzal = zelzal.message
    else:
        return await edit_or_reply(event, "**⎉╎باضافة رابـط ستـوري لـ الامـر او بالـࢪد ؏ــلى رابـط الستـوري**")
    if not zilzal:
        return await edit_or_reply(event, "**⎉╎باضافة رابـط ستـوري لـ الامـر او بالـࢪد ؏ــلى رابـط الستـوري**")
    if ("https://t.me" not in zilzal) and ("/s/" not in zilzal):
        return await edit_delete(event, "**- قم بإدخـال رابـط ستـوري صالـح .. للتحميــل ❌**", 10)
    #chat_url = "https://t.me/msaver_bot?start=1895219306"
    zzz = await edit_or_reply(event, f"**- جـارِ تحميـل الستـوري انتظـر ... 🍧╰\n- رابـط الستـوري :\n{zilzal}**")
    chat = "@msaver_bot"
    async with borg.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message(zelzal)
        except YouBlockedUserError:
            await zedub(unblock("msaver_bot"))
            purgeflag = await conv.send_message(zelzal)
        response = await conv.get_response()
        await asyncio.sleep(3)
        if response.media:
            zedthon1 = response.media
        else:
            zedthon1 = await conv.get_response()
        await borg.send_file(
            event.chat_id,
            zedthon1,
            caption=f"<b>⎉╎تم تحميـل ستـوري تيليجرام .. بنجـاح 🎆\n⎉╎الرابـط 🖇:  {zilzal}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
            parse_mode="html",
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(6135950112, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="(انمي|كارتون)$")
async def zelzal_anime(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لتحويلهـا لـ انمـي**")
    chat = "@qq_neural_anime_bot"
    zzz = await edit_or_reply(event, "**- جـارِ تحويـل الصـورة لـ انمـي (كارتـون) ...💡╰**\n**- الرجاء الانتظار دقيقـه كاملـه ..... 🍧╰**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        except YouBlockedUserError:
            await zedub(unblock("qq_neural_anime_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        await conv.get_response()
        await asyncio.sleep(5)
        zedthon1 = await conv.get_response()
        await borg.send_file(
            event.chat_id,
            zedthon1,
            caption=f"<b>⎉╎تم تحويـل الصـورة .. بنجـاح 🍧🎆</b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(5894660331, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="سكانر$")
async def zelzal_scanner(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لاستخـراج النـص**")
    chat = "@rrobbootooBot"
    zzz = await edit_or_reply(event, "**- جـارِ استخـراج النـص من الصـورة ...💡╰\n- يجب ان تكـون الصـورة بدقـه واضحـه ... 🎟╰\n- الرجاء الانتظار دقيقـه كاملـه ..... 🍧╰**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
            #await conv.send_message("/ocr", reply_to=purgeflag)  # إرسال /ocr بالرد على الصورة داخل البوت
        except YouBlockedUserError:
            await zedub(unblock("rrobbootooBot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
            #await conv.send_message("/ocr", reply_to=purgeflag)  # إرسال /ocr بالرد على الصورة داخل البوت
        await conv.get_response()
        await asyncio.sleep(3)
        zedthon1 = await conv.get_response()
        replay_z = await borg.send_message(event.chat_id, zedthon1, reply_to=reply_message)
        await borg.send_message(event.chat_id, "**⎉╎تم استخـراج النـص من الصـورة .. بنجـاح 🍧🎆\n⎉╎بواسطـة @ZThon**", reply_to=replay_z)
        await zzz.delete()
        await asyncio.sleep(2)
        await event.client(DeleteHistoryRequest(1668602822, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="ازاله$")
async def zelzal_rr(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لـ ازالـة الخلفيـة**")
    chat = "@bgkillerbot"
    zzz = await edit_or_reply(event, "**- جـارِ ازالـة الخلفيـة مـن الصـورة ...💡╰**\n**- الرجاء الانتظار دقيقـه كاملـه ..... 🍧╰**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        except YouBlockedUserError:
            await zedub(unblock("bgkillerbot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        await conv.get_response()
        await asyncio.sleep(3)
        zedthon1 = await conv.get_response()
        if zedthon1.file:
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم ازالـة الخلفيـة من الصـورة .. بنجـاح 🍧🎆\n⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        else:
            zedthon1 = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم ازالـة الخلفيـة من الصـورة .. بنجـاح 🍧🎆\n⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(1744388227, max_id=0, just_clear=True))


@zedub.on(events.NewMessage(outgoing=True, pattern='.موقع (.*)'))
async def _(event):
    con = event.pattern_match.group(1) 
    sender = await event.get_sender()
    if sender.id != zedub.uid:
        return
    zid = int(gvarstatus("ZThon_Vip"))
    if Zel_Uid != zid:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    zzz = await event.edit("**⎉╎جـارِ البحث في خرائـط جـوجـل ...**")
    channel_entity = await zedub.get_entity(gpsbb)
    await zedub.send_message(gpsbb, '/start')
    await asyncio.sleep(0.5)
    msg0 = await zedub.get_messages(gpsbb, limit=1)
    await zedub.send_message(gpsbb, con)
    await asyncio.sleep(0.5)
    try:
        msg1 = await zedub.get_messages(gpsbb, limit=1)
        await msg1[0].click(2)
    except:
        await event.client(DeleteHistoryRequest(364791564, max_id=0, just_clear=True))
        return await zzz.edit("**⎉╎لم يتم العثـور ع الموقـع ...؟!**\n**⎉╎قم بادخـال الموقـع بشكـل صحيـح**")
    await asyncio.sleep(0.5)
    msg2 = await zedub.get_messages(gpsbb, limit=1)
    await msg2[0].click(2)
    await asyncio.sleep(0.5)
    msg3 = await zedub.get_messages(gpsbb, limit=1)
    await msg3[0].click(2)
    await asyncio.sleep(0.5)
    msg4 = await zedub.get_messages(gpsbb, limit=1)
    await zedub.send_file(
        event.chat_id,
        msg4[0],
        caption=f"<b>⎉╎تم جلب المـوقـع .. بنجـاح \n⎉╎</b><code>{con}</code>  🗺 \n<b>⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
        parse_mode="html",
    )
    await msg4[0].click(3)
    await asyncio.sleep(0.5)
    msg5 = await zedub.get_messages(gpsbb, limit=1)
    await zedub.send_file(
        event.chat_id,
        msg5[0],
        caption=f"<b>⎉╎تم الجلب عبـر الاقمـار الصناعيـه .. بنجـاح 🛰\n⎉╎</b><code>{con}</code>  🗺 \n<b>⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
        parse_mode="html",
    )
    await zzz.delete()
    await asyncio.sleep(2)
    await event.client(DeleteHistoryRequest(364791564, max_id=0, just_clear=True))

# Write code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="(عدسه|عدسة)$")
async def _(event): # Write code by T.me/zzzzl1l
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره/ملصق/فيديـو ...\n- لـ البحث فـي عدسـة جـوجـل**")
    zellzall = '@reverse_image_search_bot' # Write code by T.me/zzzzl1l)
    channel_entity = await zedub.get_entity(zellzall)
    zzz = await event.edit("**⎉╎جـارِ البحث في عدسـة جـوجـل ...🔍**")
    channel_entity = await zedub.get_entity(zellzall)
    await zedub.send_message(zellzall, '/start')
    await asyncio.sleep(2)
    msga = await zedub.get_messages(zellzall, limit=1)
    await zedub.send_file(zellzall, reply_message)
    await asyncio.sleep(2)
    msg1 = await zedub.get_messages(zellzall, limit=1)
    msg2 = await zedub.get_messages(zellzall, limit=1)
    await asyncio.sleep(3)
    try: # Write code by T.me/zzzzl1l
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        url_pic = msgs.reply_markup.rows[1].buttons[0].url
        url_snao = msgs.reply_markup.rows[2].buttons[0].url
        url_google = msgs.reply_markup.rows[2].buttons[1].url
        url_trace = msgs.reply_markup.rows[3].buttons[0].url
        url_iqdb = msgs.reply_markup.rows[3].buttons[1].url
        url_3d = msgs.reply_markup.rows[4].buttons[0].url
        url_yandex = msgs.reply_markup.rows[4].buttons[1].url
        url_baidu = msgs.reply_markup.rows[5].buttons[0].url
        url_bing = msgs.reply_markup.rows[5].buttons[1].url
        url_tineye = msgs.reply_markup.rows[6].buttons[0].url
        url_sogou = msgs.reply_markup.rows[6].buttons[1].url
        url_ascii2d = msgs.reply_markup.rows[7].buttons[0].url
        await asyncio.sleep(0.5)
        await zedub.send_file(
            event.chat_id,
            url_pic,
            caption=f"<b>⎉╎تم البحث عبـر عدسـة جـوجـل .. بنجـاح ☑️\n⎉╎بواسطـة سـورس <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a>\n⎉╎اليـك روابـط بنتائـج البحث لـ عـدة محركـات بحث :</b>\n\n<b><a href = {url_pic}>- رابــط الصــورة</a> 🖇\n\n<a href = {url_google}>- عدسـة جوجـل Google</a> 🌐\n\n<a href = {url_yandex}>- ياندكس Yandex</a> 〽️\n\n<a href = {url_bing}>- بينـج Bing</a> 🅿️\n\n<a href = {url_baidu}>- بايـدو Baidu</a> 🛜\n\n<a href = {url_snao}>- سوسـناو SauceNAO</a> 🈯️\n\n<a href = {url_sogou}>- سوجـو Sogou</a> ❇️\n\n<a href = {url_tineye}>- تينـآي TinEye</a> 🚺\n\n<a href = {url_trace}>- تـراك Trace</a> 🚼\n\n<a href = {url_iqdb}>- آي كيو ديبي IQDB</a> 🚾\n\n<a href = {url_3d}>- ثـري دي ديبي 3D IQDB</a> Ⓜ️\n\n<a href = {url_ascii2d}>- آسكـي Ascii2d</a> 🔡</b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await event.client(DeleteHistoryRequest(812573486, max_id=0, just_clear=True))
    except: # Write code by T.me/zzzzl1l
        try:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=2, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[1]
            url_pic = msgs.reply_markup.rows[1].buttons[0].url
            url_snao = msgs.reply_markup.rows[2].buttons[0].url
            url_google = msgs.reply_markup.rows[2].buttons[1].url
            url_trace = msgs.reply_markup.rows[3].buttons[0].url
            url_iqdb = msgs.reply_markup.rows[3].buttons[1].url
            url_3d = msgs.reply_markup.rows[4].buttons[0].url
            url_yandex = msgs.reply_markup.rows[4].buttons[1].url
            url_baidu = msgs.reply_markup.rows[5].buttons[0].url
            url_bing = msgs.reply_markup.rows[5].buttons[1].url
            url_tineye = msgs.reply_markup.rows[6].buttons[0].url
            url_sogou = msgs.reply_markup.rows[6].buttons[1].url
            url_ascii2d = msgs.reply_markup.rows[7].buttons[0].url
            await asyncio.sleep(0.5)
            await zedub.send_file(
                event.chat_id,
                url_pic,
                caption=f"<b>⎉╎تم البحث عبـر عدسـة جـوجـل .. بنجـاح ☑️\n⎉╎بواسطـة سـورس <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a>\n⎉╎اليـك روابـط بنتائـج البحث لـ عـدة محركـات بحث :</b>\n\n<b><a href = {url_pic}>- رابــط الصــورة</a> 🖇\n\n<a href = {url_google}>- عدسـة جوجـل Google</a> 🌐\n\n<a href = {url_yandex}>- ياندكس Yandex</a> 〽️\n\n<a href = {url_bing}>- بينـج Bing</a> 🅿️\n\n<a href = {url_baidu}>- بايـدو Baidu</a> 🛜\n\n<a href = {url_snao}>- سوسـناو SauceNAO</a> 🈯️\n\n<a href = {url_sogou}>- سوجـو Sogou</a> ❇️\n\n<a href = {url_tineye}>- تينـآي TinEye</a> 🚺\n\n<a href = {url_trace}>- تـراك Trace</a> 🚼\n\n<a href = {url_iqdb}>- آي كيو ديبي IQDB</a> 🚾\n\n<a href = {url_3d}>- ثـري دي ديبي 3D IQDB</a> Ⓜ️\n\n<a href = {url_ascii2d}>- آسكـي Ascii2d</a> 🔡</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zzz.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(812573486, max_id=0, just_clear=True))
        except: # Write code by T.me/zzzzl1l
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=3, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[2]
            url_pic = msgs.reply_markup.rows[1].buttons[0].url
            url_snao = msgs.reply_markup.rows[2].buttons[0].url
            url_google = msgs.reply_markup.rows[2].buttons[1].url
            url_trace = msgs.reply_markup.rows[3].buttons[0].url
            url_iqdb = msgs.reply_markup.rows[3].buttons[1].url
            url_3d = msgs.reply_markup.rows[4].buttons[0].url
            url_yandex = msgs.reply_markup.rows[4].buttons[1].url
            url_baidu = msgs.reply_markup.rows[5].buttons[0].url
            url_bing = msgs.reply_markup.rows[5].buttons[1].url
            url_tineye = msgs.reply_markup.rows[6].buttons[0].url
            url_sogou = msgs.reply_markup.rows[6].buttons[1].url
            url_ascii2d = msgs.reply_markup.rows[7].buttons[0].url
            await asyncio.sleep(0.5)
            await zedub.send_file(
                event.chat_id,
                url_pic,
                caption=f"<b>⎉╎تم البحث عبـر عدسـة جـوجـل .. بنجـاح ☑️\n⎉╎بواسطـة سـورس <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a>\n⎉╎اليـك روابـط بنتائـج البحث لـ عـدة محركـات بحث :</b>\n\n<b><a href = {url_pic}>- رابــط الصــورة</a> 🖇\n\n<a href = {url_google}>- عدسـة جوجـل Google</a> 🌐\n\n<a href = {url_yandex}>- ياندكس Yandex</a> 〽️\n\n<a href = {url_bing}>- بينـج Bing</a> 🅿️\n\n<a href = {url_baidu}>- بايـدو Baidu</a> 🛜\n\n<a href = {url_snao}>- سوسـناو SauceNAO</a> 🈯️\n\n<a href = {url_sogou}>- سوجـو Sogou</a> ❇️\n\n<a href = {url_tineye}>- تينـآي TinEye</a> 🚺\n\n<a href = {url_trace}>- تـراك Trace</a> 🚼\n\n<a href = {url_iqdb}>- آي كيو ديبي IQDB</a> 🚾\n\n<a href = {url_3d}>- ثـري دي ديبي 3D IQDB</a> Ⓜ️\n\n<a href = {url_ascii2d}>- آسكـي Ascii2d</a> 🔡</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zzz.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(812573486, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="انستا(?: |$)(.*)")
async def zelzal_insta(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.انستا) + رابـط او بالـرد ع رابـط**", 10)
    if "instagram.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من الانستـا .. للتحميــل ؟!**", 10)
    if link.startswith("https://instagram"):
        link = link.replace("https://instagram", "https://www.instagram")
    if link.startswith("http://instagram"):
        link = link.replace("http://instagram", "http://www.instagram")
    if "/reel/" in link:
        cap_zzz = f"<b>⎉╎تم تحميـل مقطـع انستـا (ريلـز) .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    elif "/tv/" in link:
        cap_zzz = f"<b>⎉╎تم تحميـل بث انستـا (Tv) .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    elif "/stories/" in link:
        cap_zzz = f"<b>⎉╎تم تحميـل ستـوري انستـا .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵??𝗻</a> </b>"
    else:
        cap_zzz = f"<b>⎉╎تم تحميـل مقطـع انستـا .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@story_repost_bot"
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من الانستـا .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(2036153627, max_id=0, just_clear=True))
        except YouBlockedUserError:
            await zedub(unblock("story_repost_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(2036153627, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="تيك(?: |$)(.*)")
async def zelzal_insta(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_delete(event, "**- ارسـل (.تيك) + رابـط او بالـرد ع رابـط**", 10)
    if "tiktok.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من تيـك تـوك .. للتحميــل ؟!**", 10)
    cap_zzz = f"<b>⎉╎تم تحميـل مـن تيـك تـوك .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@downloader_tiktok_bot"
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من تيـك تـوك .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))
        except YouBlockedUserError:
            await zedub(unblock("downloader_tiktok_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(1332941342, max_id=0, just_clear=True))

#Code by T.me/zzzzl1l
"""
@zedub.zed_cmd(pattern="تحميل صوت(?: |$)([\s\S]*)")
async def zelzal_insta(event): #Code by T.me/zzzzl1l
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/zzzzl1l
        link = reply.text
    if not link: #Code by T.me/zzzzl1l
        return await edit_delete(event, "**- ارسـل (.تحميل صوت) + رابـط او بالـرد ع رابـط**", 10)
    cap_zzz = f"<b>⎉╎تم تحميـل مـن يـوتيـوب .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@u2b2mp3_bot" #Code by T.me/zzzzl1l
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من يـوتيـوب .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv: #Code by T.me/zzzzl1l
        try: #Code by T.me/zzzzl1l
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/zzzzl1l
            await conv.get_response()
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(5512501816, max_id=0, just_clear=True))
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("u2b2mp3_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/zzzzl1l
            await conv.get_response()
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(5512501816, max_id=0, just_clear=True))
"""

#Code by T.me/zzzzl1l
"""
@zedub.zed_cmd(pattern="تحميل فيديو(?: |$)([\s\S]*)")
async def zelzal_vvid(event): #Code by T.me/zzzzl1l
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/zzzzl1l
        link = reply.text
    if not link: #Code by T.me/zzzzl1l
        return await edit_delete(event, "**- ارسـل (.تحميل فيديو) + رابـط او بالـرد ع رابـط**", 10)
    cap_zzz = f"<b>⎉╎تم تحميـل مـن يـوتيـوب .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chatbot = "@YtbDownBot" #Code by T.me/zzzzl1l
    zzz = await edit_or_reply(event, "**⎉╎جـارِ التحميل من يـوتيـوب .. انتظر قليلا ▬▭**")
    try:
        send = await zedub.send_message(chatbot, '/start')
    except YouBlockedUserError: #Code by T.me/zzzzl1l
        await zedub(unblock("YtbDownBot"))
        send = await zedub.send_message(chatbot, '/start')
    sleep(2)
    song = await zedub.send_message(chatbot, link)
    sleep(1)
    msg1 = await zedub.get_messages(chatbot, limit=1)
    sleep(0.5)
    await msg1[0].click(1)
    sleep(2)
    msgt = await zedub.get_messages(chatbot, limit=1)
    song_file = msgt[0].media
    try:
        await zedub.send_file(
            event.chat_id,
            song_file,
            caption=cap_zzz,
            parse_mode="html",
        )
        await zzz.delete()
    except ChatSendMediaForbiddenError: # Code By T.me/zzzzl1l
        await zzz.edit("**- عـذراً .. الوسـائـط مغلقـه هنـا ؟!**")
    await event.client(DeleteHistoryRequest(794633388, max_id=0, just_clear=True))
"""

#Code by T.me/zzzzl1l
"""
@zedub.zed_cmd(pattern="فيس(?: |$)([\s\S]*)")
async def zelzal_insta(event): #Code by T.me/zzzzl1l
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/zzzzl1l
        link = reply.text
    if not link: #Code by T.me/zzzzl1l
        return await edit_delete(event, "**- ارسـل (.فيس) + رابـط او بالـرد ع رابـط**", 10)
    if "share/r" in link:
        return await edit_delete(event, "**- قم باستخـدام الامـر (.تيك + الرابط) لتحميل هذا النـوع من الفيديوهـات**", 10)
    if ("https://fb" not in link) and ("facebook.com" not in link):
        return await edit_delete(event, "**- احتـاج الـى رابــط من فيـس بـوك .. للتحميــل ؟!**", 10)
    if link.startswith("https://fb.watch"):
        link = link.replace("https://fb.watch", "https://www.facebook.com/watch")
    if link.startswith("http://fb.watch"):
        link = link.replace("http://fb.watch", "http://www.facebook.com/watch")
    cap_zzz = f"<b>⎉╎تم تحميـل مـن فيـس بـوك .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@FBDLBOT" #Code by T.me/zzzzl1l
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من فيـس بـوك .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv: #Code by T.me/zzzzl1l
        try: #Code by T.me/zzzzl1l
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/zzzzl1l
            await conv.get_response()
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(6361899360, max_id=0, just_clear=True))
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("FBDLBOT"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/zzzzl1l
            await conv.get_response()
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(6361899360, max_id=0, just_clear=True))
"""

#Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="(النص|لنص)$")
async def zelzal_ai(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع بصمـه (تسجيـل صـوتـي) .. لـ استخـراج النـص منهـا**")
    chat = "@Speechpro_ASR_bot"
    zzz = await edit_or_reply(event, "**- جـارِ إستخـراج النـص مـن الصـوت . . .🎙╰\n- الرجـاء الانتظـار دقيـقـه . . .⏳╰**")
    async with borg.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message("/lang ara")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        except YouBlockedUserError:
            await zedub(unblock("Speechpro_ASR_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message("/lang ara")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
        zm = await conv.get_response()
        ztxt = zm.message
        await borg.send_message(
            event.chat_id,
            f"<b>{ztxt}\n\n<a href = https://t.me/ZThon/1>𓆩 𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𓆪</a> </b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(916427203, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="كتاب(?: |$)(.*)")
async def zelzal_gif(event):
    zelzal = str(event.pattern_match.group(1))
    if not zelzal:
        return await edit_or_reply(event, "**- ارسـل (.كتاب) + اسـم الكتـاب ...**")
    chat = "@GoogleBooksSearchBot" 
    zed = await edit_or_reply(event, "**⎉╎جـارِ البحث عن الكتـاب المحـدد ...**")
    async with borg.conversation(chat) as conv: 
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
        except YouBlockedUserError:
            await zedub(unblock("GoogleBooksSearchBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
        try:
            zedthon1 = await conv.get_response()
            malath1 = zedthon1.text
            if "Find books with" in malath1: 
                zz1 = malath1.replace("Find books with @GoogleBooksSearchBot", "📕\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await zed.delete()
                await borg.send_file(
                    event.chat_id,
                    zedthon1,
                    caption=zz1,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon2 = await conv.get_response()
            malath2 = zedthon2.text
            if "Find books with" in malath2: 
                zz2 = malath2.replace("Find books with @GoogleBooksSearchBot", "📗\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon2,
                    caption=zz2,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon3 = await conv.get_response()
            malath3 = zedthon3.text
            if "Find books with" in malath3: 
                zz3 = malath3.replace("Find books with @GoogleBooksSearchBot", "📘\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon3,
                    caption=zz3,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon4 = await conv.get_response()
            malath4 = zedthon4.text
            if "Find books with" in malath4: 
                zz4 = malath3.replace("Find books with @GoogleBooksSearchBot", "📙\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon4,
                    caption=zz4,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon5 = await conv.get_response()
            malath5 = zedthon5.text
            if "Find books with" in malath5: 
                zz5 = malath5.replace("Find books with @GoogleBooksSearchBot", "📚\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon5,
                    caption=zz5,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon6 = await conv.get_response()
            malath6 = zedthon6.text
            if "Find books with" in malath6: 
                zz6 = malath6.replace("Find books with @GoogleBooksSearchBot", "📖\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon6,
                    caption=zz6,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon7 = await conv.get_response()
            malath7 = zedthon7.text
            if "Find books with" in malath7: 
                zz7 = malath7.replace("Find books with @GoogleBooksSearchBot", "📔\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon7,
                    caption=zz7,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon8 = await conv.get_response()
            malath8 = zedthon8.text
            if "Find books with" in malath8: 
                zz8 = malath8.replace("Find books with @GoogleBooksSearchBot", "📒\n<b>- تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon8,
                    caption=zz8,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))

# Code by T.me/zzzzl1l
"""
@zedub.zed_cmd(pattern=f"ستوريات(?: |$)(.*)")
async def zelzal_ai(event):
    malath = event.pattern_match.group(1)
    zid = int(gvarstatus("ZThon_Vip"))
    if Zel_Uid != zid:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    if malath: #Write Code By T.me/zzzzl1l
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة يـوزر الشخـص لـ الامـر**")
    zzz = await event.edit("**⎉╎جـارِ تحميـل ستـوريـات الشخـص ...**")
    channel_entity = await zedub.get_entity(storyz)
    await zedub.send_message(storyz, '/start')
    await asyncio.sleep(0.5)
    await zedub.get_messages(storyz, limit=1)
    await zedub.send_message(storyz, f"/dlStories {zelzal}")
    await asyncio.sleep(2)
    await zedub.get_messages(storyz, limit=1)
    messages = await zedub.get_messages(storyz, limit=None)
    await asyncio.sleep(0.5)
    for message in messages:
        if "- ID" in message.text:
            entities = message.entities
            mentions = [entity for entity in entities if isinstance(entity, (types.MessageEntityTextUrl, types.MessageEntityUrl))]
            if mentions:
                for mention in mentions:
                    urs = str(mention)
                    urls = extractor.find_urls(urs)
                    for url in urls:
                        try:
                            await zedub.send_file(
                                event.chat_id,
                                url,
                                caption=f"**⎉╎تم جلب الستـوري .. بنجـاح ☑️\n⎉╎من الحسـاب {zelzal}\n⎉╎بواسطـة 𝗭𝗧𝗵𝗼𝗻**",
                            )
                            await asyncio.sleep(2)
                        except:
                            pass
        else:
            return await zzz.edit("**⎉╎تعـذر العثـور ع الستـوري ...؟!**\n**⎉╎حـال مجـدداً وقت لاحـق**")
"""

@zedub.zed_cmd(pattern="قط$")
async def zelzal_ss(event):
    zzz = await edit_or_reply(event, "** 🐈 . . .**")
    cat_url = get_random_cat()
    await zzz.delete()
    await bot.send_file(
        event.chat_id,
        cat_url,
        caption=f"<b>⎉╎صـورة قـط عشـوائـي .. 🐈 🎆\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
        parse_mode="html",
    )


"""
@zedub.zed_cmd(pattern="زد(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.زد من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    chat = "@gpt3_unlim_chatbot" 
    async with borg.conversation(chat) as conv: 
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(question)
        except YouBlockedUserError:
            await zedub(unblock("gpt3_unlim_chatbot"))
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(question)
        zlz = await conv.get_response()
        ztxt = zlz.message
        await zed.delete()
        await borg.send_message(event.chat_id, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗖𝗵𝗮𝘁𝗚𝗽𝘁 -💡-](t.me/ZThon) **الذكاء الاصطناعي\n⋆──┄─┄─┄───┄─┄─┄──⋆**\n**• س/ {question}\n\n• {ztxt}**", link_preview=False)
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(5815596965, max_id=0, just_clear=True))

@zedub.zed_cmd(pattern="س(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.زد من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    chat = "@gpt3_unlim_chatbot" 
    async with borg.conversation(chat) as conv: 
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(question)
        except YouBlockedUserError:
            await zedub(unblock("gpt3_unlim_chatbot"))
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(question)
        zlz = await conv.get_response()
        ztxt = zlz.message
        await zed.delete()
        await borg.send_message(event.chat_id, f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗖𝗵𝗮𝘁𝗚𝗽𝘁 -💡-](t.me/ZThon) **الذكاء الاصطناعي\n⋆──┄─┄─┄───┄─┄─┄──⋆**\n**• س/ {question}\n\n• {ztxt}**", link_preview=False)
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(5815596965, max_id=0, just_clear=True))
"""


@zedub.zed_cmd(pattern="زد(?: |$)(.*)")
async def zelzal_gpt(event):
    global lastResponse
    if lastResponse is None:
        lastResponse = []
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.زد من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    if question == "مسح" or question == "حذف":
        lastResponse.pop(0)
        return await edit_or_reply(event, "**⎉╎تم حذف سجل الذكاء الاصطناعي .. بنجاح ✅**\n**⎉╎ارسـل الان(.زد + سؤالك) لـ البـدء من جديد**")
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي**\n**⎉╎الرجـاء الانتظـار .. لحظـات**\n\n**⎉╎ملاحظـه 🏷**\n- هذا النموذج يقوم بحفظ الموضوعات السابقة\n- اذا كان لديك اكثر من سؤال لـ نفس الموضوع\n- وتريد تقديم الاسئله رداً على الاجوبة السابقة\n**- لـ مسح سجل تخزين الموضوعات السابقة**\n**- ارسـل الامـر** ( `.زد مسح` ) **لـ بدء موضوع جديد**")
    answer = await process_gpt(question)
    if answer:
        await zed.edit(f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗭𝗧𝗚𝗽𝘁 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {question}**\n\n• {answer}", link_preview=False)
        lastResponse.append(str(answer))
        if len(lastResponse) > 8:
            lastResponse.pop(0)

"""
# القديم
@zedub.zed_cmd(pattern="س(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.س من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    answer = await get_chatgpt_response(question)
    await zed.edit(f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗖𝗵𝗮𝘁𝗚𝗽𝘁 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {question}**\n\n• {answer}", link_preview=False)
"""

@zedub.zed_cmd(pattern="س(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.س من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    answer = await gpt3_response(question)
    await zed.edit(f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗖𝗵𝗮𝘁𝗚𝗽𝘁 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {question}**\n\n• {answer}", link_preview=False)


@zedub.zed_cmd(pattern="دارك(?: |$)(.*)")
async def dark_ai(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    query = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not query and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.دارك من هو مكتشف الجاذبية الارضية`")
    if not query and event.reply_to_msg_id and zzz.text: 
        query = zzz.text
    if not event.reply_to_msg_id: 
        query = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي (Dark)\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    try:
        querys = query.strip()
        translator = Translator()
        lan = "en" 
        translated = translator.translate(querys, dest=lan)
        querry = translated.text
    except Exception:
        querry = query
    answer = await dark_response(querry)
    try:
        answers = answer.strip()
        translator = Translator()
        lan = "ar" 
        translated = translator.translate(answers, dest=lan)
        after_tr_text = translated.text
        await zed.edit(f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗗𝗮𝗿𝗸𝗔𝗶 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {query}**\n\n• {after_tr_text}", link_preview=False)
        #await zed.delete()
    except Exception as exc:
        #await zed.edit(f"**- خطـأ :**\n`{exc}`", time=5)
        await zed.edit(f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗗𝗮𝗿𝗸𝗔𝗶 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {query}**\n\n• {answer}", link_preview=False)


@zedub.zed_cmd(pattern="gpt(?: |$)(.*)")
async def gpt3_ai(event):
    query = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not query and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.دارك من هو مكتشف الجاذبية الارضية`")
    if not query and event.reply_to_msg_id and zzz.text: 
        query = zzz.text
    if not event.reply_to_msg_id: 
        query = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    answer = await gpt3_response(query)
    await zed.edit(answer)

@zedub.zed_cmd(pattern="جيمي(?: |$)(.*)")
async def gemini_ai(event):
    query = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not query and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.جيمي من هو مكتشف الجاذبية الارضية`")
    if not query and event.reply_to_msg_id and zzz.text: 
        query = zzz.text
    if not event.reply_to_msg_id: 
        query = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي (Gemini)\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    try:
        querys = query.strip()
        translator = Translator()
        lan = "en" 
        translated = translator.translate(querys, dest=lan)
        querry = translated.text
        #print(query)
    except Exception:
        querry = query
    answer = await gemini_response(querry)
    try:
        answers = answer.strip()
        translator = Translator()
        lan = "ar" 
        translated = translator.translate(answers, dest=lan)
        after_tr_text = translated.text
        print(after_tr_text)
        await zed.edit(f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗲𝗺𝗶𝗻𝗶 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {query}**\n\n• {after_tr_text}", link_preview=False)
        #await zed.delete()
    except Exception as exc:
        #await zed.edit(f"**- خطـأ :**\n`{exc}`", time=5)
        await zed.edit(f"ᯓ .𝗭𝗧𝗵𝗼𝗻 𝗚𝗲𝗺𝗶𝗻𝗶 -💡- **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• س/ {query}**\n\n• {exc}", link_preview=False)

@zedub.zed_cmd(pattern="جيم(?: |$)(.*)")
async def dark_ai(event):
    prompt = event.pattern_match.group(1)
    query = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not query and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.جيم من هو مكتشف الجاذبية الارضية`")
    if not query and event.reply_to_msg_id and zzz.text: 
        query = zzz.text
        prompt = zzz.text
    if not event.reply_to_msg_id: 
        query = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي (Gemini)\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    try:
        query = query.strip()
        translator = Translator()
        lan = "en" 
        translated = translator.translate(query, dest=lan)
        querry = translated.text
        query = f"img {querry}"
    except Exception:
        pass
    images = await gemini_images(query)
    if images:
        #  تحميل  الصور  في  قائمة 
        input_media = []
        for image_url in images:
            input_media.append(image_url)
        if input_media:
            await zedub.send_file(event.chat_id, input_media, caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗚𝗲𝗺𝗶𝗻𝗶.𝗔𝗶 -💡-](t.me/ZThon) **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• تم البحث عن الصـور 📇**\n**• بواسطة الذكاء الاصطناعي💡**\n• `{prompt}`")
            await zzz.delete()
        else:
            await zzz.edit(f"**- اووبـس .. لم استطـع ايجـاد صـور عـن {prompt} ؟!**\n**- حـاول مجـدداً واكتـب الكلمـه بشكـل صحيح**")
            return
        #  حذف  الملفات  المؤقتة 
        for each_file in input_media:
            os.remove(each_file)
        shutil.rmtree(wzed_dir, ignore_errors=True)
    else:
        await event.reply(f"لم يتم العثور على صور لـ '{prompt}")

@zedub.zed_cmd(pattern="ارسم ?(.*)")
async def search_photo(event):
    prompt = event.pattern_match.group(1)
    if not prompt:
        return await edit_or_reply(event, "**-ارسـل** `.ارسم` **+ نـص لـ البـدء**")
    wzed_dir = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY,
        prompt
    )
    if not os.path.isdir(wzed_dir):
        os.makedirs(wzed_dir)
    zzz = await edit_or_reply(event, "**╮ ❐ جـاري رسـم الصـور بواسطـة الذكـاء الاصطنـاعـي ...𓅫╰**")
    image_urls = await ai_img_gen(prompt)

    if image_urls:
        #  تحميل  الصور  في  قائمة 
        input_media = []
        for i in range(10): #  تحميل  حتى  10  صور 
            try:
                image_url = await ai_img_gen(prompt)
                image_save_path = os.path.join(
                    wzed_dir,
                    f"{prompt}_{i}.jpg"
                )
                with open(image_save_path, "wb") as f:
                    f.write(image_url)
                input_media.append(image_save_path)
            except Exception as e:
                print(f"حدث خطأ أثناء تحميل الصورة: {e}")

        #  إرسال  جميع  الصور  في  رسالة  واحدة 
        if input_media:
            await zedub.send_file(event.chat_id, input_media, caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗣𝗵𝗼𝘁𝗼.𝗔𝗶 -💡-](t.me/ZThon) **الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• تم رسم ³ صور 📇**\n**• بواسطة الذكاء الاصطناعي💡**\n• `{prompt}`")
            await zzz.delete()
        else:
            await zzz.edit(f"**- اووبـس .. لم استطـع ايجـاد صـور عـن {prompt} ؟!**\n**- حـاول مجـدداً واكتـب الكلمـه بشكـل صحيح**")
            return
        #  حذف  الملفات  المؤقتة 
        for each_file in input_media:
            os.remove(each_file)
        shutil.rmtree(wzed_dir, ignore_errors=True)
    else:
        await event.reply(f"لم يتم العثور على صور لـ '{prompt}")


@zedub.zed_cmd(pattern="(pdf|نص pdf)$")
async def zelzal_ai(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع رسالـة (نص) .. لـ طباعتهـا لـ  مـلف PDF**")
    chat = "@pdfbot"
    zzz = await edit_or_reply(event, "**- جـارِ طباعـة النـص الـى ملـف PDF . . .📕╰\n- الرجـاء الانتظـار ثوانـي . . .⏳╰**")
    async with borg.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/text")
            await conv.get_response()
            await conv.send_message(reply_message)
            await conv.get_response()
            await conv.send_message("Noto Naskh Arabic")
        except YouBlockedUserError:
            await zedub(unblock("pdfbot"))
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/text")
            await conv.get_response()
            await conv.send_message(reply_message)
            await conv.get_response()
            await conv.send_message("Noto Naskh Arabic")
        zedthon1 = await conv.get_response()
        if zedthon1.file:
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم تحويـل النص الى PDF .. بنجـاح 🍧📕\n⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        else:
            zedthon1 = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم تحويـل النص الى PDF .. بنجـاح 🍧📕\n⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(381839844, max_id=0, just_clear=True))


@zedub.on(events.NewMessage(outgoing=True, pattern='.صورة pdf$'))
async def _(event):
    reply_message = await event.get_reply_message()
    zzz = await edit_or_reply(event, "**- جـارِ طباعـة الصـورة الـى ملـف PDF . . .📕╰\n- الرجـاء الانتظـار ثوانـي . . .⏳╰**")
    channel_entity = await zedub.get_entity(ppdf)
    await zedub.send_message(ppdf, '/start')
    await asyncio.sleep(0.5)
    msg0 = await zedub.get_messages(ppdf, limit=1)
    await zedub.send_file(ppdf, reply_message)
    await asyncio.sleep(0.5)
    try:
        msg1 = await zedub.get_messages(ppdf, limit=1)
        await msg1[0].click(0)
    except:
        await event.client(DeleteHistoryRequest(1549375781, max_id=0, just_clear=True))
        return await zzz.edit("**⎉╎اووبـس حـدث خطـأ ...؟!**\n**⎉╎حـاول مجـدداً في وقت لاحـق**")
    await asyncio.sleep(0.5)
    msg2 = await zedub.get_messages(ppdf, limit=1)
    await msg2[0].click(0)
    await asyncio.sleep(0.5)
    msg3 = await zedub.get_messages(ppdf, limit=1)
    await asyncio.sleep(0.5)
    msg4 = await zedub.get_messages(ppdf, limit=1)
    await zedub.send_file(
        event.chat_id,
        msg4[0],
        caption=f"<b>⎉╎تم تحويـل الصـورة الى PDF .. بنجـاح 🍧📕\n⎉╎بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
        parse_mode="html",
    )
    await zzz.delete()
    await event.client(DeleteHistoryRequest(1549375781, max_id=0, just_clear=True))



@zedub.zed_cmd(pattern="كشف(?: |$)(.*)")
async def zelzal_gif(event):
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    if input_str and not reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if input_str and reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        uid = user.id
    #user = await get_user_from_event(event)
    #if not user:
        #return
    #uid = user.id
    chat = "@SangMata_beta_bot" 
    zed = await edit_or_reply(event, "**⎉╎جـارِ الكشـف ...**")
    async with borg.conversation(chat) as conv: 
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        except YouBlockedUserError:
            await zedub(unblock("SangMata_beta_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        zlz = await conv.get_response()
        mallath = zlz.text
        if "No data available" in mallath: 
            zzl = "<b>⎉╎المستخدم ليس لديه أي سجل اسمـاء بعـد ...</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "Sorry, you have used up your quota for today" in zlz.text:
            zzl = "<b>⎉╎عـذراً .. لقد استنفدت محاولاتك لهذا اليوم.\n⎉╎لديـك 5 محاولات فقط كل يوم\n⎉╎يتم تحديث محاولاتك في الساعة 03:00 بتوقيت مكة كل يوم</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "👤 History for" in mallath:
            zzl = mallath.replace("👤 History for", "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - <b>سجـل الحسـاب 🪪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔ تم جلب السجـلات .. بنجـاح ☑️</b> ❝") 
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        await zed.delete()
        return await borg.send_message(event.chat_id, zlz, parse_mode="html")


@zedub.zed_cmd(pattern="الاسماء(?: |$)(.*)")
async def zelzal_gif(event):
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    if input_str and not reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if input_str and reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        uid = user.id
    #user = await get_user_from_event(event)
    #if not user:
        #return
    #uid = user.id
    chat = "@SangMata_beta_bot" 
    zed = await edit_or_reply(event, "**⎉╎جـارِ الكشـف ...**")
    async with borg.conversation(chat) as conv: 
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        except YouBlockedUserError:
            await zedub(unblock("SangMata_beta_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        zlz = await conv.get_response()
        mallath = zlz.text
        if "No data available" in mallath: 
            zzl = "<b>⎉╎المستخدم ليس لديه أي سجل اسمـاء بعـد ...</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "Sorry, you have used up your quota for today" in zlz.text:
            zzl = "<b>⎉╎عـذراً .. لقد استنفدت محاولاتك لهذا اليوم.\n⎉╎لديـك 5 محاولات فقط كل يوم\n⎉╎يتم تحديث محاولاتك في الساعة 03:00 بتوقيت مكة كل يوم</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "👤 History for" in mallath:
            zzl = mallath.replace("👤 History for", "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - <b>سجـل الحسـاب 🪪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔ تم جلب السجـلات .. بنجـاح ☑️</b> ❝") 
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        await zed.delete()
        return await borg.send_message(event.chat_id, zlz, parse_mode="html")


@zedub.zed_cmd(pattern="تحقق ?(.*)")
async def check_user(event):
    input_str = event.pattern_match.group(1)
    if input_str.startswith("+"):
        phone_number = event.pattern_match.group(1)
    else:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي ...𓅫 :**\n`.تحقق` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.تحقق +967777118223")
    try:
        username, user_id = await get_names(phone_number)
        if user_id:
            await edit_or_reply(event, f"ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟\n**⋆─┄─┄─┄─┄─┄─┄─⋆**\n**• معلومـات حسـاب تيليجـرام 📑 :**\n**- اليـوزر :** @{username}\n**- الايـدي :** `{user_id}`")
        else:
            await edit_or_reply(event, "**- الرقـم ليس مسجـل بعـد على تيليجـرام !!**")
    except Exception as e:
        print(f"An error occurred: {e}")


@zedub.zed_cmd(pattern="احفظ(?: |$)(.*)")
async def zelzal_ss(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await edit_or_reply(event, "**⎉╎باضافة رابـط منشـور لـ الامـر او بالـࢪد ؏ــلى رابـط المنشـور المقيـد**")
    if not link.startswith("https://t.me/"):
        return await edit_or_reply(event, "**⎉╎باضافة رابـط منشـور لـ الامـر او بالـࢪد ؏ــلى رابـط المنشـور المقيـد**")
    if "?single" in link:
        link = link.replace("?single", "")
    zzz = await edit_or_reply(event, f"**- جـارِ تحميـل المنشـور المقيـد انتظـر ... 🍧╰\n- رابـط المنشـور المقيـد :\n{link}**")
    chat = "@Save_restricted_robot"
    await zedub(JoinChannelRequest(channel="@logicxupdates"))
    async with borg.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message(link)
        except YouBlockedUserError:
            await zedub(unblock("Save_restricted_robot"))
            purgeflag = await conv.send_message(link)
        response = await conv.get_response()
        await asyncio.sleep(3)
        try:
            if response.media:
                zedthon1 = response.media
                await borg.send_file(
                    event.chat_id,
                    zedthon1,
                    caption=f"<b>⎉╎تم تحميـل المنشـور المقيـد .. بنجـاح 🎆\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                    parse_mode="html",
                )
            else:
                zedthon1 = await conv.get_response()
                await borg.send_message(
                    event.chat_id,
                    f"{zedthon1}\n\n<b>⎉╎تم تحميـل المنشـور المقيـد .. بنجـاح 🎆\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>",
                    parse_mode="html",
                    link_preview=False,
                )
        except:
            pass
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(6109696397, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="(معرفاتي|يوزراتي)$")
async def _(event):
    zzz = await edit_or_reply(event, "**⎉╎جـارِ جلب يـوزرات حسابـك ⅏ . . .**")
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 **- 🝢 - يوزراتـك العامـة** \n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
    for channel_obj in result.chats:
        output_str += f"•┊{channel_obj.title} - @{channel_obj.username} \n"
    await zzz.delete()
    await zedub.send_message(event.chat_id, output_str)


# Function to split Arabic words into individual letters
def split_arabic(input_text):
    letters = []
    for char in input_text:
        if char.isalpha():
            letters.append(char)
    return ' '.join(letters)

@zedub.zed_cmd(pattern=f"تفكيك(?: |$)(.*)")
async def handle_event(event):
    malath = event.pattern_match.group(1)
    if malath:
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة كلمة لـ الامـر او بالـࢪد ؏ــلى كلمة لتفكيكها**")
    split_message = split_arabic(zelzal)
    await zedub.send_message(event.chat_id, split_message)
    await event.delete()

@zedub.zed_cmd(pattern=f"ت(?: |$)(.*)")
async def handle_event(event):
    malath = event.pattern_match.group(1)
    if malath:
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة كلمة لـ الامـر او بالـࢪد ؏ــلى كلمة لتفكيكها**")
    split_message = split_arabic(zelzal)
    await zedub.send_message(event.chat_id, split_message)
    await event.delete()

# Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="حالتي$")
async def zelzal_gif(event):
    chat = "@SpamBot" # Code by T.me/zzzzl1l
    zed = await edit_or_reply(event, "**- جـارِ التحقـق انتظـر قليـلاً . . .**")
    async with borg.conversation(chat) as conv: # Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
        except YouBlockedUserError:
            await zedub(unblock("SpamBot"))
            await conv.send_message("/start")
        zlz = await conv.get_response()
        mallath = zlz.text
        if "Good news, no limits" in mallath: # Code by T.me/zzzzl1l
            zzl = "<b>⎉╎حالة حسابـك حاليـاً هـي :</b>\n\n<b>⎉╎رائع! لاتوجد قيود على حسابك. أنت حر طليق ✅</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "أنت حر طليق!" in mallath: # Code by T.me/zzzzl1l
            zzl = "<b>⎉╎حالة حسابـك حاليـاً هـي :</b>\n\n<b>⎉╎رائع! لاتوجد قيود على حسابك. أنت حر طليق ✅</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "abuse@telegram.org" in mallath:
            zzl = "<b>⎉╎حالة حسابـك حاليـاً هـي :</b>\n\n<b>• يؤسفنا إبلاغك أن بعض مستخدمي تيليجرام قاموا بالإبلاغ عن محتوى قمت بنشره في منصات عامة كمتحوى مخالف وقام مشرفو تيليجرام بالتحقق من ذلك وأزالوه. لسوء الحظ، تم تقييد حسابك. لن تستطيع إنشاء قنوات جديدة أو نشر رسائل في منصات عامة أخرى.</b>\n\n<b>• إن لم تقم بنشر محتوى مخالف على تيليجرام قط وتعتقد أن هذه القيود تم وضعها بشكل خاطئ، يرجى مراسلتنا على</b>\n• abuse@telegram.org."
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "تقديم شكوى إلى المشرفين لدينا" in mallath: # Code by T.me/zzzzl1l
            zzl = "<b>⎉╎حالة حسابـك حاليـاً هـي :</b>\n\n<b>• نعتذر بشدة لأنك اضطررت إلى التواصل معنا. للأسف، قد تسبب بعض التصرفات إلى استجابة قاسية من «نظام مكافحة الرسائل المزعجة» لدينا. إن كنتم تعتقدون أنه تم تقييد حسابكم عن طريق الخطأ؛ فيمكنكم تقديم شكوى إلى المشرفين لدينا.</b>\n\n<b>• عندما يكون الحساب مُقيّدًا؛ قد لا تتمكنون من مراسلة من لا يمتلك رقم هاتفك، ولا إضافتهم إلى المجموعات والقنوات. يمكنك بالتأكيد الرد دائمًا على من يبدؤون بمراسلتك.</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        await zed.delete()
        return await borg.send_message(event.chat_id, zlz, parse_mode="html")

# Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="فك الحظر$")
async def zelzal_gif(event):
    chat = "@SpamBot" # Code by T.me/zzzzl1l
    zed = await edit_or_reply(event, "**- جـارِ التحقـق .. انتظـر قليـلاً ⏳**\n**- في حالة اذا محظور من الخاص 🚷**\n**- سوف يتم ارسـال بـلاغ تلقائـي لـ دعـم تيليجـرام 📬**")
    async with borg.conversation(chat) as conv: # Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
        except YouBlockedUserError:
            await zedub(unblock("SpamBot"))
            await conv.send_message("/start")
        zlz = await conv.get_response()
        mallath = zlz.text
        if "Good news, no limits" in mallath: # Code by T.me/zzzzl1l
            zzl = "<b>⌔ حالة حسابـك حاليـاً هـي 📑:</b>\n\n<b>⌔ رائع .. لاتوجد أي قيود على حسابك حالياً</b>\n<b>⌔ أنت حر طليق ✅</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "أنت حر طليق!" in mallath or "You’re free as a bird!" in mallath: # Code by T.me/zzzzl1l
            zzl = "<b>⌔ حالة حسابـك حاليـاً هـي 📑:</b>\n\n<b>⌔ رائع .. لاتوجد أي قيود على حسابك حالياً</b>\n<b>⌔ أنت حر طليق ✅</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "abuse@telegram.org" in mallath:
            zzl = "<b>⌔ حالة حسابـك حاليـاً هـي :</b>\n\n<b>• يؤسفنا إبلاغك أن بعض مستخدمي تيليجرام قاموا بالإبلاغ عن محتوى قمت بنشره في منصات عامة كمتحوى مخالف وقام مشرفو تيليجرام بالتحقق من ذلك وأزالوه. لسوء الحظ، تم تقييد حسابك. لن تستطيع إنشاء قنوات جديدة أو نشر رسائل في منصات عامة أخرى.</b>\n\n<b>• إن لم تقم بنشر محتوى مخالف على تيليجرام قط وتعتقد أن هذه القيود تم وضعها بشكل خاطئ، يرجى مراسلتنا على</b>\n• abuse@telegram.org."
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "you can submit a complaint to our moderators or subscribe" in mallath: # Code by T.me/zzzzl1l
            await conv.send_message("Submit a complaint")
            zlz1 = await conv.get_response()
            mallath1 = zlz1.text
            if "Would you like to submit a complaint?" in mallath1: # Code by T.me/zzzzl1l
                await conv.send_message("No, I will never send these letters!")
                zlz2 = await conv.get_response()
                mallath2 = zlz2.text
                if "What happened?" in mallath2: # Code by T.me/zzzzl1l
                    await conv.send_message("I created my account recently, and I did not do anything wrong as shown previously\nI hope to remove these restrictions on my account as soon as possible so that I can continue using Telegram and have better usage\nI hope to direct your attention and thank you in advance for your support to Telegram subscribers")
                    zlz3 = await conv.get_response()
                    mallath3 = zlz3.text
                    if "Thank you" in mallath3: # Code by T.me/zzzzl1l
                        zzll = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - <b>رفـع الحظـر 💡\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄⋆</b>\n<b>⌔ تم إرسـال بـلاغ فك الحظر 📬</b>\n<b>⌔ الى دعم تيليجرام .. بنجاح ✅</b>\n<b>⌔ سوف يقوم الدعم بمراجعة بلاغك 🛂</b>\n<b>⌔ ثم رفع الحظر عن حسابك خلال دقائق او ساعات قليلة بالكثير ⏳</b>"
                        await zed.delete()
                        return await borg.send_message(event.chat_id, zzll, parse_mode="html")
        if "تقديم شكوى إلى المشرفين لدينا" in mallath: # Code by T.me/zzzzl1l
            await conv.send_message("هذا خطأ")
            zlz1 = await conv.get_response()
            mallath1 = zlz1.text
            if "هل ترغب في إرسـال بـلاغ؟" in mallath1: # Code by T.me/zzzzl1l
                await conv.send_message("نعم")
                zlz2 = await conv.get_response()
                mallath2 = zlz2.text
                if "هل قمت بأي شيء من ذلك؟" in mallath2: # Code by T.me/zzzzl1l
                    await conv.send_message("لا! لم أقم بهذا قط!")
                    zlz3 = await conv.get_response()
                    mallath3 = zlz3.text
                    if "أرجو كتابة تفاصيل بالمشكلة وسأقوم بتحويلها إلى المسئول" in mallath3: # Code by T.me/zzzzl1l
                        await conv.send_message("I created my account recently, and I did not do anything wrong as shown previously\nI hope to remove these restrictions on my account as soon as possible so that I can continue using Telegram and have better usage\nI hope to direct your attention and thank you in advance for your support to Telegram subscribers")
                        zlz4 = await conv.get_response()
                        mallath4 = zlz4.text
                        if "تم رفع شكواك بنجاح" in mallath4: # Code by T.me/zzzzl1l
                            zzll = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - <b>رفـع الحظـر 💡\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄⋆</b>\n<b>⌔ تم إرسـال بـلاغ فك الحظر 📬</b>\n<b>⌔ الى دعم تيليجرام .. بنجاح ✅</b>\n<b>⌔ سوف يقوم الدعم بمراجعة بلاغك 🛂</b>\n<b>⌔ ثم رفع الحظر عن حسابك خلال دقائق او ساعات قليلة بالكثير ⏳</b>"
                            await zed.delete()
                            return await borg.send_message(event.chat_id, zzll, parse_mode="html")
        if "you can submit a complaint to our moderators." in mallath: # Code by T.me/zzzzl1l
            await conv.send_message("This is a mistake")
            zlz1 = await conv.get_response()
            mallath1 = zlz1.text
            if "Would you like to submit a complaint?" in mallath1: # Code by T.me/zzzzl1l
                await conv.send_message("Yes")
                zlz2 = await conv.get_response()
                mallath2 = zlz2.text
                if "Did you ever do any of this?" in mallath2: # Code by T.me/zzzzl1l
                    await conv.send_message("No! Never did that!")
                    zlz3 = await conv.get_response()
                    mallath3 = zlz3.text
                    if "Please write me some details about your case, I will forward it to the supervisor" in mallath3: # Code by T.me/zzzzl1l
                        await conv.send_message("I created my account recently, and I did not do anything wrong as shown previously\nI hope to remove these restrictions on my account as soon as possible so that I can continue using Telegram and have better usage\nI hope to direct your attention and thank you in advance for your support to Telegram subscribers")
                        zlz4 = await conv.get_response()
                        mallath4 = zlz4.text
                        if "Your complaint has been successfully submitted" in mallath4: # Code by T.me/zzzzl1l
                            zzll = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - <b>رفـع الحظـر 💡\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄⋆</b>\n<b>⌔ تم إرسـال بـلاغ فك الحظر 📬</b>\n<b>⌔ الى دعم تيليجرام .. بنجاح ✅</b>\n<b>⌔ سوف يقوم الدعم بمراجعة بلاغك 🛂</b>\n<b>⌔ ثم رفع الحظر عن حسابك خلال دقائق او ساعات قليلة بالكثير ⏳</b>"
                            await zed.delete()
                            return await borg.send_message(event.chat_id, zzll, parse_mode="html")
        await zed.delete()
        return await borg.send_message(event.chat_id, zlz, parse_mode="html")

# Code by T.me/zzzzl1l
"""
bot_you = '@LyBot'

@zedub.zed_cmd(pattern="بحث (.*)")
async def ZelzalYou(event):
    title = event.pattern_match.group(1)
    zzz = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰**")
    try:
        send = await zedub.send_message(bot_you, '/start')
    except YouBlockedUserError: #Code by T.me/zzzzl1l
        await zedub(unblock(bot_you))
        send = await zedub.send_message(bot_you, '/start')
    sleep(2)
    song = await zedub.send_message(bot_you, title)
    sleep(1)
    msg1 = await zedub.get_messages(bot_you, limit=1)
    sleep(0.5)
    await msg1[0].click(0)
    sleep(1)
    msgt = await zedub.get_messages(bot_you, limit=1)
    song_file = msgt[0].media
    try:
        await zedub.send_file(
            event.chat_id,
            song_file,
            caption=f"**⎉╎البحث :** `{title}`",
        )
        await zzz.delete()
    except ChatSendMediaForbiddenError: # Code By T.me/zzzzl1l
        await zzz.edit("**- عـذراً .. الوسـائـط مغلقـه هنـا ؟!**")
    await event.client(DeleteHistoryRequest(473587803, max_id=0, just_clear=True))
"""

#Code by T.me/zzzzl1l
"""
@zedub.zed_cmd(pattern="(تويتر|x)(?: |$)([\s\S]*)")
async def zelzal_x(event): #Code by T.me/zzzzl1l
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/zzzzl1l
        link = reply.text
    if not link: #Code by T.me/zzzzl1l
        return await edit_delete(event, "**- ارسـل (.تويتر) + رابـط او بالـرد ع رابـط**", 10)
    #if ("twitter.com" not in link) and ("x.com" not in link):
        #return await edit_delete(event, "**- احتـاج الـى رابــط مـن تويتـر (𝕏) .. للتحميــل ؟!**", 10)
    cap_zzz = f"<b>⎉╎تم التحميـل مـن تويتـر (𝕏) .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@twitterimage_bot" #Code by T.me/zzzzl1l
    zzz = await edit_or_reply(event, "**⎉╎جـارِ التحميل مـن تويتـر (𝕏) .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv: #Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_message(link)
            #await conv.send_message("/ocr", reply_to=purgeflag)  # إرسال /ocr بالرد على الصورة داخل البوت
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("twitterimage_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_message(link)
            #await conv.send_message("/ocr", reply_to=purgeflag)  # إرسال /ocr بالرد على الصورة داخل البوت
        zedthon1 = await conv.get_response()
        if zedthon1.media:
            try:
                await borg.send_file(
                    event.chat_id,
                    zedthon1,
                    caption=cap_zzz,
                    parse_mode="html",
                )
                await zzz.delete()
            except ChatSendMediaForbiddenError: # Code By T.me/zzzzl1l
                await zzz.edit("**- عـذراً .. الوسـائـط مغلقـه هنـا ؟!**")
            await event.client(DeleteHistoryRequest(2023564203, max_id=0, just_clear=True))
        else:
            await zzz.edit("**- عـذراً .. لـم يتم العثـور عـلى الفيـديـو ؟!**")
            await event.client(DeleteHistoryRequest(2023564203, max_id=0, just_clear=True))
"""

# Write Code by T.me/zzzzl1l
"""
@zedub.zed_cmd(pattern="تحميل (.*)")
async def ZelzalYou(event):
    bot_you = '@Any_Music_search_bot'
    title = event.pattern_match.group(1)
    zzz = await edit_or_reply(event, "**╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰**")
    try:
        send = await zedub.send_message(bot_you, '/start')
    except YouBlockedUserError: #Code by T.me/zzzzl1l
        await zedub(unblock(bot_you))
        send = await zedub.send_message(bot_you, '/start')
    sleep(2)
    song = await zedub.send_message(bot_you, title)
    sleep(2)
    await zzz.edit("**╮ جـارِ التحميل ▬▭ . . .🎧♥️╰**")
    try:
        msg1 = await zedub.get_messages(bot_you, limit=1)
        sleep(1)
        if msgt1[0].media:
            await msg1[0].click(0)
            sleep(1)
        else:
            msg1 = await zedub.get_messages(bot_you, limit=1)
            sleep(1)
            await msg1[0].click(0)
            sleep(1)
    except Exception:
        msg1 = await zedub.get_messages(bot_you, limit=1)
        sleep(1)
        await msg1[0].click(0)
        sleep(1)
    await zzz.edit("**╮ جـارِ الرفـع ▬▬ . . .🎧♥️╰**")
    msgg = await zedub.get_messages(bot_you, limit=1)
    sleep(1)
    mass = msgg[0].text
    if "подпишитесь" in mass:
        channel_entity = await zedub.get_entity(bot_you)
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.reply_markup:
            for i, row in enumerate(msgs.reply_markup.rows):
                if row.buttons:
                    button = row.buttons[0]
                    url = msgs.reply_markup.rows[i].buttons[0].url
                    try:
                        await zedub(JoinChannelRequest(url))
                    except:
                        bott = url.split('/')[-1]
                        await zedub(ImportChatInviteRequest(bott))
                else:
                    break
        msg1 = await zedub.get_messages(bot_you, limit=2)
        sleep(1)
        if msg1[0].media:
            await msg1[0].click(0)
            sleep(1)
        else:
            msg1 = await zedub.get_messages(bot_you, limit=1)
            sleep(1)
            await msg1[0].click(0)
            sleep(1)
    try:
        msgt = await zedub.get_messages(bot_you, limit=1)
        song_file = msgt[0].media
    except Exception:
        msgt = await zedub.get_messages(bot_you, limit=1)
        song_file = msgt[0].media
    try:
        await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
        await zzz.delete()
    except ChatSendMediaForbiddenError: # Code By T.me/zzzzl1l
        await zzz.edit("**- عـذراً .. الوسـائـط مغلقـه هنـا ؟!**")
    except ChatForwardsRestrictedError:
        sleep(2)
        try:
            msgt = await zedub.get_messages(bot_you, limit=1)
            song_file = msgt[0].media
            await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
            await zzz.delete()
        except ChatForwardsRestrictedError:
            sleep(2)
            msgt = await zedub.get_messages(bot_you, limit=1)
            song_file = msgt[0].media
            await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
            await zzz.delete()
    except TypeError as x:
        #if "None as file" in str(x):
        try:
            msgt = await zedub.get_messages(bot_you, limit=2)
            song_file = msgt[0].media
            await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
            await zzz.delete()
        except Exception:
            msgt = await zedub.get_messages(bot_you, limit=2)
            song_file = msgt[0].media
            await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
            await zzz.delete()
    except Exception:
        try:
            msgd = await zedub.get_messages(bot_you, limit=1)
            song_file = msgd[0].media
            await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
            await zzz.delete()
        except ChatForwardsRestrictedError:
            sleep(2)
            msgt = await zedub.get_messages(bot_you, limit=1)
            song_file = msgt[0].media
            await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
            await zzz.delete()
        except TypeError as x:
            #if "None as file" in str(x):
            try:
                msgt = await zedub.get_messages(bot_you, limit=1)
                song_file = msgt[0].media
                await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
                await zzz.delete()
            except Exception:
                msgt = await zedub.get_messages(bot_you, limit=1)
                song_file = msgt[0].media
                await zedub.send_file(event.chat_id, song_file, caption=f"**⎉╎البحث :** `{title}`")
                await zzz.delete()

    await event.client(DeleteHistoryRequest(6017830301, max_id=0, just_clear=True))
"""

@zedub.zed_cmd(pattern="دمج1$")
async def handle_swap_command(event):
    global target_img
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "**- بالرد ع صوره يامطي**.")
        return
    if event.fwd_from:
        return
    #  تحميل  الصور  في  قائمة 
    input_media = [] 
    zed = await edit_or_reply(event, "**⎉╎جـارِ رفـع الصـورة ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)

    wzed_dir = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY,
        "swap"
    )
    if not os.path.isdir(wzed_dir):
        os.makedirs(wzed_dir)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        downloaded_file_name = await event.client.download_media(
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
            target_img = vinfo
            #addgvar("pmpermit_pic", target_img)
            try:
                image_data = requests.get(target_img).content
                image_save_path = os.path.join(
                    wzed_dir,
                    f"swap1.jpg"
                )
                with open(image_save_path, "wb") as f:
                    f.write(image_data)
                input_media.append(image_save_path)
            except Exception as e:
                pass
            await zed.edit("**⎉╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶**\n `{}` \n\n**⎉╎قنـاة السـورس : @ZThon**".format(target_img, target_img))

    #reply_msg = await event.get_reply_message()
    #if reply_msg.photo:
        #target_img = reply_msg.media.photo.sizes[-1].url
        #await edit_or_reply(event, "Target image saved. Now reply to the face image with /face.")
    #else:
        #await edit_or_reply(event, "Please reply to an image message with /swap.")

@zedub.zed_cmd(pattern="دمج2$")
async def handle_face_command(event):
    global face_img, target_img, input_media
    #user = await event.get_sender()
    #chat = await event.get_input_chat()

    if not event.reply_to_msg_id:
        await edit_or_reply(event, "**- بالرد ع الصورة يامطي**.")
        return

    if event.fwd_from:
        return
    zed = await edit_or_reply(event, "**⎉╎جـارِ رفـع الصـورة ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)

    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    file_name = "swaped.jpg"
    input_media = []
    wzed_dir = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY,
        "swap"
    )
    if not os.path.isdir(wzed_dir):
        os.makedirs(wzed_dir)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        downloaded_file_name = await event.client.download_media(
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
            face_img = vinfo
            #addgvar("pmpermit_pic", face_img)
            try:
                image_data = requests.get(face_img).content
                image_save_path = os.path.join(
                    wzed_dir,
                    f"face1.jpg"
                )
                with open(image_save_path, "wb") as f:
                    f.write(image_data)
                input_media.append(image_save_path)
            except Exception as e:
                pass
            #  إرسال  جميع  الصور  في  رسالة  واحدة 
            try:
                if input_media:
                    await zedub.send_file(event.chat_id, input_media, caption="**- جـارِ دمج الصور وتبديل الوجوه . . .**")
                else:
                    pass
            except Exception:
                pass
            #  حذف  الملفات  المؤقتة 
            for each_file in input_media:
                os.remove(each_file)
            shutil.rmtree(wzed_dir, ignore_errors=True)
        if target_img:
            await zed.edit("**- جـارِ المعالجـه . . .**")
            task_id = await create_swap_task(target_img, face_img)
            if task_id:
                await zed.edit(f"**- Task created with ID**: `{task_id}`\n**- Please wait while processing...**")
                for _ in range(10):
                    result_image = await check_swap_task(task_id)
                    if result_image:
                        # تحويل الصورة إلى JPG وحفظها مؤقتًا
                        jpg_image_path = await convert_webp_to_jpg(result_image)
                        # إرسال الملف الجديد إلى المحادثة
                        if os.path.exists(jpg_image_path):
                            photo = await event.client.send_file(
                                event.chat_id,
                                jpg_image_path,
                                caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗔𝗶𝗣𝗵𝗼𝘁𝗼 -💡-](t.me/ZThon) **دمـج الصـور\n⋆─┄─┄─┄─┄─┄─┄─┄─⋆**\n**• تم دمج الصورتان .. بنجاح 📇**\n**• بواسطة الذكاء الاصطناعي💡**",
                                force_document=False,
                                #reply_to=reply_to_id,
                            )
                            os.remove(jpg_image_path)  # حذف الملف المؤقت بعد الإرسال
                            await zed.delete()
                            break
                        else:
                            #await event.edit("Can't Convert")
                            await bot.send_file(event.chat_id, result_image)
                            await bot.send_message(event.chat_id, "[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗔𝗶𝗣𝗵𝗼𝘁𝗼 -💡-](t.me/ZThon) **دمـج الصـور\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆**\n**• تم دمج الصورتان .. بنجاح 📇**\n**• بواسطة الذكاء الاصطناعي💡**")
                            await zed.delete()
                            break
                    await asyncio.sleep(2)
                else:
                    await zed.edit(event, "Face swap process took longer than expected. Please try again.")
            else:
                await zed.edit("Failed to create face swap task. Please check the image URLs and try again.")
            # Reset image URLs after processing
            target_img = None
            face_img = None
        else:
            await zed.edit("**- ارسل (.دمج1) اولاً**")
    else:
        await zed.edit("**- ارسل (.دمج1) اولاً**")


async def start_copier(destination_channel_username, source_channel_username):
    try:
        # الحصول على معلومات القنوات
        source_channel = await zedub.get_entity(source_channel_username)
        destination_channel = await zedub.get_entity(destination_channel_username)
        destination_channel_id = destination_channel.id

        # الحصول على جميع المنشورات من القناة المصدر
        posts = await zedub(GetHistoryRequest(
            peer=source_channel,
            limit=10000,  # عدد المنشورات المراد نقلها (ضع قيمة كبيرة لنقل جميع المنشورات)
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        ))

        # عكس ترتيب الرسائل لنقلها من الأقدم إلى الأحدث
        posts.messages.reverse() 

        # نقل المنشورات إلى القناة المستهدفة
        for message in posts.messages:
            try:
                media = None
                caption = message.message or ""
                if message.media:
                    file_media = f"https://t.me/{source_channel_username}/{message.id}"
                    await zedub.send_file(destination_channel_id, file_media, caption=caption)
                    #print(f"تم نقل المنشور: {message.id}")
                    await asyncio.sleep(1)  # تجنب حظر Telegram بإضافة تأخير بين كل عملية إرسال
                    await zedub.send_message(BOTLOG_CHATID, f"**- تم نقل المنشور .. بنجاح✅**\n**- رابـط المنشور:**\n- https://t.me/{source_channel_username}/{message.id}", link_preview=False)
                    await asyncio.sleep(1)  # تجنب حظر Telegram بإضافة تأخير بين كل عملية إرسال

            except Exception as e:
                #print(f"خطأ في نقل المنشور {message.id}: {e}")
                await zedub.send_message(BOTLOG_CHATID, f"**- خطـأ بنقـل المنشـور ❌**\n**- رابـط المنشور:**\n- https://t.me/{source_channel_username}/{message.id}\n**- تفاصيـل الخطـأ:**\n- {e}", link_preview=False)

    except Exception as e:
        #print(f"حدث خطأ: {e}")
        await zedub.send_message(BOTLOG_CHATID, f"**- حدث خطـأ ❌**\n**- تفاصيـل الخطـأ:**\n- {e}")


@zedub.zed_cmd(pattern="كوبي(?:\s|$)([\s\S]*)")
async def channel_copier(event):
    catty = event.pattern_match.group(1)
    #limit = int(catty.split(" ")[0])
    channel_username = str(catty.split(" ")[0])
    if channel_username.startswith("@"):
        channel_username = channel_username.replace("@", "")
    await edit_or_reply(event, f"**- جـارِ نقـل منشـورات الميديـا . . .**\n**- مـن القنـاة @{channel_username}**\n\n**- انتظـر .. قد تستمـر العمليـة بضـع دقائـق**")
    copier_start = await start_copier(event.chat_id, channel_username)


# =========================================================== #
#                           الملـــف كتـــابـــة مـــن الصفـــر - T.me/ZThon                           #
# =========================================================== #
Warn = "تخمـط بـدون ذكـر المصـدر - ابلعــك نعــال وراح اهينــك"
REPO_SEARCH_STRING = "<b>╮ جـارِ التحميـل مـن كيثـاب ...♥️╰</b>"
REPO_NOT_FOUND = "<b>⎉╎عـذراً .. لـم استطـع ايجـاد المطلـوب</b>"
# =========================================================== #
#                                      زلـــزال الهيبـــه - T.me/zzzzl1l                                  #
# =========================================================== #


#Write Code By T.me/zzzzl1l
@zedub.zed_cmd(pattern="repo(?:\s|$)([\s\S]*)")
async def zelzal2(event):
    zelzal = event.pattern_match.group(1)
    cap_zzz = f"<b>⎉╎الريبـو :- <code>{zelzal}</code>\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@octocatbbot"
    reply_id_ = await reply_id(event)
    zedthon = await edit_or_reply(event, REPO_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_message(zelzal)
        except YouBlockedUserError:
            await zedub(unblock("octocatbbot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_message(zelzal)
        await conv.get_response()
        repo = await conv.get_response()
        if repo.document:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_file(
                event.chat_id,
                repo,
                caption=cap_zzz,
                parse_mode="html",
                reply_to=reply_id_,
            )
            await zedthon.delete()
            await delete_conv(event, chat, purgeflag)
            await event.client(DeleteHistoryRequest(6392904112, max_id=0, just_clear=True))
        else:
            repo = await conv.get_response()
            if not repo.document:
                return await edit_delete(zedthon, REPO_NOT_FOUND, parse_mode="html")
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_file(
                event.chat_id,
                repo,
                caption=cap_zzz,
                parse_mode="html",
                reply_to=reply_id_,
            )
            await zedthon.delete()
            await delete_conv(event, chat, purgeflag)
            await event.client(DeleteHistoryRequest(6392904112, max_id=0, just_clear=True))


#Write Code By T.me/zzzzl1l
@zedub.zed_cmd(pattern="كيثاب(?:\s|$)([\s\S]*)")
async def zelzal2(event):
    zelzal = event.pattern_match.group(1)
    cap_zzz = f"<b>⎉╎الريبـو :- <code>{zelzal}</code>\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/ZThon/1>𝗭𝗧𝗵𝗼𝗻</a> </b>"
    chat = "@octocatbbot"
    reply_id_ = await reply_id(event)
    zedthon = await edit_or_reply(event, REPO_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_message(zelzal)
        except YouBlockedUserError:
            await zedub(unblock("octocatbbot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_message(zelzal)
        await conv.get_response()
        repo = await conv.get_response()
        if repo.document:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_file(
                event.chat_id,
                repo,
                caption=cap_zzz,
                parse_mode="html",
                reply_to=reply_id_,
            )
            await zedthon.delete()
            await delete_conv(event, chat, purgeflag)
            await event.client(DeleteHistoryRequest(6392904112, max_id=0, just_clear=True))
        else:
            repo = await conv.get_response()
            if not repo.document:
                return await edit_delete(zedthon, REPO_NOT_FOUND, parse_mode="html")
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_file(
                event.chat_id,
                repo,
                caption=cap_zzz,
                parse_mode="html",
                reply_to=reply_id_,
            )
            await zedthon.delete()
            await delete_conv(event, chat, purgeflag)
            await event.client(DeleteHistoryRequest(6392904112, max_id=0, just_clear=True))
