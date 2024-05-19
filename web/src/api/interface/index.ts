// 请求响应参数（不包含data）
export interface Result {
  code: string;
  msg: string;
}

// 请求响应参数（包含data）
export interface ResultData<T = any> extends Result {
  data: T;
}

// 分页响应参数
export interface ResPage<T> {
  list: T[];
  /** 当前分页数 */
  pageNum: number;
  /** 页面最大条目数 */
  pageSize: number;
  /** 总页数 */
  total: number;
}

// 分页请求参数
export interface ReqPage {
  pageNum: number;
  pageSize: number;
}

// 登录模块
export namespace Login {
  export interface ReqLoginForm {
    username: string;
    password: string;
  }
  export interface ResLogin {
    access_token: string;
  }
  export interface ResAuthButtons {
    [key: string]: string[];
  }
}

// 注册模块
export namespace Register {
  export interface ReqRegisterForm {
    id: string;
    username: string;
    password: string;
    repeat_password: string;
    email: string;
    telephone: string;
  }
  export interface ResRegister {
    code: number;
    msg: string;
  }
}

// 系统用户管理模块
export namespace User {
  /** 查询过滤条件 */
  export interface ReqUserParams extends ReqPage {
    username: string;
    id: string;
    email: string;
    createTime: string[];
    status: number;
  }
  /** 返回结果 */
  export interface ResUser {
    id: string;
    auth: number;
    username: string;
    email: string;
    telephone: string;
    createTime: string;
    status: number;
    avatar: string;
  }
  export interface ResStatus {
    userLabel: string;
    userValue: number;
  }
}

// 用户信息模块
export namespace UserInfo {
  export interface BasicInfo {
    id: string;
    name: string;
    avatar: string;
    password: string;
  }
  export interface ContactInfo {
    email: string;
    telephone: string;
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
    danger_heat_limit: number;
    use_danger_composed_limits: boolean;
    danger_composed_limits: SingleCond[];
    warning_heat_limit: number;
    use_warning_composed_limits: boolean;
    warning_composed_limits: SingleCond[];
    auto_star: boolean;
    heat_formula: string;
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
