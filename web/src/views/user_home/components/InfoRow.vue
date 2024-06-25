/* stylelint-disable order/properties-order */
<template>
  <div class="single_info" @click.stop="$emit('rowClicked')">
    <div v-if="displayText.length > 0" class="text_container">
      <span class="info_text">{{ $props.displayText }}</span>
    </div>
    <span v-if="!$props.selected" class="info_text">{{ $props.displayValue }}</span>
    <div v-else class="slot_container">
      <el-popover :visible="$props.toolTipVisivle" placement="right" width="200">
        <template #reference>
          <slot />
        </template>
        <template #default>
          <span>{{ $props.tipText }}</span>
        </template>
      </el-popover>
    </div>
    <div v-if="$props.displayIcon">
      <slot name="icon">
        <el-icon v-if="!$props.selected"><Edit /></el-icon>
        <el-icon v-else :size="20" @click="$emit('checked')"><Check /></el-icon>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    selected: boolean;
    displayText: string;
    displayValue?: string;
    displayIcon?: boolean;
    cursor?: string;
    toolTipVisivle?: boolean;
    tipText?: string;
  }>(),
  {
    displayValue: "",
    displayIcon: true,
    toolTipVisivle: false,
    cursor: "auto",
    tipText: ""
  }
);
defineEmits<{
  rowClicked: any;
  checked: any;
}>();
</script>

<style scoped lang="scss">
.single_info {
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
  padding: 15px 20px;
  margin: 0;
  cursor: v-bind("cursor");
}
.single_info:hover {
  background-color: rgba($color: #afafaf, $alpha: 20%);
}
.text_container {
  position: static;
  display: flex;
  flex: none;
  flex-direction: row;
  flex-grow: 1;
  align-items: center;
  align-self: stretch;
  justify-content: flex-start;
  max-width: 200px;
}
.info_text {
  position: static;
  display: flex;
  flex: none;
  flex-direction: row;
  flex-grow: 1;
  align-items: center;
  align-self: stretch;
  justify-content: flex-start;
  font-size: 13px;
  font-weight: 300;
  line-height: 30px;
  text-align: left;
  letter-spacing: 0;
}
.slot_container {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  align-items: center;
  align-self: stretch;
}
</style>
