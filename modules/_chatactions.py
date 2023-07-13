# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import asyncio

from Ayra.dB import stickers
from Ayra.dB.forcesub_db import get_forcesetting
from Ayra.dB.gban_mute_db import is_gbanned
from Ayra.dB.greetings_db import get_goodbye, get_welcome, must_thank
from Ayra.dB.nsfw_db import is_profan
from Ayra.fns.helper import inline_mention
from Ayra.fns.tools import async_searcher, create_tl_btn, get_chatbot_reply
from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

try:
    from ProfanityDetector import detector
except ImportError:
    detector = None
from . import LOG_CHANNEL, LOGS, asst, ayra_bot, get_string, types, udB
from ._inline import something


@ayra_bot.on(events.ChatAction())
async def Function(event):
    try:
        await DummyHandler(event)
    except Exception as er:
        LOGS.exception(er)


async def DummyHandler(ayra):
    # clean chat actions
    key = udB.get_key("CLEANCHAT") or []
    if ayra.chat_id in key:
        try:
            await ayra.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(ayra.chat_id):
        chat_count = (await ayra.client.get_participants(ayra.chat_id, limit=0)).total
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await ayra.respond(file=sticker)
    # force subscribe
    if (
        udB.get_key("FORCESUB")
        and ((ayra.user_joined or ayra.user_added))
        and get_forcesetting(ayra.chat_id)
    ):
        user = await ayra.get_user()
        if not user.bot:
            joinchat = get_forcesetting(ayra.chat_id)
            try:
                await ayra_bot(GetParticipantRequest(int(joinchat), user.id))
            except UserNotParticipantError:
                await ayra_bot.edit_permissions(
                    ayra.chat_id, user.id, send_messages=False
                )
                res = await ayra_bot.inline_query(
                    asst.me.username, f"fsub {user.id}_{joinchat}"
                )
                await res[0].click(ayra.chat_id, reply_to=ayra.action_message.id)

    if ayra.user_joined or ayra.added_by:
        user = await ayra.get_user()
        chat = await ayra.get_chat()
        # gbans and @Ayra checks
        if udB.get_key("ayra_BANS"):
            try:
                is_banned = await async_searcher(
                    "https://bans.ayra/api/status",
                    json={"userId": user.id},
                    post=True,
                    re_json=True,
                )
                if is_banned["is_banned"]:
                    await ayra.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    await ayra.client.send_message(
                        chat.id,
                        f'**@AyraBans:** Banned user detected and banned!\n`{str(is_banned)}`.\nBan reason: {is_banned["reason"]}',
                    )

            except BaseException:
                pass
        reason = is_gbanned(user.id)
        if reason and chat.admin_rights:
            try:
                await ayra.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = get_string("can_1").format(inline_mention(user), reason)
                await ayra.reply(gban_watch)
            except Exception as er:
                LOGS.exception(er)

        elif get_welcome(ayra.chat_id):
            user = await ayra.get_user()
            chat = await ayra.get_chat()
            title = chat.title or "this chat"
            count = (
                chat.participants_count
                or (await ayra.client.get_participants(chat, limit=0)).total
            )
            mention = inline_mention(user)
            name = user.first_name
            fullname = get_display_name(user)
            uu = user.username
            username = f"@{uu}" if uu else mention
            wel = get_welcome(ayra.chat_id)
            med = wel["media"] or None
            userid = user.id
            msg = None
            if msgg := wel["welcome"]:
                msg = msgg.format(
                    mention=mention,
                    group=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )
            if wel.get("button"):
                btn = create_tl_btn(wel["button"])
                await something(ayra, msg, med, btn)
            elif msg:
                send = await ayra.reply(
                    msg,
                    file=med,
                )
                await asyncio.sleep(150)
                await send.delete()
            else:
                await ayra.reply(file=med)
    elif (ayra.user_left or ayra.user_kicked) and get_goodbye(ayra.chat_id):
        user = await ayra.get_user()
        chat = await ayra.get_chat()
        title = chat.title or "this chat"
        count = (
            chat.participants_count
            or (await ayra.client.get_participants(chat, limit=0)).total
        )
        mention = inline_mention(user)
        name = user.first_name
        fullname = get_display_name(user)
        uu = user.username
        username = f"@{uu}" if uu else mention
        wel = get_goodbye(ayra.chat_id)
        med = wel["media"]
        userid = user.id
        msg = None
        if msgg := wel["goodbye"]:
            msg = msgg.format(
                mention=mention,
                group=title,
                count=count,
                name=name,
                fullname=fullname,
                username=username,
                userid=userid,
            )
        if wel.get("button"):
            btn = create_tl_btn(wel["button"])
            await something(ayra, msg, med, btn)
        elif msg:
            send = await ayra.reply(
                msg,
                file=med,
            )
            await asyncio.sleep(150)
            await send.delete()
        else:
            await ayra.reply(file=med)


@ayra_bot.on(events.NewMessage(incoming=True))
async def chatBot_replies(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User):
        return
    key = udB.get_key("CHATBOT_USERS") or {}
    if e.text and key.get(e.chat_id) and sender.id in key[e.chat_id]:
        msg = await get_chatbot_reply(e.message.message)
        if msg:
            sleep = udB.get_key("CHATBOT_SLEEP") or 1.5
            await asyncio.sleep(sleep)
            await e.reply(msg)
    chat = await e.get_chat()
    if e.is_group and not sender.bot:
        if sender.username:
            await uname_stuff(e.sender_id, sender.username, sender.first_name)
    elif e.is_private and not sender.bot:
        if chat.username:
            await uname_stuff(e.sender_id, chat.username, chat.first_name)
    if detector and is_profan(e.chat_id) and e.text:
        x, y = detector(e.text)
        if y:
            await e.delete()


@ayra_bot.on(events.Raw(types.UpdateUserName))
async def uname_change(e):
    await uname_stuff(e.user_id, e.username, e.first_name)


async def uname_stuff(id, uname, name):
    if udB.get_key("USERNAME_LOG"):
        old_ = udB.get_key("USERNAME_DB") or {}
        old = old_.get(id)
        # Ignore Name Logs
        if old and old == uname:
            return
        if old and uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_2").format(old, uname),
            )
        elif old:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_3").format(f"[{name}](tg://user?id={id})", old),
            )
        elif uname:
            await asst.send_message(
                LOG_CHANNEL,
                get_string("can_4").format(f"[{name}](tg://user?id={id})", uname),
            )

        old_[id] = uname
        udB.set_key("USERNAME_DB", old_)
