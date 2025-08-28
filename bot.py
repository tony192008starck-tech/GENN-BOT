import telebot, random, re, time, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# ✅ Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


# ✅ Anime clips list
anime_clips = [
    'https://t.me/animeshorts12/4',
    'https://t.me/animeshorts12/7',
    'https://t.me/animeshorts5/19',
    'https://t.me/animeshorts5/11',
    'https://t.me/animeshorts5/10',
    'https://t.me/animeshorts5/8',
    'https://t.me/animeshorts5/7',
    'https://t.me/animeshorts5/3',
    'https://t.me/animeshorts5/23',
]

# ✅ Welcome buttons
def get_welcome_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📜 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎", callback_data="commands"),
        InlineKeyboardButton("👨‍💻 𝙊𝙒𝙉𝙀𝙍", url="https://t.me/Billy_badson")  # apna username dalna
    )
    return markup

# ✅ Luhn Algorithm
def luhn(card):
    nums = [int(x) for x in card]
    return (sum(nums[-1::-2]) + sum(sum(divmod(2 * x, 10)) for x in nums[-2::-2])) % 10 == 0

# ✅ Generate credit card number
def generate_card(bin_format):
    bin_format = bin_format.lower()
    if len(bin_format) < 16:
        bin_format += "x" * (16 - len(bin_format))
    else:
        bin_format = bin_format[:16]
    while True:
        cc = ''.join(str(random.randint(0, 9)) if x == 'x' else x for x in bin_format)
        if luhn(cc):
            return cc

# ✅ Generate card info block
def generate_output(bin_input, username):
    parts = bin_input.split("|")
    bin_format = parts[0] if len(parts) > 0 else ""
    mm_input = parts[1] if len(parts) > 1 and parts[1] != "xx" else None
    yy_input = parts[2] if len(parts) > 2 and parts[2] != "xxxx" else None
    cvv_input = parts[3] if len(parts) > 3 and parts[3] != "xxx" else None

    bin_clean = re.sub(r"[^\d]", "", bin_format)[:6]

    if not bin_clean.isdigit() or len(bin_clean) < 6:
        return f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝘽𝙄𝙉 𝙥𝙧𝙤𝙫𝙞𝙙𝙚𝙙.\n\n𝙀𝙭𝙖𝙢𝙥𝙡𝙚:\n<code>/gen 545231xxxxxxxxxx|03|27|xxx</code>"

    scheme = "MASTERCARD" if bin_clean.startswith("5") else "VISA" if bin_clean.startswith("4") else "UNKNOWN"
    ctype = "DEBIT" if bin_clean.startswith("5") else "CREDIT" if bin_clean.startswith("4") else "UNKNOWN"

    cards = []
    start = time.time()
    for _ in range(10):
        cc = generate_card(bin_format)
        mm = mm_input if mm_input else str(random.randint(1, 12)).zfill(2)
        yy_full = yy_input if yy_input else str(random.randint(2026, 2032))
        yy = yy_full[-2:]
        cvv = cvv_input if cvv_input else str(random.randint(100, 999))
        cards.append(f"<code>{cc}|{mm}|{yy}|{cvv}</code>")
    elapsed = round(time.time() - start, 3)

    card_lines = "\n".join(cards)

    text = f"""<b>───────────────</b>
<b>Info</b> - ↯ {scheme} - {ctype}
<b>───────────────</b>
<b>Bin</b> - ↯ {bin_clean} |<b>Time</b> - ↯ {elapsed}s
<b>Input</b> - ↯ <code>{bin_input}</code>
<b>───────────────</b>
{card_lines}
<b>───────────────</b>
<b>Requested By</b> - ↯ @{username} [Free]
"""
    return text

# ✅ /start command with anime clip + styled welcome
@bot.message_handler(commands=['start'])
def start_handler(message):
    # Save user ID
    user_id = str(message.from_user.id)
    with open("users.txt", "a+") as f:
        f.seek(0)
        if user_id not in f.read().splitlines():
            f.write(user_id + "\n")

    first_name = message.from_user.first_name
    welcome_text = f"""
「✦ 𝙊𝙎𝙉 𝙂𝙀𝙉 ✦」

𝙐𝙎𝙀𝙍 ↯ <i>{first_name}</i>  
𝙎𝙏𝘼𝙏𝘼𝙎 ↯ New Member  
𝙈𝙀𝙈ʙᴇʀ ↯ Free User   

━━━━━━━━━━━━━━━━
"""
    clip = random.choice(anime_clips)

    bot.send_video(
        chat_id=message.chat.id,
        video=clip,
        caption=welcome_text,
        parse_mode='HTML',
        reply_markup=get_welcome_markup()
    )

