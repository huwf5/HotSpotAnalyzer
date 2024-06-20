<template>
  <div v-if="message.display" class="item_container">
    <div :class="{ default: checkboxVisible, scaled: !checkboxVisible }" style="padding: 0; transition: all 0.25s ease-out">
      <el-checkbox v-model="isChecked" @change="dealChecked"></el-checkbox>
    </div>
    <icon :size="20">
      <Warning v-if="message.type === 0" />
      <WarnTriangleFilled v-else />
    </icon>
    <div class="message_head">
      <label class="title">{{ Messages.titles[message.id] }}</label>
      <label v-if="message.type === 0" class="content">{{ message.content }}</label>
      <div v-else>
        <label class="content">来源：{{ Messages.platforms[(message as Messages.Event).platform] }}</label>
        <label class="content">关键词：{{ (message as Messages.Event).keywords }}</label>
      </div>
    </div>
    <div class="event_body">
      <label v-if="message.type !== 0" class="content">{{ (message as Messages.Event).title }}</label>
      <label v-if="message.type !== 0" class="content">{{ message.content }}</label>
    </div>
    <div class="side_bar">
      <div class="star">
        <icon style="cursor: pointer" :color="color" @click="dealStared">
          <StarFilled />
        </icon>
      </div>
      <label class="content">{{ message.unread ? "未读" : "已读" }}</label>
      <label class="content">{{ time }}</label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Messages } from "@/api/interface";
import icon from "@/components/el-icon/icon.vue";
import { computed, watch } from "vue";
import { ref } from "vue";
const message = defineModel<Messages.Message>({ required: true });
const props = defineProps<{
  checkboxVisible: boolean;
  checked: boolean;
  toggle: boolean;
}>();
watch(props, newVal => {
  isChecked.value = newVal.checked;
});

const time = computed(() => {
  return message.value.time;
});
const isChecked = ref(false);
const color = computed(() => {
  return message.value.starred ? "#FFF102" : "";
});
const shadow_color = computed(() => {
  if (!message.value.unread) return "#737373";
  switch (message.value.type) {
    case 1:
      return "#FFBF00";
    case 2:
      return "#FF0000";
    default:
      return "#008BFF";
  }
});

const emits = defineEmits<{
  checked: [id: number, state: boolean];
  needSort: any;
}>();
function dealChecked(val: boolean) {
  emits("checked", message.value.id, val);
}
function dealStared() {
  message.value.starred = !message.value.starred;
  emits("needSort");
}
</script>

<style scoped lang="scss">
.item_container {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: row;
  flex-grow: 0;
  align-items: center;
  align-self: stretch;
  justify-content: flex-start;
  height: fit-content;
  padding: 10px;
  margin: 8px 0;
  border-radius: 15px;
  box-shadow: 0 0 5px 1px v-bind("shadow_color");
}
.message_head {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 1;
  align-items: flex-start;
  justify-content: flex-start;
  width: 0;
  max-width: 200px;
  max-height: 200px;
  padding: 0;
  margin: 0 10px;
  overflow: hidden;
}
.title {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 0;
  align-items: center;
  justify-content: flex-start;
  width: fit-content;
  height: fit-content;
  padding: 10px 75px 10px 10px;
  padding: 0;
  margin: 10px;

  /* Base/Base Normal */
  font-family: Inter;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
  text-align: center;
  letter-spacing: 0%;
}
.content {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 0;
  align-items: center;
  justify-content: flex-start;
  width: fit-content;
  height: fit-content;
  padding: 0 10px;
  margin: 0;
  font-family: Inter;
  font-size: 12px;
  font-weight: 500;
  line-height: 22px;

  /* Base/Base Normal */
  color: rgb(115 115 115);
  text-align: start;
  letter-spacing: 0%;
}
.event_body {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 2;
  align-items: flex-start;
  align-self: stretch;
  justify-content: flex-start;
  width: 0;
  height: fit-content;
  padding: 10px;
  margin: 0 10px;
}
.side_bar {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 0;
  align-items: center;
  align-self: stretch;
  justify-content: flex-end;
  width: fit-content;
  padding: 0 15px;
  margin: 0 10px;
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
.scaled {
  margin: 0 10px;
  transform: scale(0);
  transform-origin: left;
}
.default {
  margin: 0 20px;
  transform: scale(1);

  /* 缩放中心 */
  transform-origin: left;
}
</style>
