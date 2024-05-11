<!-- 💥 这里是一次性加载 LayoutComponents -->
<template>
  <LayoutClassic />
  <ThemeDrawer />
</template>

<script setup lang="ts" name="layout">
import ThemeDrawer from "./components/ThemeDrawer/index.vue";
import LayoutClassic from "./LayoutClassic/index.vue";
</script>

<style scoped lang="scss">
.layout {
  min-width: 600px;
}
</style>
