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
  export const titles = ["系统消息", "预警消息", "警告消息"];
  export const platforms = ["Bilibili", "小红书", "微博"];
  export interface Message {
    id: number;
    display: boolean;
    /** 0表示系统消息，1表示预警消息，2表示警告消息 */
    type: number;
    starred: boolean;
    unread: boolean;
    time: string;
    content: string;
  }
  export interface Event extends Message {
    platform: number;
    keywords: string;
    title: string;
  }
  export const conds = ["👍点赞数", "❤喜爱数", "✨转发数"];
  export const predicators = ["大于＞", "小于＜", "大于等于≥", "小于等于≤"];
  export interface SingleCond {
    /** 0表示点赞数，1表示喜爱数，2表示转发数，其它表示空 */
    key: number;
    /** 0表示大于，1表示小于，2表示大于等于，3表示小于等于 */
    predicator: number;
    limit: number;
  }
  export interface ReqMessages {
    id: number;
    starred?: boolean;
    unread?: boolean;
  }
  export interface ResMessageSettings {
    // use_danger_heat_limit: boolean;
    // danger_heat_limit: number;
    // use_warning_heat_limit: boolean;
    // warning_heat_limit: number;
    // heat_formula: string;

    use_danger_composed_limits: boolean;
    danger_composed_limits: SingleCond[];
    use_warning_composed_limits: boolean;
    warning_composed_limits: SingleCond[];
    auto_star: boolean;
  }
  export interface ReqMessageSettings {
    danger_heat_limit?: number;
    danger_compsed_limit?: SingleCond[];
    warning_heat_limit?: number;
    warning_compsed_limit?: SingleCond[];
    auto_star?: boolean;
    heat_formula?: string;
  }
}
