from aiogram.fsm.state import State, StatesGroup


class FeedbackSG(StatesGroup):
    GET_FEEDBACK = State()
    GET_ANSWER_TO_USER = State()


class AddRssSG(StatesGroup):
    GET_RSS_URL = State()


class ViewRssSG(StatesGroup):
    SELECT_RSS = State()
    DELETE_RSS_CONFIRMATION = State()
    VIEW_FEED_ERROR = State()
    MORE_DETAILS_VIEW = State()
    VIEW_FEED = State()


class SettingsSG(StatesGroup):
    OVERALL_SETTINGS = State()
    CHANGE_LANGUAGE = State()
    CHANGE_NOTIFICATION_TIME = State()
