import { ManagePort } from "../config/servicePort";
import http from "@/api";
import { ResDataList, Result, WhiteList } from "../interface";

// 获取白名单
export const getWhiteListApi = () => {
  return http.get<ResDataList<WhiteList.ResWhiteList>>(ManagePort.IWhiteList.GET_LIST);
};

// 获取tags列表
export const getTagsApi = () => {
  return http.get<ResDataList<WhiteList.ResTags>>(ManagePort.IWhiteList.GET_TAGS);
};

// 添加白名单
export const addToWhiteListApi = (params: WhiteList.ReqOnWhiteList) => {
  return http.post<Result>(ManagePort.IWhiteList.ADD_TO_LIST, params, { loading: false });
};

// 添加tag
export const addTagApi = (params: WhiteList.ReqOnTags) => {
  return http.post<Result>(ManagePort.IWhiteList.ADD_TAG, params, { loading: false });
};

// 删除白名单
export const deleteFromWhiteListApi = (params: WhiteList.ReqOnWhiteList) => {
  return http.delete<Result>(ManagePort.IWhiteList.DELETE_FROM_LIST, params, { loading: false });
};

// 删除tag
export const deleteTagApi = (params: WhiteList.ReqOnTags) => {
  return http.delete<Result>(ManagePort.IWhiteList.DELETE_TAG, params, { loading: false });
};

// 启用白名单
export const activateWhiteListApi = (params: WhiteList.ReqOnWhiteList | WhiteList.ReqOnWhiteList[], config?: any) => {
  if (Array.isArray(params)) {
    let success = true;
    params.forEach(param =>
      http.patch<Result>(ManagePort.IWhiteList.ACTIVATE, param, config).catch(() => {
        success = false;
      })
    );
    return new Promise<Result>(resolve => {
      if (success) {
        resolve({
          message: "批量启用成功"
        });
      }
    });
  } else return http.patch<Result>(ManagePort.IWhiteList.ACTIVATE, params, config);
};

// 禁用白名单
export const deactivateWhiteListApi = (params: WhiteList.ReqOnWhiteList | WhiteList.ReqOnWhiteList[], config?: any) => {
  if (Array.isArray(params)) {
    let success = true;
    params.forEach(param =>
      http.patch<Result>(ManagePort.IWhiteList.DEACTIVATE, param, config).catch(() => {
        success = false;
      })
    );
    return new Promise<Result>(resolve => {
      if (success) {
        resolve({
          message: "批量禁用成功"
        });
      }
    });
  } else return http.patch<Result>(ManagePort.IWhiteList.DEACTIVATE, params, config);
};
