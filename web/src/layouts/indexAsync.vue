<!-- 💥 这里是异步加载 LayoutComponents -->
<template>
  <suspense>
    <template #default>
      <LayoutClassic />
    </template>
    <template #fallback>
      <Loading />
    </template>
  </suspense>
  <ThemeDrawer />
</template>

<script setup lang="ts" name="layoutAsync">
import { defineAsyncComponent } from "vue";
import Loading from "@/components/Loading/index.vue";
import ThemeDrawer from "./components/ThemeDrawer/index.vue";

const LayoutClassic = defineAsyncComponent(() => import("./LayoutClassic/index.vue"));
</script>

<style scoped lang="scss">
.layout {
  min-width: 600px;
}
</style>
