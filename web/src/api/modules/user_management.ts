import { ResDataList, Result, User } from "@/api/interface/index";
import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

/**
 * @name 用户管理模块
 */

// 获取待处理的注册申请列表
export const getPendingList = () => {
  return http.get<ResDataList<User.ResPendingUser>>(PORT1 + `/waitinglist/`);
};

// 获取用户列表
export const getUserList = () => {
  return http.get<ResDataList<User.ResUser>>(PORT1 + `/user/list/`);
};

// 授权用户
export const BatchMandateUser = (params: User.ReqMandate) => {
  return http.post(PORT1 + `/user/mandate/`, params);
};

// 删除用户
export const batchDeleteUser = (params: User.ReqDelete) => {
  return http.post<Result>(PORT1 + `/user/delete/`, params);
};

// 重置用户密码
export const resetUserPassWord = () => {
  let req = {
    password: "12345" // 默认密码12345
  };
  return http.post<Result>(PORT1 + `/user/update-profile/`, req);
};
