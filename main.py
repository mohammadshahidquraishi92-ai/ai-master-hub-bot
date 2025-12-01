import telebot
import time
import requests
from telebot import types
from server import run
import threading

# -----------------------------
# CONFIGURATION (REPLACE THESE)
# -----------------------------
BOT_TOKEN = "8049499534:AAEfdAd05fFnjphdsRcU39asOGcamSvMVKg"
CHANNEL_USERNAME = "@botx_updates1"
BINANCE_PAY_ID = "1011581500"
TRUST_WALLET_ADDRESS = "TPZWjEsRy2TJKyn192zK9vrSqUfVdzCkdp"

bot = telebot.TeleBot(BOT_TOKEN)

# -----------------------------
# PREMIUM DATABASE (SIMPLE)
# -----------------------------
premium_users = {}
referrals = {}

# -----------------------------
# START MESSAGE
# -----------------------------
@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    name = msg.from_user.first_name

    # Referral check
    if msg.text.startswith("/start ") and user_id not in referrals:
        ref = msg.text.split("/start ")[1]
        if ref != str(user_id):
            if ref not in referrals:
                referrals[ref] = 0
            referrals[ref] += 1

            # Reward 7 days premium
            if referrals[ref] == 3:
                premium_users[ref] = time.time() + (7 * 24 * 3600)
                bot.send_message(ref, "🎉 You invited 3 people!\nYou received **7 DAYS PREMIUM** 🎁")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📢 Bot Updates Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))

    bot.send_message(
        user_id,
        f"👋 **Welcome {name}!**\n\n"
        "🔥 *AI Master Hub – Your Smart All-in-One AI Assistant*\n\n"
        "**Free version includes:**\n"
        "• 3 AI image generations per day\n"
        "• Basic AI chat\n"
        "• Simple text tools\n\n"
        "**Premium version includes:**\n"
        "• Unlimited AI images\n"
        "• Unlimited AI chat\n"
        "• 10+ extra AI tools\n"
        "• Faster responses\n"
        "• No limits\n\n"
        "Invite **3 friends** to get **7-day premium free** 🎁\n"
        f"Your referral link:\n`https://t.me/{bot.get_me().username}?start={user_id}`",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# -----------------------------
# CHECK PREMIUM
# -----------------------------
def is_premium(user_id):
    if user_id in premium_users:
        if time.time() < premium_users[user_id]:
            return True
    return False

# -----------------------------
# PAYMENT / PREMIUM
# -----------------------------
@bot.message_handler(commands=['premium'])
def premium(msg):
    user_id = msg.chat.id

    text = (
        "🌟 **AI Master Hub Premium Plans**\n\n"
        "💛 1 Month → 4.99 USD\n"
        "💙 6 Months → 19.99 USD\n"
        "❤️ 1 Year → 29.99 USD\n\n"
        "**Payment Methods:**\n"
        f"• Binance Pay ID: `{BINANCE_PAY_ID}`\n"
        f"• Trust Wallet (USDT TRC20): `{TRUST_WALLET_ADDRESS}`\n\n"
        "After payment, send the screenshot here."
    )

    bot.send_message(user_id, text, parse_mode="Markdown")

# -----------------------------
# IMAGE GENERATION LIMIT
# -----------------------------
daily_usage = {}

def can_generate(user_id):
    if is_premium(user_id):
        return True  # unlimited

    today = int(time.time() // 86400)

    if user_id not in daily_usage:
        daily_usage[user_id] = {}

    if today not in daily_usage[user_id]:
        daily_usage[user_id][today] = 0

    if daily_usage[user_id][today] < 3:
        daily_usage[user_id][today] += 1
        return True

    return False

# -----------------------------
# AI IMAGE GENERATION (DEMO)
# -----------------------------
@bot.message_handler(commands=['image'])
def image(msg):
    user_id = msg.chat.id

    if not can_generate(user_id):
        bot.send_message(user_id, "❌ You reached your daily limit (3 images).\nBuy premium for unlimited images.")
        return

    bot.send_message(user_id, "🖼️ Send the prompt for your image:")

    bot.register_next_step_handler(msg, make_image)

def make_image(msg):
    user_id = msg.chat.id
    prompt = msg.text

    bot.send_message(user_id, "⏳ Generating your image...")

    # Demo image generation (replace with actual API later)
    bot.send_photo(user_id, "https://picsum.photos/512", caption=f"Prompt: {prompt}")

# -----------------------------
# TEXT AI (DEMO)
# -----------------------------
@bot.message_handler(func=lambda m: True)
def chat(msg):
    user_id = msg.chat.id

    if not is_premium(user_id):
        bot.send_message(user_id, "💬 *Free Chat:* You can ask simple questions.\nUpgrade to premium for full AI power.", parse_mode="Markdown")

    # Demo response
    bot.send_message(user_id, "🤖 I am your AI Assistant! Ask me anything.")

# -----------------------------
# RUN BOT + SERVER
# -----------------------------
t = threading.Thread(target=run)
t.start()

print("Bot is running...")
bot.polling()
