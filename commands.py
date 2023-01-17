from collections import namedtuple
from email import message
from numpy import number
from imports import *

api = CoinGeckoAPI()



async def commands_handler(message: types.Message):

    await get_course()
    await get_x2donate()


    name = message.from_user.get_mention(as_html=True)

    i = f'''
👋 Привет <b>{name}</b>, я игровой бот <b>👾{config.full_bot_name}</b>
💸 Тебе как новому пользователю был выдан подарок в размере <code>{'{:,}'.format(config.start_money).replace(',', '.')}$</code>
❗️ Для ознакомление с моими командами, введи команду <code>Помощь</code> , или вибери кнопку <b>ниже</b>
➕ Так же ты можешь добавить бота в свой чат по кнопке <b>ниже</b>
    '''

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
    if int(result.tm_mday) <= 9:
      m = "0"
    else:
      m = ''
    if int(result.tm_hour) <= 9:
      h = "0"
    else:
      h = ''
    if int(result.tm_min) <= 9:
      min = "0"
    else:
      min = ''
    if int(result.tm_sec) <= 9:
      s = "0"
    else:
      s = ''
    times = f'{m}{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {h}{result.tm_hour}:{min}{result.tm_min}:{s}{result.tm_sec}'
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
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO console VALUES(?, ?);",(user_id, status_console))
       cursor.execute("INSERT INTO time_prefix VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_sms VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO channel_pov VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO avatarka VALUES(?, ?);",(user_id, avatarka_start))
       cursor.execute("INSERT INTO reput VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO h_module VALUES(?, ?);",(user_id, 0))
       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')

       await message.bot.send_message(message.chat.id, i, reply_markup=reg, parse_mode='html')
    else:
       pass
       
    
    check_update = cursor.execute(f'SELECT user_id from money_balance where user_id = "{user_id}"').fetchone()
    if check_update == None:
      await message.answer(f'🔁 Ваши данные были обновлены (следите за обновлениями на канале @minko_channel)')
      await register_money(user_id)
    else:
      pass


    
    
   
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       if chat_id == user_id:
          return await message.reply(f'❗️ Ваш аккаунт находиться в стадии <b>блокировки</b> ', parse_mode='html')
       return

    if message.forward_date != None:
       if chat_id == user_id:
          return await message.reply(f'❗️ Я не реагирую на <b>пер. сообщение</b>', parse_mode='html')
       return


    period = 1
    get = cursor.execute("SELECT stavka FROM ob_time WHERE user_id = ?",(message.from_user.id,)).fetchone()
    last_stavka = f"{int(get[0])}"
    stavkatime = time.time() - float(last_stavka)
    if stavkatime < period:
       chat_id = message.chat.id
       user_id = message.from_user.id

       if chat_id == user_id:
          return await message.reply(f'💬 <b>[ANTI-FLOOD]</b> - Не так быстро, в боте стоит ограничение между командами <b>{period} секунд(а)</b>', parse_mode='html')
       else:
          return
    else:
       user_id = message.from_user.id
       cursor.execute(f'UPDATE ob_time SET stavka = {time.time()} WHERE user_id = {user_id}')
       connect.commit()

    bot = Bot(token=config.token)
    dp = Dispatcher(bot)
    
    if message.text.startswith('снять игроку') or message.text.startswith('Снять игроку'):
      if not message.reply_to_message:
               await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
               return

      if user_id != config.owner_id:
         return await message.reply(f'❗️Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass

      try:
         summ = int(message.text.split()[2])
      except:
         return await message.reply(f'<b>❗️ Неправильные аргументы</b> \n<b>❕ Пример:</b> <code>снять игроку 100</code>', parse_mode='html')
      
      reply_money = await user_money(message.reply_to_message.from_user.id)
      if reply_money < summ:
         return await message.reply(f'❗️ Вы не можете снять сумму больше, чем сам рублевый баланс игрока')
      else:
         pass
      
      new_user_money = reply_money - summ

      await update_money(message.reply_to_message.from_user.id, new_user_money)
      return await message.reply(f'❗️ Вы обновили рублевый баланс игрока <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> . Теперь его баланс: {new_user_money} руб.', parse_mode='html')


    if message.text.startswith('пополнить игроку') or message.text.startswith('Пополнить игроку'):
      if not message.reply_to_message:
               await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
               return

      if user_id != config.owner_id:
         return await message.reply(f'❗️Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass

      try:
         summ = int(message.text.split()[2])
      except:
         return await message.reply(f'<b>❗️ Неправильные аргументы</b> \n<b>❕ Пример:</b> <code>пополнить игроку 100</code>', parse_mode='html')
      
      reply_money = await user_money(message.reply_to_message.from_user.id)
      new_user_money = reply_money + summ

      await update_money(message.reply_to_message.from_user.id, new_user_money)
      return await message.reply(f'❗️ Вы обновили рублевый баланс игрока <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.full_name}</a> . Теперь его баланс: {new_user_money} руб.', parse_mode='html')



    if message.text.startswith('пополнить') or message.text.startswith('Пополнить'):
        if message.chat.id != user_id:
            return await message.reply(f'<i><a href="t.me/{config.bot_name}">❗️ Авто оплата доступна только в личные сообщения с ботом</a></i>', parse_mode='html')
        try:
            donate = int(message.text.split()[1])
        except:
            await message.reply(f'❗️<b> Введены не правильно аргументы</b> !\n❕<b> Пример:</b> <code>пополнить 100</code>', parse_mode='html')
        
        if donate < 3:
            return await message.answer('💰 Минимальная сумма пополнение 3 рубля')
        else:
            pass

        comment = f'Online Donate | от {message.from_user.id} на {donate} руб.'

        bill = p2p.bill(amount=donate, lifetime=15, comment=comment)

        await add_check(message.from_user.id, donate, bill.bill_id)

        await message.reply(f'👍 Ваш чек на {donate} руб. готов \n✈️ Вы можете оплатить через <b><a href="{bill.pay_url}">ссылку</a></b> либо кнопку\n⌛️ Данная оплата будет действительна только 15 минут',reply_markup=pay(url=bill.pay_url, money=donate, bill=bill.bill_id),  parse_mode='html')



    if message.text.startswith('обменять') or message.text.startswith('Обменять'):
        users_money = await user_money(message.from_user.id)

        if users_money == 0:
            return await message.reply('❗️ У вас 0 рублей. Вы не можете обменять деньги на Donate-Coins')
        else:
            pass
        try:
            summ = message.text.split()[1]
        except:
            summ = int(users_money)

        try:
            summ = int(summ)
        except:
            return await message.reply('❗️<b> Введены не правильно аргументы .</b>\n❕<b> Пример:</b> <code>пополнить 100</code>', parse_mode='html')

        if summ <= 0:
            return await message.reply('❗️ Сумма обмена не может быть отрицательным числом')

        if summ > users_money:
            return await message.reply(f'❗️ Не хватает средств.\n💰 Баланс: {users_money} руб.')
        else:
            pass

        donate_coins = await user_donate(message.from_user.id)
        course_donate_coins = int(summ / 3)
        new_donate_coins = donate_coins + course_donate_coins
        await update_donate(message.from_user.id, new_donate_coins)
        await update_money(message.from_user.id, users_money - summ)
        await message.reply(f'🔁 Вы обменяли {summ} руб на {course_donate_coins} Donate-Coins.\n❕ Для просмотра своих Donate-Coins, напишите: <code>донат</code>', parse_mode='html')



    if message.text.lower() == 'курс':
        money1 = await course_money1()
        full_money1 = await utils.scor_summ(money1)
        cash_money1 = await course_cash_money1()

        money2 = await course_money2()
        full_money2 = await utils.scor_summ(money2)
        cash_money2 = await course_cash_money2()

        money3 = await course_money3()
        full_money3 = await utils.scor_summ(money3)
        cash_money3 = await course_cash_money3()

        course_pay = InlineKeyboardMarkup(row_width=2)
        course_pay.add(
        InlineKeyboardButton(text=f'💸 Купить {full_money1}', callback_data=f"pay_money1_{time.time()}"),
        InlineKeyboardButton(text=f'💸 Купить {full_money2}', callback_data=f"pay_money2_{time.time()}"),
        InlineKeyboardButton(text=f'💸 Купить {full_money3}', callback_data=f"pay_money3_{time.time()}")
        )

        course_pay.row(
        InlineKeyboardButton(text=f'💰 Пополнить', callback_data='info_donate')
        )
        
        await message.answer(f'''
👨‍💼 <b>{full_money1} - {cash_money1}RUB</b> 
🤵‍♂️ <b>{full_money2} - {cash_money2}RUB</b> 
🤴 <b>{full_money3} - {cash_money3}RUB</b>      
        ''', reply_markup=course_pay, parse_mode='html')


    if message.text.startswith('новый курс') or message.text.startswith('Новый курс'):
        if message.from_user.id != config.owner_id:
            return await message.answer('❗️ Сменить курс валют может только <b>владелец бота</b>', parse_mode='html')
        else:
            pass

        try:
            money1 = message.text.split()[2]
            money1 = await utils.sistem_number(money1)
            cash_money1 = int(message.text.split()[3])

            money2 = message.text.split()[4]
            money2 = await utils.sistem_number(money2)
            cash_money2 = int(message.text.split()[5])

            money3 = message.text.split()[6]
            money3 = await utils.sistem_number(money3)
            cash_money3 = int(message.text.split()[7])
        except ValueError:
            print(ValueError)
            #return await message.answer(f'Не правильно ввели оргументы (например: <code>новый курс 1e12 50 1e15 100 1e18 200</code> )', parse_mode='html')

        await add_cuorse(money1, cash_money1, money2, cash_money2, money3, cash_money3)
        await message.answer(f'<b>🔄 Был обновлен курс</b>\n<b>❕ Для просмотра нового курса, напишите:</b> <code>курс</code>', parse_mode='html')


    if message.text.startswith('x2donate статус') or message.text.startswith('X2donate статус'):
        if message.from_user.id != config.owner_id:
            return await message.answer('❗️ Х2 Донат может включать только <b>владелец бота</b>', parse_mode='html')
        else:
            pass

        status = message.text.split()[2]

        if status == 'on' or status == 'off':
            await update_status_x2donate(status)
            if status == 'on':
               status = 'включен'
               smile = '🚀'
            else:
               status = 'выключен'
               smile = '⛔️'
            await message.answer(f'{smile} X2 Донат был успешно {status}')
        else:
            return await message.answer(f'Ваш оргумент {status} не найден. Верные огрументы: on, off')
        

    if message.text.lower() in ['репорт', 'система репорта', 'репорты']:
       msg = message
       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       await message.reply( f"""
⛔️Правила по использованию репортов
      ❗️ <b>Запрещено</b> материться, оскорблять кого-либо, проявлять неуважение к администрации и тому подобное.
      ❗️ <b>Запрещено</b> капсить, писать неразборчиво, использовать спам, писать один и тот-же текст несколько раз получивши на него ответ.
      ❗️ <b>Запрещено</b> всячески дразнить администрацию и отвлекать от работы.
      ❗️ <b>Запрещено</b> интересоваться/писать вещи которые ни коем образом ни относятся к игре
      ❗️ <b>Запрещена</b> реклама в любом её проявлении
      ❗️ <b>Запрещено</b> обращаться к своим друзьям администраторам по личным вопросам
      ❗️ <b>Запрещено</b> клеветать на игроков, обвинять их в нарушениях, которые они не совершали.
      ❗️ Репорт работает по принципу - <b>Вопрос/Просьба/Жалоба</b> (исключение - Приветствие) и не иначе. Иные формы обращения будут оставаться без ответа и будет выдано наказание.

⚠️Форма отправки репорта - <code>/report</code> <b>[сообщение]</b>

⛔️Прошу вас соблюдать правила отправки репорта
       """, parse_mode='html')
    if message.text.lower() in ["баланс", "Баланс", "Б", "б"]:
       msg = message
       user_id = msg.from_user.id
       
       chat_id = message.chat.id
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])

       avatarka = cursor.execute("SELECT avatarka from avatarka where user_id = ?",(message.from_user.id,)).fetchone()
       avatarka = avatarka[0]

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = int(balance[0])
       balance2 = '{:,}'.format(balance).replace(',', '.')
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       bank2 = '{:,}'.format(bank).replace(',', '.')
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])
       ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

       c = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')
       else:
        pass
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank).replace(',', '.')
       else:
        pass
       if ethereum >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          ethereum = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET ethereum = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          ethereum2 = '{:,}'.format(ethereum).replace(',', '.')
       else:
        pass

        obb_summ = balance + bank

        
        all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
        all_family2 = []
        proverka_family = 0
        for all_owner_id in all_family:
           all_family2.append(all_owner_id[0])

        user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()


        proverka_family = 0

        if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0] 

         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = f'{int(rank_family[0])} ранг'

        else:
         proverka_family += 1

        if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]   

         rank_family = 'Владелец семьи'
        else:
         proverka_family += 1
        
        if proverka_family == 2:
         family = ''
        else:
         family = f'\n<b>👨‍👩‍👧‍👦 Семья:</b> «<b>{name_family}</b>» <i>({rank_family})</i>'
       
       from utils import scor_summ

       obb_summ2 = await scor_summ(obb_summ)
       
       text_balance = f'''
<b>👤𝗻𝗮𝗺𝗲</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>{family}
<b>📄𝗽𝗿𝗲𝗳𝗶𝘅:</b> <code>{pref} </code>
<b>💸𝗺𝗼𝗻𝗲𝘆:</b> <code>{balance2}$</code>
<b>🏛𝗯𝗮𝗻𝗸:</b> <code>{bank2}$</code>
<b>🟪𝗲𝘁𝗵𝗲𝗿𝗲𝘂𝗺</b> <code>{ethereum2} шт</code>

<b>🤑 𝗰𝗮𝘀𝗵:</b> <code>{obb_summ2}$ </code>    
       '''

       if avatarka == 'apper':
          ava = open('apper.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava,text_balance, parse_mode='html')
          return
       
       if avatarka == 'admin':
          ava = open('админ.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava,text_balance, parse_mode='html')
          return
       
       if avatarka == 'girl':
          ava = open('girl.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, text_balance, parse_mode='html')
          return
       
       if avatarka == 'cheat':
          ava = open('cheat.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, text_balance, parse_mode='html')
          return
       
       if avatarka == 'dyp':
          ava = open('дюп.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, text_balance, parse_mode='html')
          return
       
       if avatarka == 'strach':
          ava = open('страж.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"👫 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a> \n✏️ | Префикс: {pref} \n💰 | Деньги: {balance2}$ \n🏦 | Банк: {bank2}$\n🟣 | Эфириум: {ethereum2}🟪", parse_mode='html')
          return


       await bot.send_message(message.chat.id,text_balance, parse_mode='html')
    ################################################ПРОФИЛЬ#############################################################
    if message.text.lower() in ["профиль", "Профиль"]:
       msg = message
       chat_id = message.chat.id
       name = message.from_user.get_mention(as_html=True)

       time_register = cursor.execute("SELECT time_register FROM users WHERE user_id=?", (message.from_user.id,)).fetchall()
       time_register = time_register[0]

       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.from_user.id,)).fetchone()
       reput = int(reput[0])

       avatarka = cursor.execute("SELECT avatarka from avatarka where user_id = ?",(message.from_user.id,)).fetchone()
       avatarka = avatarka[0]

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])
       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       game = cursor.execute("SELECT game from users where user_id = ?",(message.from_user.id,)).fetchone()
       game = int(game[0])
       game2 = '{:,}'.format(game).replace(',', '.')

       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       ethereum = int(ethereum[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?",(message.from_user.id,)).fetchone()
       cars = int(cars[0])

       house = cursor.execute("SELECT house from house where user_id = ?",(message.from_user.id,)).fetchone()
       house = int(house[0])
       
       all_org = 0
       all_proverka_family = 0

       all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
       all_family2 = []
      
       for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

       if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     

         family = f'\n    👨‍👩‍👧‍👦 <b>Семья:</b> <code>{name_family}</code>'

         all_org += 1
         all_proverka_family += 1
       else:
         pass

       user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

       if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     

         family = f'\n    👨‍👩‍👧‍👦 <b>Семья:</b> <code>{name_family}</code>'

         all_org += 1
         all_proverka_family += 1
       else:
         pass

       if all_org == 0:
         all_org2 = '\n      Вы не состоите в организациях 😿'
       else:
         all_org2 = '\n🏰 Организации:'
       
       if all_proverka_family == 0:
         family = ''
       else:
         pass


       d5 = 0

       if house == 1:
          house2 = '\n    <b>🏠Дом:</b> <code>Коробка</code>\n'
          d5 += 1
       if house == 2:
          house2 = '    <b>🏠Дом:</b> <code>Сарай</code>\n'
          d5 += 1
       if house == 3:
          house2 = '    <b>🏠Дом:</b> <code>Маленький домик</code>\n'
          d5 += 1
       if house == 4:
          house2 = '    <b>🏠Дом:</b> <code>Квартира</code>\n'
          d5 += 1
       if house == 5:
          house2 = '    <b>🏠Дом:</b> <code>Огромный дом</code>\n'
          d5 += 1
       if house == 6:
          house2 = '    <b>🏠Дом:</b> <code>Коттедж</code>\n'
          d5 += 1
       if house == 7:
          house2 = '    <b>🏠Дом:</b> <code>Вилла</code>\n'
          d5 += 1
       if house == 8:
          house2 = '    <b>🏠Дом:</b> <code>Загородный дом</code>\n'
          d5 += 1
       else:
          house2 = ''
          
       if cars == 1:
          cars2 = '    <b>🚘Машина:</b> <code>Самокат</code>\n'
          d5 += 1
       if cars == 2:
          cars2 = '    <b>🚘Машина:</b> <code>Велосипед</code>\n'
          d5 += 1
       if cars == 3:
          cars2 = '    <b>🚘Машина:</b> <code>Гироскутер</code>\n'
          d5 += 1
       if cars == 4:
          cars2 = '    <b>🚘Машина:</b> <code>Сегвей</code>\n'
          d5 += 1
       if cars == 5:
          cars2 = '    <b>🚘Машина:</b> <code>Мопед</code>\n'
          d5 += 1
       if cars == 6:
          cars2 = '    <b>🚘Машина:</b> <code>Мотоцикл</code>\n'
          d5 += 1
       if cars == 7:
          cars2 = '    <b>🚘Машина:</b> <code>ВАЗ 2109</code>\n'
          d5 += 1
       if cars == 8:
          cars2 = '    <b>🚘Машина:</b> <code>Квадроцикл</code>\n'
          d5 += 1
       if cars == 9:
          cars2 = '    <b>🚘Машина:</b> <code>Багги</code>\n'
          d5 += 1
       if cars == 10:
          cars2 = '    <b>🚘Машина:</b> <code>Вездеход</code>\n'
          d5 += 1
       if cars == 11:
          cars2 = '    <b>🚘Машина:</b> <code>Лада Xray</code>\n'
          d5 += 1
       if cars == 12:
          cars2 = '    <b>🚘Машина:</b> <code>Audi Q7</code>\n'
          d5 += 1
       if cars == 13:
          cars2 = '    <b>🚘Машина:</b> <code>BMW X6</code>\n'
          d5 += 1
       if cars == 14:
          cars2 = '    <b>🚘Машина:</b> <code>Toyota FT-HS</code>\n'
          d5 += 1
       if cars == 15:
          cars2 = '    <b>🚘Машина:</b> <code>BMW Z4 M</code>\n'
          d5 += 1
       if cars == 16:
          cars2 = '    <b>🚘Машина:</b> <code>Subaru WRX STI</code>\n'
          d5 += 1
       if cars == 17:
          cars2 = '    <b>🚘Машина:</b> <code>Lamborghini Veneno</code>\n'
          d5 += 1
       if cars == 18:
          cars2 = '    <b>🚘Машина:</b> <code>Tesla Roadster</code>\n'
          d5 += 1
       else:
          cars2 = ''

       if d5 == 0:
          d6 = '\n      У вас нету имущества 🙁'
       else:
          d6 = '🕋 | Имущество:\n'
       
       c = 999999999999999999999999
       if user_status == 'Player':
          priv = 'Пользователь'
       if user_status == 'Vip':
          priv = 'ВИП❤️'
       if user_status == 'Premium':
          priv = ' ПРЕМИУМ🧡'
       if user_status == 'Platina':
          priv = ' ПЛАТИНА💛'
       if user_status == 'Helper':
          priv = ' ХЕЛПЕР💚'
       if user_status == 'Sponsor':
          priv = ' СПОНСОР💙'
       if user_status == 'Osnovatel':
          priv = ' ОСНОВАТЕЛЬ💜'
       if user_status == 'Vladelec':
          priv = ' ВЛАДЕЛЕЦ🖤'
       if user_status == 'Bog':
          priv = ' БОГ🤍'
       if user_status == 'Vlaselin':
          priv = ' ВЛАСТЕЛИН🤎'
       if user_status == 'Owner':
          priv = 'OWNER ❗️'
       if user_status == 'Admin':
          priv = 'ADMIN ❗️'
       if user_status == 'Helper_Admin':
          priv = 'HELPER ADMIN ❗️'

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit() 
       else:
        pass
       from utils import scor_summ
       balance3 = await scor_summ(balance)
       
       if ethereum >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          ethereum = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET ethereum = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit() 
       else:
        pass
       
       ethereum3 = await scor_summ(ethereum)

       if bank >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()   
       else:
        pass
       bank3 = await scor_summ(bank)

       if rating >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          rating = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET rating = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
       else:
        pass
       rating3 = await scor_summ(rating)


       text_profile= f'''
{name} , ваш профиль : 
👤 <b>𝗻𝗮𝗺𝗲:</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>
🔎 <b>𝗶𝗱:</b> <code>{user_id}</code>
📄 <b>𝗽𝗿𝗲𝗳𝗶𝘅:</b> <code>{pref} </code>
🎖️️ <b>𝗽𝗿𝗶𝘃𝗶𝗹𝗲𝗴𝗲:</b> <code>{priv}</code>
💸 <b>𝗺𝗼𝗻𝗲𝘆:</b> <code>{balance3}</code>
🏛 <b>𝗶𝗻 𝘁𝗵𝗲 𝗯𝗮𝗻𝗸:</b> <code>{bank3}</code>
🟪 <b>𝗲𝘁𝗵𝗲𝗿𝗲𝘂𝗺:</b> <code>{ethereum3} шт</code>
💎 <b>𝗿𝗮𝘁𝗶𝗻𝗴:</b> <code>{rating3}</code>
📊 <b>𝗿𝗲𝗽𝘂𝘁𝗮𝘁𝗶𝗼𝗻:</b> <code>{reput}</code>
🪙 <b>𝗱𝗼𝗻𝗮𝘁𝗲-𝗰𝗼𝗶𝗻𝘀:</b> <code>{donate_coins2}</code>
🎰 <b>𝘁𝗼𝘁𝗮𝗹 𝗴𝗮𝗺𝗲𝘀 𝗽𝗹𝗮𝘆𝗲𝗱:</b> <code>{game2}</code>
<b>{d6}</b>{house2}{cars2}\n<b>{all_org2}</b>{family}

📆 <b>𝗱𝗮𝘁𝗲 𝗼𝗳 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻:</b> <code>{time_register}</code>
       '''

       await bot.send_message(message.chat.id, text_profile,  parse_mode='html')

###########################################БАНК###########################################
    # bank
    if message.text.lower() in ["Банк", "банк"]:
       msg = message
       chat_id = message.chat.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank_hran = cursor.execute("SELECT bank2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?",(message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       bank_hran = int(bank_hran[0])
       bank_hran2 = '{:,}'.format(bank_hran).replace(',', '.')
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit2 = '{:,}'.format(depozit).replace(',', '.')
       bank2 = '{:,}'.format(bank).replace(',', '.')
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2).replace(',', '.')

       c = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank).replace(',', '.')
       else:
          pass
       if bank_hran >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          bank_hran = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank2 = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank_hran2 = '{:,}'.format(bank_hran).replace(',', '.')
       else:
          pass
       if depozit >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          depozit = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET depozit = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          depozit2 = '{:,}'.format(depozit).replace(',', '.')

       

       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о вашем банке 🏦\n\n👨‍💼 | Владелец: {user_name}\n🏛 | Основной счёт: {bank2}$\n💼 | Хранительный счёт: {bank_hran2}$\n🔐 | Деньги на депозите: {depozit2}$\n     💎 Статус депозита: {stats_depozit}\n     📈 Процент под депозит: {procent}\n      💵 Деньги на вывод: {money_vivod3}$", parse_mode='html')
    if message.text.startswith('процент') or message.text.startswith('Процент'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2).replace(',', '.')
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}$ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   

   
    if message.text.startswith('депозит') or message.text.startswith('Депозит'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
          
    if message.text.startswith("Банк положить") or message.text.startswith("банк положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       bank_p = int(su3)

       if bank_p >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя ложить в банк больше лимита")
          return

       print(f"{name} положил в банк: {bank_p}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p).replace(',', '.')
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 180
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили в банк {bank2}$ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в банк отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в банк можно раз в 3 минуты", parse_mode='html')
    if message.text.startswith("Банк снять") or message.text.startswith("банк снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       bank_s = int(su3)
       print(f"{name} снял с банка: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s).replace(',', '.')
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли с банковского счёта {bank2}$ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств на банковском счету! {rloser}",
                                    parse_mode='html')


###########################################АДМИН КОМАНДЫ###########################################
    if message.text.startswith("Поделить") or message.text.startswith("поделить"):
       if not message.reply_to_message:
                await message.reply("❗️ <b>Эта команда должна быть ответом на сообщение</b>", parse_mode='html')
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       console = cursor.execute('SELECT user_id from users where user_status = "Owner"').fetchall()
       console2 = cursor.execute('SELECT user_id from users where user_status = "Helper_Admin"').fetchall()
       console3 = []

       for console_owner in console:
         console3.append(console_owner[0])
      
       for console_helper in console:
         console3.append(console_helper[0])
       
       if int(balance2 / perevod) <= 0:
          return await message.reply(f'❗️ <b>Запрещено</b> чтобы баланс игрока был равен отрицательному числу', parse_mode='html')
       else:
         pass
      
       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ <b>Действие:</b> <code>Деление баланса</code>
💈 <b>Количество:</b> <code>{perevod2} раз</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''
       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')

          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f"⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}", parse_mode='html')

          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 /  perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')



    
    if message.text.startswith('Выдать донат') or message.text.startswith('выдать донат'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       if user_status == 'Owner':
          text = f'''
⛔️ <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a><b>, вам было начислено <code>{'{:,}'.format(summ).replace(',','.')}</code> Donate Coins</b> 🪙
          '''
          await bot.send_message(message.chat.id,text, parse_mode='html')
          cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + summ} WHERE user_id = {reply_user_id}')
          connect.commit()
       else:
          pass
    if message.text.lower() == 'забрать права':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️<b> Разработчик: <a href="tg://user?id={user_id}">{user_name}</a> забрал все права администрации у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a></b>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Player" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')

    if message.text.lower() == 'передать права':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️ <b>Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> передал все права игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a></b>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Owner" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'выдать админа':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️ Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> выдал права администратора уровня <b>ADMIN</b> игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Admin" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'выдать хелпера':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          text = f'''
⛔️ |Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> выдал права администратора уровня <b>HELPER ADMIN</b> игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
          '''
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Helper_Admin" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')

    if message.text.lower() in ["админ", "Админ"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       admin_menu = InlineKeyboardMarkup(row_width=1)
       Admins_menu_up = InlineKeyboardButton(text='Войти ✅', callback_data='Admins_menu_up')
       admin_menu.add(Admins_menu_up)
       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a>, войдите в админ меню 🆘", reply_markup=admin_menu, parse_mode='html')
    
    if message.text.startswith("Умножить") or message.text.startswith("умножить"):
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
                return
                
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 * perevod) >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 999 фенд!", parse_mode='html')
          return
       
       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ <b>Действие:</b> <code>Умножение баланса</code>
💈 <b>Количество:</b> <code>{perevod2} раз</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''
       if user_status[0] == 'Owner':

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await message.reply(text, parse_mode='html')

          await bot.send_message(config.owner_id, text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await message.reply(text, parse_mode='html')

          await bot.send_message(config.owner_id, text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')

    if message.text.startswith("выдать") or message.text.startswith("Выдать"):
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 + perevod) >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 999 фенд!", parse_mode='html')
          return
       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ <b>Действие:</b> <code>Выдача денег</code>
💈 <b>Количество:</b> <code>{perevod2}$</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''
       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return 
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')


    if message.text.startswith("забрать") or message.text.startswith("Забрать"):
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 - perevod) < 0:
         
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя заберать больше <b>баланса игрока</b>", parse_mode='html')
          return

       text = f''''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚙️ <b>Действие:</b> <code>Отбор денег</code>
💈 <b>Количество:</b> <code>{perevod2}$</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''

       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id, text, parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')

    if message.text.lower() in ["обнулить", "Обнулить"]:
       if not message.reply_to_message:
                await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()

       text = f'''
⛔️ <b>Администратор:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚙️ <b>Действие:</b> <code>Обнуление</code>
👨 <b>Игроку:</b> <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       '''

       if user_status[0] == 'Owner':
          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET donate_coins = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
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
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
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
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0],f'<b>⚠️ ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b>\n\n' + text, parse_mode='html')


          await bot.send_message(config.owner_id,f'⚠️ <b>ДЕЙСТВИЕ АДМИНИСТРАТОРА:</b> \n\n{text}', parse_mode='html')

          await message.reply(text, parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
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
          cursor.execute(f'UPDATE user_case SET case_money = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE user_case SET case_donate = {0} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f'❗️ Данная команда доступна от прав администратора <b>ADMIN</b>', parse_mode='html')
###########################################ПРАВИЛА###########################################
    if message.text.lower() in ["Правила", "правила"]:
       await bot.send_message(message.chat.id, f"""
🤬 | 1. Оскорбление [Мут - 15 минут ]
🤬 | 1.1 Оскорбление друзей личности [Мут - 10 минут]
🤬 | 1.2 Оскорбление родителем/родственников [Мут - 2 часа] + [ Варн ]
🤬 | 1.3 Оскорбление администрации [Мут - от 2 до 5 часов ] + [ Варн ]
🤬 | 1.4 Провокация на оскорбление [Мут - 5 минут]
🔞 | 2. Порнография в любом виде [Мут - 5 минут]
🔞 | 2.1 Спам контента порнографии [ Мут - 15 минут ]
🚷 | 3. Обман игроков [ Бан - 1 день ] + [ Варн ]
⛔️ | 4. Продажа игровой валюты [ Бан - 7 дней ] + [ Варн ] + [ Обнуление ]
⛔️ | 4.1 Продажа "Схем заработка" [Бан - 3 дня ] + [ Варн ]
⚠️ | 5. Капс (ПРИМЕР) [ Мут - 1 минута ]
⚠️ | 5.1 Флуд , спам [ Мут - 15 минут ]
⚠️ | 5.2 Не соглашёная реклама [ Мут - 1 час ] 
🆘 | 6. Любые действия связанные с вредом проекту [ Бан - 1 день ] + [ Варн ] [Если вред был нанесён тогда чс проекта ]
🆘 | 6.1 Читерство/Дюпинг в боте [ Обнуление ] + [ Варн ]      
       """, parse_mode='html')
###########################################ПОМОЩЬ###########################################
    if message.text.lower() in ["помощь", "Помощь"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])


       await bot.send_message(message.chat.id, f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, Вот информация о боте 🔎

📊 {config.channel} - <b>Игровой канал</b>
💬 {config.chat} - <b>Игровой чат</b>
🧑‍💻 {config.owner} - <b>Разработчик</b>

➖➖➖➖➖➖➖➖➖➖➖

📖 Доступные категории:

📝 <b>Основные</b>
🎮 <b>Игры </b>
🔨 <b>Работы</b>
🏘 <b>Имущество</b>
📖 <b>Привилегии</b>
⛔️ <b>Admins menu </b>
❕ <b>Остальные</b> 

➖➖➖➖➖➖➖➖➖➖➖
↘️Выберите одну из доступных <b>категорий </b>
    ''', reply_markup=help2, parse_mode='html')

###########################################СПИН#############################################
    if message.text.startswith("спин") or message.text.startswith("Спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])

        balance2 = '{:,}'.format(balance).replace(',', '.')
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0, 1001)
        msg = message
        user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])

        user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_status = str(user_status[0])

        name = msg.from_user.full_name
        su = msg.text.split()[1]
        su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
        su3 = float(su2)
        summ = int(su3)

        summ2 = '{:,}'.format(summ).replace(',', '.')
        print(f"{name} поставил в спин: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))

        if user_status in ['Vlaselin', 'Bog']:
           period = 2
        elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
           period = 1
        else:
           period = 5
         
        get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        loz = ['💩|👑|👑','💩|🖕|👑','💎|🖕|👑','💎|💣|🍌','👑|🍌|🖕','💎|🍓|💣']
        win = ['💎|🍓|🍌','👑|💎|🍓','🍓|👑|💎','💎|🍓|🍌','💎|🍓|🍓','🍌|🍌|💎']
        Twin = ['💎|💎|💎','🍓|🍓|🍓','👑|👑|👑','🍌|🍌|🍌']
        smtwin = ['🤯','🤩','😵','🙀']
        smwin = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rsmtwin = random.choice(smtwin)
        rsmtwin2 = random.choice(smtwin)
        rtwin = random.choice(Twin)
        rloser = random.choice(loser)
        rloser2 = random.choice(loser)
        rwin = random.choice(win)
        rloz = random.choice(loz)
        rsmwin = random.choice(smwin)
        rsmwin2 = random.choice(smwin)
        if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 350):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')

                        await bot.send_message(chat_id,
                                               f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 <b>Игра:</b> <code>Спин</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{rwin} - {c2}$</code>",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return

        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(351, 1000):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 <b>Игра:</b> <code>Спин</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>{rloz} - {c2}$</code>",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) == 1001:
                        c = Decimal(summ * 25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 <b>Игра:</b> <code>Спин</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{rwin} - {c2}$</code>",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}",
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
        else:
            await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые {period} секунд. {rloser}",
                                       parse_mode='html')


################################################### GAME-VB ########################################


    if message.text.lower() in ['vb', "вб"]:
       msg = message
       user_id = msg.from_user.id
   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вся информация за игру "Game-VB" 🧊

📌 | Пример: /gamevb

⚠️ | ВАЖНО: Это игра, в которой нету ставки. В этой игре вы играете сразу на весь свой баланс

⚖️ | Шансы:
🟥 | 70% - LOSER - [0.1X]
🟩 | 30% - WIN - [1.5X]
       """, parse_mode='html')

#################################################### ФУТБОЛ ########################################

    if message.text.lower() in ['футбол', "фб"]:
       msg = message
       user_id = msg.from_user.id
   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вся информация за игру "Футбол" ⚽️

📌 | Пример: Футбол\Фб [ставка] | Футбол 1

⚖️ | Шансы:
🟥 | 29% - Промах - [0.2Х]
🟥 | 31% - Штанга - [0.4Х]
🟥 | 20% - Перекладина - [0.8X]
🟩 | 12% - Гол - [1.4X]
🟩 | 3% - Девятка - [2.3X]
🟩 | 1% - Крестовина - [4.3X]
""", parse_mode='html')





    if message.text.startswith('Фб') or message.text.startswith('фб'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       rx = random.randint(0,9550)
       
       if user_status in ['Vlaselin', 'Bog']:
          period = 2
       elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
          period = 1
       else:
          period = 5

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Гол! - {i3}$</code> <b>[1.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Штанга! - {i3}$</code> <b>[0.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Перекладина! - {i3}$</code> <b>[0.8X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Гол! - {i3}$</code> <b>[1.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Девятка! - {i3}$</code> <b>[2.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Крестовина! - {i3}$</code> <b>[4.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в {period} секунд ", parse_mode='html')




    if message.text.startswith('Футбол') or message.text.startswith('футбол'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       rx = random.randint(0,9550)
       
       if user_status in ['Vlaselin', 'Bog']:
          period = 2
       elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
          period = 1
       else:
          period = 5
          
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Промах! - {i3}$</code> <b>[0.2X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Штанга! - {i3}$</code> <b>[0.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Проигрыш:</b> <code>Перекладина! - {i3}$</code> <b>[0.8X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Гол! - {i3}$</code> <b>[1.4X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Девятка! - {i3}$</code> <b>[2.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ <b>Игра:</b> <code>Футбол</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>Выигрыш:</b> <code>Крестовина! - {i3}$</code> <b>[4.3X]</b>
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в {period} секунд ", parse_mode='html')









##################################################КАЗИНО############################################
   
    if message.text.startswith('казино') or message.text.startswith('Казино'):
      try:
         msg = message
         user_id = msg.from_user.id

         games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         games = int(games[0])

         user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)

         summ2 = '{:,}'.format(summ).replace(',', '.')
         
         comment = msg.text.split()[2:]
         comment2 = ' '.join(comment)

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = round(int(balance[0]))

         rx = random.randint(0, 990)

         if len(comment2) > 50:
            return await message.reply(f'❗️ <b>Ваш комментарий</b> не может быть больше чем 50 символов ', parse_mode='html')
         else:
            pass

         if comment2 == '':
            comment3 = ''
         else:
            comment3 = f'\n<b>💬 Комментарий:</b> <code>{comment2}</code>'
         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         if user_status in ['Vlaselin', 'Bog']:
            period = 2
         elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
            period = 1
         else:
            period = 5

         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = f"{int(get[0])}"
         stavkatime = time.time() - float(last_stavka)

         if stavkatime < period:
            return await message.reply(f'❗️ Играть можно раз в <b>{period} секунд</b>', parse_mode='html')
         else:
            pass
         
         if balance < summ:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass
         
         if summ <= 0:
            return await message.reply('❗️ Ставка не может быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass
         
         if int(rx) in range(0, 100):
            status_stavka = 'Проигрыш'
            stavka = summ
            stavka2 = summ2
            stavka_x = 'x0'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(101, 350):
            status_stavka = 'Проигрыш'
            stavka = int(summ - summ * 0.3)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x0.3'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.7} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(351, 700):
            status_stavka = 'Проигрыш'
            stavka = int(summ - summ * 0.5)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x0.5'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(701, 850):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 1.5)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x1.5'
            stavka_smile = ['🙃', '😕', '😔', '😪']
            balance_new = balance - stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance + summ * 1.5)} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(851, 950):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 2.8)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'х2.8'
            stavka_smile = ['😌', '😇', '😲', '🤑']
            balance_new = balance 
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance + summ * 2.8)} WHERE user_id = {user_id}')
            connect.commit()

         if int(rx) in range(951, 960):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 5)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x5'
            stavka_smile = ['😌', '😇', '😲', '🤑']
            balance_new = (balance - summ) + stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance +summ * 5)} WHERE user_id = {user_id}')
            connect.commit()
         if int(rx) in range(961, 990):
            status_stavka = 'Выигрыш'
            stavka = int(summ * 25)
            stavka2 = '{:,}'.format(stavka).replace(',', '.')
            stavka_x = 'x25'
            stavka_smile = ['😌', '😇', '😲', '🤑']
            balance_new = (balance - summ) + stavka
            balance_new2 = '{:,}'.format(int(balance_new)).replace(',', '.')
            cursor.execute(f'UPDATE users SET balance = {(balance +summ * 25)} WHERE user_id = {user_id}')
            connect.commit()

         
         text = f'''
🤵‍♂️ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>
🤵‍♀️ <b>Игра:</b> <code>Казино</code>
🎟 <b>Ставка:</b> <code>{summ2}$</code>
🧾 <b>{status_stavka}:</b> <code>{stavka2}$</code>  <b>({stavka_x})</b>{comment3}
         '''
         await message.bot.send_message(message.chat.id, text, parse_mode='html')
         cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
         connect.commit()
      except IndexError:
         return await message.reply(f'❗️ <b>Вы не вели сумму ставки -</b> <code>казино 1</code> ', parse_mode='html')
      except ValueError:
         return await message.reply(f'❗️ <b>Вы не правильно ввели сумму - <code>казино 1</code> | <code>казино 1е1</code> | <code>казино 1к</code></b>', parse_mode='html')





###########################################PLINKO###########################################
    
    
    if message.text.startswith("плинко") or message.text.startswith("Плинко"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       win = ['🙂', '😋', '😄', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,937)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       name = msg.from_user.full_name 

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       summ2 = '{:,}'.format(summ).replace(',', '.')
       print(f"{name} поставил в казино: {summ} и выиграл/проиграл: {rx}")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,100):
                   c = Decimal(summ)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>0$</code> <b>[x0]</b>", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()   
                   return                           
                if int(rx) in range(101,300):
                   c = Decimal(summ - summ * 0.25)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>{c2}$</code> <b>[x0.25]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()  
                   return   
                if int(rx) in range(301,600):
                   c = Decimal(summ * 0.5)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Проигрыш:</b> <code>{c2}$</code> <b>[x0.25]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(601,850):
                   c = Decimal(summ - summ * 0.75)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.75]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.25} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(851,900):
                   c = Decimal(summ * 2)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x2]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
                if int(rx) in range(901,930):
                   c = Decimal(summ * 3)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x3]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return
                if int(rx) in range(931,932):
                    c = Decimal(summ * 29)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(config.owner_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x29]</b>", parse_mode='html')                   

                    await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x29]</b>", parse_mode='html')                   
                    cursor.execute(
                        f'UPDATE users SET balance = {(balance - summ) + (summ * 29)} WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                    connect.commit()
                if int(rx) in range(933,937):
                   c = Decimal(summ * 10)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2).replace(',', '.')
                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x10]</b>", parse_mode='html')                   

                   await bot.send_message(chat_id, f"🤵‍♂ <b>Игрок:</b> <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ <b>Игра:</b> <code>Плинко</code>\n🎟 <b>Ставка:</b> <code>{summ2}$</code>\n🧾 <b>Выигрыш:</b> <code>{c2}$</code> <b>[x10]</b>", parse_mode='html')                   
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 10)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
             elif summ <= 1:
                  await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}", parse_mode='html')                                      
          elif int(balance) <= int(summ):
               await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
       else:
        await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые 5️⃣ секунд. {rloser}", parse_mode='html')
        return











