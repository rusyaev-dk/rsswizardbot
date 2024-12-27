import random

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from infrastructure.api.models.rss import RSS
from infrastructure.database.repositories.rss_repo import RSSRepository
from l10n.translator import Translator
from tgbot.services.micro_functions import extract_domain, format_error_message


@inject
async def rss_list_getter(
        dialog_manager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository],
        **kwargs
):
    user_id = dialog_manager.event.from_user.id
    user_rss: list[RSS] = await rss_repo.get_all_user_rss(owner_tg_id=user_id)

    rss_list = [
        {
            "name": extract_domain(rss.rss_url),
            "url": rss.rss_url,
            "rss_id": rss.rss_id
        } for rss in user_rss
    ]
    data = {
        "rss_list": rss_list,
        "choose_feed_text": l10n.get_text(key="choose-feed-msg"),
        "close_btn_text": l10n.get_text(key="close-btn"),
        "show_group": len(rss_list) <= 10,
        "show_scrolling_group": len(rss_list) > 10,
    }
    return data


@inject
async def feed_getter(
        dialog_manager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository],
        **kwargs
):
    rss_id = dialog_manager.dialog_data.get("selected_rss_id")
    rss = await rss_repo.get_rss_by_id(rss_id=rss_id)
    entries = dialog_manager.dialog_data.get("entries")

    current_page = dialog_manager.dialog_data.get("current_page", 1)
    per_page = 5
    start = (current_page - 1) * per_page
    end = start + per_page

    total_pages = (len(entries) + per_page - 1) // per_page
    dialog_manager.dialog_data["total_pages"] = total_pages

    page_entries = entries[start:end]
    data = {
        "entries": page_entries,
        "current_page": current_page,
        "total_pages": total_pages,
        "feed_name": extract_domain(rss.rss_url),
        "read_more_text": l10n.get_text(key="read-more"),
        "back_btn_text": l10n.get_text(key="back-btn"),
        "delete_rss_text": l10n.get_text(key="delete-rss-btn"),
        "more_details_text": l10n.get_text(key="more-details-btn"),
        "show_pagination": total_pages > 1
    }
    return data


@inject
async def single_publication_getter(
        dialog_manager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository],
        **kwargs
):
    rss_id = dialog_manager.dialog_data.get("selected_rss_id")
    rss = await rss_repo.get_rss_by_id(rss_id=rss_id)
    entries = dialog_manager.dialog_data.get("entries")

    current_page = dialog_manager.dialog_data.get("current_page", 1)
    per_page = 1
    start = (current_page - 1) * per_page
    end = start + per_page

    total_pages = (len(entries) + per_page - 1) // per_page
    dialog_manager.dialog_data["total_pages"] = total_pages

    page_entries = entries[start:end]

    data = {
        "entries": page_entries,
        "entry_idx": 0,
        "feed_name": extract_domain(rss.rss_url),
        "read_more_text": l10n.get_text(key="read-more"),
        "back_btn_text": l10n.get_text(key="back-btn"),
        "go_to_source_text": l10n.get_text(key="go-to-source"),
        "show_pagination": total_pages > 1,
        "current_page": current_page,
        "total_pages": total_pages,
    }

    return data


@inject
async def feed_error_getter(
        dialog_manager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository],
        **kwargs
):
    status_code = dialog_manager.dialog_data["status_code"]
    error_msg_text = format_error_message(status_code=status_code, l10n=l10n)
    data = {
        "error_msg_text": error_msg_text,
        "back_btn_text": l10n.get_text(key="back-btn"),
        "delete_rss_text": l10n.get_text(key="delete-rss-btn")
    }

    dialog_manager.dialog_data["status_code"] = None
    return data


@inject
async def delete_rss_confirmation_getter(
        dialog_manager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository],
        **kwargs
):
    rss_id = dialog_manager.dialog_data.get("selected_rss_id")
    rss = await rss_repo.get_rss_by_id(rss_id=rss_id)
    rss_url = extract_domain(rss.rss_url)

    data = {
        "confirm_delete_text": l10n.get_text(key="confirm-rss-delete-msg",
                                             args={"rss_url": rss_url}),
        "yes_btn_text": l10n.get_text(key="yes-btn"),
        "no_btn_text": l10n.get_text(key="no-btn"),
    }

    return data
