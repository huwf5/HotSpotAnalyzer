// 请求响应参数（不包含data）
export interface Result {
  message: string;
}

// 请求响应参数（包含data）
export interface ResultData<T = any> extends Result {
  data: T;
}

// 分页响应参数
export interface ResDataList<T> extends Result {
  data: T[];
}

// 分页请求参数
export interface ReqPage {
  pageNum: number;
  pageSize: number;
}

// 登录模块
export namespace Login {
  export interface ReqLoginForm {
    email: string;
    password: string;
  }
  export interface ReqRefresh {
    refresh: string;
  }
  export interface ReqLogout {
    refresh: string;
  }
  export interface ReqForgetPwd {
    email: string;
    verify_code: string;
    password: string;
  }
  export interface ResLogin {
    email: string;
    username: string;
    role: string;
    token: string;
    refresh: string;
    token_lifetime: number;
    refresh_lifetime: number;
  }
  export interface ResAuthButtons {
    [key: string]: string[];
  }
  export interface ResRefresh {
    refresh: string;
    access: string;
  }
}

// 注册模块
export namespace Register {
  export interface ReqRegisterForm {
    username: string;
    password: string;
    repeat_password: string;
    email: string;
    captcha: string;
  }
  export enum CodeUsage {
    REGISTER = "register",
    RESETPWD = "reset_password"
  }
  export interface ReqEmailCaptcha {
    email: string;
    usage: CodeUsage;
  }
}

// 系统用户管理模块
export namespace User {
  /** 查询过滤条件 */
  export interface EmailList {
    emailList: string[];
  }
  /** 返回结果 */
  export interface ResUser {
    username: string;
    email: string;
    role: number;
  }
  export interface RoleDict {
    id: number;
    role: string;
  }
  /** 等待激活用户 */
  export interface ResPendingUser {
    username: string;
    email: string;
    role: number;
  }
  export interface ResStatus {
    userLabel: string;
    userValue: number;
  }
}

// 用户信息模块
export namespace UserInfo {
  export interface ResUserProfile {
    username: string;
    email: string;
    role: string;
  }
  export interface ReqUpdate {
    username?: string;
    password?: string;
  }
  export interface BasicInfo {
    name: string;
  }
  export interface ContactInfo {
    email: string;
  }
  export interface AccountInfo {
    role: string;
  }
}

// 邮箱后缀白名单模块
export namespace WhiteList {
  export interface ReqOnWhiteList {
    format: string;
  }
  export interface ReqOnTags {
    email_format: string;
    email_tag: string;
  }
  export interface ResWhiteList {
    format: string;
    is_active: boolean;
  }
  export interface ResTags {
    id: number;
    email_format: string;
    email_tag: string;
  }
}

// 消息模块
export namespace Messages {
  export interface ReqMessageSetting {
    allow_non_news: boolean;
    warning_threshold: number;
    info_threshold: number;
  }
  export interface ReqMessages {
    id: number;
    is_starred: boolean;
    is_read: boolean;
  }
  export enum MessageType {
    WARN = "warn",
    INFO = "info"
  }
  export interface ResMessage {
    id: number;
    type: MessageType;
    is_starred: boolean;
    is_read: boolean;
    message: {
      id: number;
      title: string;
      summary: string;
      negative_sentiment_ratio: number;
      is_news: boolean;
      created_at: string;
    };
  }
  export interface ResMessageSetting {
    allow_non_news: boolean;
    warning_threshold: number;
    info_threshold: number;
  }
}