# ✅ Callback handler for /start buttons
@bot.callback_query_handler(func=lambda call: call.data == "commands")
def callback_handler(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "📜 𝘼𝙑𝘼𝙄𝙇𝘼𝘽𝙇𝙀 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:\n\n/start - 𝙎𝙏𝘼𝙍𝙏 𝙏𝙃𝙀 𝘽𝙊𝙏\n/gen - 𝙂𝙀𝙉𝙀𝙍𝘼𝙏𝙀 𝘾𝘼𝙍𝘿𝙎\n/fake - 𝙂𝙀𝙉𝙀𝙍𝘼𝙏𝙀 𝙁𝘼𝙆𝙀 𝘼𝘿𝘿𝙍𝙀𝙎𝙎\n/country - 𝘾𝙊𝙐𝙉𝙏𝙍𝙔 𝘼𝙑𝘼𝙄𝙇𝘼𝘽𝙇𝙀 𝙁𝙊𝙍 𝙁𝘼𝙆𝙀 𝘼𝘿𝘿𝙍𝙀𝙎𝙎\n/ask - 𝘼𝙎𝙆 𝘾𝙃𝘼𝙏𝙂𝙋𝙏"
    )

# ✅ /gen command
@bot.message_handler(commands=['gen'])
def gen_handler(message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return bot.reply_to(message, "⚠️ 𝙀𝙭𝙖𝙢𝙥𝙡𝙚:\n<code>/gen 545231xxxxxxxxxx|03|27|xxx</code>", parse_mode="HTML")

    bin_input = parts[1].strip()
    username = message.from_user.username or "anonymous"
    text = generate_output(bin_input, username)

    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton("Re-Generate ♻️", callback_data=f"again|{bin_input}"))
    bot.reply_to(message, text, parse_mode="HTML", reply_markup=btn)

# ✅ /gen button callback
@bot.callback_query_handler(func=lambda call: call.data.startswith("again|"))
def again_handler(call):
    bin_input = call.data.split("|", 1)[1]
    username = call.from_user.username or "anonymous"
    text = generate_output(bin_input, username)

    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton("Re-Generate ♻️", callback_data=f"again|{bin_input}"))

    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              parse_mode="HTML",
                              reply_markup=btn)
    except:
        bot.send_message(call.message.chat.id, text, parse_mode="HTML", reply_markup=btn)

