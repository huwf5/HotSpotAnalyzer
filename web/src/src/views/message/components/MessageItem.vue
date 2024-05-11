<template>
  <div v-if="message.display" class="item_container">
    <div :class="{ default: checkboxVisible, scaled: !checkboxVisible }" style="transition: all 0.25s ease-out; padding: 0px">
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
  color.value = message.value.starred ? "#FFF102" : "";
});

const time = computed(() => {
  return message.value.time;
});
const isChecked = ref(false);
const color = ref(message.value.starred ? "#FFF102" : "");
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
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 10px;

  /* Inside Auto Layout */
  flex: none;
  align-self: stretch;
  flex-grow: 0;
  margin: 8px 0px;

  border-radius: 15px;
  box-shadow: 0px 0px 5px 1px v-bind("shadow_color");
}

.message_head {
  position: static;
  max-height: 200px;
  width: 0;
  max-width: 200px;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;

  /* Inside Auto Layout */
  flex: none;
  flex-grow: 1;
  margin: 0px 10px;
  overflow: hidden;
}

.title {
  position: static;
  width: fit-content;
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 10px 75px 10px 10px;

  /* Inside Auto Layout */
  flex: none;
  flex-grow: 0;
  margin: 10px 10px;
  padding: 0px;

  /* Base/Base Normal */
  font-family: Inter;
  font-size: 14px;
  font-weight: 500;
  line-height: 22px;
  letter-spacing: 0%;
  text-align: center;
}

.content {
  position: static;
  width: fit-content;
  height: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 0px 10px;

  /* Inside Auto Layout */
  flex: none;
  flex-grow: 0;
  margin: 0px;

  /* Base/Base Normal */
  color: rgb(115, 115, 115);
  font-family: Inter;
  font-size: 12px;
  font-weight: 500;
  line-height: 22px;
  letter-spacing: 0%;
  text-align: start;
}

.event_body {
  position: static;
  height: fit-content;
  width: 0;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 10px;

  /* Inside Auto Layout */
  flex: none;
  align-self: stretch;
  flex-grow: 2;
  margin: 0px 10px;
}

.side_bar {
  position: static;
  width: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  padding: 0px 15px 0px 15px;

  /* Inside Auto Layout */
  flex: none;
  flex-grow: 0;
  align-self: stretch;
  margin: 0px 10px;
}

.star {
  position: static;
  width: fit-content;
  /* 自动布局 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 0px 4.5px 0px 4.5px;

  /* Inside Auto Layout */
  flex: none;
  flex-grow: 1;
  margin: 10px 0px;
}

.scaled {
  transform: scale(0);
  transform-origin: left;
  margin: 0px 10px;
}

.default {
  transform: scale(1);
  /* 缩放中心 */
  transform-origin: left;
  margin: 0px 20px;
}
</style>
