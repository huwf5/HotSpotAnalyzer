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
    <el-form-item prop="captcha">
      <div class="captcha_container">
        <el-input v-model="registerForm.captcha" placeholder="验证码">
          <template #prefix>
            <el-icon class="el-input__icon">
              <Message />
            </el-icon>
          </template>
        </el-input>
        <el-button
          plain
          round
          style="margin: 0 0 0 10px"
          @click="getCaptcha"
          :disabled="countdown !== 0"
          :loading="captchaLoading"
          >{{ getCaptchaButtonText }}
        </el-button>
      </div>
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
import { getCaptchaApi, registerApi } from "@/api/modules/register";
import { validateEmail, validatePassword, validateUserName } from "@/utils/eleValidate";

const router = useRouter();
const userStore = useUserStore();
const tabsStore = useTabsStore();
const keepAliveStore = useKeepAliveStore();

type FormInstance = InstanceType<typeof ElForm>;
const registerFormRef = ref<FormInstance>();
const getCaptchaButtonText = ref("获取验证码");
const timer = ref<NodeJS.Timeout>();
const captchaLoading = ref(false);
const countdown = ref(0);

function validateRepeat(rule: any, value: string, callback: any) {
  if (value.match(/^[a-zA-Z0-9]+$/g) === null) callback(new Error("密码仅由大小写英文字符与数字0~9组成"));
  else if (value === registerForm.password) callback();
  else callback(new Error("密码不一致"));
}
function validateCaptcha(rule: any, value: string, callback: any) {
  if (value.length === 0) callback(new Error("请输入验证码"));
  else callback();
}
function getCaptcha() {
  registerFormRef.value?.validateField("email", isValid => {
    if (isValid) {
      captchaLoading.value = true;
      getCaptchaApi({ email: registerForm.email })
        .then(() => {
          countdown.value = 60;
          captchaLoading.value = false;
          getCaptchaButtonText.value = "60秒后重新获取";
          timer.value = setInterval(() => {
            countdown.value--;
            if (countdown.value > 0) {
              getCaptchaButtonText.value = countdown.value.toString() + "秒后重新获取";
            } else {
              getCaptchaButtonText.value = "重新获取";
              clearInterval(timer.value);
            }
          }, 1000);
        })
        .catch(() => (captchaLoading.value = false));
    }
  });
}

const registerRules = reactive<FormRules>({
  username: [{ required: true, validator: validateUserName, trigger: "blur" }],
  password: [{ required: true, validator: validatePassword, trigger: "blur" }],
  repeat_password: [{ required: true, validator: validateRepeat, trigger: "blur" }],
  email: [{ required: true, validator: validateEmail, trigger: "blur" }],
  captcha: [{ required: true, validator: validateCaptcha, trigger: "blur" }]
});
const loading = ref(false);
const registerForm = reactive<Register.ReqRegisterForm>({
  username: "",
  password: "",
  repeat_password: "",
  email: "",
  captcha: ""
});
// register
const register = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate(async valid => {
    if (!valid) return;
    loading.value = true;
    try {
      // 1.执行注册接口
      await registerApi(registerForm).then(() => {
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
      });
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
.captcha_container {
  display: flex;
  flex: none;
  flex-direction: row;
  flex-grow: 1;
  padding: 0;
  margin: 0;
}
</style>
