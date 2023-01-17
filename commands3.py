#from regex import E
from imports import *

bot = Bot(token=config.token, disable_web_page_preview=True)
dp = Dispatcher(bot)

async def info_donate_callback(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f'Чтобы пополнить счёт, введите команду: <code>пополнить</code> <i>(сумма)</i>', parse_mode='html')


async def check_pays_callback(callback: types.CallbackQuery):
    bill_id = str(callback.data[10:])
    info = await get_check(bill_id)

    if info == False:
        return callback.answer(f'Счёт не найден')
    else:
        pass

    if str(p2p.check(bill_id=bill_id).status) == 'PAID':
        users_money = await user_money(callback.from_user.id)
        donate = int(info[1])

        x2donate_status = await status_x2donate()

        if x2donate_status == 'on':
            await update_money(callback.from_user.id, users_money + donate * 2)
            await delete_check(bill_id)
            await callback.message.answer(f'✅ <b>{callback.from_user.full_name}, вы успешно оплатили свой счёт и получили {donate * 2} руб.</b> <i>🎗X2 Донат</i>', parse_mode='html')
            return
        else:
            pass
        await update_money(callback.from_user.id, users_money + donate)
        await delete_check(bill_id)
        await callback.message.answer(f'✅ <b>{callback.from_user.full_name}, вы успешно оплатили свой счёт и получили {donate} руб.</b>', parse_mode='html')
    else:
        await callback.message.answer('Вы не оплатили счёт', reply_markup=pay(False, bill=bill_id))


async def pay_money3_callback(callback: types.CallbackQuery):
    times = float(callback.data[11:])

    last_time = f"{int(times)}"
    sec_time = time.time() - float(last_time)

    period = 60
    if sec_time >= period:
        await callback.message.delete()
        return await callback.message.answer(f'⏰ {callback.from_user.full_name} Срок действия этой кнопки истёк. Кнопка была удалена')
    else:
        pass

    money_pay = await course_money3()
    cash_money_pay = await course_cash_money3()

    users_money = await user_money(callback.from_user.id)

    if users_money < cash_money_pay:
        return await callback.answer('❗️ У вас не хватает средств')
    else:
        pass
    
    users_balance = await user_balance(callback.from_user.id)

    await update_money(callback.from_user.id, users_money - cash_money_pay)
    await update_balance(callback.from_user.id, users_balance + money_pay)
    full_summ = await utils.scor_summ(money_pay)
    await callback.message.answer(f'🎉 Вы успешно купили <b>{full_summ}</b>', parse_mode='html')





async def pay_money1_callback(callback: types.CallbackQuery):
    times = float(callback.data[11:])

    last_time = f"{int(times)}"
    sec_time = time.time() - float(last_time)

    period = 60
    if sec_time >= period:
        await callback.message.delete()
        return await callback.message.answer(f'⏰ {callback.from_user.full_name} Срок действия этой кнопки истёк. Кнопка была удалена')
    else:
        pass

    money_pay = await course_money1()
    cash_money_pay = await course_cash_money1()

    users_money = await user_money(callback.from_user.id)

    if users_money < cash_money_pay:
        return await callback.answer('❗️ У вас не хватает средств')
    else:
        pass
    
    users_balance = await user_balance(callback.from_user.id)

    await update_money(callback.from_user.id, users_money - cash_money_pay)
    await update_balance(callback.from_user.id, users_balance + money_pay)
    full_summ = await utils.scor_summ(money_pay)
    await callback.message.answer(f'🎉 Вы успешно купили <b>{full_summ}</b>', parse_mode='html')




async def pay_money2_callback(callback: types.CallbackQuery):
    times = float(callback.data[11:])

    last_time = f"{int(times)}"
    sec_time = time.time() - float(last_time)

    period = 60
    if sec_time >= period:
        await callback.message.delete()
        return await callback.message.answer(f'⏰ {callback.from_user.full_name} Срок действия этой кнопки истёк. Кнопка была удалена')
    else:
        pass

    money_pay = await course_money2()
    cash_money_pay = await course_cash_money2()

    users_money = await user_money(callback.from_user.id)

    if users_money < cash_money_pay:
        return await callback.answer('❗️ У вас не хватает средств')
    else:
        pass
    
    users_balance = await user_balance(callback.from_user.id)

    await update_money(callback.from_user.id, users_money - cash_money_pay)
    await update_balance(callback.from_user.id, users_balance + money_pay)
    full_summ = await utils.scor_summ(money_pay)
    await callback.message.answer(f'🎉 Вы успешно купили <b>{full_summ}</b>', parse_mode='html')




