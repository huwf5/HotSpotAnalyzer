// import { PORT1 } from "@/api/config/servicePort";
// import http from "@/api";
import { Result, ResultData, UserInfo } from "../interface";

export const fetchUserInfo = () => {
  // return http.get<{ basicInfo: UserInfo.BasicInfo; contactInfo: UserInfo.ContactInfo }>(PORT1 + `/user/info`, params);

  //  测试数据
  return new Promise<
    ResultData<{ basicInfo: UserInfo.BasicInfo; contactInfo: UserInfo.ContactInfo; accountInfo: UserInfo.AccountInfo }>
  >(resolve => {
    setTimeout(() => {
      resolve({
        msg: "OK",
        data: {
          basicInfo: {
            name: "geek-user",
            password: ""
          },
          contactInfo: {
            email: "1234567890@sysu.edu.cn"
          },
          accountInfo: {
            role: 0
          }
        }
      });
    }, 200);
  });
};

export const uploadUserInfo = (params: { basicInfo: UserInfo.BasicInfo; contactInfo: UserInfo.ContactInfo }) => {
  // return http.post(PORT1 + `/user/setInfo`, params);

  // 测试
  return new Promise<ResultData<{}>>(resolve => {
    setTimeout(() => {
      if (params)
        resolve({
          msg: "OK",
          data: {}
        });
    }, 200);
  });
};

export const applyMandate = (params: { email: string }) => {
  // return http.post(PORT1 + `/user/apply`, params);

  // 测试
  return new Promise<Result>(resolve => {
    setTimeout(() => {
      if (params)
        resolve({
          msg: "申请成功，请耐心等待管理员审核"
        });
    }, 200);
  });
};

export const confirmDelete = (params: { email: string }) => {
  // return http.post(PORT1 + `/user/apply`, params);

  // 测试
  return new Promise<Result>(resolve => {
    setTimeout(() => {
      if (params)
        resolve({
          msg: ""
        });
    }, 200);
  });
};
