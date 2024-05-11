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
  settingTitle: String;
}>();
</script>

<style scoped lang="scss">
.setting_panel {
  position: static;
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 10px 10px;
  margin: 10px 5%;

  /* Inside Auto Layout */
  flex: none;
  align-self: stretch;
  flex-grow: 1;
}

.setting_title {
  position: static;
  width: fit-content;
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 10px;

  /* Inside Auto Layout */
  flex: none;
  order: 0;
  flex-grow: 0;
  margin: 0px;

  font-size: 20px;
  font-weight: 300;
  line-height: 29px;
  letter-spacing: 0px;
  text-align: left;
}

.setting_container {
  position: static;
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

  /* Inside Auto Layout */
  flex: none;
  align-self: stretch;
  flex-grow: 1;
  margin: 0px;
  padding: 0px;

  border-radius: 15px;
  box-shadow: 0px 1.5px 6px 0px;
  overflow: hidden;
}
</style>
