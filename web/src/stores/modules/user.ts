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
        name: "",
        password: ""
      },
      contactInfo: {
        email: ""
      },
      messages: []
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