async def priglashenie_callback(call: types.CallbackQuery):

   user1, user2, name_family = call.data.replace('accept_', '', 1).split(':')
   print(call.from_user.id, user1)
   
   if int(call.from_user.id) == int(user1):
      pass
   else:
      return await call.answer('Приглашение не для тебя ❗️')

   user_id = call.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(call.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
   all_family2 = []
   
   for all_owner_id in all_family:
      all_family2.append(all_owner_id[0])

   if user_id in all_family2:
      return await call.message.answer(f'❗️У вас есть <b>своя семья.</b> Зачем вам ещё одна? | <code>Распустить семью</code> - удаление семьи ', parse_mode='html')
   else:
      pass

   user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

   if user_id_family != None:
      return await call.message.answer('❗️ Вы уже <b>состоите в семье</b> | напишите «<code>выйти с семьи</code>» - для выхода с вашей семьи',parse_mode='html')
   else:
      pass

   text = f'''
✅ <a href='tg://user?id={user1}'>{user2}</a>, вы приняли приглашение в семью «<b>{name_family}</b>». Вы теперь состоите в семье
   '''

   text2 = f'''
❗️ В вашу семью «<b>{name_family}</b>» вступил <a href='tg://user?id={user1}'>{user2}</a>
   '''
   owner_id_family = cursor.execute(f"SELECT owner_id from family where name = \"{name_family}\"").fetchone()
   owner_id_family = owner_id_family[0]

   cursor.execute("INSERT INTO user_family VALUES(?, ?, ?, ?);",(user2, user1, name_family, 1))
   await call.message.bot.send_message(owner_id_family, text2, parse_mode='html')
   await call.message.answer(text, parse_mode='html')


async def organiz_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       text = f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за все организации 🏰

👨‍👩‍👧‍👦 <code>Информация о семьях</code> <b>- Выводит список команд семьей</b>
       '''
       
       await callback.message.edit_text(text,reply_markup=help_back, parse_mode='html')









async def top_f_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM family ORDER BY balance DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:

          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>🎯ТОП 1🎯</b> |'
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
          
          balance = '{:,}'.format(user[4]).replace(',','.')
          
          if user[1] == config.owner_id:
            pass
          else:
            text = f'{num2} {user[0]} |{num3} 🔎 ID: <code>{user[3]}</code> | {balance} с. монет'

          top_list.append(text)  


       if top_list == ['']:
         top_f = '\n    ❗️ <b>На данный момент нету ни одной семьи</b>'
       else:
         top_f = '\n'.join(top_list)

       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 семьей в «<b>{config.full_bot_name}</b>»:\n" + top_f, parse_mode='html')


async def top_а_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM users ORDER BY game DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:

          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>🎯ТОП 1🎯</b> |'
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

          top_list.append(f'{num2} {user[1]} |{num3} 🔎 ID: <code>{user[0]}</code> | {user[12]} всего игр')  

       top_a = '\n'.join(top_list)

       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 азартных игроков в боте:\n" + top_a, parse_mode='html')

async def top_y_callback(callback: types.CallbackQuery):
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM reput ORDER BY reput DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:
          user_top = cursor.execute(f'SELECT user_name from users where user_id = {user[0]}').fetchone()
          user_top = user_top[0]

          num += 1

          summ = '{:,}'.format(user[1]).replace(',','.')

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>📈ТОП 1📈</b> |'
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
          

          top_list.append(f'{num2} {user_top} |{num3} 🔎 ID: <code>{user[0]}</code> | 📊 {summ} репутации')  
       top_y = '\n'.join(top_list)

       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 успешных игроков в боте:\n" + top_y, parse_mode='html')




async def top_b_callback(callback: types.CallbackQuery):
       import utils
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM users ORDER BY balance DESC").fetchmany(10)
       top_list = []

       num = 0

       for user in list:
          balance3 = await utils.scor_summ(user[4])
            
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
       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 богачей в боте:\n" + top, parse_mode='html')

async def top_callback(callback: types.CallbackQuery):
       list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
       top_list = []
       user_id = callback.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (callback.from_user.id,)).fetchone()
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

           top_list.append(f"{num2}. {user[1]} |{stats}{num3} ID: <code>{user[0]}</code> |  — {c2}💎 ")

       top = "\n".join(top_list)
       await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, топ 10 игроков бота:\n" + top, parse_mode='html')



async def prodazh_valyte_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    text = f'''
📊<b> Для просмотра курса валют, пропишите:</b> <code>курс</code>
    '''
    await callback.message.edit_text(text, parse_mode='html')
async def ysloviya_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    text = f'''
🌐  <b>УСЛОВИЯ ПОКУПОК В ИГРОВОМ БОТЕ {config.full_bot_name}</b>

<b>❗️ ОПЛАТА С ЮМАНИ И ДРУГИХ БАНКОВ</b>
<i>- Если вы не имеете QIWI, и так же банковскую карточку, тогда по поводу покупки обращайтесь к {config.owner}</i>

❗️<b> ОПЛАТА С УКРАИНЫ 🇺🇦</b>
<i>- Для жителей Украины, которые хотят пополнить свой счёт, прошу обратиться к {config.owner} </i>

<b>❗️ ДРУГИЕ ВАЛЮТЫ</b>
<i>- Если у вас не рубли, а доллары , эвро, грн , злотые, тогда прошу обратиться к {config.owner}</i>
'''

    await callback.message.answer(text, parse_mode='html')


async def oston_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>,  вот список остальных команд ❕

🧮 <code>.cl 2+2</code> - <b>данная команда позволяет считать любые математические примеры</b>
🖼  <code>Ава</code> | <code>Удалить аву</code> - <b>с помощью этой команды можно поставить аватарку на баланс, и так же её удалить </b>
💰 <code>Ограбить банк</code> - <b>команда с помощью какой можно ограбить банк</b>
🎁 <code>Кит-бонусы</code> - <b>выводит информацию за кит бонусы</b>
💭 <code>Рп-команды</code> - <b>команда выводит список доступных рп-команд</b>
🎁 <code>Ежедневный бонус</code> - <b>Позволяет получить ежедневный бонус</b>
💼 <code>промо</code> | <code>+промо</code> - <b>Активация промокодов, создания своего промокода</b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением </b>
    ''', reply_markup=help_back , parse_mode='html')
async def register_help_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])



    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, Вот информация о боте 🔎

📊 {config.channel} - <b>Игровой канал</b>
💬 {config.chat} - <b>Игровой чат</b>
💬 {config.chat2} - <b>Игровой чат</b>
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
🏰 <b>Организации</b>

