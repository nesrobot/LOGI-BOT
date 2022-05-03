import asyncio
import importlib
import re

import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , InputTextMessageContent

from LG import (
    BOT_NAME,
    BOT_USERNAME,
    LOG_GROUP_ID,
    USERBOT_NAME,
    OWNER_USERNAME,
    START_IMG,
    SUPPORT_CHAT,
    SUPPORT_CHANNEL,
    aiohttpsession,
    app,
    log,
)
from LG.modules import ALL_MODULES
from LG.modules.sudoers import bot_sys_stats
from LG.utils import paginate_modules
from LG.utils.constants import MARKDOWN
from LG.utils.dbfunctions import clean_restart_stage

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    global HELPABLE

    for module in ALL_MODULES:
        imported_module = importlib.import_module("LG.modules." + module)
        if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                     @CL_ME_LOGESH                             |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    log.info(f"BOT STARTED AS {BOT_NAME}!")
    log.info(f"USERBOT STARTED AS {USERBOT_NAME}!")

    restart_data = await clean_restart_stage()

    try:
        log.info("Sending online status")
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot started!")
    except Exception:
        pass

    await idle()

    await aiohttpsession.close()
    log.info("Stopping clients")
    await app.stop()
    log.info("Cancelling asyncio tasks")
    for task in asyncio.all_tasks():
        task.cancel()
    log.info("Dead!")


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=" 🦋 Tʜɪꜱ Bᴏᴛ Rᴇᴘᴏ ɪɴ  GɪᴛHᴜʙ 🦋",
                url=f"https://github.com/LOGI-TECH/LOGI-BOT",
            )
        ],        
        [
            InlineKeyboardButton(
                text="🦋 Mᴀɴᴀɢᴇᴍᴇɴᴛ 🦋", callback_data="bot_commands"
            ),
            InlineKeyboardButton(
                text="🦋 Mᴜꜱɪᴄ 🦋",
                url=f"https://telegra.ph/MUSIC-COMMANDS-04-06",
            ),
        ],        
        [
            InlineKeyboardButton(
                text="🦋 Owɴᴇʀ 🦋", url=F"http://t.me/{OWNER_USERNAME}"
            ),            
            InlineKeyboardButton(
                text="🦋 Sʏꜱᴛᴇᴍ Sᴛᴀᴛꜱ 🦋",
                callback_data="stats_callback",
            )
        ],        
        [
            InlineKeyboardButton(
                text="🦋 Gʀᴏᴜᴘ 🦋",
                url=f"http://t.me/{SUPPORT_CHAT}",
            ),
            InlineKeyboardButton(
                text="🦋 Cʜᴀɴɴᴇʟ 🦋", url=F"http://t.me/{SUPPORT_CHANNEL}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=" 🦋 Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🦋",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

home_text_pm = (
f"[❤]({ START_IMG})"f"""
*Hᴇʟʟᴏ  !* 
───────────────────────
× *I'ᴍ {BOT_NAME} Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ Vᴄ ᴘʟᴀʏᴇʀ*
× *I'ᴍ Vᴇʀʏ Fᴀꜱᴛ Aɴᴅ Mᴏʀᴇ Eꜰꜰɪᴄɪᴇɴᴛ I Pʀᴏᴠɪᴅᴇ Aᴡᴇꜱᴏᴍᴇ Fᴇᴀᴛᴜʀᴇꜱ!💕* 
────────────────────────
× Hɪᴛ /help  ᴛᴏ ꜱᴇᴇ Mᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ.
× Hɪᴛ /mhelp ᴛᴏ ꜱᴇᴇ Mᴜꜱɪᴄ ᴘʟᴀʏᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ.
────────────────────────
✪ 3 ɪɴ 1 Bᴏᴛ | Mᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ | ᴍᴜꜱɪᴄ ʙᴏᴛ | ᴜꜱᴇʀ ʙᴏᴛ | ..
✪ ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴀʟʟ ᴛʜᴇ ʙᴏᴛ's ᴄᴏᴍᴍᴀɴᴅs  ᴀɴᴅ ʜᴏᴡ ᴛʜᴇʏ ᴡᴏʀᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ »  ᴄᴏᴍᴍᴀɴᴅs  ʙᴜᴛᴛᴏɴ!.
✪ ᴛʜɪs ɪs ᴀ ʙᴏᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ɪɴ ɢʀᴏᴜᴘs, ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ɴᴇᴡ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs.
✪ ɪ'ᴍ ᴀ ᴛᴇʟᴇɢʀᴀᴍ strᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴜꜱᴇꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇꜱ. ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ ʏᴏᴜᴛᴜʙᴇ, ꜱᴘᴏᴛɪꜰʏ, ʀᴇꜱꜱᴏ, ᴀᴘᴘʟᴇᴍᴜꜱɪᴄ , ꜱᴏᴜɴᴅᴄʟᴏᴜᴅ ᴇᴛᴄ.
✪ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ .
───────────────────────
× *Pᴏᴡᴇʀᴇᴅ Bʏ: @LGBots 💕!*
───────────────────────
"""
)

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=" 🦋 Tʜɪꜱ Bᴏᴛ Rᴇᴘᴏ ɪɴ  GɪᴛHᴜʙ 🦋",
                url=f"https://github.com/LOGI-TECH/LOGI-BOT",
            )
        ],        
        [
            InlineKeyboardButton(
                text="🦋 Mᴀɴᴀɢᴇᴍᴇɴᴛ 🦋", callback_data="bot_commands"
            ),
            InlineKeyboardButton(
                text="🦋 Mᴜꜱɪᴄ 🦋",
                url=f"https://telegra.ph/MUSIC-COMMANDS-04-06",
            ),
        ],        
        [
            InlineKeyboardButton(
                text="🦋 Owɴᴇʀ 🦋", url=F"http://t.me/{OWNER_USERNAME}"
            ),            
            InlineKeyboardButton(
                text="🦋 Sʏꜱᴛᴇᴍ Sᴛᴀᴛꜱ 🦋",
                callback_data="stats_callback",
            )
        ],        
        [
            InlineKeyboardButton(
                text="🦋 Gʀᴏᴜᴘ 🦋",
                url=f"http://t.me/{SUPPORT_CHAT}",
            ),
            InlineKeyboardButton(
                text="🦋 Cʜᴀɴɴᴇʟ 🦋", url=F"http://t.me/{SUPPORT_CHANNEL}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=" 🦋 Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🦋",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)


@app.on_message(~filters.edited & filters.command("start"))
async def start(_, message):
    if message.chat.type != "private":
        return await message.reply(
            "Pm Me For More Details.", reply_markup=keyboard
        )
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode="html", disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                    f"Here is the help for **{HELPABLE[module].__MODULE__}**:\n"
                    + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply(
            home_text_pm,
            reply_markup=home_keyboard_pm,
        )
    return


@app.on_message(~filters.edited & filters.command("help"))
async def help_command(_, message):
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Click here",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Click on the below button to get help about {name}",
                    reply_markup=key,
                )
            else:
                await message.reply(
                    "PM Me For More Details.", reply_markup=keyboard
                )
        else:
            await message.reply(
                "Pm Me For More Details.", reply_markup=keyboard
            )
    else:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                text = (
                        f"Here is the help for **{HELPABLE[name].__MODULE__}**:\n"
                        + HELPABLE[name].__HELP__
                )
                await message.reply(text, disable_web_page_preview=True)
            else:
                text, help_keyboard = await help_parser(
                    message.from_user.first_name
                )
                await message.reply(
                    text,
                    reply_markup=help_keyboard,
                    disable_web_page_preview=True,
                )
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text, reply_markup=help_keyboard, disable_web_page_preview=True
            )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Hᴇʟʟᴏ {first_name}, Mʏ ɴᴀᴍᴇ ɪꜱ {bot_name}.
