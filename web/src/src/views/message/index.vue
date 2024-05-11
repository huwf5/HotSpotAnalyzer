<template>
  <div class="message">
    <div class="headline">
      <label class="message_title">消息通知</label>
      <div class="operations">
        <Filter class="operation_icon" @system-message-display="displaySystemMsg" @read-message-display="displayReadMsg" />
        <icon class="operation_icon" :color="checkboxColor" @click="checkboxVisibilityVaryfied">
          <Finished />
        </icon>
        <icon class="operation_icon" :class="{ reload: loading }" @click="refresh">
          <Refresh />
        </icon>
      </div>
    </div>
    <MessageList
      class="message_list"
      v-model="messages"
      :checkbox-visible="checkboxVisible"
      :checked="checkAll"
      :toggle="toggleAll"
      @item-checked="dealMsgCheck"
    />
    <div class="bottom">
      <div v-if="checkboxVisible" class="select_all">
        <el-button v-if="!checkAll" type="primary" plain icon="Plus" @click="dealSelectAll">全选</el-button>
        <el-button v-else type="primary" plain icon="Check" @click="dealSelectAll">全选</el-button>
      </div>
      <el-button type="warning" :disabled="!checkboxVisible" plain circle icon="Star" @click="dealStarAll"></el-button>
      <el-button type="success" :disabled="!checkboxVisible" plain icon="Check" @click="dealReadAll">标记已读</el-button>
      <el-button type="danger" :disabled="!checkboxVisible" plain icon="Delete" @click="dealDeleteAll">删除消息</el-button>
    </div>
  </div>
</template>

<script setup lang="ts" name="message">
import Filter from "./components/Filter.vue";
import icon from "../../components/el-icon/icon.vue";
import MessageList from "./components/MessageList.vue";
import { ref } from "vue";
import { Messages } from "@/api/interface";
import { comp } from "./util";

const checkboxVisible = ref(false);
const checkboxColor = ref("");
const messages = ref<Messages.Message[]>([]);
const checked = ref<Set<number>>(new Set<number>());
const checkAll = ref(false);
const toggleAll = ref(false);
const loading = ref(false);
const sysMsgVisible = ref(true);
const readMsgVisible = ref(true);

function displaySystemMsg(state: boolean) {
  sysMsgVisible.value = state;
  if (state) {
    messages.value.forEach(val => {
      if (val.type === 0) {
        val.display = val.unread ? true : readMsgVisible.value;
        if (checkAll.value) checked.value.add(val.id);
      }
    });
  } else {
    messages.value.forEach(val => {
      if (val.type === 0) {
        if (checked.value.has(val.id)) checked.value.delete(val.id);
        val.display = false;
      }
    });
  }
}
function displayReadMsg(state: boolean) {
  readMsgVisible.value = state;
  if (state) {
    messages.value.forEach(val => {
      if (!val.unread) {
        val.display = val.type === 0 ? sysMsgVisible.value : true;
        if (checkAll.value) checked.value.add(val.id);
      }
    });
  } else {
    messages.value.forEach(val => {
      if (!val.unread) {
        if (checked.value.has(val.id)) checked.value.delete(val.id);
        val.display = false;
      }
    });
  }
}
function checkboxVisibilityVaryfied() {
  checkboxVisible.value = !checkboxVisible.value;
  checkboxColor.value = checkboxVisible.value ? "#3AACFF" : "";
  if (!checkboxVisible.value) checked.value.clear();
  checkAll.value = false;
}
function refresh() {
  loading.value = true;
  // TODO - 需要实现请求后端数据
  setTimeout(() => {
    loading.value = false;
  }, 2000);
  return;
}
function dealStarAll() {
  if (checked.value.size === 0) return;
  let starAll = false;
  messages.value.forEach(msg => {
    if (checked.value.has(msg.id)) {
      starAll = starAll || !msg.starred;
    }
  });
  if (starAll) {
    messages.value.forEach(msg => {
      if (checked.value.has(msg.id)) {
        msg.starred = true;
      }
    });
  } else {
    messages.value.forEach(msg => {
      if (checked.value.has(msg.id)) {
        msg.starred = false;
      }
    });
  }
  messages.value.sort(comp);
}
function dealReadAll() {
  if (checked.value.size === 0) return;
  messages.value.forEach(msg => {
    if (checked.value.has(msg.id)) {
      msg.unread = false;
    }
  });
  messages.value.sort(comp);
}
function dealDeleteAll() {
  if (checked.value.size === 0) return;
  for (let index = messages.value.length - 1; index >= 0; index--) {
    if (checked.value.has(messages.value[index].id)) messages.value.splice(index, 1);
  }
  checked.value.clear();
  checkboxVisible.value = false;
  checkboxColor.value = "";
}
function dealSelectAll() {
  let t = false;
  messages.value.forEach(val => {
    if (val.display) {
      if (!checked.value.has(val.id)) {
        t = true;
        checked.value.add(val.id);
      }
    }
  });
  if (t === false) checked.value.clear();
  checkAll.value = t;
  toggleAll.value = !toggleAll.value;
}
function dealMsgCheck(id: number, state: boolean) {
  if (state) checked.value.add(id);
  else checked.value.delete(id);
}

// 测试数据
const test1 = {
  id: 2,
  display: true,
  type: 2,
  starred: true,
  unread: false,
  time: "12-10",
  content: "test",
  platform: 0,
  keywords: "中山大学 软件工程",
  title: "中山大学"
};
const test2 = {
  id: 0,
  display: true,
  type: 0,
  starred: true,
  unread: false,
  time: "12-10",
  content: "系统通知A"
};
const test3 = {
  id: 1,
  display: true,
  type: 0,
  starred: false,
  unread: true,
  time: "12-31",
  content: "系统通知B"
};
messages.value.push(...[test1, test2, test3]);
messages.value.sort(comp);
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
