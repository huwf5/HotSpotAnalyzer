<template>
  <div class="conditions_container">
    <div v-for="(cond, cond_index) in conds" :key="cond_index" class="single_condition">
      <el-select
        :model-value="Messages.conds[cond.key]"
        class="condition_item"
        placeholder="选择指标"
        @change="handleKeyChange(cond, $event)"
      >
        <el-option v-for="(cond_name, index) in Messages.conds" :key="index" :label="cond_name" :value="index"></el-option>
      </el-select>
      <el-select
        :model-value="Messages.predicators[cond.predicator]"
        class="condition_item"
        placeholder="触发条件"
        @change="handlePredicatorChange(cond, $event)"
      >
        <el-option
          v-for="(predicator_name, index) in Messages.predicators"
          :key="index"
          :label="predicator_name"
          :value="index"
        ></el-option>
      </el-select>
      <el-input-number
        :model-value="cond.limit"
        :min="0"
        class="condition_item"
        @change="handleLimitChange(cond, $event)"
      ></el-input-number>
      <icon class="operation_icon" @click="removeCond(cond_index)">
        <Minus />
      </icon>
    </div>
    <icon class="operation_icon" @click="addCond">
      <Plus />
    </icon>
  </div>
</template>

<script setup lang="ts">
import icon from "../../../components/el-icon/icon.vue";
import { Messages } from "@/api/interface";
const conds = defineModel<Messages.SingleCond[]>({ required: true });

function removeCond(index: number) {
  conds.value.splice(index, 1);
}
function addCond() {
  conds.value.push({
    key: -1,
    predicator: 0,
    limit: 1000
  });
}
function handleKeyChange(cond: Messages.SingleCond, newKey: number) {
  cond.key = newKey;
}
function handlePredicatorChange(cond: Messages.SingleCond, newPredicator: number) {
  cond.predicator = newPredicator;
}
function handleLimitChange(cond: Messages.SingleCond, newBoundary: number) {
  cond.limit = newBoundary;
}
</script>

<style scoped lang="scss">
.conditions_container {
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
}
.single_condition {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: row;
  flex-grow: 1;
  align-items: center;
  align-self: stretch;
  justify-content: flex-start;
  height: fit-content;
  padding: 0;
  margin: 10px 0;
}
.operation_icon {
  margin: 0 10px;
  cursor: pointer;
}
.condition_item {
  max-width: 200px;
  margin: 0 10px;
}
</style>
