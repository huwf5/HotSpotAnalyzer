import { defineStore } from "pinia";
import { UserState } from "@/stores/interface";
import piniaPersistConfig from "@/stores/helper/persist";
import { Messages, UserInfo } from "@/api/interface";
import { refresh_token } from "@/api/modules/login";

export const useUserStore = defineStore({
  id: "geeker-user",
  state: (): UserState => ({
    token: "",
    refresh: "",
    token_lifetime: 60 * 60 * 1000,
    userInfo: {
      basicInfo: {
        name: ""
      },
      contactInfo: {
        email: ""
      },
      accountInfo: {
        role: 1
      },
      messages: []
    }
  }),
  getters: {},
  actions: {
    // Set Token
    setTokens(token: string, refresh: string, token_lifetime: number) {
      this.token = token;
      this.refresh = refresh;
      if (token_lifetime > 0) {
        setTimeout(() => {
          refresh_token({ refresh: this.refresh }).then(res => {
            this.setTokens(res.access, res.refresh, this.token_lifetime);
          });
        }, token_lifetime);
      }
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