➖➖➖➖➖➖➖➖➖➖➖
↘️Выберите одну из доступных <b>категорий </b>
    ''', reply_markup=help2, parse_mode='html')



async def osn2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список основных команд📝

🕴 <code>Профиль</code> - <b>выводит ваш игровой профиль</b>
🔎 <code>Ник</code>  <b>|</b> <code>Сменить ник</code>  - <b>Выводит ваш ник, и так же его меняет </b>
⚙️ <code>Сменить префикс</code>  <b>|</b> <code>+игроку префикс</code>  - <b>меняет префикс себе, меняет префикс игроку.</b>
👝 <code>Б</code>  <b>|</b> <code>Баланс</code>  - <b>выводит ваш игровой баланс</b>
🏦 <code>Банк</code>  <b>|</b> <code>Банк положить 1</code>  <b>|</b> <code>Банк снять 1</code>  - <b>выводит ваш игровой банк с депозитом , позволяет положить в банк сумму, позволяет снять с банка сумму</b>
🏛 <code>Депозит положить 1</code>  <b>|</b> <code>Депозит снять 1</code>  <b>|</b> <code>Процент снять 1</code>  - <b>Позволяет положить на депозит , позволяет снять с депозита , позволяет снять накапанный процент с депозита </b>
🟣 <code>Эфириум курс</code>  <b>|</b> <code>Эфириум купить 1</code>  <b>|</b> <code>Эфириум продать  1</code>  - <b>Выводит курс эфириума, позволяет купить эфириум, позволяет продать эфириум</b>
💎  <code>Рейтинг</code> <b>|</b> <code>Рейтинг купить 1</code> <b>|</b> <code>Рейтинг продать 1</code> - <b>Выводит ваш игровой рейтинг, позволяет купить рейтинг, позволяет продать рейтинг</b>
🤝 <code>Дать 1</code>  <b>|</b> <code>Передать 1</code>  [ID] - <b>Позволяет передать деньги игроку, позволяет передать деньги игроку по ID</b>
👑 <code>Топ</code>  <b>|</b> <code>Топ б</code>  - <b>Выводит топ по рейтингу игроков, выводит топ по игровому балансу игроков</b>
👮‍♂️ <code>Репорт</code>  - <b>Выводит информацию за систему репортов</b>

ℹ️ Что бы использовать команду , <b>напишите команду сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')



async def admins_menu_up_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    admins_menu = InlineKeyboardMarkup(row_width=2)
    statistic = InlineKeyboardButton(text='Статистика 👥', callback_data='statistic')
    admins_comands = InlineKeyboardButton(text='Админ команды 📝', callback_data='admins_comands')
    admins_menu.add(statistic, admins_comands)
    
    su4 = user_status

    text = f'''
✅ <b>УСПЕШНЫЙ ВХОД В АДМИН МЕНЮ</b>

❗️ Права администратора: <b>{su4}</b>

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🔐 Категории

