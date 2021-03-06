from dbapi import DbApi
from telegram import ParseMode
from config import CONFIG

dbApi = DbApi(CONFIG["server_db"], CONFIG["server_user"], CONFIG["server_pass"])

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello There!\n/help for help")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Commands:\n/info\n/status\n/subscribe {username}\n/unsubscribe {username}\n/subscribtions\necho")

def echo(update, context):
    msg = update.message.text
    msg = msg.replace("echo ","")
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def info(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    msg=f"""
chat_id: {chat_id}
user_id: {user_id}
username: {username}
first_name: {first_name}
last_name: {last_name}
"""
    context.bot.send_message(text=msg,chat_id=chat_id)

def status(update, context):
    chat_id = update.effective_chat.id
    if chat_id == CONFIG["chat_id"]:
        text = update.message.text
        print(text)
        if "/status " in text:
            name = text.replace("/status ","")
            print(name)
            if name:
                print(name)
                msg = str(dbApi.adminStatus_for(name))
                context.bot.send_message(text=msg,chat_id=chat_id)
        else:
            msg = dbApi.adminStatus()
            context.bot.send_message(text=msg,chat_id=chat_id)
    else:
        msg = "This is maybe not the right chat"
        context.bot.send_message(text=msg,chat_id=chat_id)

def on_error(update, context):
    print(f"Error: {context.error}")
    context.bot.send_message(text=f"Error: {context.error}",chat_id=CONFIG["chat_id"])

def subscribtions(update, context):
    chat_id=update.effective_chat.id
    msg = str(dbApi.chatSubscribedUsers(chat_id))
    context.bot.send_message(chat_id=chat_id, text=msg)

def subscribe(update, context):
    chat_id=update.effective_chat.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    text=update.message.text
    if "/subscribe " in text:
        name = text.replace("/subscribe ","")
        if name:
            try:
                dbApi.newSubscriber(chat_id,name, username, first_name, last_name)
                msg=f"Subscribed to: {name}"
            except Exception as ex:
                msg=f"Could not subscribe to: {name}\nCheck your /subsribtions"+f"\n{CONFIG['env']}: because of {ex}" if CONFIG["env"]=="dev" else ""
        else:
            msg="No Name Provided"
    else:
        msg="No Name Provided"
    context.bot.send_message(chat_id=chat_id, text=msg)

def unsubscribe(update, context):
    chat_id=update.effective_chat.id
    text=update.message.text
    if "/unsubscribe " in text:
        name = text.replace("/unsubscribe ","")
        if name:
            try:
                dbApi.rmSubscriber(chat_id,name)
                msg=f"Unsubscribed from: {name}"
            except Exception as ex:
                msg=f"Could not unsubscribe from: {name}\nCheck your /subsribtions"+f"\n{CONFIG['env']}: because of {ex}" if CONFIG["env"]=="dev" else ""
        else:
            msg="No Name Provided"
    else:
        msg="No Name Provided"
    context.bot.send_message(chat_id=chat_id, text=msg)