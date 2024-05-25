import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
import { ResultData, UserInfo } from "../interface";

// 获取用户数据
export const fetchUserInfo = () => {
  return http.get<ResultData<UserInfo.ResUserProfile>>(PORT1 + `/user/profile/`);
};
// 上传用户数据
export const uploadUserInfo = (params: {
  basicInfo: UserInfo.BasicInfo;
  contactInfo: UserInfo.ContactInfo;
  password?: string;
}) => {
  return http.post(PORT1 + `/user/update-profile/`, params);
};
// 申请升级
export const applyMandate = (params: { email: string }) => {
  return http.post(PORT1 + `/user/apply/`, params);
};
// 删除账号
export const confirmDelete = (params: { email: string }) => {
  return http.post(PORT1 + `/user/delete/`, params);
};
