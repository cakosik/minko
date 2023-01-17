from imports import * 
if __name__ == "__main__":
    bot = Bot(token=config.token, disable_web_page_preview=True); dp = Dispatcher(bot); executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)