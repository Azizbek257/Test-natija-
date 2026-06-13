import telebot
from telebot import types
import json

# SIZNING ANIQ MA'LUMOTLARINGIZ
TOKEN = '8892374177:AAF9qi4G7DLBgxPWgOj9HD_1L5YKFTkKwMk'
ADMIN_ID = 7743401064  # Sizning ID raqamingiz muvaffaqiyatli qo'yildi

bot = telebot.TeleBot(TOKEN)

MINI_APP_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>Premium Imtihon</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; padding: 15px; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; text-align: center; }
        .timer { font-size: 24px; font-weight: bold; color: #e74c3c; margin: 10px 0; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 15px; }
        .btn { background-color: #3498db; color: white; border: none; padding: 12px; font-size: 14px; font-weight: bold; border-radius: 8px; }
        .finish-btn { background-color: #2ecc71; width: 100%; font-size: 18px; padding: 15px; margin-top: 20px; color: white; border: none; border-radius: 8px; }
        h3 { margin: 0; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="card">
        <h3>⏳ Qolgan vaqt:</h3>
        <div class="timer" id="countdown">30:00</div>
    </div>
    <div class="card">
        <h3>✏️ Javoblarni belgilang:</h3>
        <div style="text-align: left; margin-bottom: 10px;"><b>1-Savol:</b></div>
        <div class="grid">
            <button class="btn" onclick="selectAns(1, 'A')">A</button>
            <button class="btn" onclick="selectAns(1, 'B')">B</button>
            <button class="btn" onclick="selectAns(1, 'C')">C</button>
            <button class="btn" onclick="selectAns(1, 'D')">D</button>
        </div>
    </div>
    <button class="finish-btn" onclick="sendResults()">🏁 Testni yakunlash</button>
    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        let answers = {};
        function selectAns(qNum, option) {
            answers[qNum] = option;
            tg.HapticFeedback.impactOccurred('light');
            alert(qNum + "-savolga " + option + " javobi tanlandi!");
        }
        function sendResults() {
            tg.sendData(JSON.stringify(answers));
            tg.close();
        }
    </script>
</body>
</html>
"""

from flask import Flask
import _thread
app = Flask(__name__)

@app.route('/')
def home():
    return MINI_APP_HTML

def run_server():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if user_id == ADMIN_ID:
        item1 = types.KeyboardButton("📊 Umumiy Statistika")
        item2 = types.KeyboardButton("➕ Yangi Test yuklash")
        markup.add(item1, item2)
        bot.send_message(user_id, "Xush kelibsiz, Ustoz (Admin)! Quyidagi paneldan foydalaning:", reply_markup=markup)
    else:
        # Keyinchalik Render server manzilini bitta shu erga yozib qo'yamiz
        web_app = types.WebAppInfo("https://google.com")
        item = types.KeyboardButton("📱 Imtihonni boshlash (Mini App)", web_app=web_app)
        markup.add(item)
        bot.send_message(user_id, f"Salom! Testni boshlash uchun quyidagi tugmani bosing.", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def web_app_data_receive(message):
    data = json.loads(message.web_app_data.data)
    javoblar_matni = "".join([f" {q}-savol: {ans}\n" for q, ans in data.items()])
    bot.send_message(message.chat.id, f"🏁 Test yakunlandi!\n\nJavoblaringiz:\n{javoblar_matni}")

if __name__ == "__main__":
    _thread.start_new_thread(run_server, ())
    print("Bot va Mini App serveri tayyor...")
    bot.polling(none_stop=True)
