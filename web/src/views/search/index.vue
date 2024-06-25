<template>
  <div class="card search_page_container">
    <div ref="affix_ref" class="affix-container">
      <el-row class="search_component" :gutter="20">
        <el-col :span="12" :offset="6">
          <el-input id="search_input" @keyup.enter="fetchData" size="large" prefix-icon="Search" v-model="searchKeyWord">
            <template #suffix>
              <el-button type="primary" @click="fetchData">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col class="date_selector" :span="3">
          <el-select v-model="search_date">
            <el-option v-for="date in valid_dates" :key="date" :value="date"></el-option>
          </el-select>
        </el-col>
      </el-row>
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
import { computed, nextTick, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";

interface EventData {
  title: string;
  desc: string;
}

const router = useRouter();
const searchKeyWord = ref(router.currentRoute.value.query ? router.currentRoute.value.query.keyword : "");

const affix_ref = ref<HTMLElement>();
const affix_width = ref(0);
const valid_dates = ref(["history"]);
const search_date = ref("history");
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
const timerId = ref<NodeJS.Timeout>();

const input_height = ref(0);
onMounted(async () => {
  await nextTick();
  input_height.value = document.getElementById("search_input")!.getBoundingClientRect().height;
  affix_width.value = affix_ref.value!.getBoundingClientRect().width;
  window.addEventListener("resize", adjustWidth);
});
onUnmounted(() => {
  window.removeEventListener("resize", adjustWidth);
});
function adjustWidth() {
  if (timerId.value) {
    clearTimeout(timerId.value);
    timerId.value = undefined;
  }
  timerId.value = setTimeout(() => {
    affix_width.value = affix_ref.value!.getBoundingClientRect().width;
    timerId.value = undefined;
  }, 250);
}
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
</script>

<style scoped lang="scss">
@import "./index.scss";
.search_component {
  position: fixed;
  display: flex;
  flex: none;
  width: v-bind("affix_width + 'px'");
  transition: all 0.1s linear;
}
.affix-container {
  position: relative;
  display: flex;
  flex: none;
  justify-content: center;
  height: v-bind("input_height + 'px'");
}
</style>
