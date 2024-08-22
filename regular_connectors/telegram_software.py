from telegram import Bot,InlineKeyboardButton,InlineKeyboardMarkup,ForceReply,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InputMediaPhoto,InputMediaVideo,InputMediaAudio,InputMediaDocument
import json
async def telegram_get_chat_info(params,cred):
    """
    Get information about a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A JSON string containing information about the chat.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.get_chat(**data)
            await bot.shutdown()
            return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_get_chat_administrators(params,cred):
    """
    Get a list of administrators in a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A JSON string containing information about the administrators in the chat.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.get_chat_administrators(**data)
            admin_data = []
            for admin in chat:
                admin_data.append(admin.to_dict())
            await bot.shutdown()
            return json.dumps(admin_data)
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
    
async def telegram_leave_chat(params,cred):
    """
    Leave a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of leaving the chat.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.leave_chat(**data)
            await bot.shutdown()
            return 'Success'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_get_chat_member(params,cred):
    """
    Get information about a chat member using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - user_id (int): Unique identifier for the target user. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A JSON string containing information about the chat member.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'user_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.get_chat_member(**data)
            await bot.shutdown()
            return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
    
async def telegram_set_description(params,cred):
    """
    Set the description of a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - description (str): The new description to be set for the chat. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of setting the description.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'description' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.set_chat_description(**data)
            await bot.shutdown()
            return 'Description set successfully'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_set_title(params,cred):
    """
    Set the title of a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - title (str): The new title to be set for the chat. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of setting the title.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'title' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.set_chat_title(**data)
            await bot.shutdown()
            return 'Title set successfully'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
    
async def telegram_delete_chat_message(params,cred):
    """
    Delete a message from a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - message_id (int): Identifier of the message to be deleted. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of deleting the message.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'message_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.delete_message(**data)
            await bot.shutdown()
            return 'Message Deleted successfully'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
    
async def telegram_pin_message(params,cred):
    """
    Pin a message in a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - message_id (int): Identifier of the message to be pinned. (required)
        - disable_notification (bool): Pass True to disable notification for the pinned message. (optional)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of pinning the message.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'message_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.pin_chat_message(**data)
            await bot.shutdown()
            return 'Message pinned successfully'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
  
