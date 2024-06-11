<template>
  <div class="card search_page_container">
    <div class="affix-container">
      <el-input
        id="search_input"
        class="search_component"
        @keyup.enter="fetchData"
        size="large"
        prefix-icon="Search"
        v-model="searchKeyWord"
      >
        <template #suffix>
          <el-button type="primary" @click="fetchData">搜索</el-button>
        </template>
      </el-input>
    </div>
    <ul v-infinite-scroll="loadMore" :infinite-scroll-disabled="disabled" style="padding: 0">
      <li v-for="(event, index) in display_events" :key="index" class="list-item">
        <el-card shadow="hover">
          <div class="event-title">{{ event.title }}</div>
          <div class="event-body">{{ event.desc }}</div>
        </el-card>
      </li>
    </ul>
    <div v-if="noMore" class="no-more">~ 已经到底啦 ~</div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

interface EventData {
  title: string;
  desc: string;
}

const router = useRouter();
const searchKeyWord = ref(router.currentRoute.value.query ? router.currentRoute.value.query.keyword : "");

const all_events = ref<EventData[]>([
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  },
  {
    title: "#事件标题",
    desc: "事件描述"
  }
]);
const display_count = ref(10);
const display_events = computed(() => all_events.value.slice(0, display_count.value));
const loading = ref(false);
const noMore = computed(() => display_events.value.length == all_events.value.length);
const disabled = computed(() => loading.value || noMore.value);

const input_height = ref(0);
onMounted(async () => {
  await nextTick();
  input_height.value = document.getElementById("search_input")!.getBoundingClientRect().height;
});
function fetchData() {
  return;
}
function loadMore() {
  loading.value = true;
  setTimeout(() => {
    display_count.value = Math.min(display_count.value + 10, all_events.value.length);
    loading.value = false;
  }, 1000);
}

// onMounted(() => {
//   // 监听 enter 事件（调用登录）
//   document.onkeydown = (e: KeyboardEvent) => {
//     if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
//     }
//   };
// });
</script>

<style scoped lang="scss">
@import "./index.scss";
.affix-container {
  display: flex;
  flex: none;
  justify-content: center;
  height: v-bind("input_height + 'px'");
}
</style>
