<template>
  <div class="filter-container">
    <el-popover :visible="filterVisible" placement="bottom">
      <template #reference>
        <icon class="filter-icon" :color="color" @click="handleFilterClick">
          <Filter />
        </icon>
      </template>
      <template #default>
        <div v-click-outside="handleClickOutside">
          <el-checkbox v-model="sysChecked" @change="displaySystemMessage" style="margin: 0 10px">显示系统消息</el-checkbox>
          <el-checkbox v-model="readChecked" @change="displayReadMessage" style="margin: 0 10px">显示已读消息</el-checkbox>
        </div>
      </template>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import icon from "../../../components/el-icon/icon.vue";

const color = ref("");
const filterVisible = ref(false);
const ignore = ref(false);
const emits = defineEmits<{
  systemMessageDisplay: [state: boolean];
  readMessageDisplay: [state: boolean];
}>();
const sysChecked = ref(true);
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

function displaySystemMessage(val: boolean) {
  emits("systemMessageDisplay", val);
}

function displayReadMessage(val: boolean) {
  emits("readMessageDisplay", val);
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