<b>👥 Статистика бота</b>
<b>📝 Админ команды</b>

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
↘️ Выбери одну из <b>категорий</b>
    '''
    if user_status == 'Owner':
       await callback.message.edit_text(text, reply_markup=admins_menu , parse_mode='html')
       return

    if user_status == 'Helper_Admin':
       await callback.message.edit_text(text, reply_markup=admins_menu , parse_mode='html')
       return
    if user_status == 'Admin':
       await callback.message.edit_text(text, reply_markup=admins_menu , parse_mode='html')
       return
    else:
       await callback.message.edit_text(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/bs_bro5/'>RedSharkQ</a>  ⚠️ ", parse_mode='html')


async def statiskik_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Admin\""""
    cursor.execute(sqlite_select_query2)
    records2 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Helper_Admin\""""
    cursor.execute(sqlite_select_query2)
    records3 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Owner\""""
    cursor.execute(sqlite_select_query2)
    records4 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from chats"""
    cursor.execute(sqlite_select_query2)
    chats = cursor.fetchall()

    stats222 = InlineKeyboardMarkup(row_width=1)
    ob_statistik2 = InlineKeyboardButton(text='Общая статистика 🔎', callback_data='stats222')
    
    stats222.add(ob_statistik2)

    text = f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот статистика бота  📊

🤵 <b>Игроков:</b> <code>{'{:,}'.format(len(records)).replace(',', '.')}</code>
💬 <b>Чатов: </b><code>{'{:,}'.format(len(chats)).replace(',', '.')}</code>

👨‍⚖️ <b>OWNER:</b> <code>{len(records4)}</code>
👮‍♀️ <b>HELPER-ADMINS:</b> <code>{len(records3)}</code>
🤠 <b>ADMIN:</b> <code>{len(records2)}</code>
    '''
    if user_status == "Admin":
       await callback.message.answer(text,reply_markup=stats222, parse_mode='html')
       return
    if user_status == "Helper_Admin":
       await callback.message.answer(text,reply_markup=stats222, parse_mode='html')
       return

    if user_status == "Owner":
       await callback.message.answer(text,reply_markup=stats222, parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/bs_bro5/'>RedSharkQ</a>  ⚠️ ", parse_mode='html')


async def ob_Statisyik_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = user_status[0]

    sqlite_select_query21 = """SELECT * from users where user_status = \"Vip\""""
    cursor.execute(sqlite_select_query21)
    vip = cursor.fetchall()

    sqlite_select_query22 = """SELECT * from users where user_status = \"Premium\""""
    cursor.execute(sqlite_select_query22)
    premium = cursor.fetchall()

    sqlite_select_query23 = """SELECT * from users where user_status = \"Platina\""""
    cursor.execute(sqlite_select_query23)
    platina = cursor.fetchall()

    sqlite_select_query24 = """SELECT * from users where user_status = \"Helper\""""
    cursor.execute(sqlite_select_query24)
    helper = cursor.fetchall()

    sqlite_select_query25 = """SELECT * from users where user_status = \"Sponsor\""""
    cursor.execute(sqlite_select_query25)
    sponsor = cursor.fetchall()

    sqlite_select_query26 = """SELECT * from users where user_status = \"Osnovatel\""""
    cursor.execute(sqlite_select_query26)
    osnovatel = cursor.fetchall()

    sqlite_select_query27 = """SELECT * from users where user_status = \"Vladelec\""""
    cursor.execute(sqlite_select_query27)
    vladelec = cursor.fetchall()

    sqlite_select_query28 = """SELECT * from users where user_status = \"Bog\""""
    cursor.execute(sqlite_select_query28)
    bog = cursor.fetchall()

    sqlite_select_query29 = """SELECT * from users where user_status = \"Vlaselin\""""
    cursor.execute(sqlite_select_query29)
    vlaselin = cursor.fetchall()

    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Admin\""""
    cursor.execute(sqlite_select_query2)
    records2 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Helper_Admin\""""
    cursor.execute(sqlite_select_query2)
    records3 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Owner\""""
    cursor.execute(sqlite_select_query2)
    records4 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from family"""
    cursor.execute(sqlite_select_query2)
    all_family = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from user_family"""
    cursor.execute(sqlite_select_query2)
    all_family_users = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from chats"""
    cursor.execute(sqlite_select_query2)
    all_chats = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users WHERE status_block = 'on'"""
    cursor.execute(sqlite_select_query2)
    block_users = cursor.fetchall()

    if user_status in ['Owner', 'Helper_Admin']:
       await callback.message.answer(f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот общая статистика бота 🔎

🔓 <b>Основная</b>
         👤 <b>Игроков:</b> <code>{'{:,}'.format(len(records)).replace(',', '.')}</code>
         🌐 <b>Чатов с ботом:</b> <code>{'{:,}'.format(len(all_chats)).replace(',','.')}</code>

🔰 <b>Привилегии</b>
         ❤️ <b>ВИП:</b> <code>{len(vip)}</code>
         🧡 <b>ПРЕМИУМ:</b> <code>{len(premium)}</code>
         💛 <b>ПЛАТИНА:</b> <code>{len(platina)}</code>
         💚 <b>ХЕЛПЕР:</b> <code>{len(helper)}</code>
         💙 <b>СПОНСОР:</b> <code>{len(sponsor)}</code>
         💜 <b>ОСНОВАТЕЛЬ:</b> <code>{len(osnovatel)}</code>
         🖤 <b>ВЛАДЕЛЕЦ:</b> <code>{len(vladelec)}</code>
         🤍 <b>БОГ:</b> <code>{len(bog)}</code>
         🤎 <b>ВЛАСТЕЛИН:</b> <code>{len(vlaselin)}</code>

🏰 <b>Организации:</b>
        👨‍👩‍👧‍👦 <b>Семьей:</b> <code>{len(all_family)}</code>
        👶 <b>Состоят в семье:</b> <code>{len(all_family_users)}</code>

🛑 <b>Администрация</b>
         💂‍♂️ <b>Заблокированных игроков:</b> <code>{len(block_users)}</code>
         ⛔️ <b>ADMIN:</b> <code>{len(records2)}</code>
         ⚠️ <b>HELPER-ADMIN:</b> <code>{len(records3)}</code>
         ✅ <b>OWNER</b>: <code>{len(records4)}    </code>    
       """, parse_mode='html')
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, статистика бота доступна только от прав администратора \"HELPER-ADMINS\" ", parse_mode='html')



async def admin_commands_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0]) 
    if user_status == 'Owner':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /ban
6️⃣ | /unban
7️⃣ |Выдать админа
8️⃣ | Выдать хелпера
9️⃣ | Передать права
🔟 | Забрать права
1️⃣1️⃣ | /reset
1️⃣2️⃣ | /warn
1️⃣3️⃣ | reset_id [ID]
1️⃣4️⃣ | /info
1️⃣5️⃣ | /info_id [ID]
1️⃣6️⃣ | Поделить [количество]
1️⃣7️⃣ | /ban_id [ID]
1️⃣8️⃣ | /unban_id [ID]
1️⃣9️⃣ | /warn_id [ID]
2️⃣0️⃣ | /unwarn_id [ID]
2️⃣1️⃣ | /disconect_database
2️⃣2️⃣ | /chats 
2️⃣3️⃣ | reset promo | очистить промо - очистка всех промокодов
2️⃣4️⃣ | новый курс 1е15 10 10е18 100 100е21 1000
2️⃣5️⃣ | пополнить игроку 100
2️⃣6️⃣ | снять игроку 100
2️⃣7️⃣ | x2donate статус off/on
       '''

    if user_status == 'Helper_Admin':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /ban
6️⃣ | /unban
7️⃣ | /warn
8️⃣ | reset_id [ID]
9️⃣ | /info
🔟 | /info_id [ID]
1️⃣1️⃣ | Поделить [количество]
1️⃣2️⃣ | /ban_id [ID]
1️⃣3️⃣ | /unban_id [ID]
1️⃣4️⃣ | /warn_id [ID]
1️⃣5️⃣ | /unwarn_id [ID]
1️⃣6️⃣ | /chats
       '''
    if user_status == 'Admin':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /info
