from imports import *

bot = Bot(token=config.token, disable_web_page_preview=True)
dp = Dispatcher(bot)

async def chats_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
      return


   user_id = message.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
   user_status = str(user_status[0])

   if user_status in ['Owner', 'Helper_Admin', 'Admin']:
      chats = cursor.execute(f'SELECT * from chats')
      list_chat = []
      num = 0

      for chat in chats:
         
         num += 1

         list_chat.append(f'📎 <b>NAME: {chat[1]} | 🔎 ID:</b> <code>{chat[0]}</code> <b>| 📅 DATA:</b> <code>{chat[2]}</code>')
      
      list = '\n'.join(list_chat)

      await message.reply(list, parse_mode='html')
   else:
      return await message.reply('❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')




async def register_chat_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
      return

   user_id = message.from_user.id
   user_name = message.from_user.get_mention(as_html=True)

   chat_id = message.chat.id
   group_name = message.chat.full_name
   cursor.execute(f"SELECT chat_id FROM chats WHERE chat_id = '{chat_id}'")

   if user_id == chat_id:
      return await message.reply('❗️ Нельзя регистрировать ЛС бота, в <b>качестве чата</b>', parse_mode='html')

   if cursor.fetchone() is None:
      text_register_chat = f'''
💭 <code>{user_name}</code> , вы <b>успешно зарегистрировали</b> чат <code>{group_name}</code> 
      '''
      time_register = f'{datetime.now()}'
      
      cursor.execute("INSERT INTO chats VALUES(?, ?, ?);", (chat_id, group_name, time_register[:19]))
      connect.commit()

      await bot.send_photo(message.chat.id, text_register_chat, parse_mode='html')
   else:
      return await message.reply(f'❗️ <code>{group_name}</code> <b>уже зарегистрирован</b>', parse_mode='html')

async def cl_handler(message):
   try:
      status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
      status_block = str(status_block[0])

      if status_block == 'on':
         return


      
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      su1 = str(message.text.split()[1])
      win = numexpr.evaluate(f'{su1}')
      win2 = '{:,}'.format(win).replace(',', '.')

      text_cl = f'''
➗ <b>{su1}</b> = <code>{win2}</code>
      '''
      await message.reply(text_cl, parse_mode='html')
   except OverflowError :
      text = f'''
❗️ <b>Ошибка</b> , слишком большое число 
      '''
      await message.reply(f'{text}', parse_mode='html')
   except SyntaxError:
      text = f'''
❗️ <b>Ошибка</b>, в примере есть STRING [буквы, символы]
      '''
      await message.reply(f'{text}', parse_mode='html')

   except TypeError:
      text = f'''
❗️ <b>Ошибка</b>, число должно быть полным
      '''
      await message.reply(f'{text}', parse_mode='html')

