<template>
  <div class="setting_panel">
    <label class="setting_title">{{ $props.settingTitle }}</label>
    <div class="setting_container">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  settingTitle: string;
}>();
</script>

<style scoped lang="scss">
.setting_panel {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 1;
  align-items: flex-start;
  align-self: stretch;
  justify-content: flex-start;
  height: fit-content;
  padding: 10px;
  margin: 10px 5%;
}
.setting_title {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 0;
  align-items: flex-start;
  justify-content: flex-start;
  order: 0;
  width: fit-content;
  height: fit-content;
  padding: 10px;
  margin: 0;
  font-size: 20px;
  font-weight: 300;
  line-height: 29px;
  text-align: left;
  letter-spacing: 0;
}
.setting_container {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 1;
  align-items: flex-start;
  align-self: stretch;
  justify-content: flex-start;
  height: fit-content;
  padding: 0;
  margin: 0;
  overflow: hidden;
  border-radius: 15px;
  outline: 1px solid var(--el-border-color);
  box-shadow: var(--el-box-shadow-light);
}
</style>
