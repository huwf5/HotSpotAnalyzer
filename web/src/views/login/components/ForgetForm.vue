<template>
  <el-form ref="registerFormRef" :model="resetPwdForm" :rules="resetPwdRules" size="large">
    <el-form-item prop="email">
      <el-input v-model="resetPwdForm.email" placeholder="邮箱地址" clearable>
        <template #prefix>
          <el-icon class="el-input__icon">
            <Message />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input
        v-model="resetPwdForm.password"
        type="password"
        placeholder="新密码"
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
      <el-input v-model="resetPwdForm.repeat_password" type="password" show-password placeholder="确认密码" clearable>
        <template #prefix>
          <el-icon class="el-input__icon">
            <Lock />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="verify_code">
      <div class="captcha_container">
        <el-input v-model="resetPwdForm.verify_code" placeholder="验证码">
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
  <div class="login-btn">
    <el-button icon="Back" round size="large" @click="goBack"> 返回 </el-button>
    <el-button icon="Check" round size="large" type="primary" :loading="loading" @click="resetPwd(registerFormRef)">
      设置密码
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { Login, Register } from "@/api/interface";
import { useUserStore } from "@/stores/modules/user";
import { ElMessage, type ElForm, type FormRules } from "element-plus";
import { getCaptchaApi } from "@/api/modules/register";
import { forgetPwdApi } from "@/api/modules/login";
import { validateEmail, validatePassword } from "@/utils/eleValidate";

const userStore = useUserStore();

type FormInstance = InstanceType<typeof ElForm>;
const registerFormRef = ref<FormInstance>();
const getCaptchaButtonText = ref("获取验证码");
const timer = ref<NodeJS.Timeout>();
const captchaLoading = ref(false);
const countdown = ref(0);

function validateRepeat(rule: any, value: string, callback: any) {
  if (value.match(/^[a-zA-Z0-9]+$/g) === null) callback(new Error("密码仅由大小写英文字符与数字0~9组成"));
  else if (value === resetPwdForm.password) callback();
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
      getCaptchaApi({ email: resetPwdForm.email, usage: Register.CodeUsage.RESETPWD })
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

const resetPwdRules = reactive<FormRules>({
  password: [{ required: true, validator: validatePassword, trigger: "blur" }],
  repeat_password: [{ required: true, validator: validateRepeat, trigger: "blur" }],
  email: [{ required: true, validator: validateEmail, trigger: "blur" }],
  verify_code: [{ required: true, validator: validateCaptcha, trigger: "blur" }]
});
const loading = ref(false);
const resetPwdForm = reactive<Login.ReqForgetPwd & { repeat_password: string }>({
  password: "",
  repeat_password: "",
  email: "",
  verify_code: ""
});
const emits = defineEmits<{
  finished: any;
}>();
// reset password
const resetPwd = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate(async valid => {
    if (!valid) return;
    loading.value = true;
    try {
      // 1.执行重置密码接口
      await forgetPwdApi(resetPwdForm).then(() => {
        userStore.userInfo.contactInfo.email = resetPwdForm.email;
        ElMessage({
          type: "success",
          message: "密码重置成功",
          duration: 3000
        });
        // 2.返回到登录页
        emits("finished");
      });
    } finally {
      loading.value = false;
    }
  });
};
function goBack() {
  emits("finished");
}
onMounted(() => {
  // 监听 enter 事件（调用注册）
  document.onkeydown = (e: KeyboardEvent) => {
    if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
      if (loading.value) return;
      resetPwd(registerFormRef.value);
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