async def reset_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = int(message.text.split()[1])

    text = ' '.join(message.text.split()[2:])


    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')

       await message.bot.send_message(message.chat.id, f"""
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')

       connect.commit()
       await message.bot.send_message(reply_user_id, f"""
<b>🆘 | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, ВЫ БЫЛИ ОБНУЛЕНЫ | 🆘</b>
💭 | Причина: <i>{text}</i>
⛔️ | Администратором: <a href='tg://user?id={user_id}'>{user_name}</a> 
       """, parse_mode='html')
       return

    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from user_family WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'DELETE from family WHERE owner_id = "{reply_user_id}"')
       connect.commit()
       await message.bot.send_message(reply_user_id, f"""
<b>🆘 | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, ВЫ БЫЛИ ОБНУЛЕНЫ | 🆘</b>
💭 | Причина: <i>{text}</i>
⛔️ | Администратором: <a href='tg://user?id={user_id}'>{user_name}</a> 
       """, parse_mode='html')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна от прав админитсратора \"ХЕЛПЕР АДМИН\"", parse_mode='html')




async def ban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    if not message.reply_to_message:
       await message.reply("Эта команда должна быть ответом на сообщение!")
       return


    msg = message
    user_id = msg.from_user.id
    reply_user_id = msg.reply_to_message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])

    


    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал бан игроку: {reply_full_name}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':

       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать бан <b>владельцу бота</b>', parse_mode='html')
       else:
         pass

       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал бан игроку: {reply_full_name}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')



async def ban_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    reply_user_id = int(message.text.split()[1])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    


    if user_status == 'Owner':
       await message.bot.send_message(reply_user_id, f"📛 | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был заблокирован по ID", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       
       print(f'{full_name} выдал бан игроку: {reply_user_name}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать бан <b>владельцу бота</b>', parse_mode='html')
       else:
         pass


       await message.bot.send_message(reply_user_id, f"📛 | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был заблокирован по ID", parse_mode='html')
       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       
       print(f'{full_name} выдал бан игроку: {reply_user_name}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')






async def unban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    if not message.reply_to_message:
       await message.reply("Эта команда должна быть ответом на сообщение!")
       return

    msg = message
    user_id = msg.from_user.id
    reply_user_id = msg.reply_to_message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])

    

    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал разбан игроку: {reply_full_name}')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')




async def unban_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    
    msg = message
    user_id = msg.from_user.id
    reply_user_id = int(message.text.split()[1])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    

    if user_status == 'Owner':
       await message.bot.send_message(reply_user_id, f"✅ | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был разблокирован по ID", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(reply_user_id, f"✅ | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был разблокирован по ID", parse_mode='html')
       await message.bot.send_message(config.owner_id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал разбан игроку: {reply_full_name}')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')



async def reset_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    

    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Масовое обнуление\n💈 | Время: навсегда\n👨 |Игроку: Всем игрокам", parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {config.start_money}')
       cursor.execute(f'UPDATE users SET bank = {0}')
       cursor.execute(f'UPDATE users SET depozit = {0}')
       cursor.execute(f'UPDATE users SET rating = {0}')
       cursor.execute(f'UPDATE users SET ethereum = {100}')
       cursor.execute(f'UPDATE mine SET iron = {0}')
       cursor.execute(f'UPDATE mine SET metall = {0}')
       cursor.execute(f'UPDATE mine SET silver = {0}')
       cursor.execute(f'UPDATE mine SET bronza = {0}')
       cursor.execute(f'UPDATE mine SET gold = {0}')
       cursor.execute(f'UPDATE farm SET linen = {0}')
       cursor.execute(f'UPDATE farm SET cotton = {0}')
       cursor.execute(f'UPDATE house SET house = {0}')
       cursor.execute(f'UPDATE house SET basement = {0}')
       cursor.execute(f'UPDATE cars SET cars = {0}')
       cursor.execute(f'UPDATE cars SET hp = {0}')
       cursor.execute(f'UPDATE cars SET benz = {0}')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} ')
       cursor.execute(f'UPDATE family SET balance = {0} ')
       connect.commit()
       full_name = msg.from_user.full_name
       print(f'{full_name} сделал масовое обнуление')
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"OWNER\"", parse_mode='html')


async def help_admins_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация для администрации чата ⛔️

1️⃣ /channel_mute [количество] [м\д\ч] [причина] - Выдача затычки игроку 
2️⃣ /channel_ban [количество] [м\д\ч] [причина] - Выдача бана игроку
3️⃣ /channel_unmute - снятие затычки игроку 
4️⃣ /channel_unban - снятие бана игроку 

ℹ️Команды работают ответом на сообщение нарушителя     
    """, parse_mode='html')



