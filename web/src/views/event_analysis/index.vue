<template>
  <div class="card">
    <el-card>
      <el-row>
        <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
          <div class="title">{{ props.title }}</div>
          <div class="content">{{ summary }}</div>
        </el-col>
        <el-col :span="12" :lg="12" :md="24" :sm="24" :xs="24">
          <el-row class="statistic_container">
            <el-statistic class="statistic_col" :value="upVoteValue" title="点赞数"></el-statistic>
            <el-statistic class="statistic_col" :value="likeValue" title="喜爱数"></el-statistic>
            <el-statistic class="statistic_col" :value="commentValue" title="评论数"></el-statistic>
          </el-row>
        </el-col>
      </el-row>
    </el-card>
    <el-row class="event_analysis" :gutter="20">
      <el-col v-if="emotionData.length > 0" :span="12" :lg="12" :md="24" :sm="24" :xs="24">
        <el-space fill wrap direction="vertical" :fill-ratio="100" style="width: 100%; height: 100%">
          <el-card>
            <PieChart :is-loading="loading" :data="emotionData" chart-title="情感分析" />
          </el-card>
          <el-card> <BarChart :is-loading="loading" :data="eventsData" /></el-card>
        </el-space>
      </el-col>
      <el-col :span="rightChartSpan" :lg="rightChartSpan" :md="24" :sm="24" :xs="24">
        <el-card>
          <el-tabs v-if="displayRightChart" class="map_container">
            <el-tab-pane label="词云图">
              <WordCloud :is-loading="loading" :data="wordFreqData" />
            </el-tab-pane>
            <el-tab-pane label="关系图">
              <Graph2D :data="graphData" />
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
import Graph2D from "./components/Graph2D.vue";
import { computed, onMounted, ref } from "vue";
import { useTransition } from "@vueuse/core";
import { useRouter } from "vue-router";
import { getDetail, getDetailedSentiment } from "@/api/modules/event_analysis";
import { useTabsStore } from "@/stores/modules/tabs";

const router = useRouter();
const props = defineProps<{
  title: string;
}>();
const summary = ref("");
const loading = ref(false);
const tabStore = useTabsStore();

const dataSource = ref<{
  emotionStatisics: { value: number; name: string }[];
  wordFreqStatistics: { name: string; value: number }[];
  eventsData: { [key: string]: number }[];
  graphData: {
    nodes: {
      id: number;
      name: string;
      attributes: {
        type: string;
        value: string;
      }[];
    }[];
    links: {
      source: number;
      target: number;
      type: string;
    }[];
  };
}>({
  emotionStatisics: [],
  wordFreqStatistics: [],
  eventsData: [],
  graphData: {
    nodes: [],
    links: []
  }
});
const rightChartSpan = computed(() => (emotionData.value.length > 0 ? 12 : 24));
const emotionData = computed(() => dataSource.value.emotionStatisics);
const wordFreqData = computed(() => dataSource.value.wordFreqStatistics);
const eventsData = computed(() => dataSource.value.eventsData);
const graphData = computed(() => dataSource.value.graphData);

onMounted(() => {
  loading.value = true;
  getDetail(props.title)
    .then(response => {
      let err = false;
      getDetailedSentiment(props.title)
        .then(emotions => {
          dataSource.value.eventsData = emotions.data;
        })
        .catch(() => {
          err = true;
        });
      if (err) return;
      let processed_sentiment_data: { value: number; name: string }[] = [];
      let sentiment_count = 0;
      for (const entry of Object.entries(response.senti_count)) {
        processed_sentiment_data.push({ name: entry[0], value: entry[1] });
        sentiment_count += entry[1];
      }
      sentiment_count == 0 && (processed_sentiment_data = []);
      response.graph &&
        (dataSource.value.graphData = {
          nodes: response.graph.events.map(item => {
            return { name: item.event, ...item };
          }),
          links: response.graph.relationships ? response.graph.relationships : []
        });
      dataSource.value.emotionStatisics = processed_sentiment_data;
      dataSource.value.wordFreqStatistics = response.word_count;
      upVotes.value = response.forward_count;
      likes.value = response.like_count;
      comments.value = response.comment_count;
      summary.value = response.summary;
    })
    .catch(() => {
      tabStore.removeTabs(router.currentRoute.value.fullPath);
      router.back();
    })
    .finally(() => {
      loading.value = false;
    });
});

const expand_chart = ref(10);
const expand_statistic = ref(0);
const displayRightChart = ref(true);

const upVotes = ref(0);
const likes = ref(0);
const comments = ref(0);
const upVoteValue = useTransition(upVotes, { duration: 1500 });
const likeValue = useTransition(likes, { duration: 1500 });
const commentValue = useTransition(comments, { duration: 1500 });
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
