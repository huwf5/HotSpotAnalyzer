<template>
  <MessageItem v-for="(message, index) in messages" v-model="messages[index]" :key="message.id" @click="msgClicked(message)">
    <template #prefix>
      <div class="check-box">
        <el-checkbox v-model="message.selected" @change="itemChecked(message)" @click.stop />
      </div>
    </template>
    <template #suffix>
      <div class="side-bar">
        <div class="star" @click.stop>
          <el-icon :color="message.is_starred ? '#FFF102' : ''" @click="itemStarred(message)">
            <StarFilled />
          </el-icon>
        </div>
        <span>{{ message.is_read ? "已读" : "未读" }}</span>
        <span>{{ transferTime(message.message.created_at) }}</span>
      </div>
    </template>
  </MessageItem>
</template>

<script setup lang="ts">
import { Messages } from "@/api/interface";
import MessageItem from "./MessageItem.vue";
import { comp } from "../util";

const messages = defineModel<(Messages.ResMessage & { display: boolean; selected: boolean })[]>({ required: true });
defineProps<{
  checkboxVisible: boolean;
}>();

const current = new Date();
const emits = defineEmits<{
  itemChecked: [msg: Messages.ResMessage];
  itemStarred: [msg: Messages.ResMessage];
  itemClicked: [msg: Messages.ResMessage & { selected: boolean }];
}>();
function itemChecked(msg: Messages.ResMessage) {
  emits("itemChecked", msg);
}
function itemStarred(msg: Messages.ResMessage) {
  msg.is_starred = !msg.is_starred;
  emits("itemStarred", msg);
  messages.value.sort(comp);
}
function transferTime(time: string) {
  let msg_created_at = new Date(time);
  return msg_created_at.getFullYear() < current.getFullYear() ||
    msg_created_at.getMonth() < current.getMonth() ||
    msg_created_at.getDate() < current.getDate()
    ? time.split("T")[0]
    : time.split("T")[1].split("+")[0];
}
function msgClicked(msg: Messages.ResMessage & { selected: boolean }) {
  emits("itemClicked", msg);
}
</script>

<style scoped lang="scss">
.check-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: v-bind("checkboxVisible ? '25px' : '0'");
  overflow: hidden;
}
.side-bar {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  align-items: flex-end;
  align-self: stretch;
  justify-content: flex-end;
  width: 100px;
  padding: 0 15px 0 0;
}
.side-bar span {
  /* Inside Auto Layout */
  font-family: Inter;
  font-size: 12px;
  font-weight: 500;
  line-height: 22px;

  /* Base/Base Normal */
  color: rgb(115 115 115);
  text-align: start;
  letter-spacing: 0%;
  word-break: break-all;
}
.star {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 1;
  align-items: center;
  justify-content: flex-start;
  width: fit-content;
  padding: 0 4.5px;
  margin: 10px 0;
}
</style>
