# @riizzvbss
"""
✘ **Bantuan Untuk Salam**

๏ **Perintah:** `ass`
◉ **Keterangan:** Coba sendiri.

๏ **Perintah:** `as`
◉ **Keterangan:** Coba sendiri.

๏ **Perintah:** `ws`
◉ **Keterangan:** Coba sendiri

๏ **Perintah:** `ks`
◉ **Keterangan:** Coba sendiri.

๏ **Perintah:** `3x`
◉ **Keterangan:** Coba sendiri.

๏ **Perintah:** `kg`
◉ **Keterangan:** Coba sendiri.
"""

from time import sleep

from . import ayra_cmd


@ayra_cmd(pattern="[aA][sS][sS]")
async def _(event):
    await event.eor("**Assalamu'alaikum Warohmatulohi Wabarokatu**")


@ayra_cmd(pattern="[aA][sS]")
async def _(event):
    await event.eor("**Assalamu'alaikum**")


@ayra_cmd(pattern="[wW][sS]")
async def _(event):
    await event.eor("**Wa'alaikumussalam**")


@ayra_cmd(pattern="[kK][sS]")
async def _(event):
    xx = await event.eor("**Hy kaa 🥺**")
    sleep(2)
    await xx.edit("**Assalamualaikum...**")


@ayra_cmd(pattern="[jJ][wW][sS]")
async def _(event):
    xx = await event.eor(event, "**Astaghfirullah, Jawab salam dong**")
    sleep(2)
    await xx.edit("**Assalamu'alaikum**")


@ayra_cmd(pattern="3x")
async def _(event):
    xx = await event.eor("**Bismillah, 3x**")
    sleep(2)
    await xx.edit("**Assalamu'alaikum Bisa Kali**")


@ayra_cmd(pattern="[kK][gG]")
async def _(event):
    xx = await event.eor("**Lu Ngapah Begitu ?**")
    sleep(2)
    await xx.edit("**Keren Lu Begitu ?**")
