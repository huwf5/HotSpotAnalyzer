<template>
  <div v-if="message.display" class="item_container">
    <slot name="prefix" />
    <el-icon :size="20">
      <Warning v-if="message.type !== Messages.MessageType.WARN" />
      <WarnTriangleFilled v-else />
    </el-icon>
    <div class="message_head">
      <span class="title">{{ message.message.title }}</span>
      <span class="content" style="margin: 0 10px; overflow: hidden">
        负面指数：{{ message.message.negative_sentiment_ratio }}
      </span>
    </div>
    <div class="event_body">
      <span class="content">{{ message.message.summary }}</span>
    </div>
    <slot name="suffix" />
  </div>
</template>

<script setup lang="ts">
import { Messages } from "@/api/interface";
import { computed } from "vue";
const message = defineModel<Messages.ResMessage & { display: boolean }>({ required: true });
const shadow_color = computed(() => {
  console.log(message.value.type);
  if (message.value.is_read) return "163, 163, 163";
  switch (message.value.type) {
    case Messages.MessageType.WARN:
      return "255, 00, 00";
    case Messages.MessageType.INFO:
      return "64, 158, 255";
    default:
      return "163, 163, 163";
  }
});
</script>

<style scoped lang="css">
.item_container {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 70%;
  min-width: 500px;
  height: fit-content;
  max-height: 100px;
  cursor: pointer;
  padding: 10px;
  margin: 8px 0;
  box-shadow: 0 0 5px 1px v-bind("'rgba(' + shadow_color + ', 40%)'");
  &:hover {
    box-shadow: 0 0 5px 1px v-bind("'rgba(' + shadow_color + ', 100%)'");
  }
}
.message_head {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  width: 0;
  width: 110px;
  padding: 0;
  margin: 0 0 0 10px;
  overflow: hidden;
}
.title {
  position: static;
  width: 100%;
  height: fit-content;
  padding: 10px 75px 10px 10px;
  padding: 0;
  margin: 10px;
  overflow: hidden;

  /* Base/Base Normal */
  font-family: Inter;
  font-size: 14px;
  font-weight: 800;
  line-height: 22px;
  text-align: start;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  justify-content: center;
  width: fit-content;
  height: 100%;
  overflow: scroll;
  font-family: Inter;
  font-size: 12px;
  font-weight: 500;
  line-height: 22px;

  /* Base/Base Normal */
  color: var(--el-text-color-secondary);
  text-align: start;
  letter-spacing: 0%;
  word-break: break-all;
}
.event_body {
  position: static;

  /* 自动布局 */
  display: flex;

  /* Inside Auto Layout */
  flex: none;
  flex-direction: column;
  flex-grow: 1;
  align-items: flex-start;
  align-self: stretch;
  justify-content: center;
  width: 0;
  min-width: 200px;
}
</style>
