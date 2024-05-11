<template>
  <div>
    <MessageItem
      v-for="(message, index) in messages"
      :key="message.id"
      v-model="messages[index]"
      :checked="$props.checked"
      :checkbox-visible="$props.checkboxVisible"
      :toggle="$props.toggle"
      @need-sort="sortMsg"
      @checked="itemChecked"
    />
  </div>
</template>

<script setup lang="ts">
import { Messages } from "@/api/interface";
import MessageItem from "./MessageItem.vue";
import { comp } from "../util";

const messages = defineModel<Messages.Message[]>({ required: true });
defineProps<{
  checkboxVisible: boolean;
  checked: boolean;
  toggle: boolean;
}>();

const emits = defineEmits<{
  itemChecked: [id: number, state: boolean];
}>();
function itemChecked(id: number, state: boolean) {
  emits("itemChecked", id, state);
}
function sortMsg() {
  messages.value.sort(comp);
}
</script>

<style scoped lang="scss">
.item {
  position: static;
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 10px;

  /* Inside Auto Layout */
  flex: none;
  order: 0;
  align-self: stretch;
  flex-grow: 1;
  margin: 15px 0px;
}
</style>
