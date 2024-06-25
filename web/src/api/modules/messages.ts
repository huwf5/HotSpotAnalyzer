import http from "@/api";
import { Messages, ResDataList } from "../interface";
import { MessagePort } from "../config/servicePort";

// 请求用户消息
export const fetchMessagesApi = () => {
  return http.get<ResDataList<Messages.ResMessage>>(MessagePort.MSG_BASE_PORT + "/", undefined, { loading: false });
};

export const batchUpdateMsgApi = (params: Messages.ReqMessages[]) => {
  let success = true;
  params.forEach(msg => {
    http.put(MessagePort.MSG_BASE_PORT + `/${msg.id}/`, msg, { loading: false }).catch(() => {
      success = false;
    });
  });
  return new Promise<void>((resolve, reject) => {
    success ? resolve() : reject();
  });
};

export const batchDeleteMsgApi = (params: number[]) => {
  let success = true;
  params.forEach(msg_id => {
    http.delete(MessagePort.MSG_BASE_PORT + `/${msg_id}/delete/`, { loading: false }).catch(() => {
      success = false;
    });
  });
  return new Promise<void>((resolve, reject) => {
    success ? resolve() : reject();
  });
};
