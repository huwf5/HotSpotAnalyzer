// import { PORT1 } from "../config/servicePort";
import { Register, ResultData } from "../interface";
// import http from "@/api";

/**
 * @name 注册模块
 */
// 用户注册
export const registerApi = (params: Register.ReqRegisterForm) => {
  // return http.post<Register.ResRegister>(PORT1 + `/register`, params, { loading: false }); // 正常 post json 请求  ==>  application/json
  // return http.post<register.ResRegister>(PORT1 + `/register`, params, { loading: false }); // 控制当前请求不显示 loading
  // return http.post<register.ResRegister>(PORT1 + `/register`, {}, { params }); // post 请求携带 query 参数  ==>  ?username=admin&password=123456
  // return http.post<register.ResRegister>(PORT1 + `/register`, qs.stringify(params)); // post 请求携带表单参数  ==>  application/x-www-form-urlencoded
  // return http.get<register.ResRegister>(PORT1 + `/register?${qs.stringify(params, { arrayFormat: "repeat" })}`); // get 请求可以携带数组等复杂参数

  // 测试数据
  return new Promise<ResultData<Register.ResRegister>>(resolve => {
    setTimeout(() => {
      if (params) {
      }
      resolve({
        msg: "OK",
        data: {
          code: 200,
          msg: ""
        }
      });
    }, 200);
  });
};