6️⃣ | Поделить [количество]
7️⃣ | /chats
       '''
    if user_status == 'Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    if user_status == 'Helper_Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    if user_status == 'Owner':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/bs_bro5/'>RedSharkQ</a>  ⚠️", parse_mode='html')


async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список игровых команд 📝

🧊 <code>/gamevb</code> | <code>вб</code> - <b>игра на весь баланс, выводит информацию за игру</b>
⚽️ <code>Футбол  1</code> | <code>Фб 1</code> - <b>Азартная игра футбол</b>
🎱 <code>Dice ч 1</code> | <code>Dice к 1</code> | <code>Wheel</code> - <b>Азартная игра , со ставкой на чёрный цвет, ставка на красный цвет, выводит информацию за игру</b>
🤵‍♀️ <code>Казино 1</code> - <b>Азартная игра казино</b>
◾️ <code>Плинко 1</code> -  <b>Азартная игра Плинко</b>
🎰 | <code>Спин 1</code> - <b>Азартная игра Спин</b>
🎲 <code>Кубик 1</code> <b>[до 7]</b> <code>1</code> - <b>Азартная игра Кубик</b>
🎲 <code>Чётное 1</code> | <code>нечётное 1</code> - <b>Азартная игра Чётное нечётное со ставкой на чётное , со ставкой на нечётное</b>
🏎 <code>Гонка 1</code> - <b>Гонки со ставками </b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')


async def rabot2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список работних команд📝

⛏ <code>Шахта</code> | <code>Купить кирку</code> | <code>Копать руду</code> | <code>Продать</code> <b>[название руды] [количество] - Выводит информацию за шахту, покупка кирки для добычи руды, добыча руды, продажа руды</b>

🌾  <code>Ферма</code> | <code>Купить грабли</code> | <code>Собрать</code> <b>[название урожая]</b> | <code>Продать</code> <b>[название урожая] [количество] - Выводит информацию за ферму, покупка граблей для сбора урожая , сбор урожая , продажа урожая </b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')


async def im2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот все команды на имущество📝

🏠  <code>Дома</code> | <code>Мой дом</code> - <b>Выводит список доступных домов для покупки и так же информацию для покупки, выводит информацию за ваш дом</b>

🕋 <code>Подвалы</code> | <code>Продать подвал</code> - <b>Выводит список доступных подвалов и так информацию за покупки их , позволяет продать подвал</b>

🛠 <code>Крафтить</code> | <code>Система крафта</code> - <b>позволяет крафтить предметы и так далее , выводит информацию за крафт предметов</b>

🚘 <code>Машины</code> | <code>Моя машина</code> - <b>Выводит доступные машины , и так же информацию за покупку их , выводит информацию за вашу машину</b>

🚗 <code>Заправить</code> | <code>Починить</code> - <b>Позволяет вам заправить ваш автомобиль , позволяет его починить</b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')


async def priv2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a> , вот все доступные привилегии📝

❤️ <code>ВИП</code> - <b>Выводит список возможностей привилегии ВИП</b>
🧡 <code>ПРЕМИУМ</code> - <b>Выводит список возможностей привилегии ПРЕМИУМ</b>
💛 <code>ПЛАТИНА</code> - <b>Выводит список возможностей привилегии ПЛАТИНА</b>
💚 <code>ХЕЛПЕР</code> - <b>Выводит список возможностей привилегии ХЕЛПЕР</b>
💙 <code>СПОНСОР</code> - <b>Выводит список возможностей привилегии СПОНСОР</b>
💜 <code>ОСНОВАТЕЛЬ</code> - <b>Выводит список возможностей привилегии ОСНОВАТЕЛЬ</b>
🖤 <code>ВЛАДЕЛЕЦ</code> - <b>Выводит список возможностей привилегии ВЛАДЕЛЕЦ</b>
🤍 <code>БОГ</code> - <b>Выводит список возможностей привилегии БОГ</b>
🤎 <code>ВЛАСТЕЛИН</code> - <b>Выводит список возможностей привилегии ВЛАСТЕЛИН</b>

ℹ️ Что бы использовать команду , напишите команду <b>сообщением</b>
    ''', reply_markup=help_back , parse_mode='html')



async def craft_resurs1(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,750):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Zerro ⛏\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(751,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Zerro ⛏\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Кирка Zerro⛏\n🔱 | Уникальность: Х2 Добыча ресурсов", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET pick = "Zerro" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)



async def craft_resurs2(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,750):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Zerro 🌾\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(751,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Zerro 🌾\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Грабли Zerro 🌾\n🔱 | Уникальность: Х2 Добыча ресурсов", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE farm SET rake = "Zerro" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)




async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,900):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Cherick ⛏\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(901,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Cherick ⛏\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Кирка Cherick ⛏\n🔱 | Уникальность: Х2 Добыча ресурсов, Ограничение на время снимаеться на 50%", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET pick = "Cherick" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)


async def resurs4_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,900):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Cherick 🌾\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(901,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Cherick 🌾\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Грабли Cherick 🌾\n🔱 | Уникальность: Х2 Добыча ресурсов, Ограничение на время снимаеться на 50%", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE farm SET rake = "Cherick" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)




async def case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    case_shop = InlineKeyboardMarkup(row_width=2)
    money_case1 = InlineKeyboardButton(text='💸 Money-Case', callback_data='money_case')
    donate_case2 = InlineKeyboardButton(text='🧧 Donate-Case', callback_data='donate_case')
    case_shop.add(money_case1, donate_case2)

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

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за кейсы 🎁

💸 | Money-Case - 50 Donate-Coins 🪙
🧧 | Donate-Case - 100 Donate-Coins 🪙

{casee}{money_case2}{donate_case2}

🛒 Чтобы купить\посмотреть информацию, виберите кнопку ниже ⬇️  
    """, reply_markup=case_shop,  parse_mode='html')
 


async def donate_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    donate_case_cash = InlineKeyboardMarkup(row_width=2)
    donate_case_cash1 = InlineKeyboardButton(text='🛒 Купить кейс', callback_data='donate_case_cash1')
    donate_case_cash.add(donate_case_cash1)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за Donate-Case 🧧

ℹ️ | В 1 Donate-Case падает рандомно случайная привилегия!

🛒 Чтобы купить нажмите кнопку ниже 🔽
    """, reply_markup=donate_case_cash,  parse_mode='html')


async def donate_case_cash1_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])

    if donate_coins >= 100:
       await callback.message.answer(f"🧧 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купил 1 Donate-Case", parse_mode='html')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 100} WHERE user_id = {user_id}')
       connect.commit()
       return
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не достаточно Donate-Coins 🪙", parse_mode='html')