I'ᴍ ᴀ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ wɪᴛʜ ꜱᴏᴍᴇ ᴜꜱᴇꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇꜱ.
Yᴏᴜ ᴄᴀɴ ᴄʜᴏᴏꜱᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏw, ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴀ ʙᴜᴛᴛᴏɴ.
Aʟꜱᴏ ʏᴏᴜ ᴄᴀɴ ᴀꜱᴋ ᴀɴʏᴛʜɪɴɢ ɪɴ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ.
  Tᴏ ꜱᴇᴇ ᴍᴜꜱɪᴄ ᴄᴏᴍᴍᴀɴᴅꜱ ʜɪᴛ   /mhelp
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
Hᴇʟʟᴏ {query.from_user.first_name}, Mʏ ɴᴀᴍᴇ ɪꜱ {BOT_NAME}.
I'ᴍ ᴀ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ wɪᴛʜ ꜱᴏᴍᴇ ᴜꜱᴇꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇꜱ.
Yᴏᴜ ᴄᴀɴ ᴄʜᴏᴏꜱᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏw, ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴀ ʙᴜᴛᴛᴏɴ.
Aʟꜱᴏ ʏᴏᴜ ᴄᴀɴ ᴀꜱᴋ ᴀɴʏᴛʜɪɴɢ ɪɴ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ.
  Tᴏ ꜱᴇᴇ ᴍᴜꜱɪᴄ ᴄᴏᴍᴍᴀɴᴅꜱ ʜɪᴛ   /mhelp

Gᴇɴᴇʀᴀʟ ᴄᴏᴍᴍᴀɴᴅ ᴀʀᴇ:
 - /start : To Sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
 - /help  : Tᴏ ꜱᴇᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ
 - /mhelp : ᴛᴏ ꜱᴇᴇ ᴍᴜꜱɪᴄ ᴄᴏᴍᴍᴀɴᴅ ʟɪꜱᴛ
 """
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = (
                "{} **{}**:\n".format(
                    "Here is the help for", HELPABLE[module].__MODULE__
                )
                + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    uvloop.install()
    try:
        try:
            loop.run_until_complete(start_bot())
        except asyncio.exceptions.CancelledError:
            pass
        loop.run_until_complete(asyncio.sleep(3.0))  # task cancel wait
    finally:
        loop.close()
