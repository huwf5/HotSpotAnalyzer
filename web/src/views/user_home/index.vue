<template>
  <div class="user_infos card">
    <SettingPanel setting-title="基本信息">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="edit === 0"
          :display-value="basicInfo.name"
          :tool-tip-visivle="invalidName"
          display-text="名称"
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
          :tip-text="invalidPassword ? '密码仅由大小写英文字符与数字0~9组成' : invalidRepeatPwd ? '两次输入的密码不一致' : ''"
          @checked="confirm(1)"
          @row-clicked="handleClick(1)"
        >
          <div class="input_container">
            <el-input v-model="newPassword" placeholder="新密码" name="input_box"></el-input>
            <el-input v-model="repeatPassword" placeholder="重复密码"></el-input>
          </div>
        </InfoRow>
      </div>
    </SettingPanel>
    <SettingPanel setting-title="联系信息">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="edit === 2"
          :display-value="contactInfo.email"
          :tool-tip-visivle="invalidEmail"
          display-text="邮箱地址"
          tip-text="无效的邮箱格式"
          @checked="confirm(2)"
          @row-clicked="handleClick(2)"
        >
          <div class="input_container"><el-input v-model="newEmail" name="input_box"></el-input></div>
        </InfoRow>
      </div>
    </SettingPanel>
    <SettingPanel setting-title="账号与权限">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="true"
          :tool-tip-visivle="role_tip_visible"
          display-text="权限等级"
          :tip-text="role_tip"
          @row-clicked="confirm(3), handleClick(-1)"
        >
          <template #default>
            <div class="role_text" @mouseenter="toggleRoleTipVisibility(true)" @mouseleave="toggleRoleTipVisibility(false)">
              {{ role }}
            </div>
          </template>
          <template #icon>
            <icon><Top /></icon>
          </template>
        </InfoRow>
        <InfoRow :selected="true" :display-icon="false" display-text="" @row-clicked="confirm(4), handleClick(-1)">
          <div class="delete_account">删除账号</div>
        </InfoRow>
      </div>
    </SettingPanel>
  </div>
</template>

<script setup lang="ts">
import icon from "./../../components/el-icon/icon.vue";
import { applyMandate, confirmDelete, fetchUserInfo, uploadUserInfo } from "@/api/modules/user_info";
import SettingPanel from "@/components/SettingPanel/index.vue";
import { useUserStore } from "@/stores/modules/user";
import InfoRow from "./components/InfoRow.vue";
import { Ref, nextTick, onMounted, onUnmounted, ref } from "vue";
import { UserInfo } from "@/api/interface";
import { useHandleData } from "@/hooks/useHandleData";
import { ElMessageBox } from "element-plus";
import router from "@/routers";
import { LOGIN_URL } from "@/config";
const store = useUserStore();

const edit = ref(-1);
const basicInfo = ref(store.userInfo.basicInfo);
const contactInfo = ref(store.userInfo.contactInfo);
const role = ref("普通用户");

const newName = ref(basicInfo.value.name);
const newPassword = ref("");
const repeatPassword = ref("");
const newEmail = ref(contactInfo.value.email);

const invalidName = ref(false);
const invalidPassword = ref(false);
const invalidRepeatPwd = ref(false);
const invalidEmail = ref(false);
const tips = ref<Ref<boolean>[]>([invalidName, invalidPassword, invalidEmail]);
const role_tips = [
  "普通用户拥有系统基本功能的使用权，可以查看热点事件与事件时间线等",
  "管理员拥有系统所有的使用权限与操作权限，可授权新用户以及管理其它用户"
];
const role_tip_visible = ref(false);
const role_tip = ref("");

fetchUserInfo().then(response => {
  store.setUserBasicInfo(response.data.basicInfo);
  store.setUserContactInfo(response.data.contactInfo);
  basicInfo.value = response.data.basicInfo;
  contactInfo.value = response.data.contactInfo;
  role.value = UserInfo.roleNames[response.data.accountInfo.role];
  role_tip.value = role_tips[response.data.accountInfo.role];
});
function outsideClicked() {
  if (edit.value === -1) return;
  switch (edit.value) {
    case 1:
      newName.value = basicInfo.value.name;
      break;
    case 2:
      newPassword.value = "";
      repeatPassword.value = "";
      invalidRepeatPwd.value = false;
      break;
    case 3:
      newEmail.value = contactInfo.value.email;
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
  role_tip_visible.value = visible;
}
function handleClick(index: number) {
  if (edit.value >= 0 && edit.value !== index) {
    tips.value[edit.value].value = false;
    invalidRepeatPwd.value = false;
  }
  edit.value = index;
  nextTick(() => {
    // auto focus
    let input_ref = document.getElementsByName("input_box");
    if (input_ref.length > 0) {
      input_ref.item(0).focus();
    }
  });
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
        uploadUserInfo({
          basicInfo: { ...basicInfo.value, name: newName.value },
          contactInfo: { ...contactInfo.value }
        }).then(() => {
          basicInfo.value.name = newName.value;
          edit.value = -1;
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
        uploadUserInfo({
          basicInfo: { ...basicInfo.value, password: newPassword.value },
          contactInfo: { ...contactInfo.value }
        }).then(() => {
          newPassword.value = "";
          repeatPassword.value = "";
          edit.value = -1;
        });
      }
      break;
    // Edit Email
    case 2:
      if (newEmail.value.match(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/g) !== null) {
        uploadUserInfo({
          basicInfo: { ...basicInfo.value },
          contactInfo: { ...contactInfo.value, email: newEmail.value }
        }).then(() => {
          contactInfo.value.email = newEmail.value;
          edit.value = -1;
        });
      } else invalidEmail.value = true;
      break;
    // Apply for Mandate
    case 3:
      useHandleData(applyMandate, { email: contactInfo.value.email }, "申请提升权限").then(response => {
        ElMessageBox.confirm(response.msg, "温馨提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "success",
          draggable: true
        });
      });
      break;
    // Delete Account
    case 4:
      useHandleData(confirmDelete, { email: contactInfo.value.email }, "删除账号（包含所有账号记录）").then(() => {
        store.setToken("");
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
