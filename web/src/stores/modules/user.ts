import { defineStore } from "pinia";
import { UserState } from "@/stores/interface";
import piniaPersistConfig from "@/stores/helper/persist";
import { Messages, UserInfo } from "@/api/interface";

export const useUserStore = defineStore({
  id: "geeker-user",
  state: (): UserState => ({
    token: "",
    userInfo: {
      basicInfo: {
        id: "12345678",
        name: "",
        avatar: "",
        password: ""
      },
      contactInfo: {
        email: "",
        telephone: ""
      },
      messages: [],
      settings: {
        danger_heat_limit: 1000,
        warning_heat_limit: 900,
        danger_composed_limits: [],
        warning_composed_limits: [],
        auto_star: true,
        heat_formula: "$upVote+$like*5+$share*10"
      }
    }
  }),
  getters: {},
  actions: {
    // Set Token
    setToken(token: string) {
      this.token = token;
    },
    // Set setUserInfo
    setUserBasicInfo(basicInfo: UserInfo.BasicInfo) {
      this.userInfo.basicInfo = basicInfo;
    },
    setUserContactInfo(contactInfo: UserInfo.ContactInfo) {
      this.userInfo.contactInfo = contactInfo;
    },
    setUserMsg(msg: Messages.Message[]) {
      this.userInfo.messages = msg;
    }
  },
  persist: piniaPersistConfig("geeker-user")
});
