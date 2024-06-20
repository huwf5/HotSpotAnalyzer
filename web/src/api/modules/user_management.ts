import { ResDataList, Result, User } from "@/api/interface/index";
import { AuthPort, ManagePort } from "@/api/config/servicePort";
import http from "@/api";

/**
 * @name 用户管理模块
 */

// 获取待处理的注册申请列表
export const getPendingListApi = () => {
  return http.get<ResDataList<User.ResPendingUser>>(ManagePort.IWaitList.GET_LIST);
};

// 激活用户
export const activateUserApi = (params: User.EmailList) => {
  return http.post<Result>(ManagePort.IWaitList.ACTIVATE, params);
};

// 拒绝激活请求
export const rejectActivationApi = (params: User.EmailList) => {
  return http.post<Result>(ManagePort.IWaitList.REJECT, params);
};

// 获取用户列表
export const getUserListApi = () => {
  return http.get<ResDataList<User.ResUser>>(ManagePort.IAdmin.USER_LIST);
};

// 授权用户
export const batchMandateUserApi = (params: User.EmailList) => {
  return http.post<Result>(ManagePort.IAdmin.UP_GRADE, params);
};

// 撤回用户权限
export const batchDemoteUserApi = (params: User.EmailList) => {
  return http.post<Result>(ManagePort.IAdmin.DOWN_GRADE, params);
};

// 删除用户
export const batchDeleteUserApi = (params: User.EmailList) => {
  return http.post<Result>(ManagePort.IAdmin.DELETE, params);
};

// 重置用户密码
export const resetUserPassWordApi = () => {
  let req = {
    password: "12345" // 默认密码12345
  };
  return http.post<Result>(ManagePort.IGuest.UPDATE_PROFILE, req);
};

// 获取用户身份字典
export const getRoleDictApi = () => {
  return http.get<ResDataList<User.RoleDict>>(AuthPort.ROLE_DICT);
};
