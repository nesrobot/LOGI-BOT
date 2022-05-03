from pyrogram import filters

from LG import app
from LG.core.decorators.errors import capture_err
from LG.utils.http import get

__MODULE__ = "✨ Rᴇᴘᴏ"
__HELP__ = "/repo - To Get My Github Repository Link " "And Support Group Link"


@app.on_message(filters.command("repo") & ~filters.edited)
@capture_err
async def repo(_, message):
    users = await get(
        "https://api.github.com/repos/LOGI-TECH/LOGI-BOT/contributors"
    )
    list_of_users = ""
    count = 1
    for user in users:
        list_of_users += (
            f"**{count}.** [{user['login']}]({user['html_url']})\n"
        )
        count += 1

    text = f"""[BOT REPO](https://t.me/LOGI_CHANNEL/55) | [More Bots](t.me/LGBOTS) | [Bot Repos](t.me/Logi_channel)
```----------------
| Contributors |
----------------```
{list_of_users}"""
    await app.send_message(
        message.chat.id, text=text, disable_web_page_preview=True
    )
