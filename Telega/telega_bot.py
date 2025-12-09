import urllib.request
import urllib.parse

BOT_TOKEN = ""
CHAT_ID = ""

# Открываем и читаем файл
with open('test.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Отправляем в Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = urllib.parse.urlencode({
    'chat_id': CHAT_ID,
    'text': text
}).encode('utf-8')

req = urllib.request.Request(url, data=data)
urllib.request.urlopen(req)
print("✅ Файл text.txt отправлен!")
