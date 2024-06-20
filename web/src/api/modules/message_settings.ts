import { Messages, ResultData } from "../interface";
// import { PORT1 } from "../config/servicePort";
// import http from "@/api";

export const fetchMessagesSettingsApi = () => {
  // return http.get<Messages.ResMessageSettings>(PORT1 + `/message/settings`);

  return new Promise<ResultData<Messages.ResMessageSettings>>(resolve => {
    setTimeout(() => {
      resolve({
        message: "OK",
        data: {
          // use_danger_heat_limit: true,
          // use_warning_heat_limit: true,
          // danger_heat_limit: 1000,
          // warning_heat_limit: 900,
          // heat_formula: "$upVote+5*$like+10*$share",
          use_danger_composed_limits: false,
          use_warning_composed_limits: false,
          danger_composed_limits: [],
          warning_composed_limits: [],
          auto_star: true
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
        message: "OK",
        data: undefined
      });
    }, 1000);
  });
};
