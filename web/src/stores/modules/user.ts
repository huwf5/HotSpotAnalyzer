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
      if (token_lifetime > 0) {
        if (this.timer) {
          clearTimeout(this.timer);
        }
        this.timer = setTimeout(() => {
          refreshTokenApi({ refresh: this.refresh }).then(res => {
            this.setTokens(res.data.access, res.data.refresh, this.token_lifetime);
          });
        }, token_lifetime);
      } else {
        if (this.timer) {
          clearTimeout(this.timer);
          this.timer = undefined;
        }
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
    setUserMsg(msg: Messages.Message[]) {
      this.userInfo.messages = msg;
    }
  },
  persist: piniaPersistConfig("geeker-user")
});
