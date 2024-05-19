import { ResPage, ResultData, User } from "@/api/interface/index";
import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

import testA from "@/assets/json/test_data_userList.json";
/**
 * @name 用户管理模块
 */

// 获取待处理的注册申请列表
export const getApplication = (params: User.ReqUserParams) => {
  // return http.get<ResPage<User.ResUserList>>(PORT1 + `/user/applications`, params);

  return new Promise<ResultData<ResPage<User.ResUser>>>(resolve => {
    if (params) {
    }
    setTimeout(() => {
      resolve({
        code: "200",
        msg: "OK",
        data: testA
      });
    }, 200);
  });
};

// 获取用户列表
export const getUserList = (params: User.ReqUserParams) => {
  // return http.get<ResPage<User.ResUserList>>(PORT1 + `/user/list`, params);

  return new Promise<ResultData<ResPage<User.ResUser>>>(resolve => {
    if (params) {
    }
    setTimeout(() => {
      resolve({
        code: "200",
        msg: "OK",
        data: testA
        // data: {
        //   list: [],
        //   pageNum: 0,
        //   pageSize: 0,
        //   total: 0
        // }
      });
    }, 200);
  });
};

// 批量授权用户
export const BatchMandateUser = (params: FormData) => {
  return http.post(PORT1 + `/user/mandate`, params);
};

// 批量删除用户
export const batchDeleteUser = (params: string[]) => {
  return http.post(PORT1 + `/user/remove`, params);
};

// 批量切换用户状态
export const batchChangeStatus = (params: FormData) => {
  return http.post(PORT1 + `/user/batch_change`, params);
};

// 重置用户密码
export const resetUserPassWord = (params: { id: string }) => {
  return http.post(PORT1 + `/user/rest_password`, params);
};
