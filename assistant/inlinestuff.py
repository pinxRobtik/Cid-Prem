# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.


from telethon import Button
from telethon.tl.types import InputWebDocument as wb

from . import *

SUP_BUTTONS = [
    [
        Button.url("• Repo •", url="https://github.com/Pinxrobtik/Cid-Prem"),
        Button.url("• Support •", url="t.me/cidsupport"),
    ],
]

ofox = "https://graph.org/file/231f0049fcd722824f13b.jpg"
gugirl = "https://graph.org/file/0df54ae4541abca96aa11.jpg"
aypic = "./resources/extras/logo.jpg"

apis = [
    "QUl6YVN5QXlEQnNZM1dSdEI1WVBDNmFCX3c4SkF5NlpkWE5jNkZV",
    "QUl6YVN5QkYwenhMbFlsUE1wOXh3TVFxVktDUVJxOERnZHJMWHNn",
    "QUl6YVN5RGRPS253blB3VklRX2xiSDVzWUU0Rm9YakFLSVFWMERR",
]


@in_pattern("repo", owner=True)
async def repo(e):
    res = [
        await e.builder.article(
            title="Naya Userbot",
            description="Userbot | Telethon",
            thumb=wb(aypic, 0, "image/jpeg", []),
            text="**ᴄɪᴅ ꭙ ᴘʀᴇᴍɪᴜᴍ**",
            buttons=SUP_BUTTONS,
        ),
    ]
    await e.answer(res, switch_pm="ᴄɪᴅ ꭙ ᴘʀᴇᴍɪᴜᴍ", switch_pm_param="start")
