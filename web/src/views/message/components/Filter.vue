<template>
  <div class="filter-container">
    <el-popover :visible="filterVisible" placement="bottom">
      <template #reference>
        <el-icon class="filter-icon" :color="color" @click="handleFilterClick">
          <Filter />
        </el-icon>
      </template>
      <template #default>
        <div v-click-outside="handleClickOutside">
          <el-checkbox v-model="infoChecked" @change="displayInfoMsg" style="margin: 0 10px">显示提醒消息</el-checkbox>
          <el-checkbox v-model="warnChecked" @change="displayWarnMsg" style="margin: 0 10px">显示预警消息</el-checkbox>
          <el-checkbox v-model="readChecked" @change="displayReadMsg" style="margin: 0 10px">显示已读消息</el-checkbox>
        </div>
      </template>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const color = ref("");
const filterVisible = ref(false);
const ignore = ref(false);
const emits = defineEmits<{
  infoMsgDisplay: [state: boolean];
  warnMsgDisplay: [state: boolean];
  readMsgDisplay: [state: boolean];
}>();
const infoChecked = ref(true);
const warnChecked = ref(true);
const readChecked = ref(true);

function handleFilterClick() {
  filterVisible.value = !filterVisible.value;
  ignore.value = true;
  color.value = filterVisible.value ? "#3AACFF" : "";
}

function handleClickOutside() {
  if (ignore.value) {
    ignore.value = false;
    return;
  }
  filterVisible.value = false;
  color.value = filterVisible.value ? "#3AACFF" : "";
}

function displayInfoMsg(val: boolean) {
  emits("infoMsgDisplay", val);
}
function displayWarnMsg(val: boolean) {
  emits("warnMsgDisplay", val);
}
function displayReadMsg(val: boolean) {
  emits("readMsgDisplay", val);
}
</script>

<style scoped lang="scss">
.filter-container {
  position: relative;
  cursor: pointer;
}
.split_line {
  /* Inside Auto Layout */
  flex: none;
  flex-grow: 1;
  align-self: stretch;
  order: 1;
  height: 0;
  margin: 5px 0;
  border: 1px solid;
}
</style>
