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
        <LoginForm v-if="login_page_visible" @forget="login_page_visible = false" />
        <ForgetForm v-else @finished="login_page_visible = true"></ForgetForm>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="login">
import { ref } from "vue";
import LoginForm from "./components/LoginForm.vue";
import ForgetForm from "./components/ForgetForm.vue";
import SwitchDark from "@/components/SwitchDark/index.vue";

const login_page_visible = ref(true);
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
