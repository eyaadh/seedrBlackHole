from bh.helpers import Common
from pyrogram import emoji, Client, filters
from bh.helpers.radarr import RadarrProcessor
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Client.on_inline_query()
async def inline_query_handler(c: Client, iq: InlineQuery):
    q = iq.query
    q_res_data = await RadarrProcessor().search_movie(q)
    res = []
    if q_res_data is not None:
        if q_res_data is not None:
            for movie in q_res_data:
                if 'title' in movie:
                    if 'imdbId' in movie:
                        res.append(
                            InlineQueryResultArticle(
                                title=movie['title'],
                                description=f"{movie['overview']}",
                                thumb_url=movie[
                                    'remotePoster'] if 'remotePoster' in movie else 'https://1080motion.com/wp-content/uploads/2018/06/NoImageFound.jpg.png',
                                input_message_content=InputTextMessageContent(
                                    message_text=f"<a href=https://www.imdb.com/title/"
                                                 f"{movie['imdbId'] if 'imdbId' in movie else None}>"
                                                 f"<b>{movie['title']}</b></a>\n{movie['overview']}",
                                    parse_mode="html"
                                ),
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton(
                                                text=f"{emoji.ROCKET} Add This Movie to Library",
                                                callback_data=f"radarrad_{movie['imdbId']}"
                                            )
                                        ]
                                    ]
                                )
                            )
                        )

        if res:
            await iq.answer(
                results=res,
                cache_time=0,
                is_personal=False
            )


@Client.on_callback_query(filters.regex('^radarrad.*'))
async def radarrad_handler(c: Client, cb: CallbackQuery):
    if cb.from_user.id in Common().app_sudo_users:
        cb_data = cb.data.split('_')
        if len(cb_data) > 1:
            imdb_id = cb_data[1]
            await RadarrProcessor().add_movie(imdb_id)
            await cb.answer(
                "Your request has been sent to Radarr!",
                show_alert=True
            )
            await cb.edit_message_reply_markup()
    else:
        await cb.answer(
            "You are not allowed to approve this request. An admin should accept it first!",
            show_alert=True
        )
