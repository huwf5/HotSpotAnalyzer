<template>
  <div class="login-container flx-center">
    <div class="login-box">
      <SwitchDark class="dark" />
      <div class="login-left">
        <img class="login-left-img" src="@/assets/images/login_left.png" alt="login" />
      </div>
      <div class="login-form">
        <div class="login-logo">
          <img class="login-icon" src="@/assets/images/logo.svg" alt="" />
          <h2 class="logo-text">HotSpotAnalyzer</h2>
        </div>
        <LoginForm v-if="login_page_visible" @forget="jumpToForget" />
        <ForgetForm v-else :email="login_page_email" @finished="jumpToLogin"></ForgetForm>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="login">
import { ref } from "vue";
import LoginForm from "./components/LoginForm.vue";
import ForgetForm from "./components/ForgetForm.vue";
import SwitchDark from "@/components/SwitchDark/index.vue";
import { useUserStore } from "@/stores/modules/user";

const login_page_visible = ref(true);
const login_page_email = ref("");
const store = useUserStore();

function jumpToForget(email: string) {
  login_page_email.value = email;
  login_page_visible.value = false;
}

function jumpToLogin(email: string) {
  store.userInfo.contactInfo.email = email;
  login_page_visible.value = true;
}
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
