import { AuthPort } from "../config/servicePort";
import { Register, Result } from "../interface";
import http from "@/api";

/**
 * @name 注册模块
 */
// 用户注册
export const registerApi = (params: Register.ReqRegisterForm) => {
  let req = {
    email: params.email,
    username: params.username,
    password: params.password,
    verify_code: params.captcha
  };
  return http.post<Result>(AuthPort.REGISTER, req, { loading: false }); // 正常 post json 请求  ==>  application/json
  // return http.post<register.ResRegister>(PORT1 + `/register`, params, { loading: false }); // 控制当前请求不显示 loading
  // return http.post<register.ResRegister>(PORT1 + `/register`, {}, { params }); // post 请求携带 query 参数  ==>  ?username=admin&password=123456
  // return http.post<register.ResRegister>(PORT1 + `/register`, qs.stringify(params)); // post 请求携带表单参数  ==>  application/x-www-form-urlencoded
  // return http.get<register.ResRegister>(PORT1 + `/register?${qs.stringify(params, { arrayFormat: "repeat" })}`); // get 请求可以携带数组等复杂参数
};

// 获取验证码
export const getCaptchaApi = (params: Register.ReqEmailCaptcha) => {
  return http.post<Result>(AuthPort.CAPTCHA, params, { loading: false });
};