async def up_donate_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])

    if donate_case < 1:
       await callback.message.answer( f"🆘 | Игрок, у вас нету Донат кейсов", parse_mode='html')
       return
   
    rx = random.randint(0, 935)

    if int(rx) in range(0,500):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💚 ХЕЛПЕР</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Helper" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ХЕЛПЕР 💚" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(501,750):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💙 СПОНСОР</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Sponsor" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "СПОНСОР 💙" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(751,850):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💜 ОСНОВАТЕЛЬ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Osnovatel" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ОСНОВАТЕЛЬ 💜" WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(851,900):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🖤 ВЛАДЕЛЕЦ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Vladelec" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАДЕЛЕЦ 🖤" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(901,925):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🤍 БОГ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Bog" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "БОГ 🤍" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(925,935):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🤎 ВЛАСТЕЛИН</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Vlaselin" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАСТЕЛИН 🤎" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()


async def up_money_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
    balance = int(balance[0])

    if money_case < 1:
       await callback.message.answer( f"🆘 | Игрок, у вас нету Money кейсов", parse_mode='html')
       return
       
    rx = random.randint(0, 100000000000000000000000000000)
    rx2 = '{:,}'.format(rx).replace(',', '.')

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы открыли Money-Case 💸

🔎 | Результат: {rx2}$    
    """, parse_mode='html')
    cursor.execute(f'UPDATE users SET balance = {balance + rx} WHERE user_id = {user_id}')
    cursor.execute(f'UPDATE user_case SET case_money = {money_case - 1} WHERE user_id = {user_id}')
    connect.commit()


async def money_case_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    money_case_cash = InlineKeyboardMarkup(row_width=2)
    money_case_cash1 = InlineKeyboardButton(text='🛒 Купить кейс', callback_data='money_case_cash1')
    money_case_cash.add(money_case_cash1)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за Money-Case 💸

ℹ️ | В 1 Money-Case выпадает от 0$ и до 999гугл.

🛒 Чтобы купить нажмите кнопку ниже 🔽
    """, reply_markup=money_case_cash,  parse_mode='html')



async def money_case_cash1_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    if donate_coins >= 50:
       await callback.message.answer(f"💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купил 1 Money-Case", parse_mode='html')
       cursor.execute(f'UPDATE user_case SET case_money = {money_case + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}')
       connect.commit()
       return
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не достаточно Donate-Coins 🪙", parse_mode='html')


async def privilegii_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    privilegii_inline = InlineKeyboardMarkup(row_width=3)
    vip = InlineKeyboardButton(text='❤️ ВИП ', callback_data='vip')
    premium = InlineKeyboardButton(text='🧡 ПРЕМИУМ', callback_data='premium')
    platina = InlineKeyboardButton(text='💛 ПЛАТИНА', callback_data='platina')
    helper = InlineKeyboardButton(text='💚 ХЕЛПЕР', callback_data='helper')
    sponsor = InlineKeyboardButton(text='💙 СПОНСОР', callback_data='sponsor')
    osnovatel = InlineKeyboardButton(text='💜 ОСНОВАТЕЛЬ', callback_data='osnovatel')
    vladelec = InlineKeyboardButton(text='🖤 ВЛАДЕЛЕЦ', callback_data='vladelec')
    bog = InlineKeyboardButton(text='🤍 БОГ', callback_data='bog')
    vlastelin = InlineKeyboardButton(text='🤎 ВЛАСТЕЛИН', callback_data='vlastelin')
    privilegii_inline.add(vip, premium, platina, helper, sponsor, osnovatel, vladelec, bog, vlastelin)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот все доступные привилегии📝

❤️ | ВИП - 10 Donate-coins 🪙
🧡 | ПРЕМИУМ - 30 Donate-coins 🪙
💛 | ПЛАТИНА - 50 Donate-coins 🪙
💚 | ХЕЛПЕР - 100 Donate-coins 🪙
💙 | СПОНСОР - 155 Donate-coins 🪙
💜 | ОСНОВАТЕЛЬ - 170 Donate-coins 🪙
🖤 | ВЛАДЕЛЕЦ - 250  Donate-coins 🪙
🤍 | БОГ - 300 Donate-coins 🪙
🤎 | ВЛАСТЕЛИН - 350 Donate-coins 🪙

