<template>
  <div class="card search_page_container">
    <div ref="affix_ref" class="affix-container">
      <el-row id="search_input" class="search_component" :gutter="10">
        <el-col :span="10" :offset="6">
          <el-input
            size="large"
            prefix-icon="Search"
            v-model="searchKeyWord"
            clearable
            @keyup.enter="fetchData"
            @clear="fetchData"
          >
          </el-input>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="fetchData">搜索</el-button>
        </el-col>
        <el-col v-if="date_picker" :span="3">
          <el-date-picker
            v-model="search_date"
            type="daterange"
            unlink-panels
            range-separator="至"
            :shortcuts="shortcuts"
            @change="fetchData"
          />
        </el-col>
      </el-row>
    </div>
    <ul v-infinite-scroll="loadMore" :infinite-scroll-disabled="disabled" :infinite-scroll-distance="300" style="padding: 0">
      <li class="affix-item"></li>
      <li v-for="(event, index) in display_events" :key="index" class="list-item">
        <el-card shadow="hover" @click="handleClick(event.title, event.summary)">
          <div class="event-title">{{ event.title }}</div>
          <div class="event-body">{{ event.summary }}</div>
          <div class="event-date">{{ event.date }}</div>
        </el-card>
      </li>
    </ul>
    <div v-if="noMore" class="no-more">~ 已经到底啦 ~</div>
  </div>
</template>

<script setup lang="ts">
import { getAllEvents, searchEvent } from "@/api/modules/event_analysis";
import { computed, nextTick, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";

interface EventData {
  title: string;
  summary: string;
  date: string;
}

const router = useRouter();
const searchKeyWord = ref<string>(
  router.currentRoute.value.query.keyword ? (router.currentRoute.value.query.keyword as string) : ""
);
const prev_keyword = ref("");
const search_date = ref<[Date, Date] | null>(null);
const shortcuts = [
  {
    text: "过去一周",
    value: () => {
      const end = new Date(Date.now());
      const start = new Date(Date.now());
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
      return [start, end];
    }
  },
  {
    text: "过去一月",
    value: () => {
      const end = new Date(Date.now());
      const start = new Date(Date.now());
      start.setMonth(start.getMonth() === 1 ? 12 : start.getMonth() - 1);
      return [start, end];
    }
  },
  {
    text: "过去一年",
    value: () => {
      const end = new Date(Date.now());
      const start = new Date(Date.now());
      start.setFullYear(start.getFullYear() - 1);
      return [start, end];
    }
  }
];

const affix_ref = ref<HTMLElement>();
const date_picker = ref(true);
const events_buffer = ref<EventData[]>([]);

// 缓存全部事件结果，有效时长为10分钟
const buffer_lifetime = 10 * 60 * 1000;
const buffer_timer = ref<NodeJS.Timeout>();

const all_events = ref<EventData[]>([]);
const display_count = ref(10);
const display_events = computed(() => all_events.value.slice(0, display_count.value));
const loading = ref(false);
const noMore = computed(() => display_events.value.length == all_events.value.length);
const disabled = computed(() => loading.value || noMore.value);

const input_height = ref(0);
onMounted(async () => {
  await nextTick();
  input_height.value = document.getElementById("search_input")!.getBoundingClientRect().height;
  fetchData();
  adjustWidth();
  window.addEventListener("resize", adjustWidth);
});
onUnmounted(() => {
  window.removeEventListener("resize", adjustWidth);
  if (buffer_timer.value) clearTimeout(buffer_timer.value);
});
function adjustWidth() {
  date_picker.value = affix_ref.value!.getBoundingClientRect().width > 850;
}
async function fetchData() {
  searchKeyWord.value = searchKeyWord.value.trim();
  if (searchKeyWord.value.length === 0) {
    if (buffer_timer.value === undefined) {
      await getAllEvents().then(response => {
        events_buffer.value = response.data;
      });
      buffer_timer.value = setTimeout(() => {
        clearTimeout(buffer_timer.value);
        buffer_timer.value = undefined;
      }, buffer_lifetime);
    }
    all_events.value = events_buffer.value;
  } else if (prev_keyword.value !== searchKeyWord.value) {
    all_events.value = [];
    await searchEvent(searchKeyWord.value).then(response => {
      all_events.value = response.data;
    });
  }
  display_count.value = 10;
  if (search_date.value !== null)
    all_events.value = all_events.value.filter(event => {
      let event_date = new Date(event.date);
      return event_date.getTime() >= search_date.value![0].getTime() && event_date.getTime() <= search_date.value![1].getTime();
    });
}
function loadMore() {
  loading.value = true;
  display_count.value = Math.min(display_count.value + 10, all_events.value.length);
  loading.value = false;
}
function handleClick(title: string, summary: string) {
  router.push({ path: `/event/analysis/${title}/${summary}` });
}
</script>

<style scoped lang="scss">
@import "./index.scss";
.affix-item {
  position: relative;
  display: flex;
  flex: none;
  justify-content: center;
  height: v-bind("input_height + 'px'");
}
</style>
