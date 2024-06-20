<template>
  <div class="message">
    <el-popover placement="bottom" :width="310" trigger="hover" @show="fetch_count">
      <template #reference>
        <el-badge :hidden="unreads === 0" :value="unreads" class="item">
          <i :class="'iconfont icon-xiaoxi'" class="toolBar-icon" @click="MsgIconClicked"></i>
        </el-badge>
      </template>
      <div v-if="unreads > 0" class="message-list">
        <div v-for="(messaage, index) in messages" :key="index">
          <div v-if="messaage.unread" class="message-item">
            <img src="@/assets/images/msg01.png" alt="" class="message-icon" />
            <div class="message-content">
              <span class="message-title">{{ messaage.content }}</span>
              <span class="message-date">{{ messaage.time }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="message-list">
        <div class="message-item" style="justify-content: center">
          <el-icon size="20">
            <MagicStick />
          </el-icon>
          <span>没有未读消息了喔~</span>
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { fetchMessagesApi } from "@/api/modules/messages";
import { useUserStore } from "@/stores/modules/user";
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

const unreads = ref(0);
const router = useRouter();
const store = useUserStore();

const messages = ref(store.userInfo.messages);

function fetch_count() {
  fetchMessagesApi().then(response => {
    store.setUserMsg(response.data);
    count_unread();
  });
}
function count_unread() {
  messages.value = store.userInfo.messages;
  let cnt = 0;
  messages.value.forEach(val => {
    if (val.unread) cnt += 1;
  });
  unreads.value = cnt;
}
function MsgIconClicked() {
  router.push("/messages/index");
}
watch(store.userInfo, count_unread);
onMounted(fetch_count);
</script>

<style scoped lang="scss">
.message-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 260px;
  line-height: 45px;
}
.message-list {
  display: flex;
  flex-direction: column;
  .message-item {
    display: flex;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid var(--el-border-color-light);
    &:last-child {
      border: none;
    }
    .message-icon {
      width: 40px;
      height: 40px;
      margin: 0 20px 0 5px;
    }
    .message-content {
      display: flex;
      flex-direction: column;
      .message-title {
        margin-bottom: 5px;
      }
      .message-date {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
  }
}
</style>
