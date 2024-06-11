import { Login, Result, ResultData } from "@/api/interface/index";
// import adminMenuList from "@/assets/json/adminMenuList.json";
// import userMenuList from "@/assets/json/userMenuList.json";
import authMenuList from "@/assets/json/adminMenuList.json";
import authButtonList from "@/assets/json/authButtonList.json";
import http from "@/api";
import { AuthPort, ManagePort } from "../config/servicePort";

/**
 * @name 登录模块
 */
// 用户登录
export const loginApi = (params: Login.ReqLoginForm) => {
  return http.post<ResultData<Login.ResLogin>>(AuthPort.LOGIN, params, { loading: true }); // 正常 post json 请求  ==>  application/json
  // return http.post<Login.ResLogin>(PORT1 + `/login`, params, { loading: false }); // 控制当前请求不显示 loading
  // return http.post<Login.ResLogin>(PORT1 + `/login`, {}, { params }); // post 请求携带 query 参数  ==>  ?username=admin&password=123456
  // return http.post<Login.ResLogin>(PORT1 + `/login`, qs.stringify(params)); // post 请求携带表单参数  ==>  application/x-www-form-urlencoded
  // return http.get<Login.ResLogin>(PORT1 + `/login?${qs.stringify(params, { arrayFormat: "repeat" })}`); // get 请求可以携带数组等复杂参数
};

// 获取菜单列表
// export const getAuthMenuListApi = async (role: string) => {
//   // return http.get<Menu.MenuOptions[]>(PORT1 + `/menu/list`, {}, { loading: false });
//   // 如果想让菜单变为本地数据，注释上一行代码，并引入本地 authMenuList.json 数据
//   return role.toLowerCase().includes("admin") ? adminMenuList : userMenuList;
// };

export const getAuthMenuListApi = () => {
  // return http.get<Menu.MenuOptions[]>(PORT1 + `/menu/list`, {}, { loading: false });
  // 如果想让菜单变为本地数据，注释上一行代码，并引入本地 authMenuList.json 数据
  return authMenuList;
};

// 获取按钮权限
export const getAuthButtonListApi = () => {
  // return http.get<Login.ResAuthButtons>(PORT1 + `/auth/buttons`, {}, { loading: false });
  // 如果想让按钮权限变为本地数据，注释上一行代码，并引入本地 authButtonList.json 数据
  return authButtonList;
};

// 忘记密码
export const forgetPwdApi = (params: Login.ReqForgetPwd) => {
  return http.post<Result>(ManagePort.IGuest.FORGET_PWD, params, { loading: false });
};

// 刷新token
export const refreshTokenApi = (params: Login.ReqRefresh) => {
  return http.post<Login.ResRefresh>(AuthPort.REFRESH, params, { loading: false });
};

// 用户退出登录
export const logoutApi = (params: Login.ReqLogout) => {
  return http.post<Result>(AuthPort.LOGOUT, params);
};