###########################################РЕЙТИНГ###########################################
    if message.text.lower() == 'рейтинг':
       msg = message
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                    (message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       rating2 = '{:,}'.format(rating).replace(',', '.')
       rey = ['👑','✨','✏️']
       ranrey = random.choice(rey)
       
      
       await bot.send_message(message.chat.id, f"💎 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш рейтинг - {rating2}", parse_mode='html')

    if message.text.startswith("рейтинг купить") or message.text.startswith("Рейтинг купить"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       rating2 = '{:,}'.format(summ).replace(',', '.')
       c = summ * 150000000
       c2 = '{:,}'.format(c).replace(',', '.')

       if (summ + rating) >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя покупать рейтинг больше лимита")
          return

       if summ > 0:
          if int(balance) >= int(summ * 150000000):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы повысили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
             connect.commit()

 
       if int(balance) < int(summ * 150000000):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if summ <= 0:
         await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя купить отрицательное число! {rloser}", parse_mode='html')
    
    if message.text.startswith("Рейтинг продать") or message.text.startswith("рейтинг продать"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       c = summ * 100000000
       c2 = '{:,}'.format(c).replace(',', '.')
       rating2 = '{:,}'.format(summ).replace(',', '.')
       if summ > 0:
        if int(rating) >= int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы понизили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
          connect.commit()

        if int(rating) < int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, у вас недостаточно рейтинга для его продажи! {rloser}", parse_mode='html')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя продать отрицательное число! {rloser}", parse_mode='html')


###########################################ПЕРЕВОДЫ###########################################
    if message.text.startswith("передать") or message.text.startswith("Передать"):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.full_name 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       id_perevod = int(msg.text.split()[2])
       
       name_id_perevod = cursor.execute(f'SELECT user_name from users where user_id ="{id_perevod}"')
       name_id_perevod = str(name_id_perevod[0])

       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       print(f"{name} перевел: {perevod} игроку на ID: {id_perevod}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       if perevod > 0:
          if balance >= perevod:  
             if user_status in ['Admin', 'Helper_Admin']:
               await bot.send_message(config.owner_id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег по ID\n💈 | Сумма: {perevod2}\n👨 | Игроку: {name_id_perevod}", parse_mode='html')

             await bot.send_message(id_perevod, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег по ID\n💈 | Сумма: {perevod2}\n👨 | Игроку: {name_id_perevod}", parse_mode='html')
             await message.reply_to_message.reply(f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег по ID\n💈 | Сумма: {perevod2}\n👨 | Игроку: {name_id_perevod}", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{id_perevod}"')
             connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f'{user_name}, недостаточно средств! {rloser}', parse_mode='html')

       if perevod <= 0:
          await message.reply( f'{user_name}, нельзя перевести отрицательное число! {rloser}', parse_mode='html')  

    if message.text.startswith("Дать") or message.text.startswith("дать"):
       if not message.reply_to_message:
          await message.reply("Эта команда должна быть ответом на сообщение!")
          return
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.full_name 
       rname =  msg.reply_to_message.from_user.full_name 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       print(f"{name} перевел: {perevod} игроку {rname}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       if perevod > 0:
          if balance >= perevod:  
             await bot.send_message(config.owner_id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег\n💈 | Сумма: {perevod2}$\n👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

             await message.reply_to_message.reply(f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег\n💈 | Сумма: {perevod2}$\n👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
             connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if perevod <= 0:
          await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя перевести отрицательное число! {rloser}", parse_mode='html')  


###########################################ТОП###########################################
    if message.text.lower() in ["топ", "Топ"]:
       list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
       top_list = []
       user_id = message.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       num = 0

       

       for user in list:
           if user[7] >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
              c6 = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
           else:
              c6 = user[7]

           

           num += 1

           if num == 1:
              num2 = '1️⃣'
              num3 = ' <b>💎ТОП 1💎</b> |'
           if num == 2:
              num2 = '2️⃣'
              num3 = ''
           if num == 3:
              num2 = '3️⃣'
              num3 = ''
           if num == 4:
              num2 = '4️⃣'
              num3 = ''
           if num == 5:
              num2 = '5️⃣'
              num3 = ''
           if num == 6:
              num2 = '6️⃣'
              num3 = ''
           if num == 7:
              num2 = '7️⃣'
              num3 = ''
           if num == 8:
              num2 = '8️⃣'
              num3 = ''
           if num == 9:
              num2 = '9️⃣'
              num3 = ''
           if num == 10:
              num2 = '🔟'
              num3 = ''
           c = Decimal(c6)
           c2 = '{:,}'.format(c).replace(',', '.')

           if user[3] == 'Owner':
             stats = ' ✅<b>РАЗРАБОТЧИК</b>✅ |'
           if user[3] == 'Admin':
             stats = ' ⛔️<b>АДМИН</b>⛔️ |'
           if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
           if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''
           
           
           top_list.append(f"{num2} {user[1]} |{stats}{num3} 🔎 ID: <code>{user[0]}</code> | {c2}💎")

       top = "\n".join(top_list)
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, топ 10 игроков бота:\n" + top, reply_markup=fulltop, parse_mode='html')
# Смена имени
    if message.text.startswith('Сменить ник') or message.text.startswith('cменить ник'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       su = " ".join(message.text.split()[2:])
       name = (su).replace('🇺🇦', '').replace('🇷🇺','').replace('🇷🇸','').replace('🇸🇰','').replace('🇸🇮','').replace('ᅠᅠᅠᅠᅠ','')

       if name in ['', ' ', '  ', '   ','    ', '     ', '      ', '       ','        ','         ','          ','           ','            ','              ','              ','               ','                ','            ']:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш ник не может быть пустым", parse_mode='html')
          return

       if len(name) <= 20:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно поменяли свое имя на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
          print(f"{user_name} сменил ник на {name}")

          all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
          all_family2 = []
          proverka_family = 0
          for all_owner_id in all_family:
            all_family2.append(all_owner_id[0])

          user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

          if user_id_family != None:
            cursor.execute(f'UPDATE user_family SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
          else:
            pass

          if user_id in all_family2:
            cursor.execute(f'UPDATE family SET owner_name = \"{name}\" WHERE owner_id = "{user_id}"')
          else:
            pass

       else: 
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ваш ник не может быть длинее 20 символов!", parse_mode='html')
    if message.text.lower() == 'Эфириум':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       await bot.send_message(message.chat.id,f"🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>, количество эфириума: {ethereum}🟣")

    if message.text.lower() == 'эфириум курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2).replace(',', '.')

       await bot.send_message(message.chat.id,f"🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>, курс эфириума: {c3}🟣", parse_mode='html')
    if message.text.startswith('Эфириум') or message.text.startswith('эфириум'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       d = int(su3)
       d2 = '{:,}'.format(d).replace(',', '.')
       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2).replace(',', '.')

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if summ >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  достигнул лимит, 999 фенд")
          return

       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= ethereum:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')          
    
    
    if message.text.lower() == 'ограбить банк':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       x = random.randint(1,3)
       period = 86400 #86400 s 24h
       get = cursor.execute("SELECT stavka_bank FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       rx = random.randint(1000000,25000000)
       rx2 = '{:,}'.format(rx).replace(',', '.')
       if stavkatime > period:
          if int(x) in range(2,3):
             await bot.send_message(message.chat.id, f"🏦 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно ограбили банк на {rx2}$ ✅", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + rx} WHERE user_id ="{user_id}"')
             cursor.execute(f'UPDATE bot_time SET stavka_bank = {time.time()} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вам не удалось ограбить банк", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ограбить банк можно раз в 24ч⏳", parse_mode='html')
# bonus 24h
    
    
    if message.text.lower() == 'ежедневный бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       period = 86400 #86400 s = 24h
       get = cursor.execute("SELECT stavka_bonus FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       
       rx = random.randint(1000000,25000000)
       rx2 = '{:,}'.format(rx).replace(',', '.')

       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ежедневный бонус в сумме {rx2}$ 💵", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + rx}  WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {time.time()} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать ежедневный бонус можно раз в 24ч⏳", parse_mode='html') 


#####################################КУБИК##############################################################
    if message.text.startswith('Кубик') or message.text.startswith('кубик'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])
         
         rx = random.randint(0,700)

         chil = int(message.text.split()[1])
         su = msg.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)
         summ2 = '{:,}'.format(summ).replace(',', '.')
         
         
         
         summ_win = summ * 3
         summ_win2 = '{:,}'.format(summ_win).replace(',', '.')

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         if chil <= 6:
            if balance >= summ:
             if summ > 0:
               if stavkatime > period:
                  if int(rx) in range(0,100):
                     if chil == 1:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲1 - {summ2}$\n🧾 | Выигрыш: 🎲1 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲1 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(101,200):
                     if chil == 2:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲2 - {summ2}$\n🧾 | Выигрыш: 🎲2 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲2 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(201,300):
                     if chil == 3:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲3 - {summ2}$\n🧾 | Выигрыш: 🎲3 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲3 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(401,500):
                     if chil == 4:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲4 - {summ2}$\n🧾 | Выигрыш: 🎲4 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲4 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(501,600):
                     if chil == 5:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲5 - {summ2}$\n🧾 | Выигрыш: 🎲5 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲5 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(601,700):
                     if chil == 6:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲6 - {summ2}$\n🧾 | Выигрыш: 🎲6 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲6 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
               else:
                  await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, данного числа нету в кубике!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример Кубик 6 1000", parse_mode='html')



#############################################################ЧЁТНОЕ \ НЕЧЁТНОЕ#########################################################



    if message.text.startswith('Нечётное') or message.text.startswith('нечётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)
         summ2 = '{:,}'.format(summ).replace(',', '.')

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win).replace(',', '.')

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if balance >= summ:
          if summ > 0:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')

    if message.text.startswith('Чётное') or message.text.startswith('чётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)
         summ2 = '{:,}'.format(summ).replace(',', '.')

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win).replace(',', '.')

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance).replace(',', '.')

         if balance >= summ:
          if summ > 0:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')




##################################################### WHEEL \ dice ##########################################################

    if message.text.startswith('dice') or message.text.startswith('Dice'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       game = int(game[0])

       black_red = str(message.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)


       summ2 = "{:,}".format(summ).replace(',', '.')

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')

       if user_status in ['Bog','Vlaselin']:
          period = 2
       else:
          period = 5
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       if balance >= summ:
        if summ > 0:
          
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
          return
       if stavkatime > period:
        if balance >= summ:
         if summ > 0:   
          if black_red in ['ч',"черный","Ч", "Черный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [🔴]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [⚫️]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit() 
          if black_red in ['к',"красный","К", "Красный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [⚫️]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🔴]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()  

    if message.text.lower() in ['wheel','dice']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за игру Wheel 🎱

✒️ | Пример: dice [ч\к] [сумма]

⚙️ | ч - черный ⚫️
⚙️ | к - красный 🔴

⚖️ | Шансы: Черный ⚫️ - 50%, Красный 🔴 - 50%, Зерро 🟢 - 0.1%   
         """, parse_mode='html')

















############################################СИСТЕМА КРАФТА#############################
    if message.text.lower() == 'крафтить':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
   
       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       menu_craft = InlineKeyboardMarkup(row_width=2)
       resurs1 = InlineKeyboardButton(text='🟥 Кирка Zerro ⛏', callback_data='resurs1')
       resurs2 = InlineKeyboardButton(text='🟥 Грабли Zerro 🌾', callback_data='resurs2')
       resurs3 = InlineKeyboardButton(text='🟨 Кирка Cherick ⛏', callback_data='resurs3')
       resurs4 = InlineKeyboardButton(text='🟨 Грабли Cherick 🌾', callback_data='resurs4')
       menu_craft.add(resurs1, resurs2, resurs3, resurs4)

       if basement == 1:
          basement_name = 'Standard'
          basement_period = 30
       
       if basement == 2:
          basement_name = 'Plus++'
          basement_period = 15
      
       if basement == 3:
          basement_name = 'Euro Plus++'
          basement_period = 4
       

       if basement > 0:
          await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, добро пожаловать в подвал🕋

👤 | Владелец: {user_name}
🕋 | Подвал: {basement_name}
⏳ | Ограничение по времени: {basement_period} секунд

↘️Выберите предмет какой хотите скрафтить       
""",reply_markup=menu_craft, parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас нету подвала", parse_mode='html')
    if message.text.lower() == 'система крафта':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные о системе крафта⚒

▶️ | ⬜️ - обычные
▶️ | 🟩 - редкие
▶️ | 🟦 - сверх-редкие
▶️ | 🟪 - эпические
▶️ | 🟥 - мифические
▶️ | 🟨 - легендарные


📦 | Предметы:
⛏ | [🟥] [1] Кирка Zerro 
🌾 | [🟥] [2] Грабли Zerro 
⛏ | [🟨] [3] Кирка Cherick 
🌾 | [🟨] [4] Грабли Cherick 

⚖️ | Шансы крафта предметов:
⛏ | [🟥] [1] Кирка Zerro - 35%
🌾 | [🟥] [2] Грабли Zerro - 35%
⛏ | [🟨] [3] Кирка Cherick - 10%
🌾 | [🟨] [4] Грабли Cherick - 10%

⚒ | Чтобы начать крафтить введите команду \"Крафтить\"
ℹ️ | Крафтить можно только при наличии подвала
ℹ️ | У каждого подвала есть свои ограничение по времени на крафт""", parse_mode='html')
########################################ДОМА########################################
    if message.text.lower() == 'продать подвал':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       if basement == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Standard'

       if basement == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Plus++'

       if basement == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Euro plus++'

       if basement > 0:
          await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Продажа подвала\n🕋 | Подвал: {basement2}\n💈 |Продано за: {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
          return


    if message.text.startswith('Купить подвал') or message.text.startswith('купить подвал') :
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Standard'

       if member == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Plus++'

       if member == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          basement2 = 'Euro plus++'

       if member > 0:
          if member < 4:
             if house > 0:
                if basement == 0:
                   if balance >= summ:
                      await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Покупка подвала\n🕋 | Подвал: {basement2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                      cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                      cursor.execute(f'UPDATE house SET basement = {member} WHERE user_id = {user_id}')
                      connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средтсв!", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
             else:
                 await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету дома! Подвал можно покупать только имея дом", parse_mode='html')
          else:
              await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')



    if message.text.lower() in ['подвал', 'подвалы']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список доступных подвалов 🕋

🕋 | [1] Standard - 5.000.000$
🕋 | [2] Plus++ - 10.000.000$
🕋 | [3] Euro Plus++ - 20.000.000$

🛒 Чтобы купить подвал себе в дом, введите команду \"Купить подвал [номер]\" """, parse_mode='html')
    
    
    
    
    if message.text.lower() == 'мой дом':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       if house == 1:
          house2 = 'Коробка'
       
       if house == 2:
          house2 = 'Сарай'

       if house == 3:
          house2 = 'Маленький домик'

       if house == 4:
          house2 = 'Квартира'

       if house == 5:
          house2 = 'Огромный дом'

       if house == 6:
          house2 = 'Коттедж'

       if house == 7:
          house2 = 'Вилла'

       if house == 8:
          house2 = 'Загородный дом'

       if basement == 1:
          basement2 = '\n🕋 | Подвал: Standard'


       if basement == 2:
          basement2 = '\n🕋 | Подвал: Plus++'
   

       if basement == 3:
          basement2 = '\n🕋 | Подвал: Euro Plus++'
      
       if basement == 0:
          basement2 = '\n🕋 | Подвал не имеиться'
         
       if house > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш дом🏡\n\n👤 | Владелец: {user_name}\n🏠 | Дом: {house2}{basement2}\n\n🛒 Чтобы купить подвал , введите команду \"Подвалы\"\nℹ️ Чтобы продать подвал введите команду \"Продать подвал\"\nℹ️ Чтобы продать дом введите команду  \"Продать дом\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нету дома, что бы купить дом введите команду \"Дома\"", parse_mode='html')
    
    
    if message.text.lower() == 'продать дом':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       if basement == 1:
          basement2 = '\n🕋 | Подвал: Standard'
          summ_basement = 5000000

       if basement == 2:
          basement2 = '\n🕋 | Подвал: Plus++'
          summ_basement = 10000000

       if basement == 3:
          basement2 = '\n🕋 | Подвал: Euro Plus++'
          summ_basement = 20000000
       else:
          basement2 = ''
          summ_basement = 0

       if house == 1:
          house2 = 'Коробка'
          summ = 500000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 1


       if house == 2:
          house2 = 'Сарай'
          summ = 3000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 2
      
       if house == 3:
          house2 = 'Маленький домик'
          summ = 5000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 3
      
       if house == 4:
          house2 = 'Квартира'
          summ = 7000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 4
      
       if house == 5:
          house2 = 'Огромный дом'
          summ = 10000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 5

       if house == 6:
          house2 = 'Коттедж'
          summ = 50000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 6

       if house == 7:
          house2 = 'Вилла'
          summ = 100000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 7

       if house == 8:
          house2 = 'Загородный дом'
          summ = 5000000000 + summ_basement
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 8

       if house > 0:
          await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Продажа дома\n🏠 | Дом: {house2}{basement2}\n💈 |Продано за: {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ + summ_basement} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас и так нету дома! Что бы купить дом введите команду \"Дома\"", parse_mode='html')
          return

    if message.text.startswith('купить дом') or message.text.startswith('Купить дом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       member = int(message.text.split()[2])

       if member == 1:
          house2 = 'Коробка'
          summ = 500000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 1


       if member == 2:
          house2 = 'Сарай'
          summ = 3000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 2
      
       if member == 3:
          house2 = 'Маленький домик'
          summ = 5000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 3
      
       if member == 4:
          house2 = 'Квартира'
          summ = 7000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 4
      
       if member == 5:
          house2 = 'Огромный дом'
          summ = 10000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 5

       if member == 6:
          house2 = 'Коттедж'
          summ = 50000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 6

       if member == 7:
          house2 = 'Вилла'
          summ = 100000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 7

       if member == 8:
          house2 = 'Загородный дом'
          summ = 5000000000
          summ2 = '{:,}'.format(summ).replace(',', '.')
          member_house = 8

       if house == 0:
          if member > 0:
             if member < 9:
                if summ <= balance:
                   await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Покупка дома\n🏠 | Дом: {house2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE house SET house = {member_house} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')               
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас уже есть дом, что бы продать дом введите команду \"Продать дом\"", parse_mode='html')







    if message.text.lower() == 'дома':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные дома:
🏠 1. Коробка - 500.000$
🏠 2. Сарай - 3.000.000$
🏠 3. Маленький домик - 5.000.000$
🏠 4. Квартира - 7.000.000$
🏠 5. Огромный дом - 10.000.000$
🏠 6. Коттедж - 50.000.000$
🏠 7. Вилла - 100.000.000$
🏠 8. Загородный дом - 5.000.000.000$

🛒 Для покупки дома введите "Купить дом [номер]"
       
       """, parse_mode='html')  




#########################################МАШИНЫ#######################################################
    if message.text.lower() == 'моя машина':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])
       if benz < 0:
             benz2 = 0
       else:
          benz2 = benz
       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошое 🟩'
          if hp == 75:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Среднее 🟧'
          if hp == 50:
             hp2 = 'Плохое 🟥'
          if hp == 26:
             hp2 = 'Плохое 🟥'
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 2:
             hp2 = 'Ужасное 🛑'

       if cars > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш автомобиль🚘\n\n👤 | Владелец: {user_name}\n🚗 | Автомобиль: {cars_name}\n🚨 | Состояние: {hp2}\n⛽️ | Бензин: {benz2}%\n💰 | Стоимость: {cars_summ2}$\n\nℹ️ Чтобы продать машину введите команду \"Машину продать\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
     


    if message.text.lower() == 'машину продать':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       if cars > 0:
          await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Продажа машины\n🚘 | Машина: {cars_name}\n💈 |Проданно за: {cars_summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
          return
      
    if message.text.startswith('Купить машину') or message.text.startswith('купить машину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if member == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       if member > 0:
          if member < 19:
             if cars == 0:
                if balance >= cars_summ:
                   await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Покупка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: {cars_summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - cars_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET cars = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть машина", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')











    if message.text.lower() == 'машины':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные машины:
🚗 1. Самокат - 10.000.000$
🚗 2. Велосипед - 15.000.000$
🚗 3. Гироскутер - 30.000.000$
🚗 4. Сегвей - 50.000.000$
🚗 5. Мопед - 90.000.000$
🚗 6. Мотоцикл - 100.000.000$
🚗 7. ВАЗ 2109 - 250.000.000$
🚗 8. Квадроцикл - 400.000.000$
🚗 9. Багги - 600.000.000$
🚗 10. Вездеход - 900.000.000$
🚗 11. Лада Xray - 1.400.000.000$
🚗 12. Audi Q7 - 2.500.000.000$
🚗 13. BMW X6 - 6.000.000.000$
🚗 14. Toyota FT-HS - 8.000.000.000$
🚗 15. BMW Z4 M - 10.000.000.000$
🚗 16. Subaru WRX STI - 40.000.000.000$
🚗 17. Lamborghini Veneno - 100.000.000.000$
🚗 18. Tesla Roadster - 300.000.000.000$

🚗 19. RedBlack Lamborghini 500₽

🛒 Для покупки дмашины введите "Купить дмашину [19]
🛒 Для покупки машины введите "Купить машину [номер]"    
       
""", parse_mode='html')







################################################ДОНАТ МАШИНА############################################################
    if message.text.lower() == 'моя дмашина':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       money = cursor.execute("SELECT money from money_balance where user_Id = ?", (message.from_user.id,)).fetchone()
       money = int(money[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])
       if benz < 0:
             benz2 = 0
       else:
          benz2 = benz
       if cars == 19:
          cars_name = 'RedBlack Lamborghini'
          cars_summ = 500
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошое 🟩'
          if hp == 75:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Среднее 🟧'
          if hp == 50:
             hp2 = 'Плохое 🟥'
          if hp == 26:
             hp2 = 'Плохое 🟥'
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 2:
             hp2 = 'Ужасное 🛑'

       if cars > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш донат автомобиль🚘\n\n👤 | Владелец: {user_name}\n🚗 | Автомобиль: {cars_name}\n🚨 | Состояние: {hp2}\n⛽️ | Бензин: {benz2}%\n💰 | Стоимость: {cars_summ2}₽\n\nℹ️ Чтобы продать машину введите команду \"Машину продать\\nℹ️ Чтобы заправить машину введите команду \"Заправить\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
     


    if message.text.lower() == 'дмашину продать':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       money = cursor.execute("SELECT money from money_balance where user_Id = ?", (message.from_user.id,)).fetchone()
       money = int(money[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       if cars == 19:
          cars_name = 'RedBlack Lamborghini'
          cars_summ = 500
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       if cars > 0:
          await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Продажа дмашины\n🚘 | Дмашина: {cars_name}\n💈 |Проданно за: {cars_summ2}₽", parse_mode='html')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету дмашины", parse_mode='html')
          return
      
    if message.text.startswith('Купить дмашину') or message.text.startswith('купить дмашину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       money = cursor.execute("SELECT money from money_balance where user_Id = ?", (message.from_user.id,)).fetchone()
       money = int(money[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       member = int(message.text.split()[2])
       
       if member == 19:
          cars_name = 'RedBlack Lamborghini'
          cars_summ = 500
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       if member > 0:
          if member < 20:
             if cars == 0:
                if money >= cars_summ:
                   await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Покупка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: {cars_summ2}₽", parse_mode='html')
                   cursor.execute(f'UPDATE money_balance SET money = {money - cars_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET cars = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть дмашина", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')

############################################################ШАХТА############################################################
    if message.text.lower() == 'шахта':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id,f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за шахту ⛏

⛏ | Руды на шахте:
      🪨 | Камень -  40%
      ⛓ | Железо - 30%
      🪙 | Серебро - 15%
      🎇 | Бронза - 10%
      ⚜️ | Золото - 5%

ℹ️ | Чтобы продать какую руду , воспользуйтесь командой \"Продать [Руда] [Количество]\"
ℹ️ | Чтобы копать руду воспользуйтесь командой \"Копать руду\"       
       """, parse_mode='html')
    if message.text.startswith('продать') or message.text.startswith('Продать'):
      try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         # iron, silver, bronza, gold
         iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
         iron = int(iron[0])
         
         metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
         metall = int(metall[0])

         silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
         silver = int(silver[0])

         bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
         bronza = int(bronza[0])

         gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
         gold = int(gold[0])

         rud = str(message.text.split()[1])

         su = msg.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         c = int(su3)

         summ = c * 25000
         summ2 = '{:,}'.format(summ).replace(',', '.')
         if rud == 'камень':
            if c <= iron:
             if c > 0:               
               summ = c * 25000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} камень 🪨 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET iron = {iron - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'железо':
            if c <= metall:
             if c > 0:               
               summ = c * 45000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} железо ⛓ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET metall = {metall - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'серебро':
            if c <= silver:
             if c > 0:               
               summ = c * 125000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} серебро 🪙 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET silver = {silver - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'бронзу':
            if c <= bronza:
             if c > 0:               
               summ = c * 200000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} бронзы 🎇 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'золото':
            if c <= gold:
             if c > 0:               
               summ = c * 500000
               summ2 = '{:,}'.format(summ).replace(',', '.')
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} золото ⚜️ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
      except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Продать [камень, железо, серебро, бронзу, золото, лён, хлопок] 1", parse_mode='html')


    if message.text.lower() == 'копать руду':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rx = random.randint(0,100)

      # iron, silver, bronza, gold
       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       
       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       
       rx_iron = random.randint(15,20)
       rx_metall = random.randint(10,15)
       rx_silver = random.randint(5,10)
       rx_bronza = random.randint(0,5)
       
       if pick == 'Cherick':
          period = 3
       else:
          period = 5
       get = cursor.execute("SELECT time_pick FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)

       if pick == 'Cherick':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron * 2} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall * 2} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver * 2} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza * 2} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 2 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return

       if pick == 'Zerro':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron * 2} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall * 2} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver * 2} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza * 2} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 2 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return

       if pick == 'on':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 1 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 1} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')
          return
          




    if message.text.lower() == 'продать кирку':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       if pick == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! вы не можете продать кирку Cherick", parse_mode='html')

       if pick == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! вы не можете продать кирку Zerro", parse_mode='html')

       if pick == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')

       if pick == 'on':
          await bot.send_message(message.chat.id, f"⛏ | Вы продали кирку за 5.000$ ", parse_mode='html')
          cursor.execute(f'UPDATE mine SET pick = "off" WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
          connect.commit()
    if message.text.lower() == 'купить кирку':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]


       if pick == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка Cherick", parse_mode='html')

       if pick == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка Zerro", parse_mode='html')


       if pick == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка, что бы продать кирку введите команду \"Продать кирку\"", parse_mode='html')

       if pick == 'off':
          if balance >= 5000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили кирку за 5.000$ ", parse_mode='html')
             cursor.execute(f'UPDATE mine SET pick = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')



#################################################ФЕРМА#################################################
    if message.text.lower() in ['ферма', 'фермы']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за ферму 🌾

🌾 | Доступный урожай:
      🍃 | Лён =  5-10
      🌿 | Хлопок = 5-10

ℹ️ | Чтобы собрать какой то урожай, воспользуйтесь командой \"Собрать [лён\ хлопок]
ℹ️ | Чтобы продать какой-то урожай, воспользуйтесь командой \" Продать [лён\хлопок] [Количество]       
       """, parse_mode='html')
    if message.text.startswith('продать хлопок') or message.text.startswith('Продать хлопок'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       c = int(su3)
       c2 = '{:,}'.format(c).replace(',', '.')
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if c <= cotton:
        if c > 0:          
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} хлопка 🌿 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {cotton - c} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько ресурсов!", parse_mode='html')



    if message.text.startswith('продать лён') or message.text.startswith('Продать лён'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       c = int(su3)
       c2 = '{:,}'.format(c).replace(',', '.')
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if c <= linen:
        if c > 0:          
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} лён 🍃 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {linen - c} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько ресурсов!", parse_mode='html')

    
    if message.text.startswith('cобрать') or message.text.startswith('Собрать'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
         rake = rake[0]

         linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
         linen = int(linen[0])

         cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
         cotton = int(cotton[0])

         rud = str(message.text.split()[1])

         rx_linen = random.randint(5,10)

      
         if rake == 'Cherick':
             period = 2
         else:
            period = 5
         get = cursor.execute("SELECT time_rake FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         
         if stavkatime > period:
            if rake == 'Cherick':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'Zerro':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'on':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету граблей, что бы купить грабли введите команду \"Купить грабли\"", parse_mode='html')
               return
         
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать урожай можно раз в {period} секунд!", parse_mode='html')     
            return      
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Собрать [лён, хлопок]", parse_mode='html')

          
    if message.text.lower() == 'продать грабли':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
       rake = rake[0]

       if rake == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету граблей, чтобы купить грабли введите команду \"Купить грабли\"", parse_mode='html')

       if rake == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Но вы не можете продать грабли Zerro", parse_mode='html')

       if rake == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Но вы не можете продать грабли Cherick", parse_mode='html')




       if rake == 'on':
         await bot.send_message(message.chat.id, f"⛏ | Вы продали грабли за 5.000$ ", parse_mode='html')
         cursor.execute(f'UPDATE farm SET rake = "off" WHERE user_id = "{user_id}"')
         cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
         connect.commit()

    if message.text.lower() == 'купить грабли':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
       rake = rake[0]

       if rake == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли, что бы продать грабли введите команду \"Продать грабли\"", parse_mode='html')

       if rake == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли", parse_mode='html')
 
       if rake == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли", parse_mode='html')


       if rake == 'off':
          if balance >= 5000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили грабли за 5.000$ ", parse_mode='html')
             cursor.execute(f'UPDATE farm SET rake = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')



###############################################ИНВЕНТАРЬ####################################################################

    if message.text.lower() == 'инвентарь':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       farm = 0
       men = 0
       ob = 0

       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       linen_f = '{:,}'.format(linen).replace(',', '.')

       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       cotton_f = '{:,}'.format(cotton).replace(',', '.')

       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       iron_f = '{:,}'.format(iron).replace(',', '.')

       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])
       metall_f = '{:,}'.format(metall).replace(',', '.')

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])
       silver_f = '{:,}'.format(silver).replace(',', '.')

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])
       bronza_f = '{:,}'.format(bronza).replace(',', '.')

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       gold_f = '{:,}'.format(gold).replace(',', '.')

       if iron > 0:
          iron2 = f'    🪨 | Камня: {iron_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          iron2 = ''

       if metall > 0:
          metall2 = f'    ⛓ | Железа: {metall_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          metall2 = ''
      
       if silver > 0:
          silver2 = f'    🪙 | Серебра: {silver_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          silver2 = ''

       if bronza > 0:
          bronza2 = f'    🎇 | Бронзы: {bronza_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          bronza2 = ''

       if gold > 0:
          gold2 = f'    ⚜️ | Золота: {gold_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          gold2 = ''

       if men > 0:
          men_2 = '\n⛏ | Шахта\n'
       else:
          men_2 = ''
       
       if linen > 0:
          linen2 = f'      🍃 | Лён: {linen_f} шт\n'
          farm = farm + 1
          ob = ob + 1
       else:
          linen2 = ''

       if cotton > 0:
          cotton2 = f'      🌿 | Хлопок: {cotton_f} шт\n'
          farm = farm + 1
          ob = ob + 1
       else:
          cotton2 = ''

       if farm > 0:
          farm2 = '🌾 | Ферма\n'
       else:
          farm2 = ''

       if ob == 0:
          ob2 = f'Вещи отсутствуют {rloser}'
       else:
          ob2 = ''
      
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваш инвентарь:\n{ob2}{men_2}{iron2}{metall2}{silver2}{bronza2}{gold2}\n{farm2}{linen2}{cotton2}", parse_mode='html')

    if message.text.startswith('гонка') or message.text.startswith('Гонка'):

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?", (message.from_user.id,)).fetchone()
       cars = cars[0]

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       rx = random.randint(0,1000)
       rx2 = random.randint(1,25)
       summ3 = summ * 2
       summ4 = '{:,}'.format(summ3).replace(',', '.')

       if summ < 1:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя играть на отрицательное число")
          return

       period = 5
       getе = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(getе[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if summ <= balance:
             if cars > 0:
                if hp > 0:
                   if benz > 0:
                      if int(rx) in range(0,800):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$", parse_mode='html')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()                   
                      if int(rx) in range(801, 1000):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {summ4}$", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()                   
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас закончился бензин в автомобиле", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас поломался автомобиль , вы не можете участвовать в гонках", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Какие гонки без автомобиля? Купите автомобиль", parse_mode='html') 
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств", parse_mode='html') 
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! играй можно раз в {period} секунд", parse_mode='html') 


    if message.text.startswith('дгонка') or message.text.startswith('Дгонка'):

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?", (message.from_user.id,)).fetchone()
       cars = cars[0]

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       if cars == 19:
          cars_name = 'RedBlack Lamborghini'
          cars_summ = 500
          cars_summ2 = '{:,}'.format(cars_summ).replace(',', '.')


       rx = random.randint(0,1000)
       rx2 = random.randint(1,25)
       summ3 = summ * 5
       summ4 = '{:,}'.format(summ3).replace(',', '.')

       if summ < 1:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя играть на отрицательное число")
          return

       period = 5
       getе = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(getе[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if summ <= balance:
             if cars > 0:
                if hp > 0:
                   if benz > 0:
                      if int(rx) in range(0, 600):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {summ4}$", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 5} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()    
                      if int(rx) in range(601, 800):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$", parse_mode='html')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()                   
                      if int(rx) in range(801, 1000):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {summ4}$", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 5} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()                   
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас закончился бензин в донат автомобиле", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас поломался донат автомобиль , вы не можете участвовать в гонках", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Какие гонки без донат автомобиля? Купите автомобиль", parse_mode='html') 
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств", parse_mode='html') 
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! играй можно раз в {period} секунд", parse_mode='html') 



######################################################Привилегии \ Донат меню##############################################

    if message.text.lower() == 'донат':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins).replace(',', '.')

       donate_menu = InlineKeyboardMarkup(row_width=2)
       donate_menu.row(
         InlineKeyboardButton(text=f'💰 Пополнить', callback_data='info_donate_online')
       )
       privilegii = InlineKeyboardButton(text='📝 Привилегии', callback_data='privilegii')
       case = InlineKeyboardButton(text='🎁 Кейсы', callback_data='case')
       adms = InlineKeyboardButton(text='⛔️ Права администратора', callback_data='adms')
       ysloviya_cash = InlineKeyboardButton(text='❗️ Условия покупок', callback_data='ysloviya_cash')
       prodazh_valyte = InlineKeyboardButton(text='💸 Продажа валюты', callback_data='prodazh_valyte')
       donate_menu.add(privilegii, adms, case, ysloviya_cash, prodazh_valyte)

       money = await user_money(message.from_user.id)
       
       x2donate_status = await status_x2donate()

       if x2donate_status == 'on':
         x2donate_status = 'Включен'
       else:
         x2donate_status = 'Выключен'

       await message.reply( f"""
❗️ Пояивились <b>проблемы с авто оплатой</b>, обращайтесь к {config.owner}
➖➖➖➖➖➖➖➖➖➖➖➖
👝 <b>Баланс:</b> <i>{'{:,}'.format(money).replace(',','.')} руб.</i>
🪙 <b>Donate-Coins:</b> <i>{donate_coins2} шт.</i>
🎗 <b>X2 Донат:</b> <i>{x2donate_status}</i>
➖➖➖➖➖➖➖➖➖➖➖➖
👾 <b>Команды:</b>
💰 <b>Пополнить баланс -</b> <code>пополнить 100</code>
📊 <b>Курс валют -</b> <code>курс</code>
🔁 <b>Обменять рубли в Donate-Coins -</b> <code>Обменять 100</code>
➖➖➖➖➖➖➖➖➖➖➖➖
🪙 <b>1 Donate-Coins =</b> <code>3Р</code> <b>/</b> <code>1грн</code> <b>/</b> <code>0.5 zl</code>
➖➖➖➖➖➖➖➖➖➖➖➖
🔎 <b>Категории:</b>
        <b>📝 Привилегии</b>
        <b>⛔️ Права администратора</b>
        <b>🎁 Кейсы</b>
        <b>❗️ Условия покупок</b>
➖➖➖➖➖➖➖➖➖➖➖➖
❗️ Прежде чем написать <b>владельцу бота</b> , посмотрите <b>условия покупок</b>
➖➖➖➖➖➖➖➖➖➖➖➖
⤵️ Выберите одну из <b>категорий</b>  
       """, reply_markup=donate_menu, parse_mode='html')
    if message.text.lower() == 'властелин':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВЛАСТЕЛИН 🤎

🛒 | При покупке:
        1️⃣ | Бонус-кит ВЛАСТЕЛИН
        2️⃣ | Префикс ВЛАСТЕЛИН
        3️⃣ | 50.000.000$
        4️⃣ | 150 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс
        9️⃣ | Ограничение на время в играх становиться 2 секунды

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ВЛАСТЕЛИН
        2️⃣ | Префикс ВЛАСТЕЛИН
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс
        5⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'бог':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию БОГ 🤍

🛒 | При покупке:
        1️⃣ | Бонус-кит БОГ
        2️⃣ | Префикс БОГ
        3️⃣ | 25.000.000$
        4️⃣ | 100 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс
        9️⃣ | Ограничение на время в играх становиться 2 секунды

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит БОГ
        2️⃣ | Префикс БОГ
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс
        5⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'владелец':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВЛАДЕЛЕЦ 🖤

🛒 | При покупке:
        1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
        2️⃣ | Префикс ВЛАДЕЛЕЦ
        3️⃣ | 10.000.000$
        4️⃣ | 74 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс
        8️⃣ | Способность менять игрокам префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
        2️⃣ | Префикс ВЛАДЕЛЕЦ
        3⃣ | Способность менять себе префикс
        4⃣ | Способность менять игрокам префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'основатель':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ОСНОВАТЕЛЬ 💜

🛒 | При покупке:
        1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
        2️⃣ | Префикс ОСНОВАТЕЛЬ
        3️⃣ | 4.000.000$
        4️⃣ | 54 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Donate-case 1 шт.
        7️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
        2️⃣ | Префикс ОСНОВАТЕЛЬ
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'спонсор':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию СПОНСОР 💙

🛒 | При покупке:
        1️⃣ | Бонус-кит СПОНСОР
        2️⃣ | Префикс СПОНСОР
        3️⃣ | 3.000.000$
        4️⃣ | 25 Рейтинга
        5️⃣ | Money-case 5 шт.
        6️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит СПОНСОР
        2️⃣ | Префикс СПОНСОР
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"   
       """, parse_mode='html') 


    if message.text.lower() == 'хелпер':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ХЕЛПЕР 💚

🛒 | При покупке:
        1️⃣ | Бонус-кит ХЕЛПЕР
        2️⃣ | Префикс ХЕЛПЕР
        3️⃣ | 750.000$
        4️⃣ | 20 Рейтинга
        5️⃣ | Money-case 3 шт.
        6️⃣ | Способность менять себе префикс

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ХЕЛПЕР
        2️⃣ | Префикс ХЕЛПЕР
        3⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"   
       """, parse_mode='html') 


    if message.text.lower() == 'платина':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ПЛАТИНА 💛

🛒 | При покупке:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА
        3️⃣ | 550.000$
        4️⃣ | 10 Рейтинга
        5️⃣ | Money-case 1 шт.

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"     
       """, parse_mode='html') 


    if message.text.lower() == 'премиум':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ПРЕМИУМ 🧡

🛒 | При покупке:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ
        3️⃣ | 300.000$

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"     
       """, parse_mode='html') 
    
    if message.text.lower() == 'вип':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВИП ❤️

🛒 | При покупке:
        1️⃣ | Бонус-кит ВИП
        2️⃣ | Префикс ВИП
        3️⃣ | 250.000$

🎁 | При использовании Donate-Case:
       1️⃣ | Бонус-кит ВИП
       2️⃣ | Префикс ВИП

🛒 Чтобы купить привилегию , ввойдите в Donate-menu с помощю команды \"Донат\"       
       """, parse_mode='html')  





###################################### КИТ-БОНУСЫ ##################################################
    if message.text.lower() == 'получить кит-бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       user_status = cursor.execute('SELECT user_status from users where user_id = ?', (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       balance = cursor.execute('SELECT balance from users where user_id = ?', (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rating = cursor.execute('SELECT rating from users where user_id = ?', (message.from_user.id,)).fetchone()
       rating = int(rating[0])

       ethereum = cursor.execute('SELECT ethereum from users where user_id = ?', (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       metall = cursor.execute('SELECT metall from mine where user_id = ?', (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute('SELECT silver from mine where user_id = ?', (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute('SELECT bronza from mine where user_id = ?', (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute('SELECT gold from mine where user_id = ?', (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       period = 43200 #43200 s = 12h
       get = cursor.execute("SELECT time_kit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно получили свой кит-бонус", parse_mode='html')
          time.sleep(0.5)
          if user_status == 'Player':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⛓ 99 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 5 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 5} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET metall = {metall + 99} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vip':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 5,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 57 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 200🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 57} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 200} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Premium':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 101 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 25 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 250🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 25} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 101} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 250} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Platina':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 15,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 125 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 300🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 15000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 125} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 300} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Helper':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 25,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 100 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 500🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 25000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Sponsor':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 150,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 150000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Osnovatel':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 400,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 400000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vladelec':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 700,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 700000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Bog':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return

          if user_status == 'Vlaselin':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, администрация бота не может получать кит-бонус", parse_mode='html') 
             return   
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать кит-бонус можно раз в 12ч", parse_mode='html')


    if message.text.lower() == 'получить кит бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       user_status = cursor.execute('SELECT user_status from users where user_id = ?', (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       balance = cursor.execute('SELECT balance from users where user_id = ?', (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rating = cursor.execute('SELECT rating from users where user_id = ?', (message.from_user.id,)).fetchone()
       rating = int(rating[0])

       ethereum = cursor.execute('SELECT ethereum from users where user_id = ?', (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       metall = cursor.execute('SELECT metall from mine where user_id = ?', (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute('SELECT silver from mine where user_id = ?', (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute('SELECT bronza from mine where user_id = ?', (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute('SELECT gold from mine where user_id = ?', (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       period = 43200 #43200 s = 12h
       get = cursor.execute("SELECT time_kit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно получили свой кит-бонус", parse_mode='html')
          time.sleep(0.5)
          if user_status == 'Player':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⛓ 99 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 5 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 5} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET metall = {metall + 99} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vip':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 5,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 57 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 200🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 57} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 200} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Premium':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 101 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 25 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 250🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 25} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 101} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 250} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Platina':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 15,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 125 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 300🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 15000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 125} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 300} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Helper':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 25,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 100 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 500🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 25000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Sponsor':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 150,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 150000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Osnovatel':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 400,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 400000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vladelec':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 700,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 700000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Bog':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return

          if user_status == 'Vlaselin':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, администрация бота не может получать кит-бонус", parse_mode='html') 
             return   
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать кит-бонус можно раз в 12ч", parse_mode='html')


    if message.text.lower() in ['кит-бонусы', 'кит бонусы', 'кит бонус', 'кит-бонус']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные о кит-бонусах 🎁

🎀 | Игрок:
      💰 | 1,000,000,000,000$
      ⛓ | 99 шт.
      💎 | 5 шт.
      🟣 | 100🟪

❤️ | Вип:
      💰 | 5,000,000,000,000$
      🪙 | 57 шт.
      💎 | 15 шт.
      🟣 | 200🟪

🧡 | Премиум:
      💰 | 10,000,000,000,000$
      🪙 | 101 шт.
      💎 |  25 шт.
      🟣 | 250🟪

💛 | Платина:
      💰 | 15,000,000,000,000$
      🪙 | 125 шт.
      💎 |  50 шт.
      🟣 | 300🟪

💚 | Хелпер:
      💰 | 25,000,000,000,000$
      🎇 | 50 шт.
      💎 |  100 шт.
      🟣 | 500🟪

💙 | Спонсор:
      💰 | 150,000,000,000,000$
      🎇 | 150 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

💜 | Основатель:
      💰 | 400,000,000,000,000$
      ⚜️ | 15 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🖤 | ВЛАДЕЛЕЦ:
      💰 | 700,000,000,000,000$
      ⚜️ | 50 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🤍 | БОГ:
      💰 | 10.000,000,000,000,000$
      ⚜️ | 150 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🤎 | ВЛАСТЕЛИН:
      💰 | 100.000,000,000,000,000$
      ⚜️ | 500 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

ℹ️ Чтобы получить кит-бонус введите команду \"Получить кит-бонус\" 
ℹ️ Кит-бонус получить можно раз в 12ч      
       """, parse_mode='html')

####################################### ТОП Мажоров#######################################

    if message.text.lower() in ['топ багочей', 'топ мажоров', 'топ б']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       from utils import scor_summ
       
       list = cursor.execute(f"SELECT * FROM users ORDER BY balance DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:
          balance3 = await scor_summ(user[4])            
          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>💰ТОП 1💰</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''
          
          if user[3] == 'Owner':
             stats = ' ✅<b>РАЗРАБОТЧИК</b>✅ |'
          if user[3] == 'Admin':
             stats = ' ⛔️<b>АДМИН</b>⛔️ |'
          if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
          if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''

          top_list.append(f"{num2} {user[1]} |{stats}{num3} 🔎 ID: <code>{user[0]}</code> | ${balance3} ")

       top = "\n".join(top_list)
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 богачей в боте:\n" + top, reply_markup=fulltop, parse_mode='html')

############################## СИСТЕМА СООБЩЕНИЙ ####################################

    if message.text.lower() in ['система с', "система сообщений", "с сообщений", "с сообщение", "сс", "с с"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за систему сообщений 💬

ℹ️ | Пример команды: /m [ID] [сообщение]

⚠️ | Система сообщений была разработана для связи с игроками, у которых SMS SPAM BAN TELEGRAM        
       """, parse_mode='html')





##############################СИСТЕМА "e" ########################################

    if message.text.lower() in ['система е', 'е', 'e']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за систему "e" ⚙️

🔩 | Информация:
<code>1e3</code> - 1.000$ - тыщ.
<code>1e6</code> - 1.000.000$ - млн.
<code>1e9</code> - 1.000.000.000$ - млрд.
<code>1e12</code> - 1.000.000.000.000$ - трлн.
<code>1e15</code> - 1.000.000.000.000.000$ - кврд.
<code>1e18</code> - 1.000.000.000.000.000.000$ - квнт.
<code>1e21</code> - 1.000.000.000.000.000.000.000$ - скст.
<code>1e24</code> - 1.000.000.000.000.000.000.000.000$ трикс.
<code>1e27</code> - 1.000.000.000.000.000.000.000.000.000$ твинкс.
<code>1e30</code> - 1.000.000.000.000.000.000.000.000.000.000$ септ.
<code>1e33</code> - 1.000.000.000.000.000.000.000.000.000.000.000$ октл.
<code>1e36</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000$ нонл.
<code>1e39</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000$ декал.
<code>1e42</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ эндк.
<code>1e45</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ доктл.
<code>1e48</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гугл.
<code>1e51</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ кинд.
<code>1e54</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ трипт.
<code>1e57</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ срист.
<code>1e60</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ манит.
<code>1e63</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гвинт.
<code>1е66</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ ланит.
<code>1е69</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ октит.
<code>1е72</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ новит.
<code>1е75</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ унд.
<code>1е78</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ конт.
<code>1е81</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ тент.
<code>1е84</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ фенд.

ℹ️ | <b>ПРИМЕР:</b> <i>казино 1е3</i>
    """, parse_mode='html')




##############################СИСТЕМА "К" ########################################

    if message.text.lower() in ['система к', 'к']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за систему "К" ⚙️

🔩 | Информация:
<code>1к</code> - 1.000$ - тыщ.
<code>1кк</code> - 1.000.000$ - млн.
<code>1ккк</code> - 1.000.000.000$ - млрд.
<code>1кккк</code> - 1.000.000.000.000$ - трлн.
<code>1ккккк</code> - 1.000.000.000.000.000$ - кврд.
<code>1кккккк</code> - 1.000.000.000.000.000.000$ - квнт.
<code>1ккккккк</code> - 1.000.000.000.000.000.000.000$ - скст.
<code>1кккккккк</code> - 1.000.000.000.000.000.000.000.000$ трикс.
<code>1ккккккккк</code> - 1.000.000.000.000.000.000.000.000.000$ твинкс.
<code>1кккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000$ септ.
<code>1ккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000$ октл.
<code>1кккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000$ нонл.
<code>1ккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000$ декал.
<code>1кккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ эндк.
<code>1ккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ доктл.
<code>1кккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гугл.
<code>1ккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ кинд.
<code>1кккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ трипт.
<code>1ккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ срист.
<code>1кккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ манит.
<code>1ккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гвинт.
<code>1кккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ ланит.
<code>1ккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ октит.
<code>1кккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ новит.
<code>1ккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ унд.
<code>1кккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ конт.
<code>1ккккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ тент.
<code>1кккккккккккккккккккккккккккк</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ фенд.

ℹ️ | <b>ПРИМЕР:</b> <i>казино 1к</i>
    """, parse_mode='html')




###################################### аватарки #######################################
    if message.text.lower() in ['убрать аву', "убрать аватарку", "удалить аву", "удалить аватарку"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0]) 

       await bot.send_message(message.chat.id, f"🪣 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно удалили свою аватарку", parse_mode='html')
       cursor.execute(f'UPDATE avatarka SET avatarka = "none" WHERE user_id = {user_id}')
       connect.commit()


    if message.text.lower() in ['ава', 'аватарки', "аватарка", "фото"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       strach_photo = open('страж.jpg', 'rb')

       cheat_photo = open('cheat.jpg', 'rb')

       apper_photo = open('apper.jpg', 'rb')

       dyp_photo = open('дюп.jpg', 'rb')

       girl_photo = open('girl.jpg', 'rb')

       admin_photo = open('админ.jpg', 'rb')

       ava_strach = InlineKeyboardMarkup(row_width=1)
       ava_strach2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_strach')
       ava_strach.add(ava_strach2)

       ava_cheat = InlineKeyboardMarkup(row_width=1)
       ava_cheat2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_cheat')
       ava_cheat.add(ava_cheat2)

       ava_apper = InlineKeyboardMarkup(row_width=1)
       ava_apper2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_apper')
       ava_apper.add(ava_apper2)

       ava_dyp = InlineKeyboardMarkup(row_width=1)
       ava_dyp2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_dyp')
       ava_dyp.add(ava_dyp2)

       ava_girl = InlineKeyboardMarkup(row_width=1)
       ava_girl2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_girl')
       ava_girl.add(ava_girl2)

       ava_admin = InlineKeyboardMarkup(row_width=1)
       ava_admin2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_admin')
       ava_admin.add(ava_admin2)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, добро пожаловать в меню аватарок 🗾

ℹ️ | Всего аватарок: 4

ℹ️ | Доступные аватарки: ДЮППЕР, СТРАЖ, АППЕР, ЧИТЕР, ДЕВУШКА

⛔️ | Админ: АДМИН

ℹ️ | Аватарка ставиться на баланс

↘️ | Виберите одну аватарок ниже 
       """, parse_mode='html')
       await bot.send_photo(message.chat.id, strach_photo, '', reply_markup=ava_strach)
       await bot.send_photo(message.chat.id, cheat_photo, '', reply_markup=ava_cheat)
       await bot.send_photo(message.chat.id, apper_photo, '', reply_markup=ava_apper)
       await bot.send_photo(message.chat.id, dyp_photo, '', reply_markup=ava_dyp)
       await bot.send_photo(message.chat.id, girl_photo, '', reply_markup=ava_girl)
       await bot.send_photo(message.chat.id, admin_photo, '', reply_markup=ava_admin)




###################################### РЕПУТАЦИЯ + ###################################

    if message.text.lower() in ['+', '++', '+++', 'кросс', "молодец", "имба"]:
       user_id = message.from_user.id

       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = user_name[0]

       reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reput = int(reput[0])

       if reply_user_id == user_id:
          await bot.send_message(message.chat.id, f"📝 Жулик, не голосуй", parse_mode='html')
          return

       await bot.send_message(message.chat.id, f"📊 | Вы успешно повысили репутацию  <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> . Теперь его репутация: {reput + 1}", parse_mode='html')
       cursor.execute(f'UPDATE reput SET reput = {reput + 1} WHERE user_id = {reply_user_id}')
       connect.commit()


###################################### РП КОМАНДЫ ####################################

    if message.text.lower() in ["рп-команды", "РП-команды"]:
       user_name = message.from_user.get_mention(as_html=True)
       await bot.send_message(message.chat.id, f"{user_name}, список РП-команд:\n🤗 | Обнять\n👏 | Похлопать\n👨‍💻 | Заскамить\n☕️ | Пригласить на чай\n👉👌 | Изнасиловать\n🤝 | Взять за руку\n📱 | Подарить айфон\n✋ | Дать пять\n😬 | Укусить\n🤛 | Ударить\n🤲 | Прижать\n💋 | Чмок\n💋 | Поцеловать\n😼 | Кусь\n🤲 | Прижать\n🔪 | Убить\n🤜 | Уебать\n💰 | Украсть\n🔞 | Выебать\n👅 | Отсосать\n👅 | Отлизать\n🔞 | Трахнуть\n🔥 | Сжечь", parse_mode='html')

    if message.text.lower() in ["чмок", "Чмок"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💋 | {user_name} чмокнул(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["кусь", "Кусь"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"😼 | {user_name} кусьнул(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["обнять", "Обнять"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤗 | {user_name} обнял(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["поцеловать", "Поцеловать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💋 | {user_name} поцеловал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["дать пять", "Дать пять"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"✋ | {user_name} дал(-а) пять {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["подарить айфон", "Подарить айфон"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"📱 | {user_name} подарил(-а) айфон {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["ударить", "Ударить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤛 | {user_name} ударил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["заскамить", "Заскамить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👨‍💻 | {user_name} заскамил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["прижать", "Прижать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤲 | {user_name} прижал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["укусить", "Укусить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"😬 | {user_name} укусил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["взять за руку", "Взять за руку"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤝 | {user_name} взял(-а) за руку {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["прижать", "Прижать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤲 | {user_name} прижал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["похлопать", "Похлопать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👏 | {user_name} похлопал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["изнасиловать", "Изнасиловать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👉👌 | {user_name} изнасиловал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["пригласить на чай", "Пригласить на чай"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"☕️ | {user_name} пригласил(-а) на чай {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["убить", "Убить"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔪 | {user_name} убил(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["уебать", "Уебать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤜 | {user_name} уебал(-а) {reply_user_name}", parse_mode='html')
    if message.text.lower() in ["украсть", "Украсть"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💰 | {user_name} украл(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["отсосать", "Отсосать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👅 | {user_name} отсосал(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["отлизать", "Отлизать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👅 | {user_name} отлизал(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["выебать", "Выебать"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔞 | {user_name} выебал(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["сжечь", "Сжечь"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔥 | {user_name} сжёг {reply_user_name}", parse_mode='html')

    if message.text.lower() in ["трахнуть", "Трахнуть"]:
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔞 | {user_name} трахнул(-а) {reply_user_name}", parse_mode='html')
########################################PROMO#########################################
    if message.text.lower() in ['очистить промокоды', 'reset promo']:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()

         if user_status == 'Owner':
            cursor.execute(f'DELETE from promo')
            cursor.execute(f'DELETE from promo_active')
            connect.commit()
            all_dell_promo = 0

            for delete_promo in all_promo:
               all_dell_promo += 1
               await message.answer(f'➖ промокод <code>{delete_promo[0]}</code> был <b>удалён</b>', parse_mode='html')

            await message.reply(f"✅ Всё промокоды были удалены\n🔢 Количество удаленных промокодов: {'{:,}'.format(all_dell_promo).replace(',','.')}")

            
         else:
            return await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER<b>', parse_mode='html')





    if message.text.startswith('промо') or message.text.startswith('Промо') or message.text.startswith('Промокод') or message.text.startswith('промокод'):
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
         balance = int(balance[0])

         donate_coins = cursor.execute(f'SELECT donate_coins from users where user_id = {user_id}').fetchone()
         donate_coins = int(donate_coins[0])

         money = cursor.execute(f'SELECT money from money_balance where user_id = {user_id}').fetchone()
         money = int(money[0])  
         
         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for item in all_promo:
            all_promo2.append(item[0])



         promo = str(message.text.split()[1])

         if str(promo) in str(all_promo2):
            
            proverka = cursor.execute(f'SELECT active from promo_active where user_id = {user_id} and promo = "{promo}"').fetchone()

            if proverka != None:
               return await message.reply(f'❗️ <b>Вы использовали промокод</b> <code>{promo}</code>', parse_mode='html')
            else:
               pass

            name_promo = cursor.execute(f'SELECT promo from promo where promo = "{promo}"').fetchone()
            name_promo = name_promo[0]

            status_promo = cursor.execute(f'SELECT status from promo where promo = "{promo}"').fetchone()
            status_promo = status_promo[0]

            owner_promo = cursor.execute(f'SELECT owner from promo where promo = "{promo}"').fetchone()
            owner_promo = owner_promo[0]

            priz_promo = cursor.execute(f'SELECT priz from promo where promo = "{promo}"').fetchone()
            priz_promo = int(priz_promo[0])
   
            active_promo = cursor.execute(f'SELECT active from promo where promo = "{promo}"').fetchone()
            active_promo = int(active_promo[0])

            ob_active_promo = cursor.execute(f'SELECT ob_active from promo where promo = "{promo}"').fetchone()
            ob_active_promo = int(ob_active_promo[0])

            if ob_active_promo == active_promo:
               return await message.reply(f'❗️ Промокод больше <b>не действительный</b>', parse_mode='html')
            else:
               pass
            

            if status_promo == 'Money':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2}$'
               new_balance = balance + priz_promo
               new_balance2 = '{:,}'.format(int(new_balance)).replace(',','.')
               update_profile = f'💸 <b>Теперь ваш текущий баланс:</b>  <code>{new_balance2}$</code>'
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE users SET balance = {int(new_balance)} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))
            elif status_promo == 'donate_coins':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2} Donate-Coins'
               update_profile = ''
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + priz_promo} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))
            elif status_promo == 'money':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2} money'
               update_profile = ''
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE money_balance SET money = {money + priz_promo} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))            
            else:
               return await message.reply(f'<b>Error: No status promo in [Money, Donate-Coins, Donate-Case, Money-Case, money]</b>', parse_mode='html')
            
            
            text = f'''
✅ <b>Вы успешно использовали промокод <code>{promo}</code> и получили  <code>{priz}</code></b>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💼 <b>Создатель промокода:</b>  <code>{owner_promo}</code>
{update_profile}
            '''

            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Нету такого промокода')


    if message.text.startswith('+админ промо'):
      try:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         if user_status != 'Owner':
            return await message.reply(f'❗️ Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')
         else:
            pass

         new_promo = message.text.split()[2]

         status_promo = int(message.text.split()[3])

         summ_promo = int(message.text.split()[4])

         active_promo = int(message.text.split()[5])

         opis = message.text.split()[6:]

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for all_promo3 in all_promo:
            all_promo2.append(all_promo3[0])

         if new_promo in all_promo2:
            return await message.reply(f'❗️ <b>Данный промокод <code>{new_promo}</code> уже существует</b>', parse_mode='html')
         else:
            pass


         if status_promo == 1:
            status = 'donate_coins'
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, summ_promo, active_promo, 0))
            text = f'''
🖊 <b>Промокод:</b> <code>{new_promo}</code>
🪙 <b>Содержит: Donate-Coins</b>
💼 <b>Создатель:</b> <code>{user_name}</code>

👥 <b>Количество использований:</b> <code>{active_promo} раз(а)</code>
👤<b> На одного человека:</b> <code>{summ_promo} Donate-Coins 🪙</code>
            '''
         if status_promo == 2:
            status = 'money'
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, summ_promo, active_promo, 0))
            text = f'''
🖊 <b>Промокод:</b> <code>{new_promo}</code>
🪙 <b>Содержит: Рублёвый донат</b>
💼 <b>Создатель:</b> <code>{user_name}</code>

👥 <b>Количество использований:</b> <code>{active_promo} раз(а)</code>
👤<b> На одного человека:</b> <code>{summ_promo} Donate-Money 🪙</code>
            '''

         else:
            text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+админ промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - Donate-Coins
      2 - Money
      3 - Money-Case
         '''            
            return await message.reply(text, parse_mode='html')

         await message.reply(text, parse_mode='html')

      except IndexError:
         text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+админ промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - Donate-Coins
      2 - Donate-Case
      3 - Money-Case
         '''
         await message.reply(text, parse_mode='html')


      except ValueError:
         text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+админ промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека] [количество активаций] </i>

❕ Номера статусов:
      1 - Donate-Coins
      2 - Donate-Case
      3 - Money-Case
         '''
         await message.reply(text, parse_mode='html')




    if message.text.startswith('+промо') or message.text.startswith('+Промо') or message.text.startswith('+Промокод') or message.text.startswith('+промокод'):
      try:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
         balance = int(balance[0])
      
         user_status = cursor.execute(f'SELECT user_status from users where user_id = {user_id}').fetchone()
         user_status = user_status[0]

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for all_promo3 in all_promo:
            all_promo2.append(all_promo3[0])
         new_promo = str(message.text.split()[1])

         su1 = message.text.split()[2]
         su2 = (su1).replace('.', '').replace(',', '').replace('е',' e').replace("к", 'k').replace('k', '000').replace('все', 'всё')
         su3 = float(su2)
         summ = int(su3)

         su1_2 = message.text.split()[3]
         su2_2 = (su1_2).replace('.', '').replace(',', '').replace('е',' e').replace("к", 'k').replace('k', '000')
         su3_2 = float(su2_2)
         active_users = int(su3_2)

         opis = message.text.split()[4:]

         all_users = cursor.execute(f'SELECT * from users').fetchall()
         all_users = len(all_users)

         if summ < 100:
            return await message.reply(f'❗️ Cумма должна быть не меньше <code>100$</code>', parse_mode='html')
         else:
            pass

         if active_users > all_users:
            return await message.reply(f'❗️ Вы не можете создать промокод больше чем на <b>{all_users} использований</b>', parse_mode='html')
         else:
            pass
         
         if len(new_promo) < 3:
            return await message.reply(f'❗️ Промокод должен быть <b>больше 3 символов</b>', parse_mode='html')
         else:
            pass

         if new_promo in all_promo2:
            return await message.reply(f'❗️ <b>Данный промокод <code>{new_promo}</code> уже существует</b>', parse_mode='html')
         else:
            pass
         
         if summ > balance:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass

         if summ <= 0:
            return await message.reply(f'❗️ Сумма не должна быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass
         
         user_summ = summ / active_users
         user_summ2 = int(user_summ)

         text_opis = ' '.join(opis)

         if text_opis == '':
            opis2 = ''
         else:
            text_opis = ' '.join(opis)
            opis2 = f'\n<b>💭 Описание:</b> <code>{text_opis}</code>'

         text = f'''
<b>🖊 Промокод:</b> <code>{new_promo}</code>
<b>🏛 Содержит:</b> <code>{'{:,}'.format(summ).replace(',', '.')}$</code>
<b>💼 Создатель:</b> <code>{user_name}</code>{opis2}

<b>👥 Количество использований:</b> <code>{active_users} раз(a)</code>
<b>👤 На одного человека:</b> <code>{'{:,}'.format(user_summ2).replace(',', '.')}$</code>
         '''

         if user_status in ['Admin', 'Helper_Admin']:
            await message.reply('❗️ Администрации запрещено создавать промокоды')

            await message.bot.send_message(config.admin_chat_id, f'⛔️ Администратор <b>{user_name}</b> (<code>{user_id}</code>) только что попытался создать промокод.', parse_mode='html')
            return await message.bot.send_message(config.admin_chat_id, text, parse_mode='html')
         else:
            pass

            
         status = 'Money'
         try:
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, user_summ2, active_users, 0))
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()
            await message.reply(text, parse_mode='html')
         except OverflowError:
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, 0, active_users, 0))
            cursor.execute(f'UPDATE promo SET priz = {user_summ2} WHERE promo = "{new_promo}"')
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()
            await message.reply(text, parse_mode='html')
      except IndexError:
         text = f'''
❗️ Неправильно введены <b>аргументы!</b>
❕ <code>+промо </code> <b>[название] [сумма] [количество использований]</b>
         '''
         await message.reply(text, parse_mode='html')

      except ValueError:
         text = f'''
❗️ Неправильно введены <b>аргументы!</b>
❕ <code>+промо </code> <b>[название] [сумма] [количество использований]</b>
         '''
         await message.reply(text, parse_mode='html')
















########################################        Смена префикса          ######################################
    if message.text.startswith('Поменять префикс') or message.text.startswith('поменять префикс') or message.text.startswith('Сменить префикс') or message.text.startswith('сменить префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          if user_status in ['Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
             await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили свой префикс на {prefix}")
             cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ХЕЛПЕР\"", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return


    if message.text.startswith('+игроку префикс') or message.text.startswith('+игроку префикс'):
       user_id = message.from_user.id


       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)


       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          period = 900
          get = cursor.execute("SELECT stavka FROM time_prefix WHERE user_id = ?", (message.from_user.id,)).fetchone()
          last_stavka = f"{int(get[0])}"
          stavkatime = time.time() - float(last_stavka)
          if user_status == 'Owner':
             period = 0
          if stavkatime > period:
             if user_status in ['Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
                await bot.send_message(message.chat.id, f"🔒 | Вы сменили игроку {reply_user_name} префикс на {prefix}", parse_mode='html')
                cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {reply_user_id}')
                cursor.execute(f'UPDATE time_prefix SET stavka = "{time.time()}" WHERE user_id = {reply_user_id}')
                connect.commit()
                return
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ВЛАДЕЛЕЦ\"", parse_mode='html')
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять игроку ник можно раз в 15 минут", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return
    
    








#####################################################      КЕЙСЫ             ####################################################
    if message.text.lower() in ["открыть кейсы", "открыть кейс"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])

       ob_member = 0

       if money_case > 0:
          ob_member += 1
       else:
          pass

       if donate_case > 0:
          ob_member += 1
       else:
          pass

       if ob_member < 1:
          await bot.send_message(message.chat.id, f"""
🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету не каких кейсов 
          """,parse_mode='html')
          return
       
       case_shop1 = InlineKeyboardMarkup(row_width=2)
       money_case1 = InlineKeyboardButton(text='Открыть Money-Case 💸', callback_data='up_money_case')
       donate_case2 = InlineKeyboardButton(text='Открыть Donate-Case 🧧', callback_data='up_donate_case')
       case_shop1.add(money_case1, donate_case2)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваши кейсы 🎁

💸 | Money-Case - {money_case} шт.
🧧 | Donate-Case - {donate_case} шт.

↘️ Виберите один из кейсов, который хотите открыть 
       """,reply_markup=case_shop1, parse_mode='html')

    if message.text.lower() == 'кейсы':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])
      
       ob_members = 0

       if donate_case > 0:
          ob_members += 1
          donate_case2 = f'      🧧 | Donate-Case - {donate_case} шт.\n'
       else:
          donate_case2 = ''

       if money_case > 0:
          ob_members += 1
          money_case2 = f'      💸 | Money-Case - {money_case} шт.\n'
       else:
          money_case2 = ''

       if ob_members > 0:
          casee = '🎁 | Ваши кейсы:\n'
       else:
          casee = '😟 | У вас нету кейсов...'

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за кейсы 🎁

💸 | Money-Case - 50 Donate-Coins 🪙
🧧 | Donate-Case - 100 Donate-Coins 🪙

{casee}{donate_case2}{money_case2}

🖲 | Чтобы открыть один из кейсов, напишите команду \"Открыть кейсы\"
       """, parse_mode='html')





#################################################### !канал ################################
    if message.text.lower() in ['канал', "!канал", "channel"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       channel_pov = cursor.execute("SELECT members from channel_pov where user_id = ?", (message.from_user.id,)).fetchone()
       channel_pov = int(channel_pov[0])

       if channel_pov > 0:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже получили деньги за подписку",parse_mode='html')
          return
       
       sub_pov = InlineKeyboardMarkup(row_width=1)
       channel_push = InlineKeyboardButton(text='КАНАЛ 🔈', url='https://t.me/csia_channel')
       channel_poverk = InlineKeyboardButton(text='ПРОВЕРИТЬ ✅', callback_data='channel_poverk')
       sub_pov.add(channel_push, channel_poverk)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот условия задание 💠

🔈 | Подписаться на канал

💰 | Приз: 500.000.000.000.000.000$

↘️ Виберите одну кнопку ниже...       
       """, reply_markup=sub_pov, parse_mode='html')
       user_channel_status = await bot.get_chat_member(chat_id="@csia_channel", user_id=message.from_user.id)
       if user_channel_status['status'] != 'left':
          print('GOOD')
       else:
          print('Luser')

    



############################### ВДЗУ - ВЫДАЧА ДЕНЕГ ЗА УЧАСТНИКОВ ################################################
    if message.text.startswith('вдзу статус') or message.text.startswith('Вдзу статус'):

         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         status = str(message.text.split()[2])

         if user_id == config.owner_id:
            if status == 'off':
               cursor.execute(f'UPDATE wdzy SET status = "off"')
               connect.commit()
               text = f'❌  Вы <b>отключили</b> раздачу в чате {config.chat}'
            elif status == 'on':
               cursor.execute(f'UPDATE wdzy SET status = "on"')
               connect.commit()
               text = f'✅ Вы <b>включили</b> выдачу в чате {config.chat}'
            else:
               text = f'❗️ Не распознано «<b>{status}</b>» | Пример: <code>вдзу статус</code> <i>[off/on]</i>'

            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')

    if message.text.startswith('вдзу цена') or message.text.startswith('Вдзу цена'):

         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         su = message.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)

         if user_id == config.owner_id:
            cursor.execute(f'UPDATE wdzy SET summ = {summ}')
            connect.commit()

            text = f'''
♻️ <b>Обновлена</b> сумма за 1 участника - <code>{'{:,}'.format(summ).replace(',','.')}$</code>
            '''
            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')






    if message.text.lower() == 'вдзу':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       if user_id == config.owner_id:
         summ = cursor.execute(f'SELECT summ from wdzy').fetchone()
         summ = int(summ[0])

         status = cursor.execute(f'SELECT status from wdzy').fetchone()
         status = status[0]

         if status == 'off':
            status2 = 'Выдача отключена ❌'
         else:
            status2 = 'Выдача включена ✅'

         text = f'''
👤 ВДЗУ [ WDZY ] - ВЫДАЧА ДЕНЕГ ЗА УЧАСТНИКОВ 

💭 Чат - {config.chat}
💸 Сумма за 1 участника - {'{:,}'.format(summ).replace(',','.')}$
👉 Статус выдачи - {status2}

❗️ <code>вдзу цена</code> <i>[сумма]</i> <b>- Устоновка суммы за 1 участника в чате</b>
❗️ <code>вдзу статус</code> <i>[off\on]</i><b> - Устоновка статуса выдачи </b>
         '''
         await message.reply(text, parse_mode='html')
       else:
         return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')








########################################### СЕМЬЯ СЕМЬИ ####################################
    

    if message.text.lower() == 'пригласить в семью':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if reply_user_id == user_id:
         return await message.reply(f'❗️ Вы не можете пригласить <b>самого себя</b> в семью.', parse_mode='html')
      else:
         pass
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass
      
      if rank_family < 2:
         return await message.reply(f'❗️ Приглашать игроков в семью можно от <b>2 ранга</b>', parse_Mode='html')
      else:
         pass

      user1 = message.reply_to_message.from_user.id
      user2 = reply_user_name
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="✅ Принять приглашение", callback_data=f"accept_{user1}:{user2}:{name_family}"))

      text = f'''
👶 <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, вас приглашают в семью «<b>{name_family}</b>»
      '''

      await message.answer(text, reply_markup=keyboard, parse_mode='html')

    if message.text.startswith('cоздать семью') or message.text.startswith('Создать семью'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
       all_family2 = []
       
       for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])
      
       if user_id in all_family2:
         return await message.reply(f'❗️У вас есть <b>своя семья.</b> Зачем вам ещё одна? | <code>Распустить семью</code> - удаление семьи ', parse_mode='html')
       else:
         pass

       user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

       if user_id_family != None:
         return await message.reply('❗️ Вы уже <b>состоите в семье</b> | напишите «<code>выйти с семьи</code>» - для выхода с вашей семьи',parse_mode='html')
       else:
         pass

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       if donate_coins < config.cash_family:
         return await message.reply(f'❗️ <b>Недостаточно Donate-Coins</b> | Стоимость: <b>{config.cash_family} Donate-Coins</b> 🪙')
       else:
         pass
       
       name_family = message.text.split()[2:]
       name_family2 = ' '.join(name_family)
       full_name_family = (name_family2).replace(' ','').replace('🇷🇺', '').replace('Россия', 'россия').replace('россия', '')

       if len(full_name_family) < 4:
         return await message.reply('❗️ Название семьи должна быть больше <b>4 символов</b>', parse_Mode='html')
       elif len(full_name_family) > 35:
         return await message.reply(f'❗️ Название семьи должна быть меньше <b>35 символов</b>', parse_mode='html')
       else:
         pass

       all_family_name = cursor.execute('SELECT name from family').fetchall()
       all_family_name2 = []

       for all_family_name3 in all_family_name:
         all_family_name2.append(all_family_name3[0])
      
       if full_name_family in all_family_name2:
         return await message.reply(f'❗️ Семья с названием «<b>{full_name_family}</b>» уже существует', parse_mode='html')
       else:
         pass
       
       family_id = cursor.execute('SELECT id from family_id').fetchone()
       family_id = int(family_id[0])
       new_family_id = family_id + 1

       text = f'''
✅ Вы успешно создали семью «<b>{full_name_family}</b>»
       '''

       text2 = f'''
❕ Для просмотра своей семьи напишите <code>моя семья</code>
       '''
       time_family = time.time()
       opis = ''
       cursor.execute(f'UPDATE family_id SET id = {new_family_id}')
       cursor.execute("INSERT INTO family VALUES(?, ?, ?, ?, ?, ?, ?);",(full_name_family, user_id, user_name, new_family_id, 0, opis, time_family))
       connect.commit()
       await message.answer(text, parse_mode='html')
       await message.answer(text2, parse_mode='html')





    if message.text.lower() in ['моя семья', "семья"]:
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0
      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      owner_name = cursor.execute(f'SELECT owner_name from family where name = "{name_family}"').fetchone()
      owner_name = owner_name[0]

      rank3 = cursor.execute(f'SELECT user_name from user_family where rank = {3} and family = "{name_family}"').fetchall()
      all_rank3 = []

      for user_rank3 in rank3:
         all_rank3.append(user_rank3[0])

      full_all_rank3 = ' '.join(all_rank3)

      if full_all_rank3 == '':
         full_all_rank3 = 'Отсутствуют 😕'
      else:
         pass

      rank2 = cursor.execute(f'SELECT user_name from user_family where rank = {2} and family = "{name_family}"').fetchall()
      all_rank2 = []

      for user_rank2 in rank2:
         all_rank2.append(user_rank2[0])

      full_all_rank2 = ' '.join(all_rank2)

      if full_all_rank2 == '':
         full_all_rank2 = 'Отсутствуют 😕'
      else:
         pass
      
      id_family = cursor.execute(f'SELECT id from family where name = "{name_family}"').fetchone()
      id_family = int(id_family[0])

      sqlite_select_query2 = f"""SELECT * from user_family where family = \"{name_family}\""""
      cursor.execute(sqlite_select_query2)
      all_user_family = cursor.fetchall()

      balance_family = cursor.execute(f'SELECT balance from family where name = "{name_family}"').fetchone()
      balance_family = int(balance_family[0])

      opis_family = cursor.execute(f'SELECT opis from family where name = "{name_family}"').fetchone()
      opis_family = opis_family[0]
      
      if opis_family == '':
         opis_family = 'Пустое'
      else:
         pass

      text = f'''
Информация за семью «<b>{name_family}</b>» 👨‍👩‍👧‍👦
➖➖➖➖➖➖➖➖
🤵‍♂️ Основатель семьи: {owner_name}
👨‍💻 Заместитель (3 ранг): {full_all_rank3} 
🧑‍💼 Помощники (2 ранг): {full_all_rank2} 
➖➖➖➖➖➖➖➖
🔎 ID: <code>{id_family}</code>
👥 Игроков в семье: <b>{len(all_user_family)}</b>
💰 Мешок семьи: <code>{balance_family} с. монет</code>
💭 Описания семьи: <i>{opis_family}</i>
      '''
      await message.reply(text, parse_mode='html')






    if message.text.lower() == 'выйти с семьи':
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      
      if status_owner_family == 'on':
         return await message.reply(f'❗️ Вы <b>владелец семьи</b>, вы не можете покинуть свою семью | Пропишите <code>Распустить семью</code> для её удаление', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from user_family where family = "{name_family}"')

      text = f'''
😧 Вы покинули семью «<b>{name_family}</b>» 
      '''

      await message.reply(text, parse_mode='html')

    if message.text.lower() == 'распустить семью':
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if status_owner_family == 'off':
         return await message.reply(f'❗️ Распустить семью может только <b>её владелец</b>', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from family where name = "{name_family}"')
      cursor.execute(f'DELETE from user_family where family = "{name_family}"')

      text = f'''
🥲 Вы успешно распустили семью «<b>{name_family}</b>»
      '''

      await message.reply(text, parse_mode='html')
    if message.text.startswith('+описание семьи'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family5 = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family5 = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Менять описание семьи можно только с <b>3 ранга</b>', parse_mode='html')
      else:
         pass

      new_opis = message.text[16:]
      
      if len(new_opis) > 150:
         return await message.reply('❗️ Описание должно быть не больше <b>150 символов</b>', parse_mode='html')
      else:
         pass
      
      cursor.execute(f'UPDATE family SET opis = "{new_opis}" where name = "{name_family5}"')

      text = f'''
✅ Вы <b>успешно</b> поменяли описание семьи
      '''

      await message.reply(text, parse_mode='html')





    if message.text.lower() == 'выгнать из семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете выгнать сами себя | Воспользуйтесь командой <code>Выйти с семьи</code>', parse_mode='html')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Выганять участников можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в клане')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем клане')
      else:
         pass


      if reply_rank_family == 3:
         if status_owner_family == 'on':
            pass
         else:
            return await message.reply(f'❗️ Вы не можете выгнать человека с <b>3 рангом</b> | <i>Под силу только владельцу семьи</i>', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from user_family where user_id = {reply_user_id}')
      connect.commit()

      text = f'''
👀 Вы выгнали <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> с семьи «<b>{name_family}</b>»
      '''

      await message.reply(text, parse_mode='html')


    if message.text.lower() == '+ранг семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете повысить сам себе ранг')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Повышать ранг в семье можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в клане')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем клане')
      else:
         pass

      if reply_rank_family == 3:
         return await message.reply(f'❗️ У данного игрока максимальный ранг', parse_mode='html')
      else:
         pass
      

      cursor.execute(f'UPDATE user_family SET rank = {reply_rank_family + 1} WHERE user_id = {reply_user_id}')
      connect.commit()

      text = f'''
🔼 Вы повысили на 1 ранг игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
      '''
      await message.reply(text, parse_mode='html')







    if message.text.lower() == '-ранг семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете понизить сам себе ранг')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Понижать ранг в семье можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в клане')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем клане')
      else:
         pass

      if reply_rank_family == 3:
         if status_owner_family == 'on':
            pass
         else:
            return await message.reply(f'❗️ Вы не можете понизить человека с <b>3 рангом</b> | <i>Под силу только владельцу семьи</i>', parse_mode='html')
      else:
         pass
      
      if reply_rank_family == 1:
         return await message.reply(f'❗️ У данного игрока и так минимальный ранг.')
      else:
         pass

      cursor.execute(f'UPDATE user_family SET rank = {reply_rank_family - 1} WHERE user_id = {reply_user_id}')
      connect.commit()

      text = f'''
🔽 Вы понизили на 1 ранг игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
      '''
      await message.reply(text, parse_mode='html')








    if message.text.startswith('Купить монеты') or message.text.startswith('купить монеты'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.from_user.id,)).fetchone()
      reput = int(reput[0])

      su = msg.text.split()[2]
      su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
      su3 = float(su2)
      summ = int(su3)

      summ2 = '{:,}'.format(summ).replace(',', '.')
      
      if summ < 10:
         return await message.reply(f'❗️ Можно покупать только от <code>10</code> <b>семейных монет</b>', parse_mode='html')
      else:
         pass

      if summ > reput:
         return await message.reply(f'❗️ У вас недостаточно <b>репутации</b> | <i>1 с. монета = 1 репутация</i>', parse_mode='html')
      else:
         pass

      if summ <= 0:
         return await message.reply(f'❗️ Сумма не должна быть отрицательным число <b>[0 и меньше]</b>', parse_mode='html')
      else:
         pass
      
      balance_family = cursor.execute(f'SELECT balance from family where name = "{name_family}"').fetchone()
      balance_family = balance_family[0]

      cursor.execute(f'UPDATE family SET balance = {balance_family + summ} WHERE name = "{name_family}"')
      cursor.execute(f'UPDATE reput SET reput = {reput - summ} WHERE user_id = "{user_id}"')
      connect.commit()

      text = f'''
💰 Вы положили в семейный мешок <code>{summ2}</code> семейный монет
      '''

      await message.reply(text, parse_mode='html')









    if message.text.startswith('+название семьи'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family5 = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family5 = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Менять название семьи можно только с <b>3 ранга</b>', parse_mode='html')
      else:
         pass

      user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_status = user_status[0]

      if user_status in ['Helper_Admin', 'Owner']:
         period = 1
      else:
         period = 604800 #7d

      get = cursor.execute(f'SELECT time_name FROM family WHERE name = "{name_family5}"').fetchone()
      last_stavka = f"{int(get[0])}"
      stavkatime = time.time() - float(last_stavka)

      if stavkatime < period:
         times2 = time.localtime(float(get[0]))
         print(times2)

         if times2.tm_mday <= 9:
            tm_mday2 = 0
         else:
            tm_mday2 = ''
         
         if times2.tm_mon <= 9:
            tm_mon2 = 0
         else:
            tm_mon2 = ''

         if times2.tm_hour <= 9:
            tm_hour2 = 0
         else:
            tm_hour2 = ''

         if times2.tm_min <= 9:
            tm_min2 = 0
         else:
            tm_min2 = ''

         full_times2 = f'{tm_mday2}{times2.tm_mday}.{tm_mon2}{times2.tm_mon}.{times2.tm_year} в {tm_hour2}{times2.tm_hour}:{tm_min2}{times2.tm_min}'

         return await message.reply(f'❗️ Менять название семьи, можно раз в <b>7 дней</b> | Последнее изменение название было <code>{full_times2}</code>', parse_mode='html')
      else:
         pass

      name_family = message.text.split()[2:]
      name_family2 = ' '.join(name_family)
      full_name_family = (name_family2).replace(' ','').replace('🇷🇺', '').replace('Россия', 'россия').replace('россия', '')

      if len(full_name_family) < 4:
         return await message.reply('❗️ Название семьи должна быть больше <b>4 символов</b>', parse_Mode='html')
      elif len(full_name_family) > 35:
         return await message.reply(f'❗️ Название семьи должна быть меньше <b>35 символов</b>', parse_mode='html')
      else:
         pass

      all_family_name = cursor.execute('SELECT name from family').fetchall()
      all_family_name2 = []

      for all_family_name3 in all_family_name:
         all_family_name2.append(all_family_name3[0])
   
      if full_name_family in all_family_name2:
         return await message.reply(f'❗️ Семья с названием «<b>{full_name_family}</b>» уже существует', parse_mode='html')
      else:
         pass

      cursor.execute(f'UPDATE family SET name = "{full_name_family}" where name = "{name_family5}"')

      sqlite_select_query27 = f"""SELECT * from user_family where family = \"{name_family5}\""""
      cursor.execute(sqlite_select_query27)
      full_user_id_family_update = cursor.fetchall()

      for update_name_family_user_id in full_user_id_family_update:
         print(update_name_family_user_id[1])
         cursor.execute(f'UPDATE user_family SET family = "{full_name_family}" where user_id = "{update_name_family_user_id[1]}"')
      connect.commit()

      text = f'''
✅ Вы успешно изменили название семьи с <b>{name_family5}</b> на <b>{full_name_family}</b>
      '''

      await message.reply(text, parse_mode='html')




    if message.text.lower() == 'информация о семьях':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       text = f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за «<b>СЕМЬИ</b>» 👨‍👩‍👧‍👦

✏️ <b><code>Создать семью</code> <i>[название]</i> - команда для создание свой семьи <i>(Стоимость: {config.cash_family} Donate-Coins 🪙)</i></b>
👨‍👩‍👧‍👦 <b><code>Моя семья</code> | <code>семья</code> - вывод информации за семью в которой вы состоите </b>
⚙️ <b><code>+название семьи</code> <i>[название]</i> - Меняет название семьи <i>( можно раз в 7d) (от 3 ранга)</i></b>
💎 <b><code>Купить монеты</code> <i>[количество]</i> - Покупка семейный монет в мешок семьи</b>
➖ <b><code>-ранг семьи</code> - Понизить игрока в семье на 1 ранг ниже <i>(от 3 ранга)</i></b>
➕ <b><code>+ранг семьи</code> - Повысить игрока в семье на 1 ранг выше <i>(от 3 ранга)</i></b>
👶 <b><code>Пригласить в семью</code> - Приглашение в вашу семью <i>(от 2 ранга)</i></b>
❌ <b><code>Выгнать из семьи</code> - Исключение игрока из вашей семьи <i>(от 3 ранга)</i></b>
💭 <b><code>+описание семьи</code> <i>[описание]</i> - Устоновка описание в вашей семье <i>(от 3 ранга)</i></b>
😔 <b><code>Распустить семью</code> - Удаление семьи <i>(от 3 ранга)</i></b>
🔙 <b><code>Выйти с семьи</code> - Выход с семьи </b>

❗️ Будьте окуратней при <b>выдаче ранга игроку</b>
       '''
       
       await message.reply(text, parse_mode='html')


#######Починка
    if message.text.startswith ('Починить'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])


       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)



       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошо '
          if hp == 65:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Средне '
          if hp == 43:
             hp2 = 'Плохое 🟥'
          if hp == 36:
             hp2 = 'Плохо '
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 12:
             hp2 = 'Ужасно '

       if hp <= 80:
          if hp > 70:
             if balance > 20000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 20.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f" 🆘 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина еше несломалась", parse_mode='html')
          

       if hp <= 70:
          if hp > 60:
             if balance > 30000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 30.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 60:
          if hp > 50:
             if balance > 40000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 40.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 40000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')


       if hp <= 50:
          if hp > 40:
             if balance > 50000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 20.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 40:
          if hp > 30:
             if balance > 60000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 60.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 60000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 30:
          if hp >20:
             if balance > 70000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 70.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 70000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 20:
          if hp > 10:
             if balance > 80000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 80.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 80000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 10:
             if balance > 90000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Починка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 90.000 $", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 90000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')


#######Заправка
    if message.text.startswith ('Заправить'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       
       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if benz <= 80:
          if benz > 70:
             if balance > 20000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 20.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f" 🆘 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>, у вашей машины полно бензина", parse_mode='html')
          

       if benz <= 70:
          if benz > 60:
             if balance > 30000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 30.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 60:
          if benz > 50:
             if balance > 40000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 40.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 40000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 50:
          if benz > 40:
             if balance > 50000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 50.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 50000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 40:
          if benz > 30:
             if balance > 60000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 60.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 60000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 30:
          if benz > 20:
             if balance > 70000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 70.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 70000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 20:
          if benz > 10:
             if balance > 80000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 80.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 80000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 10:
             if balance > 90000:
                await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Заправка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: 90.000 $", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 90000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                













##########################################################################
    if message.text.lower() == 'реклама':
      user_id = message.from_user.id

      if user_id != config.owner_id:
         return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass

      await utils.advertising_utils(1, message)
   
    if message.text.lower() == 'post реклама':
      user_id = message.from_user.id

      if user_id != config.owner_id:
         return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')
      else:
         pass
      
      await utils.advertising_utils(2, message)
    