async def warn_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    reply_user_id = message.reply_to_message.from_user.id

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute("SELECT warn from warn where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    warn = int(warn[0])

    warn2 = warn + 1
   
    if user_status == 'Owner':
       if warn2 > 5:
          await message.bot.send_message(message.chat.id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Helper_Admin':

       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать варн <b>владельцу бота</b>', parse_mode='html')
       else:
         pass

       if warn2 > 5:
          await message.bot.send_message(message.chat.id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')

       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')
    
    


async def warn_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    reply_user_id = int(message.text.split()[1])

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn + 1
   
    if user_status == 'Owner':
       if warn2 > 5:
          await message.bot.send_message(reply_user_id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован из-за 6\6 варнов", parse_mode='html')

          await message.bot.send_message(message.chat.id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Helper_Admin':

       if reply_user_id == config.owner_id:
         return await message.reply(f'❗️ Вы не можете дать варн <b>владельцу бота</b>', parse_mode='html')
       else:
         pass


       if warn2 > 5:
          await message.bot.send_message(reply_user_id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован из-за 6\6 варнов", parse_mode='html')

          await message.bot.send_message(config.owner_id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')

          await message.bot.send_message(message.chat.id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')

       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



async def unwarn_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    reply_user_id = int(message.text.split()[1])

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn - 1
   
    if user_status == 'Owner':
       if warn2 < 0:
          await message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Helper_Admin':
       if warn2 < 0:
          await message.message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Owner':
       await message.message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



async def unwarn_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    if not message.reply_to_message:
       await message.reply("🆘 | Эта команда должна быть ответом на сообщение!")
       return   
    reply_user_id = message.reply_to_message.from_user.id

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn - 1
   
    if user_status == 'Owner':
       if warn2 < 0:
          await message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Helper_Admin':
       if warn2 < 0:
          await message.bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Owner':
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await message.bot.send_message(config.owner_id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       await message.bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



async def report_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    text = message.text[7:]
    
    if text == '':
       await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, репорт не может быть пустым", parse_mode='html')
       return
    rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
    for row in rows:
       await message.bot.send_message(row[0], f"<b>🆘ВАМ ПРИШЁЛ РЕПОРТ🆘</b>\n👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>\n💬 |Сообщение: <i>{text}</i>", parse_mode='html')

    await message.bot.send_message(config.owner_id,f"""
<b>🆘ВАМ ПРИШЁЛ РЕПОРТ🆘</b>
👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>  
💬 |Сообщение: <i>{text}</i>
    """, parse_mode='html')  
    await message.bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш репорт был успешно отправлен администрации", parse_mode='html')



async def channelunban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return

    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
    await message.reply(f'👤 | Администратор: {name1}\n📲 | Разбанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')

async def channelban_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    comment = " ".join(message.text.split()[1:])
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False))
    await message.reply(f'👤 | Администратор: {name1}\n🛑 | Забанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: навсегда\n📃 | Причина: {comment}',  parse_mode='html')


async def channelunmute_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
    await message.reply(f'👤 | Администратор: {name1}\n🔊 | Размутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')


async def channelmute_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    try:
       muteint = int(message.text.split()[1])
       mutetype = message.text.split()[2]
       comment = " ".join(message.text.split()[3:])
    except IndexError:
       await message.reply('ℹ | Не хватает аргументов!\nПример:\n<code>/мут 1 ч причина</code>')
       return
    if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
       dt = datetime.now() + timedelta(hours=muteint)
       timestamp = dt.timestamp()
       await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n🛑 | Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')
    if mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
       dt = datetime.now() + timedelta(minutes=muteint)
       timestamp = dt.timestamp()
       await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n🛑 | Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')
    if mutetype == "д" or mutetype == "дней" or mutetype == "день":
       dt = datetime.now() + timedelta(days=muteint)
       timestamp = dt.timestamp()
       await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n | 🛑Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')



async def disconect_database_handler(message):
    if not message.reply_to_message:
       await message.bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, эта команда должна быть ответом на сообщение", parse_mode='html')
       return
       

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    user_id = message.from_user.id
    reply_user_id = message.reply_to_message.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    i = f'''
🗄 Вы удалили <b>{user_name}</b> с базы данных 
   '''

    i2 = f'''
❗️ Данная команда доступна от прав администратора <b>OWNER</b>
❕Для приобретение данных прав, напишите команду <code>Донат</code>
   '''

    text = [i, i2]
    if user_status == 'Owner':
        await message.reply(text[0], parse_mode='html')
        cursor.execute(f'DELETE from users where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from mine where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from user_case where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from farm where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from house where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from cars where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from bot_time where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_bank where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from ob_time where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_prefix where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_sms where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from warn where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from console where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from channel_pov where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from avatarka where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from reput where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from h_module where user_id = {reply_user_id}')
        connect.commit()
    else:  
        await message.reply(text[1], parse_mode='html')

async def gamevb_handler(message):
   status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
   status_block = str(status_block[0])

   if status_block == 'on':
       return
   msg = message
   user_id = msg.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   period = 5

   balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
   balance = int(balance[0])



   get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
   last_stavka = f"{int(get[0])}"
   stavkatime = time.time() - float(last_stavka)
   if stavkatime > period:
      if balance > 0:
         await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы уверены что хотите сыграть в GAME-VB ? 🧊

ℹ️ | В этой игре вы играете сразу на весь <b>баланс</b>

↘️ Выберите одну кнопку ниже         
""",reply_markup=gamevbmenu,  parse_mode='html')
      else:
         await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств! ", parse_mode='html')
   else:
      await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')         

      
async def info_id_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = int(message.text.split()[1])

    balance = cursor.execute(f"SELECT balance from users where user_id = {reply_user_id}").fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance).replace(',', '.')

    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    bank = cursor.execute(f"SELECT bank from users where user_id = {reply_user_id}").fetchone()
    bank = int(bank[0])
    bank3 = '{:,}'.format(bank).replace(',', '.')

    user_tg_name = 'Аккаунт'

    reply_user_status = cursor.execute(f"SELECT user_status from users where user_id = {reply_user_id}").fetchone()
    reply_user_status = str(reply_user_status[0])

    ethereum = cursor.execute(f"SELECT ethereum from users where user_id = {reply_user_id}").fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

    rating = cursor.execute(f"SELECT rating from users where user_id = {reply_user_id}").fetchone()
    rating = int(rating[0])
    rating2 = '{:,}'.format(rating).replace(',', '.')

    status_block = cursor.execute(f"SELECT status_block from users where user_id = {reply_user_id}").fetchone()
    status_block = str(status_block[0])

    time_register = cursor.execute(f"SELECT time_register from users where user_id = {reply_user_id}").fetchone()
    time_register = time_register[0]

    pref = cursor.execute(f"SELECT pref from users where user_id = {reply_user_id}").fetchone()
    pref = str(pref[0])

    donate_coins = cursor.execute(f"SELECT donate_coins from users where user_id = {reply_user_id}").fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')

    bank2 = cursor.execute(f"SELECT bank2 from users where user_id = {reply_user_id}").fetchone()
    bank2 = int(bank2[0])
    bank22 = '{:,}'.format(bank2).replace(',', '.')

    depozit = cursor.execute(f"SELECT depozit from users where user_id = {reply_user_id}").fetchone()
    depozit = int(depozit[0])
    depozit2 = '{:,}'.format(depozit).replace(',', '.')

    if user_status != ['Owner', 'Helper_Admin', 'Admin']:
       user_status2 = 'Пользователь'
    if user_status in ['Owner', 'Helper_Admin', 'Admin']:
       await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> :

💬 | Телеграм: <a href='tg://user?id={reply_user_id}'>{user_tg_name}</a>
🟢 | Статус: {reply_user_status}
🟩 | Статус блокировки: {status_block}

👤 | Ник: {reply_user_name}
💰 | Баланс: {balance2}$
🏪 | Банковский счёт: {bank3}$
🏪 | Хранительный счёт: {bank22}$
🏛 | Депозит: {depozit2}$
🟪 | Эфириум: {ethereum2} 🟣
💎 | Рейтинг: {rating2} 💎
🪙 | Donate-Coins: {donate_coins2} 🪙

📆 | Дата регистрации: {time_register}     
       """, parse_mode='html')



async def info_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return
    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    if not message.reply_to_message:
       await message.bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, эта команда должна быть ответом на сообщение", parse_mode='html')
       return
       
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = message.reply_to_message.from_user.id

    balance = cursor.execute(f"SELECT balance from users where user_id = {reply_user_id}").fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance).replace(',', '.')

    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    bank = cursor.execute(f"SELECT bank from users where user_id = {reply_user_id}").fetchone()
    bank = int(bank[0])
    bank3 = '{:,}'.format(bank).replace(',', '.')

    user_tg_name = message.reply_to_message.from_user.get_mention(as_html=True)

    reply_user_status = cursor.execute(f"SELECT user_status from users where user_id = {reply_user_id}").fetchone()
    reply_user_status = str(reply_user_status[0])

    ethereum = cursor.execute(f"SELECT ethereum from users where user_id = {reply_user_id}").fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

    rating = cursor.execute(f"SELECT rating from users where user_id = {reply_user_id}").fetchone()
    rating = int(rating[0])
    rating2 = '{:,}'.format(rating).replace(',', '.')

    status_block = cursor.execute(f"SELECT status_block from users where user_id = {reply_user_id}").fetchone()
    status_block = str(status_block[0])

    time_register = cursor.execute(f"SELECT time_register from users where user_id = {reply_user_id}").fetchone()
    time_register = time_register[0]

    pref = cursor.execute(f"SELECT pref from users where user_id = {reply_user_id}").fetchone()
    pref = str(pref[0])

    donate_coins = cursor.execute(f"SELECT donate_coins from users where user_id = {reply_user_id}").fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')

    bank2 = cursor.execute(f"SELECT bank2 from users where user_id = {reply_user_id}").fetchone()
    bank2 = int(bank2[0])
    bank22 = '{:,}'.format(bank2).replace(',', '.')

    depozit = cursor.execute(f"SELECT depozit from users where user_id = {reply_user_id}").fetchone()
    depozit = int(depozit[0])
    depozit2 = '{:,}'.format(depozit).replace(',', '.')

    if user_status in ['Owner', 'Helper_Admin', 'Admin']:
       await message.bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> :

💬 | Телеграм: {user_tg_name}
🟢 | Статус: {reply_user_status}
🟩 | Статус блокировки: {status_block}

👤 | Ник: {reply_user_name}
💰 | Баланс: {balance2}$
🏪 | Банковский счёт: {bank3}$
🏪 | Хранительный счёт: {bank22}$
🏛 | Депозит: {depozit2}$
🟪 | Эфириум: {ethereum2} 🟣
💎 | Рейтинг: {rating2} 💎
🪙 | Donate-Coins: {donate_coins2} 🪙

📆 | Дата регистрации: {time_register}     
       """, parse_mode='html')

async def start_handler(message):



    name = message.from_user.get_mention(as_html=True)
    i = f'''
👋 Привет <b>{name}</b>, я игровой бот <b>{config.full_bot_name}</b>
💸 Тебе как новому пользователю был выдан подарок в размере <code>{'{:,}'.format(config.start_money).replace(',', '.')}$</code>
❗️ Для ознакомление с моими командами, введи команду <code>Помощь</code> , или вибери кнопку <b>ниже</b>
➕ Так же ты можешь добавить бота в свой чат по кнопке <b>ниже</b>
    '''
    i2 = f'''
❗️ <b>{name}</b>, вы уже зарегистрированы в боте
❕ Если у вас возникла какая то проблема с какой то командой, обратитесь к {config.owner} для повторной регистрации <b>[Если у вас SPAM BAN, то вы можете обратиться к нему через данного бота с помощью команд /m [ID] [message] или через команду /report ]</b>
    '''

    text_register = [i, i2]
    msg = message
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name
    user_name = 'Игрок'
    user_status = "Player"
    status_block = 'off'
    stats_status = 'off'
    pref = 'Игрок'
    status_console = 'off'
    avatarka_start = 'none'
    klan_index = 0
    status_family = 0
    chat_id = message.chat.id
    result = time.localtime()

    if int(result.tm_mon) <= 9:
      p = "0"
    else:
      p = ''
    times = f'{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {result.tm_hour}:{result.tm_min}:{result.tm_sec}'
    times2 = str(times)

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
       cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, full_name, user_status, config.start_money, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status))
       cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO farm VALUES(?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0))
       cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
       cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO promo1 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO console VALUES(?, ?);",(user_id, status_console))
       cursor.execute("INSERT INTO time_prefix VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_sms VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO promo1 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO channel_pov VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO avatarka VALUES(?, ?);",(user_id, avatarka_start))
       cursor.execute("INSERT INTO reput VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO h_module VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO promo2 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo3 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo4 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo5 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo6 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo7 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo8 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo9 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo10 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo11 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo12 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo13 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo14 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo15 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo16 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo17 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo18 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo19 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo20 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo21 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo22 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo23 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo24 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo25 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo26 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo27 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo28 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo29 VALUES(?, ?, ?);",(user_id, 0, 0))

       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')
       await bot.send_message(message.chat.id, text=text_register[0], reply_markup=reg, parse_mode='html')

    else:
       await bot.send_message(message.chat.id, text=text_register[0], reply_markup=reg, parse_mode='html')


async def sistem_message_handler(message):
    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
        return
    try:
        text = ' '.join(message.text.split()[2:])

        msg = message
        user_id = msg.from_user.id
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
        user_name = str(user_name[0])

        reply_user_id = int(message.text.split()[1])
        reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
        reply_user_name = str(reply_user_name[0])

        period = 5
        get = cursor.execute("SELECT stavka FROM time_sms WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)

        if len(text) > 35:
            await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, сообщение не может быть более чем 35 символов ", parse_mode='html')
            return
        if stavkatime > period:
            await message.bot.send_message(user_id, f"💬 | [Я ➡️ <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>] {text}", parse_mode='html')
            await message.bot.send_message(reply_user_id, f"💬 | [<a href='tg://user?id={user_id}'>{user_name}</a> ➡️ Я] {text}", parse_mode='html')
            cursor.execute(f'UPDATE time_sms SET stavka = {time.time()} WHERE user_id = {user_id}')
            connect.commit()
            return
        else:
            await message.bot.send_message(user_id, f"🆘 | Игрок, сообщение писать можно раз в 5 секунд", parse_mode='html')
            return
    except:
        await message.bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Либо вы не правильно ID, или данный игрок не играет в бота", parse_mode='html')
        return
