<template>
  <div class="user_infos card">
    <UploadDialogue v-model="uploadDialogueVisible" />
    <setting-panel setting-title="基本信息">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow :selected="true" display-value="" display-text="头像" @row-clicked="avatarClicked" :display-icon="false">
          <div class="arrow_right">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </InfoRow>
        <InfoRow
          :selected="edit === 0"
          :display-value="basicInfo.id"
          :tool-tip-visivle="invalidId"
          display-text="学工号"
          tip-text="请输入学工号"
          @checked="confirm(0)"
          @row-clicked="handleClick(0)"
        >
          <div class="input_container"><el-input v-model="newId" name="input_box"></el-input></div>
        </InfoRow>
        <InfoRow
          :selected="edit === 1"
          :display-value="basicInfo.name"
          :tool-tip-visivle="invalidName"
          display-text="名称"
          tip-text="用户名仅由大小写英文字符与数字0~9组成"
          @checked="confirm(1)"
          @row-clicked="handleClick(1)"
        >
          <div class="input_container"><el-input v-model="newName" name="input_box"></el-input></div>
        </InfoRow>
        <InfoRow
          :selected="edit === 2"
          display-value="*****"
          :tool-tip-visivle="invalidPassword || invalidRepeatPwd"
          display-text="密码"
          :tip-text="invalidPassword ? '密码仅由大小写英文字符与数字0~9组成' : invalidRepeatPwd ? '两次输入的密码不一致' : ''"
          @checked="confirm(2)"
          @row-clicked="handleClick(2)"
        >
          <div class="input_container">
            <el-input v-model="newPassword" placeholder="新密码" name="input_box"></el-input>
            <el-input v-model="repeatPassword" placeholder="重复密码"></el-input>
          </div>
        </InfoRow>
      </div>
    </setting-panel>
    <setting-panel setting-title="联系信息">
      <div class="info_container" name="info_panel" @click.stop>
        <InfoRow
          :selected="edit === 3"
          :display-value="contactInfo.email"
          :tool-tip-visivle="invalidEmail"
          display-text="邮箱地址"
          tip-text="无效的邮箱格式"
          @checked="confirm(3)"
          @row-clicked="handleClick(3)"
        >
          <div class="input_container"><el-input v-model="newEmail" name="input_box"></el-input></div>
        </InfoRow>
        <InfoRow
          :selected="edit === 4"
          :display-value="contactInfo.telephone"
          :tool-tip-visivle="invalidTelephone"
          display-text="联系电话"
          tip-text="无效的联系电话格式"
          @checked="confirm(4)"
          @row-clicked="handleClick(4)"
        >
          <div class="input_container"><el-input v-model="newTelephone" name="input_box"></el-input></div>
        </InfoRow>
      </div>
    </setting-panel>
  </div>
</template>

<script setup lang="ts">
import { fetchUserInfo, uploadUserInfo } from "@/api/modules/user_info";
import SettingPanel from "@/components/SettingPanel/index.vue";
import { useUserStore } from "@/stores/modules/user";
import InfoRow from "./components/InfoRow.vue";
import UploadDialogue from "./components/UploadDialogue.vue";
import { Ref, nextTick, onMounted, onUnmounted, ref } from "vue";
const store = useUserStore();

const edit = ref(-1);
const basicInfo = ref(store.userInfo.basicInfo);
const contactInfo = ref(store.userInfo.contactInfo);
const uploadDialogueVisible = ref(false);

const newId = ref(basicInfo.value.id);
const newName = ref(basicInfo.value.name);
const newPassword = ref("");
const repeatPassword = ref("");
const newEmail = ref(contactInfo.value.email);
const newTelephone = ref(contactInfo.value.telephone);

const invalidId = ref(false);
const invalidName = ref(false);
const invalidPassword = ref(false);
const invalidRepeatPwd = ref(false);
const invalidEmail = ref(false);
const invalidTelephone = ref(false);
const tips = ref<Ref<boolean>[]>([invalidId, invalidName, invalidPassword, invalidEmail, invalidTelephone]);

fetchUserInfo().then(response => {
  if (response.code === "200") {
    store.setUserBasicInfo(response.data.basicInfo);
    store.setUserContactInfo(response.data.contactInfo);
    basicInfo.value = response.data.basicInfo;
    contactInfo.value = response.data.contactInfo;
  }
});
function outsideClicked() {
  if (edit.value === -1) return;
  switch (edit.value) {
    case 0:
      newId.value = basicInfo.value.id;
      break;
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
    case 4:
      newTelephone.value = contactInfo.value.telephone;
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

function handleClick(index: number) {
  if (edit.value >= 0 && edit.value !== index) {
    tips.value[edit.value].value = false;
    if (edit.value === 2) invalidRepeatPwd.value = false;
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
  tips.value[index].value = false;
  invalidRepeatPwd.value = false;
  switch (index) {
    // Edit Id
    case 0:
      if (newId.value.length > 0) {
        uploadUserInfo({
          basicInfo: { ...basicInfo.value, id: newId.value },
          contactInfo: { ...contactInfo.value }
        }).then(response => {
          if (response.code === "200") {
            basicInfo.value.id = newId.value;
            edit.value = -1;
          }
        });
      } else invalidId.value = true;
      break;
    // Edit Name
    case 1:
      if (newName.value.match(/^[a-zA-Z0-9]+$/g) !== null) {
        uploadUserInfo({
          basicInfo: { ...basicInfo.value, name: newName.value },
          contactInfo: { ...contactInfo.value }
        }).then(response => {
          if (response.code === "200") {
            basicInfo.value.name = newName.value;
            edit.value = -1;
          }
        });
      } else invalidName.value = true;
      break;
    // Edit Password
    case 2:
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
        }).then(response => {
          if (response.code === "200") {
            newPassword.value = "";
            repeatPassword.value = "";
            edit.value = -1;
          }
        });
      }
      break;
    // Edit Email
    case 3:
      if (newEmail.value.match(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/g) !== null) {
        uploadUserInfo({
          basicInfo: { ...basicInfo.value },
          contactInfo: { ...contactInfo.value, email: newEmail.value }
        }).then(response => {
          if (response.code === "200") {
            contactInfo.value.email = newEmail.value;
            edit.value = -1;
          }
        });
      } else invalidEmail.value = true;
      break;
    // Edit Telephone
    case 4:
      if (newTelephone.value.match(/^1\d{10}$|^(0\d{2,3}-?|\(0\d{2,3}\))?[1-9]\d{4,7}(-\d{1,8})?$/g) !== null) {
        uploadUserInfo({
          basicInfo: { ...basicInfo.value },
          contactInfo: { ...contactInfo.value, telephone: newTelephone.value }
        }).then(response => {
          if (response.code === "200") {
            contactInfo.value.telephone = newTelephone.value;
            edit.value = -1;
          }
        });
      } else invalidTelephone.value = true;
      break;
    default:
      break;
  }
}
function avatarClicked() {
  if (edit.value >= 0) {
    tips.value[edit.value].value = false;
    invalidRepeatPwd.value = false;
    edit.value = -1;
  }
  uploadDialogueVisible.value = true;
  return;
}
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