🛒 Чтобы купить привилегию , виберите её ниже
ℹ️ Чтобы посмотреть возможности привилегий , виберите привилегию ниже   
    """, reply_markup=privilegii_inline,  parse_mode='html')


async def vip_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vip_menu = InlineKeyboardMarkup(row_width=1)
    cash_vip = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vip')
    
    vip_menu.add(cash_vip)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ВИП ❤️

🛒 | При покупке:
        1️⃣ | Бонус-кит ВИП
        2️⃣ | Префикс ВИП
        3️⃣ | 250.000$

🎁 | При использовании Donate-Case:
       1️⃣ | Бонус-кит ВИП
       2️⃣ | Префикс ВИП

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vip_menu,  parse_mode='html')



async def cash_vip_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 10:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВИП", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vip" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 100} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 10000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВИП ❤️" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 10} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def premium_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    premium_menu = InlineKeyboardMarkup(row_width=1)
    cash_premium = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_premium')
    
    premium_menu.add(cash_premium)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ПРЕМИУМ 🧡

🛒 | При покупке:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ
        3️⃣ | 300.000$

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПРЕМИУМ
        2️⃣ | Префикс ПРЕМИУМ

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=premium_menu,  parse_mode='html')



async def cash_premium_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 30:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ПРЕМИУМ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Premium" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 300} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 100000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ПРЕМИУМ 🧡" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 30} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def platina_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    platina_menu = InlineKeyboardMarkup(row_width=1)
    cash_platina = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_platina')
    
    platina_menu.add(cash_platina)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ПЛАТИНА 💛

🛒 | При покупке:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА
        3️⃣ | 550.000$
        4️⃣ | 10 Рейтинга
        5️⃣ | Money-case 1 шт.

🎁 | При использовании Donate-Case:
        1️⃣ | Бонус-кит ПЛАТИНА
        2️⃣ | Префикс ПЛАТИНА

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=platina_menu,  parse_mode='html')




async def cash_platina_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 50:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ПЛАТИНА", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Platina" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 800} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 400000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ПЛАТИНА 💛" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def helper_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    helper_menu = InlineKeyboardMarkup(row_width=1)
    cash_helper = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_helper')
    
    helper_menu.add(cash_helper)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ХЕЛПЕР 💚

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

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=helper_menu,  parse_mode='html')



async def cash_helper_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 100:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ХЕЛПЕР", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Helper" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 3} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 1300} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 700000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ХЕЛПЕР 💚" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 100} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def sponsor_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    sponsor_menu = InlineKeyboardMarkup(row_width=1)
    cash_sponsor = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_sponsor')
    
    sponsor_menu.add(cash_sponsor)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию СПОНСОР 💙

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

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=sponsor_menu,  parse_mode='html')




async def cash_sponsor_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 155:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию СПОНСОР", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Sponsor" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "СПОНСОР 💙" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 155} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def osnovatel_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    osnovatel_menu = InlineKeyboardMarkup(row_width=1)
    cash_osnovatel = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_osnovatel')
    
    osnovatel_menu.add(cash_osnovatel)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ОСНОВАТЕЛЬ 💜

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

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=osnovatel_menu,  parse_mode='html')



async def cash_osnovatel_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 170:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ОСНОВАТЕЛЬ ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Osnovatel" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 100000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ОСНОВАТЕЛЬ 💜" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 170} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def vladelec_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vladelec_menu = InlineKeyboardMarkup(row_width=1)
    cash_vladelec = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vladelec')
    
    vladelec_menu.add(cash_vladelec)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> ,  вот данные за привилегию ВЛАДЕЛЕЦ 🖤

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

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vladelec_menu,  parse_mode='html')




async def cash_vladelec_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 250:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВЛАДЕЛЕЦ  ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vladelec" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 1000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАДЕЛЕЦ 🖤" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 250} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def bog_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    bog_menu = InlineKeyboardMarkup(row_width=1)
    cash_bog = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_bog')
    
    bog_menu.add(cash_bog)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию БОГ 🤍

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

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=bog_menu,  parse_mode='html')



async def cash_bog_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию БОГ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Bog" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "БОГ 🤍" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 300} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def vlastelin_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vlaselin_menu = InlineKeyboardMarkup(row_width=1)
    cash_vlaselin = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vlaselin')
    
    vlaselin_menu.add(cash_vlaselin)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ВЛАСТЕЛИН 🤎

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

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vlaselin_menu,  parse_mode='html')



async def cash_vlastelin_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВЛАСТЕЛИН ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vlaselin" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАСТЕЛИН 🤎" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 300} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )



async def adms_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    admins_menu_cash = InlineKeyboardMarkup(row_width=2)
    admins_cash = InlineKeyboardButton(text='⛔️ ADMIN', callback_data='admins_cash')
    helper_admins_cash = InlineKeyboardButton(text='⛔️ HELPER-ADMIN', callback_data='helper_admins_cash')
    owner_cash = InlineKeyboardButton(text='⛔️ OWNER', callback_data='owner_cash')
    admins_menu_cash.add(admins_cash, helper_admins_cash, owner_cash)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за статусы администраторов⛔️

1️⃣ | ADMIN - 400Р
4️⃣ | HELPER-ADMIN - 1.500Р
5️⃣ | OWNER - 5.000Р

↘️ Чтобы посмотреть возможности , виберите статус ниже   
    """,reply_markup=admins_menu_cash,  parse_mode='html' )
  


