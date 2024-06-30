import { defineStore } from "pinia";
import { UserState } from "@/stores/interface";
import piniaPersistConfig from "@/stores/helper/persist";
import { Messages, UserInfo } from "@/api/interface";
import { refreshTokenApi } from "@/api/modules/login";

export const useUserStore = defineStore({
  id: "geeker-user",
  state: (): UserState => ({
    token: "",
    refresh: "",
    timer: undefined,
    token_lifetime: 60 * 60 * 1000,
    userInfo: {
      basicInfo: {
        name: ""
      },
      contactInfo: {
        email: ""
      },
      accountInfo: {
        role: ""
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
      if (this.timer) {
        clearTimeout(this.timer);
        this.timer = undefined;
      }
      if (token_lifetime > 0) {
        this.token_lifetime = token_lifetime;
        this.timer = setTimeout(() => {
          refreshTokenApi({ refresh: this.refresh }).then(res => {
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
    setUserRole(accountInfo: UserInfo.AccountInfo) {
      this.userInfo.accountInfo = accountInfo;
    },
    setUserMsg(msg: Messages.ResMessage[]) {
      this.userInfo.messages = msg;
    }
  },
  persist: piniaPersistConfig("geeker-user")
});
