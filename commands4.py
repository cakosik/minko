from imports import *



async def new_chat_content_types(message):
    user = message.new_chat_members[0].username
    user_id = message.new_chat_members[0].id
    user_name = message.new_chat_members[0].first_name
    group_name = message.chat.full_name
    status_bot = message.new_chat_members[0].is_bot

    

    if user == config.bot_name:

        chat_id = message.chat.id
        cursor.execute(f"SELECT chat_id FROM chats WHERE chat_id = '{chat_id}'")

        if cursor.fetchone() is None:
            text = f'''
        💭 <code>{user_name}</code> , вы <b>успешно зарегистрировали</b> чат <code>{group_name}</code> 
            '''
            time_register = f'{datetime.now()}'
            
            cursor.execute("INSERT INTO chats VALUES(?, ?, ?);", (chat_id, group_name, time_register[:19]))
            connect.commit()

            await message.answer(text, parse_mode='html')
        else:
            pass

        text = f'''
🎯Я игровой бот <b>{config.full_bot_name}</b> 
🙏 Спасибо что <b>добавили меня</b> в чат <code>{group_name}</code> | Вы можете его <b>зарегистрировать чат в боте</b> командой <code>/register_chat</code>
❗️ Для того чтобы я работал в вашем чате, мне нужны <b>права администратора</b>
        '''
    elif status_bot == True:
        text = f'''
❗️ В чат <b>добавили бота</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>
➖➖➖➖➖➖➖➖➖➖➖➖
🔎 <b>АЙДИ :</b> <code>{user_id}</code>
🧷 <b>ЮЗЕР :</b> <b>@{user}</b>
👤 <b>ИМЯ :</b> <code>{user_name}</code>
        '''
    else:       

        msg = message
        user_name1 = 'Игрок'
        user_status = "Player"
        status_block = 'off'
        stats_status = 'off'
        pref = 'Игрок'
        status_console = 'off'
        avatarka_start = 'none'
        klan_index = 0
        status_family = 0
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
            
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name1, user_name, user_status, config.start_money, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status))
            cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, user_name,status_block, 0, 0, 0, 0, 0))
            cursor.execute("INSERT INTO farm VALUES(?, ?, ?, ?, ?);",(user_id, user_name,status_block, 0, 0))
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

            print(f'Зарегестрировался в боте пользователь: {user_name}')
        else:
            pass
            
        chat_id = message.chat.id
        print(chat_id)
        if chat_id == config.chat_id:

            status_wdzy = cursor.execute(f'SELECT status from wdzy').fetchone()
            status_wdzy = status_wdzy[0]

            if status_wdzy == 'on':
                summ_wdzy = cursor.execute(f'SELECT summ from wdzy').fetchone()
                summ_wdzy = int(summ_wdzy[0])

                left_user_id = message.from_user.id
                
                if left_user_id == user_id:
                    return

                left_balance = cursor.execute(f'SELECT balance from users where user_id = {left_user_id}').fetchone()
                left_balance = int(left_balance[0])

                left_user_name = cursor.execute(f'SELECT user_name from users where user_id = {left_user_id}').fetchone()
                left_user_name = str(left_user_name[0])

                cursor.execute(f'UPDATE users SET balance = {left_balance + summ_wdzy} where user_id = {left_user_id}')
                connect.commit()
                
                text = f'''
🎁 {left_user_name} вы получили <code>{'{:,}'.format(summ_wdzy).replace(',','.')}$</code> за <b>добавление участника </b>
                '''
                
                try:
                    await message.bot.send_message(left_user_id, text, parse_mode='html')
                except:
                    pass

            else:
                pass
        else:
            pass

        text = f'''
👋 <b>Добро пожаловать <a href='tg://user?id={user_id}'>{user_name}</a> в чат</b> <code>{group_name}</code>
    '''

    await message.answer(text, parse_mode='html')