# ✅ /ask command (uses external GPT API)
@bot.message_handler(commands=['ask'])
def ask_handler(message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return bot.reply_to(message, "❓ Usage: `/ask your question`", parse_mode="Markdown")
    
    prompt = parts[1]
    try:
        res = requests.get(f"https://gpt-3-5.apis-bj-devs.workers.dev/?prompt={prompt}")
        if res.status_code == 200:
            data = res.json()
            if data.get("status") and data.get("reply"):
                reply = data["reply"]
                bot.reply_to(message, f"*{reply}*", parse_mode="Markdown")
            else:
                bot.reply_to(message, "❌ Couldn't parse reply from API.", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ GPT API failed to respond.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: `{e}`", parse_mode="Markdown")

# ✅ /fake command (generate fake address)
@bot.message_handler(commands=['fake'])
def fake_address_handler(message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        return bot.reply_to(message, "⚠️ 𝙀𝙭𝙖𝙢𝙥𝙡𝙚:\n`/fake us`", parse_mode="Markdown")

    country_code = parts[1].strip().lower()

    supported = [
        "dz","ar","au","bh","bd","be","br","kh","ca","co","dk","eg",
        "fi","fr","de","in","it","jp","kz","my","mx","ma","nz","pa",
        "pk","pe","pl","qa","sa","sg","es","se","ch","th","tr","uk",
        "us"
    ]

    if country_code not in supported:
        return bot.reply_to(message, "❌ This country is not supported or you entered an invalid code.", parse_mode="Markdown")

    url = f"https://randomuser.me/api/?nat={country_code}"
    try:
        res = requests.get(url).json()
        user = res['results'][0]

        name = f"{user['name']['first']} {user['name']['last']}"
        addr = user['location']
        full_address = f"{addr['street']['number']} {addr['street']['name']}"
        city = addr['city']
        state = addr['state']
        zip_code = addr['postcode']
        country = addr['country']

        msg = f"""📦 *Fake Address Info*

👤 *Name:* `{name}`
🏠 *Address:* `{full_address}`
🏙️ *City:* `{city}`
🗺️ *State:* `{state}`
📮 *ZIP:* `{zip_code}`
🌐 *Country:* `{country.upper()}`"""

        bot.reply_to(message, msg, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "❌ Something went wrong. Please try again later.", parse_mode="Markdown")

# ✅ /country command
@bot.message_handler(commands=['country'])
def country_command(message):
    msg = """🌍 *𝙎𝙪𝙥𝙥𝙤𝙧𝙩𝙚𝙙 𝘾𝙤𝙪𝙣𝙩𝙧𝙞𝙚𝙨:*

1. 𝘼𝙡𝙜𝙚𝙧𝙞𝙖 (𝘿𝙕)
2. 𝘼𝙧𝙜𝙚𝙣𝙩𝙞𝙣𝙖 (𝘼𝙍)
3. 𝘼𝙪𝙨𝙩𝙧𝙖𝙡𝙞𝙖 (𝘼𝙐)
4. 𝘽𝙖𝙝𝙧𝙖𝙞𝙣 (𝘽𝙃)
5. 𝘽𝙖𝙣𝙜𝙡𝙖𝙙𝙚𝙨𝙝 (𝘽𝘿)
6. 𝘽𝙚𝙡𝙜𝙞𝙪𝙢 (𝘽𝙀)
7. 𝘽𝙧𝙖𝙯𝙞𝙡 (𝘽𝙍)
8. 𝘾𝙖𝙢𝙗𝙤𝙙𝙞𝙖 (𝙆𝙃)
9. 𝘾𝙖𝙣𝙖𝙙𝙖 (𝘾𝘼)
10. 𝘾𝙤𝙡𝙤𝙢𝙗𝙞𝙖 (𝘾𝙊)
11. 𝘿𝙚𝙣𝙢𝙖𝙧𝙠 (𝘿𝙆)
12. 𝙀𝙜𝙮𝙥𝙩 (𝙀𝙂)
13. 𝙁𝙞𝙣𝙡𝙖𝙣𝙙 (𝙁𝙄)
14. 𝙁𝙧𝙖𝙣𝙘𝙚 (𝙁𝙍)
15. 𝙂𝙚𝙧𝙢𝙖𝙣𝙮 (𝘿𝙀)
16. 𝙄𝙣𝙙𝙞𝙖 (𝙄𝙉)
17. 𝙄𝙩𝙖𝙡𝙮 (𝙄𝙏)
18. 𝙅𝙖𝙥𝙖𝙣 (𝙅𝙋)
19. 𝙆𝙖𝙯𝙖𝙠𝙝𝙨𝙩𝙖𝙣 (𝙆𝙕)
20. 𝙈𝙖𝙡𝙖𝙮𝙨𝙞𝙖 (𝙈𝙔)
21. 𝙈𝙚𝙭𝙞𝙘𝙤 (𝙈𝙓)
22. 𝙈𝙤𝙧𝙤𝙘𝙘𝙤 (𝙈𝘼)
23. 𝙉𝙚𝙬 𝙕𝙚𝙖𝙡𝙖𝙣𝙙 (𝙉𝙕)
24. 𝙋𝙖𝙣𝙖𝙢𝙖 (𝙋𝘼)
25. 𝙋𝙖𝙠𝙞𝙨𝙩𝙖𝙣 (𝙋𝙆)
26. 𝙋𝙚𝙧𝙪 (𝙋𝙀)
27. 𝙋𝙤𝙡𝙖𝙣𝙙 (𝙋𝙇)
28. 𝙌𝙖𝙩𝙖𝙧 (𝙌𝘼)
29. 𝙎𝙖𝙪𝙙𝙞 𝘼𝙧𝙖𝙗𝙞𝙖 (𝙎𝘼)
30. 𝙎𝙞𝙣𝙜𝙖𝙥𝙤𝙧𝙚 (𝙎𝙂)
31. 𝙎𝙥𝙖𝙞𝙣 (𝙀𝙎)
32. 𝙎𝙬𝙚𝙙𝙚𝙣 (𝙎𝙀)
33. 𝙎𝙬𝙞𝙩𝙯𝙚𝙧𝙡𝙖𝙣𝙙 (𝘾𝙃)
34. 𝙏𝙝𝙖𝙞𝙡𝙖𝙣𝙙 (𝙏𝙃)
35. 𝙏𝙪𝙧𝙠𝙞𝙮𝙚 (𝙏𝙍)
36. 𝙐𝙣𝙞𝙩𝙚𝙙 𝙆𝙞𝙣𝙜𝙙𝙤𝙢 (𝙐𝙆)
37. 𝙐𝙣𝙞𝙩𝙚𝙙 𝙎𝙩𝙖𝙩𝙚𝙨 (𝙐𝙎)"""
    bot.reply_to(message, msg, parse_mode="Markdown")

# ✅ Broadcast command (only for bot owner)
OWNER_ID = 7513014218  # apna Telegram ID dalna

@bot.message_handler(commands=['broadcast'])
def broadcast_handler(message):
    if message.from_user.id != OWNER_ID:
        return bot.reply_to(message, "🚫 You are not authorized to use this command.")

    try:
        _, text = message.text.split(" ", 1)
    except:
        return bot.reply_to(message, "⚠️ Usage:\n`/broadcast Your message here`", parse_mode="Markdown")

    bot.reply_to(message, "📢 Sending broadcast to all users...")

    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        return bot.send_message(message.chat.id, "❌ No users found in users.txt")

    sent, failed = 0, 0
    for uid in users:
        try:
            bot.send_message(uid, f"📢 *Broadcast Message:*\n\n{text}", parse_mode="Markdown")
            sent += 1
            time.sleep(0.1)
        except Exception:
            failed += 1
            continue

    bot.send_message(
        message.chat.id,
        f"✅ Broadcast completed.\n\n🟢 Sent: `{sent}`\n🔴 Failed: `{failed}`",
        parse_mode="Markdown"
    )

print("🤖 Bot is running...")
bot.polling()
