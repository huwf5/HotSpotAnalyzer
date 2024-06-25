<template>
  <div class="card">
    <el-card>
      <el-row>
        <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
          <div class="title"></div>
          <div class="content"></div>
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
import { useRouter } from "vue-router";
import { getDetail } from "@/api/modules/event_analysis";
import { EventAnalysis } from "@/api/interface";

const router = useRouter();
const event_title = ref(router.currentRoute.value.query.title ? (router.currentRoute.value.query.title as string) : "");
const loading = ref(false);

interface EventAnalysisData {
  /** 帖子标题 */
  title: string;
  /** 帖子情感分析结果 */
  emotions: any;
  /** 帖子词频分析结果 */
  wordFreq: {
    name: string;
    value: number;
  }[];
}
const dataSource = ref<{
  emotionStatisics: { value: number; name: string }[];
  wordFreqStatistics: { name: string; value: number }[];
  eventsData: { name: string; [key: string]: any }[];
}>({
  emotionStatisics: [],
  wordFreqStatistics: [],
  eventsData: []
});
const emotionData = computed(() => dataSource.value.emotionStatisics);
const wordFreqData = computed(() => dataSource.value.wordFreqStatistics);
const eventsData = computed(() => dataSource.value.eventsData);

function processEmotionData(origin_data: (EventAnalysis.ResDetailedSentiment & { title: string })[]) {
  let eventsData: { name: string; [key: string]: any }[] = [];
  for (const data of origin_data) eventsData.push({ name: data.title, ...data });
  loading.value = false;
}
getDetail(event_title.value).then(response => {
  dataSource.value.emotionStatisics = response.senti_count;
  dataSource.value.wordFreqStatistics = response.word_count;
});

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
