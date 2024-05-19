import { Messages, ResultData } from "../interface";
// import { PORT1 } from "../config/servicePort";
// import http from "@/api";

export const fetchMessagesSettingsApi = () => {
  // return http.get<Messages.ResMessageSettings>(PORT1 + `/message/settings`);

  return new Promise<ResultData<Messages.ResMessageSettings>>(resolve => {
    setTimeout(() => {
      resolve({
        code: "200",
        msg: "OK",
        data: {
          danger_heat_limit: 1000,
          warning_heat_limit: 900,
          use_danger_composed_limits: false,
          use_warning_composed_limits: false,
          danger_composed_limits: [],
          warning_composed_limits: [],
          auto_star: true,
          heat_formula: "$upVote+5*$like+10*$share"
        }
      });
    }, 1000);
  });
};

export const uploadMessagesSettingsApi = (params: Messages.ReqMessageSettings) => {
  // return http.post<undefined>(PORT1 + `/message/settings`, params);

  return new Promise<ResultData<undefined>>(resolve => {
    setTimeout(() => {
      if (params) {
      }
      resolve({
        code: "200",
        msg: "OK",
        data: undefined
      });
    }, 1000);
  });
};
