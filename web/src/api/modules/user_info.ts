import { ManagePort } from "@/api/config/servicePort";
import http from "@/api";
import { Result, ResultData, UserInfo } from "../interface";

// 获取用户数据
export const getUserInfoApi = () => {
  return http.get<ResultData<UserInfo.ResUserProfile>>(ManagePort.IGuest.GET_PROFILE);
};
// 上传用户数据
export const uploadUserInfoApi = (params: UserInfo.ReqUpdate) => {
  return http.patch<Result>(ManagePort.IGuest.UPDATE_PROFILE, params);
};
// 申请升级
export const applyMandateApi = (params: { email: string }) => {
  // return http.post(PORT1 + `/user/apply/`, params);
  return new Promise<Result>(resolve => {
    if (params) {
    }
    setTimeout(
      () =>
        resolve({
          message: "申请成功"
        }),
      500
    );
  });
};
// 删除账号
export const confirmDeleteApi = () => {
  return http.delete<Result>(ManagePort.IGuest.DELETE);
};
