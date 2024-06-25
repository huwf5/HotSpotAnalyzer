<template>
  <div class="user_infos card">
    <SettingPanel setting-title="基本信息">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="edit === 0"
          :display-value="basicInfo.name"
          :tool-tip-visivle="invalidName"
          display-text="名称"
          cursor="pointer"
          tip-text="用户名仅由大小写英文字符与数字0~9组成"
          @checked="confirm(0)"
          @row-clicked="handleClick(0)"
        >
          <div class="input_container"><el-input v-model="newName" name="input_box"></el-input></div>
        </InfoRow>
        <InfoRow
          :selected="edit === 1"
          display-value="*****"
          :tool-tip-visivle="invalidPassword || invalidRepeatPwd"
          display-text="密码"
          cursor="pointer"
          :tip-text="invalidPassword ? '密码仅由大小写英文字符与数字0~9组成' : invalidRepeatPwd ? '两次输入的密码不一致' : ''"
          @checked="confirm(1)"
          @row-clicked="handleClick(1)"
        >
          <div class="input_container">
            <el-input
              v-model="newPassword"
              placeholder="新密码"
              name="input_box"
              type="password"
              show-password
              clearable
              style="margin: 10px"
            />
            <el-input
              v-model="repeatPassword"
              placeholder="重复密码"
              type="password"
              show-password
              clearable
              style="margin: 10px"
            />
          </div>
        </InfoRow>
      </div>
    </SettingPanel>
    <SettingPanel setting-title="联系信息">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="false"
          :display-value="contactInfo.email"
          :tool-tip-visivle="invalidEmail"
          display-text="邮箱地址"
          :display-icon="false"
        />
      </div>
    </SettingPanel>
    <SettingPanel setting-title="账号与权限">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="true"
          :tool-tip-visivle="role_tip_visible"
          :display-icon="false"
          display-text="权限等级"
          :tip-text="role_tip"
          @row-clicked="handleClick(-1)"
        >
          <template #default>
            <div class="role_text" @mouseenter="toggleRoleTipVisibility(true)" @mouseleave="toggleRoleTipVisibility(false)">
              {{ role_name }}
            </div>
          </template>
        </InfoRow>
        <InfoRow
          :selected="true"
          :display-icon="false"
          cursor="pointer"
          display-text=""
          @row-clicked="confirm(2), handleClick(-1)"
        >
          <div class="delete_account">删除账号</div>
        </InfoRow>
      </div>
    </SettingPanel>
  </div>
</template>

<script setup lang="ts">
import { confirmDeleteApi, getUserInfoApi, uploadUserInfoApi } from "@/api/modules/user_info";
import SettingPanel from "@/components/SettingPanel/index.vue";
import { useUserStore } from "@/stores/modules/user";
import InfoRow from "./components/InfoRow.vue";
import { Ref, nextTick, onMounted, onUnmounted, ref } from "vue";
import { useHandleData } from "@/hooks/useHandleData";
import router from "@/routers";
import { LOGIN_URL } from "@/config";
import { ElMessage } from "element-plus";
const store = useUserStore();

const edit = ref(-1);
const basicInfo = ref(store.userInfo.basicInfo);
const contactInfo = ref(store.userInfo.contactInfo);

const newName = ref(basicInfo.value.name);
const newPassword = ref("");
const repeatPassword = ref("");

const invalidName = ref(false);
const invalidPassword = ref(false);
const invalidRepeatPwd = ref(false);
const invalidEmail = ref(false);
const tips = ref<Ref<boolean>[]>([invalidName, invalidPassword, invalidEmail]);
const role_name = ref("");
// const role_tips = [
//   "超级用户拥有系统所有的使用权限与操作权限，且账号无法被删除",
//   "管理员拥有系统所有的使用权限与操作权限，可激活、授权用户以及管理其它用户等",
//   "普通用户拥有系统基本功能的使用权，可以查看热点事件与事件时间线等"
// ];
const role_tip_visible = ref(false);
const role_tip = ref("");

await getUserInfoApi().then(async response => {
  store.setUserBasicInfo({ name: response.data.username });
  store.setUserContactInfo({ email: response.data.email });
  basicInfo.value = store.userInfo.basicInfo;
  contactInfo.value = store.userInfo.contactInfo;
  role_name.value = response.data.role;
});

function outsideClicked() {
  if (edit.value === -1) return;
  switch (edit.value) {
    case 0:
      newName.value = basicInfo.value.name;
      break;
    case 1:
      newPassword.value = "";
      repeatPassword.value = "";
      invalidRepeatPwd.value = false;
      break;
    default:
      break;
  }
  tips.value[edit.value].value = false;
  edit.value = -1;
}
onMounted(() => {
  document.addEventListener("click", outsideClicked);
});
onUnmounted(() => {
  document.removeEventListener("click", outsideClicked);
});
function toggleRoleTipVisibility(visible: boolean) {
  if (role_tip.value.length > 0) {
    role_tip_visible.value = visible;
  }
}
function handleClick(index: number) {
  if (edit.value >= 0 && edit.value !== index) {
    tips.value[edit.value].value = false;
    invalidRepeatPwd.value = false;
    newPassword.value = "";
    repeatPassword.value = "";
  }
  if (edit.value !== index) {
    edit.value = index;
    nextTick(() => {
      // auto focus
      let input_ref = document.getElementsByName("input_box");
      if (input_ref.length > 0) {
        input_ref.item(0).focus();
      }
    });
  }
}
function confirm(index: number) {
  if (index < tips.value.length) {
    tips.value[index].value = false;
    invalidRepeatPwd.value = false;
  }
  switch (index) {
    // Edit Name
    case 0:
      if (newName.value.match(/^[a-zA-Z0-9]+$/g) !== null) {
        uploadUserInfoApi({ username: newName.value }).then(() => {
          basicInfo.value.name = newName.value;
          store.userInfo.basicInfo.name = newName.value;
          edit.value = -1;
          ElMessage({
            type: "success",
            message: "用户名修改成功!"
          });
        });
      } else invalidName.value = true;
      break;
    // Edit Password
    case 1:
      let validPasswd = true;
      if (newPassword.value.match(/^[a-zA-Z0-9]+$/g) === null) {
        validPasswd = false;
        invalidPassword.value = true;
      }
      if (repeatPassword.value !== newPassword.value) {
        validPasswd = false;
        invalidRepeatPwd.value = true;
      }
      if (validPasswd) {
        uploadUserInfoApi({ password: newPassword.value }).then(() => {
          newPassword.value = "";
          repeatPassword.value = "";
          edit.value = -1;
          ElMessage({
            type: "success",
            message: "密码修改成功!"
          });
        });
      }
      break;
    // Delete Account
    case 2:
      useHandleData(confirmDeleteApi, { emailList: [contactInfo.value.email] }, "删除账号（包含所有账号记录）").then(() => {
        store.setTokens("", "", -1);
        router.replace(LOGIN_URL);
      });
      break;
    default:
      break;
  }
}
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
