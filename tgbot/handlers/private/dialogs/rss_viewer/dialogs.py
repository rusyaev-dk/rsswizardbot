from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Row, Select, SwitchTo, Group
from aiogram_dialog.widgets.text import Format, Const, Jinja

from tgbot.handlers.private.dialogs.rss_viewer.callable import *
from tgbot.handlers.private.dialogs.rss_viewer.getters import feed_getter, rss_list_getter, \
    delete_rss_confirmation_getter, feed_error_getter, single_publication_getter
from tgbot.misc.states import ViewRssSG


rss_list_window = Window(
    Format("{choose_feed_text}"),
    Group(
        Select(
            text=Format("{item[name]}"),
            items="rss_list",
            item_id_getter=lambda item: item["rss_id"],
            id="select_rss",
            on_click=select_rss_feed,
        ),
        width=2,
        id="rss_lents_group",
        when="show_group",
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[name]}"),
            items="rss_list",
            item_id_getter=lambda item: item["rss_id"],
            id="select_rss",
            on_click=select_rss_feed,
        ),
        height=4,
        width=2,
        id="rss_lents_scrolling_group",
        when="show_scrolling_group",
    ),
    Button(
        Format("{close_btn_text}"),
        id="close",
        on_click=close_feed_viewer
    ),
    state=ViewRssSG.SELECT_RSS,
    getter=rss_list_getter,
)

view_feed_window = Window(
    Jinja(
            "📢 <b>{{ feed_name }}</b>\n\n"
            "{% for entry in entries %}"
            "📄 <b>{{ entry.title }}</b>\n"
            "{% if entry.short_summary %}"
            "▪️ <i>{{ entry.short_summary }}</i>\n"
            "{% endif %}"
            "🔗 <a href='{{ entry.link }}'>{{ read_more_text }}</a>\n\n"
            "{% endfor %}"
        ),
    Row(
        Button(
            Const("⬅️"),
            id="prev_page_btn",
            on_click=prev_page
        ),
        Button(
            Jinja("{{current_page}}/{{total_pages}}"),
            id="current_page_btn",
            on_click=None
        ),
        Button(
            Const("➡️"),
            id="next_page_btn",
            on_click=next_page
        ),
        when="show_pagination",
    ),
    Button(
        Format("{more_details_text}"),
        id="more_details_btn",
        on_click=more_details,
    ),
    Row(
        Button(
            Format("{back_btn_text}"),
            id="back_btn",
            on_click=cancel_feed_viewer
        ),
        SwitchTo(
            Format("{delete_rss_text}"),
            id="delete_rss_btn",
            state=ViewRssSG.DELETE_RSS_CONFIRMATION
        ),
    ),
    disable_web_page_preview=True,
    state=ViewRssSG.VIEW_FEED,
    getter=feed_getter,
)

view_feed_error_window = Window(
    Format("{error_msg_text}"),
    SwitchTo(
        Format("{delete_rss_text}"),
        id="delete_rss_btn",
        state=ViewRssSG.DELETE_RSS_CONFIRMATION
    ),
    Button(
        Format("{back_btn_text}"),
        id="back_btn",
        on_click=cancel_feed_viewer
    ),
    disable_web_page_preview=True,
    state=ViewRssSG.VIEW_FEED_ERROR,
    getter=feed_error_getter,
)

more_details_window = Window(
    Jinja(
        "📢 <b>{{ feed_name }}</b>\n\n"
        "🔗 <a href='{{ entries[entry_idx].link }}'>{{ go_to_source_text }}</a>"
    ),
    Row(
        Button(
            Const("⬅️"),
            id="prev_page_btn",
            on_click=prev_page
        ),
        Button(
            Jinja("{{current_page}}/{{total_pages}}"),
            id="current_page_btn",
            on_click=None
        ),
        Button(
            Const("➡️"),
            id="next_page_btn",
            on_click=next_page
        ),
        when="show_pagination",
    ),
    Button(
        Format("{back_btn_text}"),
        id="back_btn",
        on_click=cancel_single_pub_viewer
    ),
    state=ViewRssSG.MORE_DETAILS_VIEW,
    getter=single_publication_getter
)

delete_rss_window = Window(
    Format("{confirm_delete_text}"),
    Row(
        Button(
            Format("{yes_btn_text}"),
            id="confirm_delete",
            on_click=delete_rss
        ),
        SwitchTo(
            Format("{no_btn_text}"),
            id="decline_delete",
            state=ViewRssSG.VIEW_FEED
        ),
    ),
    state=ViewRssSG.DELETE_RSS_CONFIRMATION,
    getter=delete_rss_confirmation_getter
)

rss_dialog = Dialog(
    rss_list_window,
    view_feed_window,
    view_feed_error_window,
    more_details_window,
    delete_rss_window
)
