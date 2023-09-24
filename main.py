import requests,os,time,telebot
from config import TOKEN

def download_video(message):
    file_name = message.text.split("/")[-1]
    try:
        response = requests.get(message.text, stream=True)
        msg = bot.reply_to(message,"يتم التحميل انتظر...")
    except Execption as error:
        print(error)
        bot.reply_to(message,"خطأ ارسل رابط صحيح.")
    file_size = int(response.headers.get("Content-Length", 0))
    downloaded_size = 0

    with open(file_name, "wb") as file:
        start_time = time.time()
        num = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                progress = round(downloaded_size / file_size * 100, 2)
                elapsed_time = round(time.time() - start_time, 2)
                remaining_size = round(file_size - downloaded_size, 2)
                file_sizes = file_size / 1048576
                
                after_point = int((file_sizes % 1) * 100)
                file_sizes = f"{int(file_sizes)}.{after_point}"
                
                remaining_sizes = remaining_size / 1048576
                after_point2 = int((remaining_sizes % 1) * 100)
                
                remaining_sizes = f"{int(remaining_sizes)}.{after_point2}"
                num += 1
                if num >= 1000:
                    bot.edit_message_text(
                    	text=f"""نسبة التحميل {progress}%

المدة المستغرقة: {elapsed_time}s 

الحجم الاجمالي: {file_sizes} MB

الحجم المتبقي: {remaining_sizes} MB""",
message_id=msg.message_id,
                    	chat_id=message.chat.id
                    )
                    num-=1000
        bot.send_video(message.chat.id,open(file_name,"rb"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message,"مرحبا ارسل الرابط")

@bot.message_handler(func = lambda message:True)
def movie(message):
	if ".mp4" not in message.text:
		return bot.reply_to(message,"ارسل رابط فيديو فقط.")
	url = message
	download_video(url)
bot.infinity_polling()