async def telegram_unpin_message(params,cred):
    """
    Unpin a message in a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - message_id (int): Identifier of the message to be unpinned. (required)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of unpinning the message.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'message_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.unpin_chat_message(**data)
            await bot.shutdown()
            return 'Message unpinned successfully.'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)


async def telegram_send_chat_action(params,cred):
    """
    Send a chat action to a chat using the Telegram API.

    :param dict params:
        - chat_id (int or str): Unique identifier for the target chat. (required)
        - action (str): Type of action to broadcast.(required)

    :param str token:
        The bot token for authentication. (required)

    :return: A string indicating the success of sending the chat action.
    :rtype: str

    """
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'action' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.send_chat_action(**data)
            await bot.shutdown()
            return 'Success.'
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
    

async def telegram_edit_message_text(params,cred):
    try:
        creds=json.loads(cred)
        if ('chat_id' in params and 'message_id' in params and 'text' in params) or ('inline_message_id' in params and 'text' in params) :
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                chat = await bot.edit_message_text(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.edit_message_text(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_send_audio(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'audio' in params :
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                elif "ReplyKeyboard" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["ReplyKeyboard"]["KeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = KeyboardButton(
                            text=button_info.get('text'),
                            request_contact=button_info.get('request_contact', None),
                            request_location=button_info.get('request_location', None),
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=ReplyKeyboardMarkup(keyboard=inline)
                elif "Force" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Force"]
                    data2['reply_markup']=ForceReply(selective=inline_keyboard.get('selective'))
                elif "Remove" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Remove"]
                    data2['reply_markup']=ReplyKeyboardRemove(selective=inline_keyboard.get('selective'))
                chat = await bot.send_audio(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.send_audio(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
    

async def telegram_send_document(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'document' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                elif "ReplyKeyboard" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["ReplyKeyboard"]["KeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = KeyboardButton(
                            text=button_info.get('text'),
                            request_contact=button_info.get('request_contact', None),
                            request_location=button_info.get('request_location', None),
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=ReplyKeyboardMarkup(keyboard=inline)
                elif "Force" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Force"]
                    data2['reply_markup']=ForceReply(selective=inline_keyboard.get('selective'))
                elif "Remove" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Remove"]
                    data2['reply_markup']=ReplyKeyboardRemove(selective=inline_keyboard.get('selective'))
                chat = await bot.send_document(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.send_document(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_send_location(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'latitude' in params and 'longitude' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                elif "ReplyKeyboard" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["ReplyKeyboard"]["KeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = KeyboardButton(
                            text=button_info.get('text'),
                            request_contact=button_info.get('request_contact', None),
                            request_location=button_info.get('request_location', None),
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=ReplyKeyboardMarkup(keyboard=inline)
                elif "Force" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Force"]
                    data2['reply_markup']=ForceReply(selective=inline_keyboard.get('selective'))
                elif "Remove" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Remove"]
                    data2['reply_markup']=ReplyKeyboardRemove(selective=inline_keyboard.get('selective'))
                chat = await bot.send_location(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.send_location(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_send_media_group(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'media' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            data2={
                'media':[],
            }
            for item in data.get("media", []):
                for media_type, media_info in item.items():
                    if media_type == "Photo":
                        caption = media_info.get('caption', None)
                        data2['media'].append(InputMediaPhoto(media=media_info['media'], caption=caption))
                    elif media_type == "Video":
                        caption = media_info.get('caption', None)
                        data2['media'].append(InputMediaVideo(media=media_info['media'], caption=caption))
                    elif media_type == "Audio":
                        caption = media_info.get('caption', None)
                        data2['media'].append(InputMediaAudio(media=media_info['media'], caption=caption))
                    elif media_type == "Document":
                        caption = media_info.get('caption', None)
                        data2['media'].append(InputMediaDocument(media=media_info['media'], caption=caption))
            for key, value in data.items():
                if key=="media":
                    continue
                if value:
                    data2[key] = value
            chat = await bot.send_media_group(**data2)
            media_data = []
            for media in chat:
                media_data.append(media.to_dict())
            await bot.shutdown()
            return json.dumps(media_data)
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_send_message(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'text' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                elif "ReplyKeyboard" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["ReplyKeyboard"]["KeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = KeyboardButton(
                            text=button_info.get('text'),
                            request_contact=button_info.get('request_contact', None),
                            request_location=button_info.get('request_location', None),
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=ReplyKeyboardMarkup(keyboard=inline)
                elif "Force" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Force"]
                    data2['reply_markup']=ForceReply(selective=inline_keyboard.get('selective'))
                elif "Remove" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Remove"]
                    data2['reply_markup']=ReplyKeyboardRemove(selective=inline_keyboard.get('selective'))
                chat = await bot.send_message(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.send_message(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_send_photo(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'photo' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                elif "ReplyKeyboard" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["ReplyKeyboard"]["KeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = KeyboardButton(
                            text=button_info.get('text'),
                            request_contact=button_info.get('request_contact', None),
                            request_location=button_info.get('request_location', None),
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=ReplyKeyboardMarkup(keyboard=inline)
                elif "Force" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Force"]
                    data2['reply_markup']=ForceReply(selective=inline_keyboard.get('selective'))
                elif "Remove" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Remove"]
                    data2['reply_markup']=ReplyKeyboardRemove(selective=inline_keyboard.get('selective'))
                chat = await bot.send_photo(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.send_photo(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)

async def telegram_send_video(params,cred):
    try:
        creds=json.loads(cred)
        if 'chat_id' in params and 'video' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if "reply_markup" in data:
                data2={}
                for key, value in data.items():
                    if key=="reply_markup":
                        continue
                    if value:
                        data2[key] = value
                if "Inline" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Inline"]["InlineKeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = InlineKeyboardButton(
                            text=button_info.get('text'),
                            url=button_info.get('url', None),
                            switch_inline_query=button_info.get('switch_inline_query', None),
                            switch_inline_query_current_chat=button_info.get('switch_inline_query_current_chat', None),
                            callback_data=button_info.get('callback_data', None),
                            pay=button_info.get('pay', False)
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=InlineKeyboardMarkup(inline)
                elif "ReplyKeyboard" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["ReplyKeyboard"]["KeyboardButton"]
                    inline = []
                    for button_info in inline_keyboard:
                        inline_button = KeyboardButton(
                            text=button_info.get('text'),
                            request_contact=button_info.get('request_contact', None),
                            request_location=button_info.get('request_location', None),
                        )
                        inline.append([inline_button])
                    data2['reply_markup']=ReplyKeyboardMarkup(keyboard=inline)
                elif "Force" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Force"]
                    data2['reply_markup']=ForceReply(selective=inline_keyboard.get('selective'))
                elif "Remove" in data['reply_markup']:
                    inline_keyboard = data['reply_markup']["Remove"]
                    data2['reply_markup']=ReplyKeyboardRemove(selective=inline_keyboard.get('selective'))
                chat = await bot.send_video(**data2)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
            else:
                chat = await bot.send_video(**data)
                await bot.shutdown()
                return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)


async def telegram_get_file(params,cred):
    try:
        creds=json.loads(cred)
        if 'file_id' in params:
            bot = Bot(token=creds['accessToken'])
            await bot.initialize()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            chat = await bot.get_file(**data)
            await bot.shutdown()
            return json.dumps(chat.to_dict())
        else:
            raise Exception('Missing parameters')
    except Exception as e:
        raise Exception(e)
