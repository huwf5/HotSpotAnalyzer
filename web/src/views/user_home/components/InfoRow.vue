/* stylelint-disable order/properties-order */
<template>
  <div class="single_info" @click.stop="$emit('rowClicked')">
    <div class="text_container">
      <span class="info_text">{{ $props.displayText }}</span>
    </div>
    <span v-if="!$props.selected" class="info_text">{{ $props.displayValue }}</span>
    <div v-else class="slot_container">
      <el-popover :visible="$props.toolTipVisivle" placement="right">
        <template #reference>
          <slot />
        </template>
        <template #default>
          <span>{{ $props.tipText }}</span>
        </template>
      </el-popover>
    </div>
    <div v-if="$props.displayIcon">
      <icon v-if="!$props.selected"><Edit /></icon>
      <icon v-else :size="20" @click="$emit('checked')"><Check /></icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import icon from "@/components/el-icon/icon.vue";
withDefaults(
  defineProps<{
    selected: boolean;
    displayText: string;
    displayValue: string;
    displayIcon?: boolean;
    toolTipVisivle?: boolean;
    tipText?: string;
  }>(),
  {
    displayIcon: true,
    toolTipVisivle: false,
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
  cursor: pointer;
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
  padding: 5px;
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
