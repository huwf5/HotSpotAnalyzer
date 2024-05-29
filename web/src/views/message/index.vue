<template>
  <div class="message card">
    <div class="headline">
      <label class="message_title">通知列表</label>
      <div class="operations">
        <Filter class="operation_icon" @system-message-display="displaySystemMsg" @read-message-display="displayReadMsg" />
        <icon class="operation_icon" :color="checkboxColor" @click="checkboxVisibilityVaryfied">
          <Finished />
        </icon>
        <icon class="operation_icon" :class="{ reload: loading }" @click="fetch">
          <Refresh />
        </icon>
        <icon class="operation_icon" @click="message_settings">
          <Setting />
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
import { useUserStore } from "@/stores/modules/user";
import { batchDeleteMsgApi, batchUpdateMsgApi, fetchMessagesApi } from "@/api/modules/messages";
import router from "@/routers";
import { ElNotification } from "element-plus";
import { getTimeState } from "@/utils";

const store = useUserStore();

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
function fetch() {
  loading.value = true;
  setTimeout(() => (loading.value = false), 2000);
  checked.value.clear();
  checkboxVisible.value = false;
  checkboxColor.value = "";
  fetchMessagesApi()
    .then(response => {
      store.setUserMsg(response.data);
      messages.value = store.userInfo.messages;
      ElNotification({
        title: getTimeState(),
        message: "消息同步成功",
        type: "info",
        duration: 1000
      });
    })
    .catch(() => {
      ElNotification({
        title: "错误",
        message: "无法获取消息，请重试",
        type: "error",
        duration: 3000
      });
    });
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
  let update_list: Messages.ReqMessages[] = [];
  checked.value.forEach(val => {
    update_list.push({
      id: val,
      starred: starAll
    });
  });
  batchUpdateMsgApi(update_list).then(() => {
    fetch();
    ElNotification({
      title: "错误",
      message: "消息更新失败，正在尝试同步数据",
      type: "warning",
      duration: 1000
    });
  });
  // 不等待服务器回复就直接更新，避免频繁出现加载页面
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
  let update_list: Messages.ReqMessages[] = [];
  checked.value.forEach(val => {
    update_list.push({
      id: val,
      unread: false
    });
  });
  batchUpdateMsgApi(update_list).then(() => {
    fetch();
    ElNotification({
      title: "错误",
      message: "消息更新失败，正在尝试同步数据",
      type: "warning",
      duration: 1000
    });
  });
  // 不等待服务器回复就直接更新，避免频繁出现加载页面
  messages.value.forEach(msg => {
    if (checked.value.has(msg.id)) {
      msg.unread = false;
    }
  });
  messages.value.sort(comp);
  store.userInfo.messages = messages.value;
}
function dealDeleteAll() {
  if (checked.value.size === 0) return;
  let delete_list: Messages.ReqMessages[] = [];
  checked.value.forEach(val => {
    delete_list.push({ id: val });
  });
  batchDeleteMsgApi(delete_list).then(() => {
    fetch();
    ElNotification({
      title: "错误",
      message: "消息更新失败，正在尝试同步数据",
      type: "warning",
      duration: 1000
    });
  });
  // 不等待服务器回复就直接更新，避免频繁出现加载页面
  for (let index = messages.value.length - 1; index >= 0; index--) {
    if (checked.value.has(messages.value[index].id)) messages.value.splice(index, 1);
  }
  checked.value.clear();
  checkboxVisible.value = false;
  checkboxColor.value = "";
  store.userInfo.messages = messages.value;
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
function message_settings() {
  router.push("/settings/message");
}
fetch();
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
