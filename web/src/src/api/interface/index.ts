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
  pageNum: number;
  pageSize: number;
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

// 用户管理模块
export namespace User {
  export interface ReqUserParams extends ReqPage {
    username: string;
    gender: number;
    idCard: string;
    email: string;
    address: string;
    createTime: string[];
    status: number;
  }
  export interface ResUserList {
    id: string;
    username: string;
    gender: number;
    user: { detail: { age: number } };
    idCard: string;
    email: string;
    address: string;
    createTime: string;
    status: number;
    avatar: string;
    photo: any[];
    children?: ResUserList[];
  }
  export interface ResStatus {
    userLabel: string;
    userValue: number;
  }
  export interface ResGender {
    genderLabel: string;
    genderValue: number;
  }
  export interface ResDepartment {
    id: string;
    name: string;
    children?: ResDepartment[];
  }
  export interface ResRole {
    id: string;
    name: string;
    children?: ResDepartment[];
  }
}

// 消息模块
export namespace Messages {
  export const titles = ["系统消息", "预警消息", "警告消息"];
  export const platforms = ["Bilibili", "小红书", "微博"];
  export interface Message {
    id: number;
    display: boolean;
    /**
     * 0表示系统消息，1表示预警消息，2表示警告消息
     */
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
    /**
     * 0表示点赞数，1表示喜爱数，2表示转发数，其它表示空
     */
    key: number;
    /**
     * 0表示大于，1表示小于，2表示大于等于，3表示小于等于
     */
    predicator: number;
    limit: number;
  }
}
