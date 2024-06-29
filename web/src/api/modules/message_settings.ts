import { MessagePort } from "../config/servicePort";
import { Messages, ResultData } from "../interface";
import http from "@/api";

export const createMessageSettingsApi = () => {
  return http.post(MessagePort.MSG_SETTINGS.BASE, { loading: false });
};

export const getMessageSettingsApi = () => {
  return http.get<ResultData<Messages.ResMessageSetting>>(MessagePort.MSG_SETTINGS.BASE, { loading: false });
};

export const uploadMessageSettingsApi = (params: Messages.ReqMessageSetting) => {
  return http.patch(MessagePort.MSG_SETTINGS.UPDATE, params);
};
