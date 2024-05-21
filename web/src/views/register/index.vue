<template>
  <div class="register-container flx-center">
    <div class="register-box">
      <SwitchDark class="dark" />
      <div class="register-left">
        <img class="register-left-img" src="@/assets/images/login_left.png" alt="register" />
      </div>
      <div class="register-form">
        <div class="register-logo">
          <img class="register-icon" src="@/assets/images/logo.svg" alt="" />
          <h2 class="logo-text">HotSpotAnalyzer</h2>
        </div>
        <RegisterForm />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="register">
import RegisterForm from "./components/RegisterForm.vue";
import SwitchDark from "@/components/SwitchDark/index.vue";
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
