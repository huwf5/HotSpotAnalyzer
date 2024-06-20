// ? Element 常用表单校验规则

/**
 *  @rule 手机号
 */
export function checkPhoneNumber(rule: any, value: any, callback: any) {
  const regexp = /^(((13[0-9]{1})|(15[0-9]{1})|(16[0-9]{1})|(17[3-8]{1})|(18[0-9]{1})|(19[0-9]{1})|(14[5-7]{1}))+\d{8})$/;
  if (value === "") callback("请输入手机号码");
  if (!regexp.test(value)) {
    callback(new Error("请输入正确的手机号码"));
  } else {
    return callback();
  }
}
/**
 *  @rule 用户名
 */
export function validateUserName(rule: any, value: string, callback: any) {
  if (value.length === 0) callback(new Error("请输入用户名"));
  else if (value.match(/^[a-zA-Z0-9]+$/g) !== null) callback();
  else callback(new Error("用户名仅由大小写英文字符与数字0~9组成"));
}
/**
 *  @rule 密码
 */
export function validatePassword(rule: any, value: string, callback: any) {
  if (value.length === 0) callback(new Error("请输入密码"));
  else if (value.match(/^[a-zA-Z0-9]+$/g) !== null) callback();
  else callback(new Error("密码仅由大小写英文字符与数字0~9组成"));
}
/**
 *  @rule 邮箱地址
 */
export function validateEmail(rule: any, value: string, callback: any) {
  if (value.length === 0) callback(new Error("请输入邮箱地址"));
  else if (value.match(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/g) !== null) callback();
  else callback(new Error("邮箱格式无效"));
}