async def admins_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ADMIN ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Просмотр профиля игрока
6️⃣ | Поделить баланс
7️⃣ | Просмотр список зарегистрированный чатов 

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - <a href='t.me/bs_bro5/'>RedSharkQ</a>
    """,  parse_mode='html' )


async def helper_admins_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за HELPER-ADMIN ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Выдача бана
6️⃣ | Выдача разбана
7️⃣ | Поделить баланс
8️⃣ | Просмотр профила 
9️⃣ | Просмотр профиля по ID 
🔟 | Выдача варна 
1️⃣1️⃣ | Отбор варна
1️⃣2️⃣ | Выдача бана по ID
1️⃣3️⃣ | Выдача разбана по ID
1️⃣4️⃣ | Выдача варна по ID
1️⃣5️⃣ | Отбор варна по ID
1️⃣6️⃣ | Обнуление по ID
1️⃣7️⃣ | ДОСТУП К КОНСОЛИ БОТА
1️⃣8️⃣ | ДОСТУП К РЕПОРТАМ
1️⃣9️⃣ | Просмотр список зарегистрированный чатов 

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - <a href='t.me/bs_bro5/'>RedSharkQ</a>
    """,  parse_mode='html' )



async def owner_cash_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за OWNER ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Выдача бана
6️⃣ | Выдача разбана
7️⃣ |Поделить баланс
8️⃣ | Выдача прав администратора "ADMIN"
9️⃣ | Выдача прав администратора "HELPER-ADMIN"
🔟 | Выдача Donate-Coins
1️⃣1️⃣ | МАССОВОЕ ОБНУЛЕНИЕ
1️⃣2️⃣ | Выдача бана по ID
1️⃣3️⃣ | Выдача разбана по ID
1️⃣4️⃣ | Выдача варна
1️⃣5️⃣ | Отбор варна 
1️⃣6️⃣ | Выдача варна по ID
1️⃣7️⃣ | Отбор варна по ID
1️⃣8️⃣ | Возможность посмотреть профиль игрока
1️⃣9️⃣ | Возможность посмотреть профиль игрока по ID
2️⃣0️⃣ | Возможность выдать права администратора "OWNER"
2️⃣1️⃣ | ДОСТУП К КОНСОЛИ БОТА
2️⃣2️⃣ | ДОСТУП К РЕПОРТАМ
2️⃣3️⃣ | ВОЗМОЖНОСТЬ УДАЛЯТЬ ИГРОКОВ С БАЗЫ ДАННЫХ
2️⃣4️⃣ | Просмотр список зарегистрированный чатов

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - <a href='t.me/bs_bro5/'>RedSharkQ</a>
    """,  parse_mode='html' )



async def channel_proverk_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
   balance = int(balance[0])
   user_channel_status = await bot.get_chat_member(chat_id="@qwechannel", user_id=callback.from_user.id)

   channel_pov = cursor.execute("SELECT members from channel_pov where user_id = ?", (callback.from_user.id,)).fetchone()
   channel_pov = int(channel_pov[0])

   if channel_pov > 0:
      await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже получили деньги за подписку", parse_mode='html')
      return

   if user_channel_status['status'] != 'left':
      await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно подписались на канал ✅", parse_mode='html')
      await callback.message.answer( f"💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили приз в размере  500.000.000.000.000.000$", parse_mode='html')
      cursor.execute(f'UPDATE channel_pov SET members = {1} WHERE user_id = {user_id}')
      cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000000} WHERE user_id = {user_id}')
      connect.commit()
   else:
      await callback.message.answer( f"❌ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не подписались на канал, попробуйте снова", parse_mode='html')



async def ava_strach_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"СТРАЖ\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "strach" WHERE user_id = {user_id}')
   connect.commit()


async def ava_cheat_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ЧИТЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "cheat" WHERE user_id = {user_id}')
   connect.commit()



async def ava_apper_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"АППЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "apper" WHERE user_id = {user_id}')
   connect.commit()



async def ava_dyp_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ДЮППЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "dyp" WHERE user_id = {user_id}')
   connect.commit()



async def ava_girl_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ДЕВУШКА\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "girl" WHERE user_id = {user_id}')
   connect.commit()


async def ava_admin_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_status = str(user_status[0])

   if user_status in ['Admin', 'Helper_Admin', 'Owner']:
      await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"АДМИН\"", parse_mode='html')
      cursor.execute(f'UPDATE avatarka SET avatarka = "admin" WHERE user_id = {user_id}')
      connect.commit()
      return
   else:
      await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику <a href='t.me/blackLy_nobot/'>BLACKLY</a>  ⚠️", parse_mode='html')



async def gamevb_callback(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
   balance = int(balance[0])

   game = cursor.execute("SELECT game from users where user_id = ?",(callback.from_user.id,)).fetchone()
   game = int(game[0])

   balance2 = '{:,}'.format(balance).replace(',', '.')


   rx = random.randint(0, 10000)

   period = 5
   get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
   last_stavka = f"{int(get[0])}"
   stavkatime = time.time() - float(last_stavka)
   if stavkatime > period:
      if balance > 0:
         if int(rx) in range(0, 7000):
            i = balance - balance * 0.1
            i2 = int(i)
            i3 = '{:,}'.format(i2).replace(',', '.')
            await callback.message.answer(  f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🧊 | Игра: GAME-VB
🎟 | Ставка: {balance2}$
🧾 | Проигрыш: {i3}$ [0.1X]            
""", parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
            connect.commit()
            return
         if int(rx) in range(7001, 10000):
            i = balance * 1.5
            i2 = int(i)
            i3 = '{:,}'.format(i2).replace(',', '.')
            await callback.message.answer( f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🧊 | Игра: GAME-VB
🎟 | Ставка: {balance2}$
🧾 | Выигрыш: {i3}$ [1.5X]            
""", parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
            connect.commit()
            return
      else:
         await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств! ", parse_mode='html')
   else:
      await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')         




