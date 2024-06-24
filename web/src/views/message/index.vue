<template>
  <div class="message card">
    <div class="headline">
      <label class="message_title">消息列表</label>
      <div class="operations">
        <Filter
          class="operation_icon"
          @info-msg-display="visualize(Messages.MessageType.INFO, state, $event, predicate)"
          @warn-msg-display="visualize(Messages.MessageType.WARN, state, $event, predicate)"
          @read-msg-display="visualize('read', state, $event, predicate)"
        />
        <el-icon class="operation_icon" :color="checkboxColor" @click="checkboxVisibilityVaryfied">
          <Finished />
        </el-icon>
        <el-icon class="operation_icon" :class="{ reload: loading }" @click="fetch">
          <Refresh />
        </el-icon>
        <el-icon class="operation_icon" @click="message_settings">
          <Setting />
        </el-icon>
      </div>
    </div>
    <div class="message_list">
      <MessageList
        v-model="messages"
        :checkbox-visible="checkboxVisible"
        @item-checked="dealMsgCheck"
        @item-starred="dealMsgStarred"
      />
    </div>
    <div class="bottom-wrapper">
      <div class="bottom" :style="{ translate: checkboxVisible ? '0 -100%' : '0' }">
        <div class="select_all">
          <el-button v-if="!checkAll" type="primary" plain icon="Plus" @click="dealSelectAll">全选</el-button>
          <el-button v-else type="primary" plain icon="Check" @click="dealSelectAll">全选</el-button>
        </div>
        <div>
          <el-button type="warning" :disabled="!checkboxVisible" plain circle icon="Star" @click="dealStarAll"></el-button>
          <el-button type="success" :disabled="!checkboxVisible" plain icon="Check" @click="dealReadAll">标记已读</el-button>
          <el-button type="danger" :disabled="!checkboxVisible" plain icon="Delete" @click="dealDeleteAll">删除消息</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="message">
import Filter from "./components/Filter.vue";
import MessageList from "./components/MessageList.vue";
import { onMounted, ref } from "vue";
import { Messages } from "@/api/interface";
import { comp } from "./util";
import { useUserStore } from "@/stores/modules/user";
import { batchDeleteMsgApi, batchUpdateMsgApi, fetchMessagesApi } from "@/api/modules/messages";
import { ElNotification } from "element-plus";
import { useRouter } from "vue-router";

const store = useUserStore();
const router = useRouter();
const checkboxVisible = ref(false);
const checkboxColor = ref("");
const messages = ref<(Messages.ResMessage & { display: boolean; selected: boolean })[]>([]);
const checked = ref<Map<number, Messages.ResMessage>>(new Map());
const checkAll = ref(false);
const loading = ref(false);

const state = ref({
  info: true,
  warn: true,
  read: true
});

function predicate(msg: Messages.ResMessage) {
  if (msg.is_read && !state.value.read) return false;
  else return state.value[msg.type];
}

function visualize<T extends { [key in Messages.MessageType]: boolean }>(
  type: string,
  stateStore: T,
  visible: boolean,
  predicator: (msg: Messages.ResMessage) => boolean
) {
  stateStore[type] = visible;
  if (visible) {
    messages.value.forEach(msg => {
      if (predicator(msg)) {
        msg.display = true;
        if (checkAll.value) {
          msg.selected = true;
          checked.value.set(msg.id, msg);
        }
      }
    });
  } else {
    messages.value.forEach(msg => {
      if (!predicator(msg)) {
        msg.display = false;
        msg.selected = false;
        checked.value.delete(msg.id);
      }
    });
  }
}

function checkboxVisibilityVaryfied() {
  checkboxVisible.value = !checkboxVisible.value;
  checkboxColor.value = checkboxVisible.value ? "#3AACFF" : "";
  if (!checkboxVisible.value) {
    messages.value.forEach(val => {
      val.selected = false;
    });
    checked.value.clear();
  }
  checkAll.value = false;
}

function fetch() {
  loading.value = true;
  checked.value.clear();
  checkboxVisible.value = false;
  checkboxColor.value = "";
  fetchMessagesApi()
    .then(response => {
      store.setUserMsg(response.data);
      messages.value = store.userInfo.messages.map(msg => {
        return { ...msg, display: true, selected: false };
      });
      messages.value.sort(comp);
    })
    .catch(() => {
      ElNotification({
        title: "错误",
        message: "无法获取消息，请重试",
        type: "error",
        duration: 3000
      });
    })
    .finally(() => {
      setTimeout(() => {
        loading.value = false;
      }, 2000);
    });
  return;
}
function dealStarAll() {
  if (checked.value.size === 0) return;
  let starAll = false;
  messages.value.forEach(msg => {
    if (checked.value.has(msg.id)) starAll = starAll || !msg.is_starred;
  });
  let update_list: Messages.ReqMessages[] = [];
  checked.value.forEach(val => {
    update_list.push({
      id: val.id,
      is_starred: starAll,
      is_read: val.is_read
    });
  });
  batchUpdateMsgApi(update_list);
  // 不等待服务器回复就直接更新，避免加载页面
  messages.value.forEach(msg => {
    if (checked.value.has(msg.id)) msg.is_starred = starAll;
  });
  messages.value.sort(comp);
}
function dealReadAll() {
  if (checked.value.size === 0) return;
  let update_list: Messages.ReqMessages[] = [];
  checked.value.forEach(val => {
    update_list.push({
      id: val.id,
      is_read: true,
      is_starred: val.is_starred
    });
  });
  batchUpdateMsgApi(update_list);
  // 不等待服务器回复就直接更新，避免加载页面
  messages.value.forEach(msg => {
    if (checked.value.has(msg.id)) msg.is_read = true;
  });
  messages.value.sort(comp);
  store.userInfo.messages = messages.value;
}
function dealDeleteAll() {
  if (checked.value.size === 0) return;
  let delete_list: number[] = [];
  checked.value.forEach(val => {
    delete_list.push(val.id);
  });
  batchDeleteMsgApi(delete_list);
  // 不等待服务器回复就直接更新，避免加载页面
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
    if (val.display) t = t || !val.selected;
  });
  messages.value.forEach(val => {
    if (val.display) {
      val.selected = t;
      t && checked.value.set(val.id, val);
    }
  });
  if (t === false) checked.value.clear();
  checkAll.value = t;
}
function dealMsgCheck(msg: Messages.ResMessage) {
  if (checked.value.has(msg.id)) checked.value.delete(msg.id);
  else checked.value.set(msg.id, msg);
  checkAll.value = checked.value.size === messages.value.length;
}
function dealMsgStarred(msg: Messages.ResMessage) {
  batchUpdateMsgApi([
    {
      id: msg.id,
      is_starred: msg.is_starred,
      is_read: msg.is_read
    }
  ]);
}
function message_settings() {
  router.push("/settings/message");
}
onMounted(fetch);
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
