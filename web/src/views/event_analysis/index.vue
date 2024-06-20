<template>
  <div class="card">
    <el-card>
      <el-row>
        <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
          <div class="title">事件标题</div>
          <div class="keyword">
            事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词
          </div>
          <el-divider></el-divider>
          <div class="content">
            事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述
          </div>
        </el-col>
        <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
          <el-row class="statistic_container">
            <el-statistic class="statistic_col" :value="upVoteValue" title="点赞数"></el-statistic>
            <el-statistic class="statistic_col" :value="likeValue" title="喜爱数"></el-statistic>
            <el-statistic class="statistic_col" :value="collectValue" title="收藏数"></el-statistic>
            <el-statistic class="statistic_col" :value="shareValue" title="转发数"></el-statistic>
          </el-row>
        </el-col>
      </el-row>
    </el-card>
    <el-row class="event_analysis" :gutter="20">
      <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
        <el-space fill wrap direction="vertical" :fill-ratio="100" style="width: 100%; height: 100%">
          <el-card>
            <PieChart :is-loading="loading" :data="emotionData" chart-title="情感分析" />
          </el-card>
          <el-card> <BarChart :is-loading="loading" :data="eventsData" /></el-card>
        </el-space>
      </el-col>
      <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
        <el-card>
          <el-tabs v-if="displayRightChart" class="map_container">
            <el-tab-pane label="词云图">
              <WordCloud :is-loading="loading" :data="wordFreqData" />
            </el-tab-pane>
            <el-tab-pane label="关系图">
              <!-- <EventGraph3D /> -->
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import PieChart from "./components/PieChart.vue";
import WordCloud from "./components/WordCloud.vue";
import BarChart from "./components/BarChart.vue";
// import EventGraph3D from "@/components/Event3D/EventGraph3D.vue";
import { computed, ref, watch } from "vue";
import { useTransition } from "@vueuse/core";

const loading = ref(false);

interface EventAnalysisData {
  /** 帖子标题 */
  title: string;
  /** 帖子情感分析结果 */
  emotions: any;
  /** 帖子词频分析结果 */
  wordFreq: any;
}
const datasource = ref<EventAnalysisData[]>([
  {
    title: "post1",
    emotions: { 高兴: 10, 愤怒: 20 },
    wordFreq: { VIVO: 30 }
  },
  {
    title: "post2",
    emotions: { 高兴: 1, 愤怒: 28 },
    wordFreq: { OPPO: 29 }
  },
  {
    title: "post3",
    emotions: { 高兴: 27, 愤怒: 1 },
    wordFreq: { HONOR: 28 }
  },
  {
    title: "post4",
    emotions: { 高兴: 7, 愤怒: 20 },
    wordFreq: { "iPhone 12 pro max": 27 }
  },
  {
    title: "post5",
    emotions: { 高兴: 23, 愤怒: 2 },
    wordFreq: { "HUAWEI MATE 10": 25 }
  },
  {
    title: "post6",
    emotions: { 高兴: 4, 愤怒: 20 },
    wordFreq: { ONEPLUS: 24 }
  },
  {
    title: "post7",
    emotions: { 高兴: 3, 愤怒: 20 },
    wordFreq: { "Lenova T470": 23 }
  },
  {
    title: "post8",
    emotions: { 高兴: 20, 愤怒: 2 },
    wordFreq: { "MacBook Air": 22 }
  },
  {
    title: "post9",
    emotions: { 高兴: 14, 愤怒: 6 },
    wordFreq: { "iPad mini": 20 }
  },
  {
    title: "post10",
    emotions: { 高兴: 14, 愤怒: 2 },
    wordFreq: { BLACKBERRY: 16 }
  },
  {
    title: "post11",
    emotions: { 高兴: 10, 愤怒: 3 },
    wordFreq: { SAMSUNG: 13 }
  },
  {
    title: "post12",
    emotions: { 高兴: 10, 愤怒: 2 },
    wordFreq: { "361": 12 }
  },
  {
    title: "post13",
    emotions: { 高兴: 1, 愤怒: 9 },
    wordFreq: { Lenova: 10 }
  }
]);
const processedData = ref<{
  emotionStatisics: { value: number; name: string }[];
  wordFreqStatistics: { name: string; value: number }[];
  eventsData: { name: string; [key: string]: any }[];
}>({
  emotionStatisics: [],
  wordFreqStatistics: [],
  eventsData: []
});
const emotionData = computed(() => processedData.value.emotionStatisics);
const wordFreqData = computed(() => processedData.value.wordFreqStatistics);
const eventsData = computed(() => processedData.value.eventsData);

function processData() {
  let emotions: any[] = [];
  let emotionStatisics: { value: number; name: string }[] = [];
  let wordFreq: any[] = [];
  let wordFreqStatistics: { name: string; value: number }[] = [];
  let eventsData: { name: string; [key: string]: any }[] = [];
  for (const data of datasource.value) {
    eventsData.push({ name: data.title, ...data.emotions });
    // 统计情感分析结果
    for (const entry of Object.entries(data.emotions)) {
      if (emotions[entry[0]] !== undefined) {
        emotions[entry[0]] += entry[1];
      } else {
        emotions[entry[0]] = entry[1];
      }
    }
    // 统计词频
    for (const entry of Object.entries(data.wordFreq)) {
      if (wordFreq[entry[0]] !== undefined) {
        wordFreq[entry[0]] += entry[1];
      } else {
        wordFreq[entry[0]] = entry[1];
      }
    }
  }
  // 格式转换
  for (const entry of Object.entries(emotions)) {
    emotionStatisics.push({ name: entry[0], value: entry[1] });
  }
  for (const entry of Object.entries(wordFreq)) {
    wordFreqStatistics.push({ name: entry[0], value: entry[1] });
  }
  processedData.value!.emotionStatisics = emotionStatisics;
  processedData.value!.eventsData = eventsData;
  processedData.value!.wordFreqStatistics = wordFreqStatistics;
  loading.value = false;
}
processData();
watch(datasource.value, processData);

const expand_chart = ref(10);
const expand_statistic = ref(0);
const displayRightChart = ref(true);

const upVotes = ref(0);
const likes = ref(0);
const collects = ref(0);
const shares = ref(0);
const upVoteValue = useTransition(upVotes, { duration: 1500 });
const likeValue = useTransition(likes, { duration: 1500 });
const collectValue = useTransition(collects, { duration: 1500 });
const shareValue = useTransition(shares, { duration: 1500 });

setTimeout(() => {
  loading.value = true;
  datasource.value.push({
    title: "post14",
    emotions: { 高兴: 16, 愤怒: 13 },
    wordFreq: { Redmi: 29 }
  });
}, 2000);
</script>

<style scoped lang="scss">
@import "./index.scss";
.expand_chart {
  flex-grow: v-bind("expand_chart");
}
.expand_statistic {
  flex-grow: v-bind("expand_statistic");
}
:deep(.el-tabs__content) {
  width: 100%;
}
</style>
