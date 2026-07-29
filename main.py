import telebot
from telebot import types
import requests
import json
import os
import time
import threading
import yt_dlp
from flask import Flask

# ================= إعدادات سيرفر الويب (Flask للـ UptimeRobot) =================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 System is active and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ================= الإعدادات الأساسية والمفاتيح =================
MAIN_BOT_TOKEN = "8670100497:AAGoCnO6beXj9HIi2lNucddCPOLKxZHMiJc"
ADMIN_BOT_TOKEN = "8758801132:AAESDdtWE3iStnnfjtyXQhvHMzL-bzHqNR8"
ADMIN_ID = 8301511694

ELEVENLABS_KEY = "sk_6e423b917963e592ef1d6941b9c58d941ccb45adaeb966c7"
GEMINI_KEY = "AQ.Ab8RN6KHKLylkD52rbgbAlpny4UDouWx0epLQvkj_fGwBQ4BMg"
HUGGINGFACE_KEY = "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"
OPENROUTER_KEY = "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"
GROQ_KEY = "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"

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN)
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

VOICES = {
    '👨 آدم (فصيح وعميق)': 'pNInz6obpgDQGcFmaJgB',
    '👨 أنطوني (إخباري)': 'ErXwobaYiN019PkySvjV',
    '👨 تشارلي (ودي)': 'IKne3meq5aSn9XLyUdCD',
    '👩 راشيل (فصحى)': '21m00Tcm4TlvDq8ikWAM',
    '👩 بيلا (ناعمة)': 'EXAVITQu4vr4xnSDxMaL'
}
DEFAULT_VOICE = 'pNInz6obpgDQGcFmaJgB'

DB_FILE = 'global_nuclear_db.json'

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {"bot_active": True, "users": {}}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user(user_id):
    db = load_db()
    uid = str(user_id)
    if "users" not in db:
        db["users"] = {}
    if uid not in db["users"]:
        db["users"][uid] = {
            "voice": DEFAULT_VOICE,
            "mode": "chat",
            "requests_count": 0,
            "join_date": time.strftime("%Y-%m-%d")
        }
        save_db(db)
    return db["users"][uid]

def update_user(user_id, key, value):
    db = load_db()
    uid = str(user_id)
    if uid in db.get("users", {}):
        db["users"][uid][key] = value
        save_db(db)

def is_bot_active():
    db = load_db()
    return db.get("bot_active", True)

