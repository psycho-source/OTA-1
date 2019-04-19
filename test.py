import json
from os import environ
from argparse import ArgumentParser

from requests import post

def arg_parse():
    global message, mode, caption, silent, photo, gif, video, note, audio, voice, file, send, out
    switches = ArgumentParser()
    group = switches.add_mutually_exclusive_group(required=True)
    group.add_argument("-M", "--message", help="Text message")
    group.add_argument("-P", "--photo", help="Photo path")
    group.add_argument("-G", "--gif", help="GIF Photo path")
    group.add_argument("-V", "--video", help="Video path")
    group.add_argument("-N", "--note", help="Video Note path")
    group.add_argument("-A", "--audio", help="Audio path")
    group.add_argument("-O", "--voice", help="Voice path")
    group.add_argument("-F", "--file", help="File path")
    switches.add_argument("-t", "--token", required=True, help="Telegram bot token")
    switches.add_argument("-c", "--chat", required=True, help="Chat to use as recipient")
    switches.add_argument("-m", "--mode", help="Text parse mode - HTML/Markdown", default="Markdown")
    switches.add_argument("-p", "--preview", help="Disable URL preview - yes/no", default="yes")
    switches.add_argument("-s", "--silent", help="Disable Notification Sound - yes/no", default="no")
    switches.add_argument("-d", "--output", help="Disable Script output - yes/no", default="yes")
    switches.add_argument("-C", "--caption", help="Media/Document caption")
    
    args = vars(switches.parse_args())
    token = args["token"]
    chat = args["chat"]
    message = args["message"]
    photo = args["photo"]
    gif = args["gif"]
    video = args["video"]
    note = args["note"]
    audio = args["audio"]
    voice = args["voice"]
    file = args["file"]
    mode = args["mode"]
    preview = args["preview"]
    silent = args["silent"]
    out = args["output"]
    caption = args["caption"]
    
    if message is not None:
        send = "text"
    elif photo is not None:
        send = "photo"
    elif gif is not None:
        send = "gif"
    elif video is not None:
        send = "video"
    elif note is not None:
        send = "note"
    elif audio is not None:
        send = "audio"
    elif voice is not None:
        send = "voice"
    elif file is not None:
        send = "file"
        
def send_format():
    global token, chat
# telegram variables
    bottoken = environ['bottoken']
    chat = "@test_channel_68"
# load the json file
with open('latest.json') as f:
    info = json.load(f)
# parse the json into telegram message
data = []
data.append('⚡️PixysOS Update⚡\n\n')
data.append('➡ *New build available for* *{}* *{}* \n'.format(info[0]['name'], info[0]['codename']))
data.append('👤 *By:* {} \n\n'.format(info[0]['maintainer_name']))

data.append('📆 *Build Date:* {}\n'.format(info[0]['build_date']))
data.append('ℹ *Build Version:* {} \n'.format(info[0]['version']))
data.append('ℹ *Build Type:* {} \n\n'.format(info[0]['build_type']))

data.append('⬇️ [Download Now: ]({}) \n'.format(info[0]['url']))
data.append('⬇️ [XDA Thread Link: ]({}) \n\n'.format(info[0]['xda_thread']))

#data.append('#```{}```#```{}```\n'.format(info[0]['rom_tag'], info[0]['codename']))
# remove empty entries
for i in data:
    if ': \n' in i or '()' in i:
        data.remove(i)
# create the message
message = ''.join(data)

def send_message():
    global r, status, response
    if send == "text":
        params = (
            ('chat_id', chat),
            ('text', message),
            ('parse_mode', "Markdown"),
            ('disable_notification', silent),
            ('disable_web_page_preview', preview)
        )
        url = "https://api.telegram.org/bot" + token + "/sendMessage"
        r = post(url, params=params)
    elif send == "photo":
        files = {
            'chat_id': (None, chat),
            'caption': (None, caption),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'photo': (photo, open(photo, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendPhoto"
        r = post(url, files=files)
    elif send == "gif":
        files = {
            'chat_id': (None, chat),
            'caption': (None, caption),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'animation': (gif, open(gif, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendAnimation"
        r = post(url, files=files)
    elif send == "video":
        files = {
            'chat_id': (None, chat),
            'caption': (None, caption),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'video': (video, open(video, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendVideo"
        r = post(url, files=files)
    elif send == "note":
        files = {
            'chat_id': (None, chat),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'video_note': (note, open(note, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendVideoNote"
        r = post(url, files=files)
    elif send == "audio":
        files = {
            'chat_id': (None, chat),
            'caption': (None, caption),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'audio': (audio, open(audio, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendAudio"
        r = post(url, files=files)
    elif send == "voice":
        files = {
            'chat_id': (None, chat),
            'caption': (None, caption),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'voice': (voice, open(voice, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendVoice"
        r = post(url, files=files)
    elif send == "file":
        files = {
            'chat_id': (None, chat),
            'caption': (None, caption),
            'parse_mode': (None, mode),
            'disable_notification': (None, silent),
            'document': (file, open(file, 'rb')),
        }
        url = "https://api.telegram.org/bot" + token + "/sendDocument"
        r = post(url, files=files)
    else:
        print("Error!")
    status = r.status_code
    response = r.reason
    
def req_status():
    if out == 'yes':
        if status == 200:
            print("Message sent")
        elif status == 400:
            print("Bad recipient / Wrong text format")
        elif status == 401:
            print("Wrong / Unauthorized token")
        else:
            print("Unknown error")
        print("Response: " + response)


arg_parse()
send_format()
send_message()
req_status()
