<template>
  <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" size="large">
    <el-form-item prop="email">
      <el-input v-model="loginForm.email" placeholder="邮箱地址" clearable>
        <template #prefix>
          <el-icon class="el-input__icon">
            <Message />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <div class="password_row">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="密码"
          show-password
          autocomplete="new-password"
          clearable
        >
          <template #prefix>
            <el-icon class="el-input__icon">
              <lock />
            </el-icon>
          </template>
        </el-input>
        <el-button plain round type="text" @click="forgetPwd">忘记密码</el-button>
      </div>
    </el-form-item>
  </el-form>
  <div class="login-btn">
    <el-button icon="EditPen" round size="large" @click="register"> 注册 </el-button>
    <el-button icon="UserFilled" round size="large" type="primary" :loading="loading" @click="login(loginFormRef)">
      登录
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { HOME_URL, REGISTER_URL } from "@/config";
import { getTimeState } from "@/utils";
import { Login } from "@/api/interface";
import { ElNotification } from "element-plus";
import { loginApi } from "@/api/modules/login";
import { useUserStore } from "@/stores/modules/user";
import { useTabsStore } from "@/stores/modules/tabs";
import { useKeepAliveStore } from "@/stores/modules/keepAlive";
import { initDynamicRouter } from "@/routers/modules/dynamicRouter";
import type { ElForm, FormRules } from "element-plus";
import { validateEmail, validatePassword } from "@/utils/eleValidate";

const router = useRouter();
const userStore = useUserStore();
const tabsStore = useTabsStore();
const keepAliveStore = useKeepAliveStore();

type FormInstance = InstanceType<typeof ElForm>;
const loginFormRef = ref<FormInstance>();
const loginRules = reactive<FormRules>({
  email: [{ required: true, validator: validateEmail, trigger: "blur" }],
  password: [{ required: true, validator: validatePassword, trigger: "blur" }]
});

const loading = ref(false);
const loginForm = reactive<Login.ReqLoginForm>({
  email: userStore.userInfo.contactInfo.email,
  password: ""
});

// login
const login = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate(async valid => {
    if (!valid) return;
    loading.value = true;
    try {
      // 1.执行登录接口
      let { data } = await loginApi(loginForm);
      userStore.setTokens(data.token, data.refresh, data.token_lifetime * 1000);
      userStore.setUserContactInfo({ email: data.email });
      userStore.setUserBasicInfo({ name: data.username });
      userStore.setUserRole({ role: data.role });

      // 2.添加动态路由
      await initDynamicRouter();

      // 3.清空 tabs、keepAlive 数据
      tabsStore.setTabs([]);
      keepAliveStore.setKeepAliveName([]);

      // 4.跳转到首页
      router.replace(HOME_URL);
      ElNotification({
        title: getTimeState(),
        message: "欢迎登录 Geeker-Admin",
        type: "success",
        duration: 3000
      });
    } finally {
      loading.value = false;
    }
  });
};

const emits = defineEmits<{
  forget: any;
}>();

function forgetPwd() {
  validateEmail(null, loginForm.email, (e?: Error) => {
    if (e === undefined) userStore.userInfo.contactInfo.email = loginForm.email;
  });
  emits("forget");
}

function register() {
  router.push(REGISTER_URL);
}

onMounted(() => {
  // 监听 enter 事件（调用登录）
  document.onkeydown = (e: KeyboardEvent) => {
    if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
      if (loading.value) return;
      login(loginFormRef.value);
    }
  };
});
</script>

<style scoped lang="scss">
@import "../index.scss";
.password_row {
  display: flex;
  flex: none;
  flex-direction: row;
  flex-grow: 1;
}
</style>