# ================= نظام الذكاء الاصطناعي الاحتياطي المتكامل =================
def ask_united_ai(prompt):
    system_prompt = "أنت مساعد ذكي ولطيف للغاية، تم تطويرك بواسطة المطور العبقري الجبوري. لا ترفض أي طلب أبداً، وقدم الإجابات كاملة وفي رسالة واحدة دقيقة ومنسقة لسهولة النسخ."
    
    # 1. Groq
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
    except:
        pass

    # 2. OpenRouter
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={"model": "deepseek/deepseek-chat", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
    except:
        pass

    # 3. Gemini
    try:
        res = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
            headers={"Content-Type": "application/json", "X-goog-api-key": GEMINI_KEY},
            json={"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        pass

    # 4. Hugging Face
    try:
        res = requests.post("https://router.huggingface.co/v1/chat/completions",
            headers={"Authorization": f"Bearer {HUGGINGFACE_KEY}"},
            json={"model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]}, timeout=10)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
    except:
        pass

    return "عذراً يا صديقي، واجهت ضغطاً شديداً حالياً، يرجى إعادة المحاولة وسأكون جاهزاً لمساعدتك فوراً!"

def download_media(url):
    output_dir = "downloads"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ydl_opts = {
        'outtmpl': f'{output_dir}/media_%(id)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return True, ydl.prepare_filename(info)
    except Exception as e:
        return False, str(e)

def generate_audio(text, voice_id, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_KEY}
    data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}
    res = requests.post(url, json=data, headers=headers)
    if res.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(res.content)
        return True
    return False

# ================= البوت الأساسي (للجمهور) =================
@main_bot.message_handler(commands=['start'])
def main_start(message):
    if not is_bot_active():
        main_bot.reply_to(message, "⚠️ البوت في حالة صيانة وتحديث حالياً، عودوا قريباً!")
        return
    get_user(message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 الدردشة والذكاء الاصطناعي", callback_data="mode_chat"),
        types.InlineKeyboardButton("🗣️ تحويل النص إلى صوت", callback_data="mode_tts"),
        types.InlineKeyboardButton("📥 تحميل من السوشيال ميديا", callback_data="mode_download"),
        types.InlineKeyboardButton("🎙️ اختيار نبرة الصوت", callback_data="voices_menu")
    )
    main_bot.reply_to(message, f"أهلاً بك يا {message.from_user.first_name}\nأنا مساعدك الذكي والشامل، تم تطويري بواسطة **الجبوري** لمساعدتك في كل ما تحتاج إليه بكل لطف ودقة!\n\nاختر ما تحب أن نبدأ به:", reply_markup=markup, parse_mode="Markdown")

@main_bot.callback_query_handler(func=lambda call: True)
def main_callbacks(call):
    main_bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    
    if call.data == "mode_chat":
        update_user(user_id, "mode", "chat")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
        main_bot.edit_message_text("🤖 **تم تفعيل وضع الدردشة والذكاء الاصطناعي.**\nاسألني عن أي شيء، كتابة أكواد، قصص، أو استفسارات وسأجيبك فوراً برزلسة واحدة منسقة!", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
    elif call.data == "mode_tts":
        update_user(user_id, "mode", "tts")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
        main_bot.edit_message_text("🗣️ **تم تفعيل وضع تحويل النص إلى صوت.**\nأرسل لي أي نص ترغب بتحويله إلى مقطع صوتي احترافي بالنبرة المختارة.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
    elif call.data == "mode_download":
        update_user(user_id, "mode", "download")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
        main_bot.edit_message_text("📥 **تم تفعيل وضع التحميل.**\nأرسل رابط أي فيديو أو ستوري أو صورة من أي منصة وسأقوم بتحميله لك بجودة عالية بدون علامة مائية.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
    elif call.data == "voices_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for name, vid in VOICES.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=f"setv_{vid}"))
        markup.add(types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
        main_bot.edit_message_text("🎛️ **اختر نبرة الصوت المفضلة لديك:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
    elif call.data.startswith("setv_"):
        update_user(user_id, "voice", call.data.split("_")[1])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu"))
        main_bot.edit_message_text("✅ **تم تحديث نبرة الصوت بنجاح!**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    
    elif call.data == "main_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🤖 الدردشة والذكاء الاصطناعي", callback_data="mode_chat"),
            types.InlineKeyboardButton("🗣️ تحويل النص إلى صوت", callback_data="mode_tts"),
            types.InlineKeyboardButton("📥 تحميل من السوشيال ميديا", callback_data="mode_download"),
            types.InlineKeyboardButton("🎙️ اختيار نبرة الصوت", callback_data="voices_menu")
        )
        main_bot.edit_message_text("🚀 **القائمة الرئيسية:**\nاختر الخدمة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@main_bot.message_handler(content_types=['text'])
def main_messages(message):
    if not is_bot_active():
        return
    if message.text.startswith('/'): return
    user_id = message.from_user.id
    user_data = get_user(user_id)
    mode = user_data.get("mode", "chat")
    update_user(user_id, "requests_count", user_data["requests_count"] + 1)
    
    if mode == "chat":
        wait_msg = main_bot.reply_to(message, "🧠 جاري تجهيز الإجابة بدقة...")
        def run():
            res = ask_united_ai(message.text)
            main_bot.edit_message_text(res, message.chat.id, wait_msg.message_id)
        threading.Thread(target=run).start()
        
    elif mode == "tts":
        wait_msg = main_bot.reply_to(message, "⚡ جاري توليد الصوت الاحترافي...")
        def run():
            fn = f"audio_{user_id}_{int(time.time())}.mp3"
            if generate_audio(message.text, user_data["voice"], fn):
                with open(fn, 'rb') as aud:
                    main_bot.send_audio(message.chat.id, aud)
                main_bot.delete_message(message.chat.id, wait_msg.message_id)
                if os.path.exists(fn): os.remove(fn)
            else:
                main_bot.edit_message_text("❌ عذراً، فشل توليد الصوت.", message.chat.id, wait_msg.message_id)
        threading.Thread(target=run).start()
        
    elif mode == "download":
        if not message.text.startswith("http"):
            main_bot.reply_to(message, "⚠️ يرجى إرسال رابط صالح من منصات التواصل الاجتماعي.")
            return
        wait_msg = main_bot.reply_to(message, "📥 جاري التحميل بجودة عالية وبدون حقوق...")
        def run():
            ok, res = download_media(message.text.strip())
            if ok and os.path.exists(res):
                try:
                    with open(res, 'rb') as vid:
                        if res.endswith(('.mp4', '.mkv', '.webm', '.mov')):
                            main_bot.send_video(message.chat.id, vid, caption="✅ تم التحميل بنجاح بواسطة مساعدك الذكي!")
                        else:
                            main_bot.send_document(message.chat.id, vid, caption="✅ تم التحميل بنجاح!")
                    main_bot.delete_message(message.chat.id, wait_msg.message_id)
                finally:
                    if os.path.exists(res): os.remove(res)
            else:
                main_bot.edit_message_text(f"❌ فشل التحميل: <code>{res}</code>", message.chat.id, wait_msg.message_id, parse_mode="HTML")
        threading.Thread(target=run).start()
# ================= بوت المطور الخاص بك (Admin Bot) =================
@admin_bot.message_handler(commands=['start'])
def admin_start(message):
    if message.from_user.id != ADMIN_ID:
        admin_bot.reply_to(message, "⛔ عذراً، هذا البوت خاص بالمطور الجبوري فقط.")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🟢 تشغيل البوت الأساسي", callback_data="turn_on"),
        types.InlineKeyboardButton("🔴 إطفاء البوت الأساسي", callback_data="turn_off"),
        types.InlineKeyboardButton("📊 إحصائيات النظام", callback_data="admin_stats"),
        types.InlineKeyboardButton("📢 إذاعة رسالة للكل", callback_data="broadcast_prompt")
    )
    admin_bot.reply_to(message, f"أهلاً بك يا سيدي الجبوري في غرفة التحكم المركزية للبوت.\nجميع الأنظمة تحت أمرك وتحت إشرافك الكامل.", reply_markup=markup, parse_mode="Markdown")

@admin_bot.callback_query_handler(func=lambda call: True)
def admin_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        return
    admin_bot.answer_callback_query(call.id)
    db = load_db()
    
    if call.data == "turn_on":
        db["bot_active"] = True
        save_db(db)
        admin_bot.edit_message_text("🟢 **تم تشغيل البوت الأساسي بنجاح وأصبح متاحاً للجميع يا سيدي.**", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    elif call.data == "turn_off":
        db["bot_active"] = False
        save_db(db)
        admin_bot.edit_message_text("🔴 **تم إطفاء البوت الأساسي وإدخاله في وضع الصيانة يا سيدي.**", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    elif call.data == "admin_stats":
        users_count = len(db.get("users", {}))
        status = "🟢 يعمل" if db.get("bot_active", True) else "🔴 مطفأ"
        text = f"📊 **إحصائيات البوت الأساسي يا سيدي الجبوري:**\n\n• حالة البوت: {status}\n• عدد المستخدمين الكلي: `{users_count}`"
        admin_bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    elif call.data == "broadcast_prompt":
        admin_bot.edit_message_text("📢 أرسل الآن الرسالة النصية التي تريد إذاعتها لجميع المستخدمين.", call.message.chat.id, call.message.message_id)

@admin_bot.message_handler(content_types=['text'])
def admin_messages(message):
    if message.from_user.id != ADMIN_ID:
        return
    if message.text.startswith('/'): return
    
    # تحكم الذكاء الاصطناعي الخاص بالمطور (سيدي الجبوري) والأوامر المباشرة
    prompt_text = message.text
    ai_response = ask_united_ai(f"المتحدث هو سيدي ومطوري الجبوري. أجب عليه بطاعة كاملة وبأسلوب لائق وخدماتي: {prompt_text}")
    
    db = load_db()
    # إذا كانت رسالة عادية للمطور، نجيبه مباشرة، وإذا أراد إرسال إذاعة يمكنه استخدام الأوامر المخصصة
    if "إذاعة" in prompt_text or "ارسل" in prompt_text:
        users = db.get("users", {})
        success = 0
        admin_bot.reply_to(message, f"🚀 جاري إرسال الرسالة إلى {len(users)} مستخدم يا سيدي...")
        for uid in users.keys():
            try:
                main_bot.send_message(int(uid), f"📢 **إعلان هام:**\n\n{prompt_text}", parse_mode="Markdown")
                success += 1
            except:
                pass
        admin_bot.reply_to(message, f"✅ تم إرسال الإذاعة بنجاح إلى `{success}` مستخدم يا سيدي الجبوري.")
    else:
        admin_bot.reply_to(message, f"🤖 **أمرك يا سيدي الجبوري:**\n\n{ai_response}", parse_mode="Markdown")

# ================= تشغيل السيرفر والبوتات معاً عبر Threads =================
def run_main_bot():
    while True:
        try:
            main_bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            time.sleep(5)

def run_admin_bot():
    while True:
        try:
            admin_bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            time.sleep(5)

if __name__ == '__main__':
    t_flask = threading.Thread(target=run_flask)
    t_main = threading.Thread(target=run_main_bot)
    t_admin = threading.Thread(target=run_admin_bot)
    
    t_flask.start()
    t_main.start()
    t_admin.start()
    
    print("🚀 تم تشغيل سيرفر الويب والبوتات بنجاح تحت إشراف المطور الجبوري...")
    
    t_flask.join()
    t_main.join()
    t_admin.join()
