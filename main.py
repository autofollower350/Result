import nest_asyncio
nest_asyncio.apply()

import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Client("jnvu_result_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await message.reply(
        "**🎓 Welcome to JNVU Result Bot!**\n\n"
        "अपना Roll Number भेजें:\nउदाहरण: `25rba00299`", quote=True)

@app.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    await message.reply(
        "**🆘 Help Menu**\n\n"
        "`/start` - Welcome message\n"
        "`/help` - Show help\n"
        "`25rba00299` - Send roll number to get your PDF result", quote=True)

@app.on_message(filters.text & filters.private)
async def handle_roll_number(client: Client, message: Message):
    roll_number = message.text.strip()

    if not (6 <= len(roll_number) <= 15 and roll_number.isalnum()):
        await message.reply("⚠️ कृपया सही Format में Roll Number भेजें: `25rba00299`")
        return

    try:
        for f in os.listdir(DOWNLOAD_DIR):
            if f.endswith(".pdf"):
                os.remove(os.path.join(DOWNLOAD_DIR, f))

        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })

        driver = webdriver.Chrome(service=Service(os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)

        driver.get("https://share.google/RiGoUdAWQEkczypqg")
        time.sleep(4)

        driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[1]/fieldset/div/div[1]/div/div[1]/table/tbody/tr[2]/td/div/div/ul/li[1]/span[3]/a").click()
        time.sleep(3)

        driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/fieldset/div/div[3]/div/div/div/table/tbody/tr[2]/td/div/ul/div/table/tbody/tr[2]/td[2]/span[1]/a").click()
        time.sleep(3)

        driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div[2]/table/tbody/tr/td[2]/span/input").send_keys(roll_number)
        time.sleep(1)

        driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div[3]/span[1]/input").click()
        time.sleep(6)

        driver.quit()

        pdf_path = None
        for _ in range(10):
            pdf_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".pdf")]
            if pdf_files:
                pdf_path = os.path.join(DOWNLOAD_DIR, pdf_files[0])
                break
            time.sleep(1)

        if pdf_path and os.path.exists(pdf_path):
            await message.reply_document(pdf_path, caption=f"📄 Result for: `{roll_number}`")
        else:
            await message.reply("❌ PDF नहीं मिला, कृपया बाद में प्रयास करें।")

    except Exception as e:
        await message.reply(f"🚨 Error: {e}")

if __name__ == "__main__":
    async def main():
        await app.start()
        print("✅ Bot is running...")
        await asyncio.Event().wait()

    asyncio.run(main())
