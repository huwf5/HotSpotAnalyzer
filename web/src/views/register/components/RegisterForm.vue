<template>
  <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" size="large">
    <el-form-item prop="username">
      <el-input v-model="registerForm.username" placeholder="用户名" clearable>
        <template #prefix>
          <el-icon class="el-input__icon">
            <User />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input
        v-model="registerForm.password"
        type="password"
        placeholder="密码"
        show-password
        autocomplete="new-password"
        clearable
      >
        <template #prefix>
          <el-icon class="el-input__icon">
            <Lock />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="repeat_password">
      <el-input v-model="registerForm.repeat_password" type="password" show-password placeholder="确认密码" clearable>
        <template #prefix>
          <el-icon class="el-input__icon">
            <Lock />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="email">
      <el-input v-model="registerForm.email" placeholder="邮箱地址" clearable>
        <template #prefix>
          <el-icon class="el-input__icon">
            <Message />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
  </el-form>
  <div class="register-btn">
    <el-button icon="Back" round size="large" @click="goBack"> 返回 </el-button>
    <el-button icon="UserFilled" round size="large" type="primary" :loading="loading" @click="register(registerFormRef)">
      注册
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { LOGIN_URL } from "@/config";
import { getTimeState } from "@/utils";
import { Register } from "@/api/interface";
import { ElNotification } from "element-plus";
import { useUserStore } from "@/stores/modules/user";
import { useTabsStore } from "@/stores/modules/tabs";
import { useKeepAliveStore } from "@/stores/modules/keepAlive";
import type { ElForm, FormRules } from "element-plus";
import md5 from "md5";
import { registerApi } from "@/api/modules/register";

const router = useRouter();
const userStore = useUserStore();
const tabsStore = useTabsStore();
const keepAliveStore = useKeepAliveStore();

type FormInstance = InstanceType<typeof ElForm>;
const registerFormRef = ref<FormInstance>();

function validateUserName(rule: any, value: string, callback: any) {
  if (value.match(/^[a-zA-Z0-9]+$/g) !== null) callback();
  else callback(new Error("用户名仅由大小写英文字符与数字0~9组成"));
}
function validatePassword(rule: any, value: string, callback: any) {
  if (value.match(/^[a-zA-Z0-9]+$/g) !== null) callback();
  else callback(new Error("密码仅由大小写英文字符与数字0~9组成"));
}
function validateRepeat(rule: any, value: string, callback: any) {
  if (value.match(/^[a-zA-Z0-9]+$/g) === null) callback(new Error("密码仅由大小写英文字符与数字0~9组成"));
  else if (value === registerForm.password) callback();
  else callback(new Error("密码不一致"));
}
function validateEmail(rule: any, value: string, callback: any) {
  if (value.match(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/g) !== null) callback();
  else callback(new Error("邮箱格式无效"));
}

const registerRules = reactive<FormRules>({
  username: [{ required: true, validator: validateUserName, trigger: "blur" }],
  password: [{ required: true, validator: validatePassword, trigger: "blur" }],
  repeat_password: [{ required: true, validator: validateRepeat, trigger: "blur" }],
  email: [{ required: true, validator: validateEmail, trigger: "blur" }]
});
const loading = ref(false);
const registerForm = reactive<Register.ReqRegisterForm>({
  username: "",
  password: "",
  repeat_password: "",
  email: ""
});
// register
const register = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate(async valid => {
    if (!valid) return;
    loading.value = true;
    try {
      // 1.执行注册接口
      const { data } = await registerApi({ ...registerForm, password: md5(registerForm.password) });

      if (data.code === 200) {
        userStore.userInfo.basicInfo.name = registerForm.username;

        // 2.清空 tabs、keepAlive 数据
        tabsStore.setTabs([]);
        keepAliveStore.setKeepAliveName([]);

        // 3.跳转到登录页
        router.push(LOGIN_URL);
        ElNotification({
          title: getTimeState(),
          message: "注册成功",
          type: "success",
          duration: 3000
        });
      } else {
        ElNotification({
          title: getTimeState(),
          message: "注册失败",
          type: "error",
          duration: 3000
        });
      }
    } finally {
      loading.value = false;
    }
  });
};
function goBack() {
  router.push(LOGIN_URL);
}
onMounted(() => {
  // 监听 enter 事件（调用注册）
  document.onkeydown = (e: KeyboardEvent) => {
    if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
      if (loading.value) return;
      register(registerFormRef.value);
    }
  };
});
</script>

<style scoped lang="scss">
@import "../index.scss";
</style>
