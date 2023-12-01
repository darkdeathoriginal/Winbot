from pyrogram import Client
from pyrogram.types import Message
from .Utils.button import ButtonMaker
from .Utils.manga import getSearchResult,getImages,getChapter,images_to_pdf
from ..handler import Module
import os
  

msg =''


async def run(app:Client,message:Message,match:str):
    global msg
    if match == "":
        return await app.send_message(message.chat.id,"example: /manga naruto")
    text = match
    buttons = ButtonMaker()
    n=1
    
    for i in getSearchResult(text):
        buttons.ibutton(i["title"], f"search,{i['link']}")
        n+=1
    reply_markup = buttons.build_menu(1)
    msg =await app.send_message(message.chat.id,text="Showing result for "+text,reply_markup=reply_markup)


chapters =[]
@Client.on_callback_query()
async def handle_callback(app, m):
    global chapters,msg
    data = m.data
    chat_id = m.message.chat.id
    if data.startswith('search'):
        await m.answer()
        link = data.split(",")[1]

        buttons = ButtonMaker()
        chapters = getChapter(link)
        if(len(chapters)>20):
            for i in chapters[0:20]:
                buttons.ibutton(i["title"], f"ch,{i['link']}")
            buttons.ibutton('more','more,1','footer')

        else:
            for i in chapters:
                buttons.ibutton(i["title"], f"ch,{i['link']}")
    
        reply_markup = buttons.build_menu(1)
        await msg.edit(text="Available chapters",reply_markup=reply_markup)

    elif data.startswith("more"):
        await m.answer()
        n = int(data.split(',')[1])
        buttons = ButtonMaker()
        if n==0:
            for i in chapters[0:20]:
                buttons.ibutton(i["title"], f"ch,{i['link']}")
            buttons.ibutton('more','more,1','footer')
        elif len(chapters)<(n*20)+20:
            for i in chapters[n*20:]:
                buttons.ibutton(i["title"], f"ch,{i['link']}")
        else:
            for i in chapters[n*20:(n*20)+20]:
                buttons.ibutton(i["title"], f"ch,{i['link']}")
            buttons.ibutton('prev',f'more,{n-1}','footer')
            buttons.ibutton('next',f'more,{n+1}','footer')
        reply_markup = buttons.build_menu(1)
        await msg.edit(text="Available chapters",reply_markup=reply_markup)
    elif data.startswith("ch"):
        await m.answer()
        await msg.delete()
        msg = await app.send_message(chat_id,"Please wait..")
        id = data.split(",")[1]
        images,title = getImages(id)
        path = title+".pdf"
        images_to_pdf(images, path)
        await msg.delete()
        await app.send_document(chat_id, path, caption=title)
        os.remove(path)


Module({
    "name":"manga",
    "description":"Manga downloader"
},run)