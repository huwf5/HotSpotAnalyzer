// import { PORT1 } from "@/api/config/servicePort";
// import http from "@/api";
import { ResultData, UserInfo } from "../interface";

export const fetchUserInfo = () => {
  // return http.get<{ basicInfo: UserInfo.BasicInfo; contactInfo: UserInfo.ContactInfo }>(PORT1 + `/user/info`, params);

  //  测试数据
  return new Promise<ResultData<{ basicInfo: UserInfo.BasicInfo; contactInfo: UserInfo.ContactInfo }>>(resolve => {
    setTimeout(() => {
      resolve({
        code: "200",
        msg: "OK",
        data: {
          basicInfo: {
            name: "geek-user",
            id: "12345678",
            avatar: "",
            password: ""
          },
          contactInfo: {
            email: "1234567890@sysu.edu.cn",
            telephone: "12345678900"
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
          code: "200",
          msg: "OK",
          data: {}
        });
    }, 200);
  });
};
