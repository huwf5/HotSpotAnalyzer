// 后端微服务模块

/** 身份验证接口 */
export namespace AuthPort {
  export const LOGIN = "/login/";
  export const LOGOUT = "/logout/";
  export const REGISTER = "/register/";
  export const ROLE_DICT = "/role/";
  export const CAPTCHA = "/send-code/";
  export const REFRESH = "/token/refresh/";
}

/** 管理接口 */
export namespace ManagePort {
  const USER_BASE_PORT = "/user";
  const WAIT_LIST_PORT = "/waitinglist";
  const WHITE_LIST_PORT = "/whitelist";
  /** 管理员接口 */
  export enum IAdmin {
    DELETE = USER_BASE_PORT + "/delete-multiple/",
    DOWN_GRADE = USER_BASE_PORT + "/downgrade/",
    UP_GRADE = USER_BASE_PORT + "/upgrade/",
    USER_LIST = USER_BASE_PORT + "/list/"
  }
  /** 用户接口 */
  export enum IGuest {
    FORGET_PWD = USER_BASE_PORT + "/forget/",
    DELETE = USER_BASE_PORT + "/delete/",
    UPDATE_PROFILE = USER_BASE_PORT + "/update-profile/",
    GET_PROFILE = USER_BASE_PORT + "/profile/"
  }
  /** 等待列表接口 */
  export enum IWaitList {
    GET_LIST = WAIT_LIST_PORT + "/",
    ACTIVATE = WAIT_LIST_PORT + "/activate/",
    REJECT = WAIT_LIST_PORT + "/bulk-delete/"
  }
  /** 邮箱白名单接口 */
  export enum IWhiteList {
    GET_LIST = WHITE_LIST_PORT + "/list/",
    GET_TAGS = WHITE_LIST_PORT + "/get-tags/",
    ADD_TO_LIST = WHITE_LIST_PORT + "/add/",
    DELETE_FROM_LIST = WHITE_LIST_PORT + "/delete/",
    ADD_TAG = WHITE_LIST_PORT + "/add-tag/",
    DELETE_TAG = WHITE_LIST_PORT + "/delete-tag/",
    ACTIVATE = WHITE_LIST_PORT + "/activate/",
    DEACTIVATE = WHITE_LIST_PORT + "/deactivate/"
  }
}

/** 消息接口 */
export namespace MessagePort {
  const MESSAGE_SETTINGS_BASE_PORT = "/messagesetting";
  export const MSG_BASE_PORT = "/usermessage";
  export enum MSG_SETTINGS {
    BASE = MESSAGE_SETTINGS_BASE_PORT + "/",
    UPDATE = MESSAGE_SETTINGS_BASE_PORT + "/update/"
  }
}

/** 事件分析接口 */
export namespace AnalysisPort {
  /** 数据大屏接口 */
  export enum MAIN {
    STATISTICS = "/cardlist/fetch_card_list/",
    LINE_CHART = "/chartData/fetch_chart_data/",
    EMOTION = "/emotion/fetch_emotions/",
    WORD_CLOUD = "/wordcloud/fetch_word_cloud",
    TOPICS = "/topiccard/fetch_topic_card/",
    GRAPH3D = "/graphs/fetch_graph/"
  }
  /** 搜索页面接口 */
  export enum SEARCH {
    ALL_EVENTS = "/allEvents/fetch_events/",
    SEARCH_EVENTS = "searchEvents/fetch_event/"
  }
  /** 详细页面接口 */
  export enum DETAIL {
    EVENT = "/event/fetch_event/",
    SENTIMENT = "/senti/fetch_sentiment/"
  }
}
