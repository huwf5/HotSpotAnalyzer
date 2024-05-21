// import { PORT1 } from "../config/servicePort";
// import http from "@/api";
import { Messages, ResultData } from "../interface";

// 请求用户消息
export const fetchMessagesApi = () => {
  // return http.get<Messages.Message[]>(PORT1 + `/message/fetch`, { loading: false });

  // 测试数据
  const test1 = {
    id: 2,
    display: true,
    type: 2,
    starred: true,
    unread: false,
    time: "12-10",
    content: "test",
    platform: 0,
    keywords: "中山大学 软件工程",
    title: "中山大学"
  };
  const test2 = {
    id: 0,
    display: true,
    type: 0,
    starred: true,
    unread: false,
    time: "12-10",
    content: "系统通知A"
  };
  const test3 = {
    id: 1,
    display: true,
    type: 0,
    starred: false,
    unread: true,
    time: "12-31",
    content: "系统通知B"
  };
  return new Promise<ResultData<Messages.Message[]>>(resolve => {
    setTimeout(() => {
      resolve({
        msg: "OK",
        data: [test1, test2, test3]
      });
    }, 200);
  });
};

export const batchUpdateMsg = (params: Messages.ReqMessages[]) => {
  // return http.post(PORT1 + `/message/update`, params, { loading: false });

  return new Promise<ResultData<undefined>>(resolve => {
    if (params) {
    }
    setTimeout(() => {
      resolve({
        msg: "OK",
        data: undefined
      });
    }, 1000);
  });
};

export const batchDeleteMsg = (params: Messages.ReqMessages[]) => {
  // return http.post(PORT1 + `/message/delete`, params, { loading: false });

  return new Promise<ResultData<undefined>>(resolve => {
    if (params) {
    }
    setTimeout(() => {
      resolve({
        msg: "OK",
        data: undefined
      });
    }, 200);
  });
};
