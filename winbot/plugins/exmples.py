from pyrogram import Client, filters
from .Utils.button import ButtonMaker


#example fpr sending photo
@Client.on_message(filters.command("photo"))
async def photo(app,message):
    await app.send_photo(message.chat.id,"https://upload.wikimedia.org/wikipedia/en/thumb/2/2c/One_Piece_Logo.svg/1024px-One_Piece_Logo.svg.png")


# Example for sending a normal button
@Client.on_message(filters.command("nbutton"))
async def nbutton(app,message):
    buttons = ButtonMaker()
    buttons.ibutton("click me", "b1")
    reply_markup = buttons.build_menu(2)
    await app.send_message(message.chat.id,text="Normal button",reply_markup=reply_markup)

#Example for url button
@Client.on_message(filters.command("ubutton"))
async def ubutton(app,message):
    buttons = ButtonMaker()
    buttons.ubutton(
        "Repo Url", "https://github.com/darkdeathoriginal/Winbot")
    reply_markup = buttons.build_menu(1)
    await app.send_message(message.chat.id,text="Url button",reply_markup=reply_markup)

#Example for how to handle normal button
# @Client.on_callback_query()
# async def handle_callback(client, callback_query):
#     data = callback_query.data
#     chat_id = callback_query.message.chat.id
#     if data == "b1":
#         await client.send_message(chat_id, "You clicked Button 1!")

#         updated_keyboard = callback_query.message.reply_markup
#         for row in updated_keyboard.inline_keyboard:
#             for button in row:
#                 if button.callback_data == data:
#                     button.callback_data = f"clicked"
#         await callback_query.message.edit_reply_markup(updated_keyboard)

