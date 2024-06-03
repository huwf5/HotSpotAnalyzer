<template>
  <div class="card event_analysis">
    <div class="abstract_container">
      <div class="title_container">
        <div class="title_text_container">
          <div class="title">事件标题</div>
          <div class="keyword">
            事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词事件关键词
          </div>
          <el-divider></el-divider>
          <div class="content">
            事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述事件描述
          </div>
        </div>
        <div v-if="displayStatistic" class="statistic_container">
          <el-statistic class="statistic_col light_border_right" :value="upVoteValue" title="点赞数"></el-statistic>
          <el-statistic class="statistic_col light_border_right" :value="likeValue" title="喜爱数"></el-statistic>
          <el-statistic class="statistic_col light_border_right" :value="collectValue" title="收藏数"></el-statistic>
          <el-statistic class="statistic_col" :value="shareValue" title="转发数"></el-statistic>
        </div>
      </div>
      <div class="abstract_charts_container">
        <div class="left_chart_container">
          <PieChart :display-mode="pieChartMode ? 1 : 0" :is-loading="loading" :data="piedata" />
        </div>
        <div class="left_chart_container"><BarChart :is-loading="loading" :data="datasource" /></div>
      </div>
    </div>
    <div class="map_outer_container expend" @transitionend="transitionFinished">
      <div class="collapse_button_container" @click="toggle_right_panel" @transitionend.stop>
        <el-icon class="collapse_button">
          <ArrowRight />
        </el-icon>
      </div>
      <div class="tab_outer_layout">
        <el-tabs v-if="displayRightChart" class="map_container">
          <el-tab-pane class="tab_container" label="词云图">
            <WordCloud :reload="displayWordCloud" :is-loading="loading" :data="datasource" />
          </el-tab-pane>
          <el-tab-pane class="tab_container" label="关系图"></el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import PieChart from "./components/PieChart.vue";
import WordCloud from "./components/WordCloud.vue";
import BarChart from "./components/BarChart.vue";
import { nextTick, ref } from "vue";
import { useToggle, useTransition } from "@vueuse/core";

const loading = ref(true);

const datasource = ref([
  { value: 30, name: "VIVO", happy: 10, anger: 20 },
  { value: 29, name: "OPPO", happy: 1, anger: 28 },
  { value: 28, name: "HONOR", happy: 27, anger: 1 },
  { value: 27, name: "iPhone 12 pro max", happy: 7, anger: 20 },
  { value: 25, name: "HUAWEI MATE 10", happy: 23, anger: 2 },
  { value: 24, name: "ONEPLUS", happy: 4, anger: 20 },
  { value: 23, name: "Lenova T470", happy: 3, anger: 20 },
  { value: 22, name: "MacBook Air ", happy: 20, anger: 2 },
  { value: 20, name: "iPad mini", happy: 14, anger: 6 },
  { value: 16, name: "BLACKBERRY", happy: 14, anger: 2 },
  { value: 13, name: "SAMSUNG", happy: 10, anger: 3 },
  { value: 12, name: "361", happy: 10, anger: 2 },
  { value: 10, name: "Lenova", happy: 1, anger: 9 }
]);
const piedata = ref([
  { value: 1048, name: "Search Engine" },
  { value: 735, name: "Direct" },
  { value: 580, name: "Email" },
  { value: 484, name: "Union Ads" },
  { value: 300, name: "Video Ads" }
]);
const rotation = ref(0);
const expansion = ref(10);
const pageMode = ref(0);
const transitionToLeft = ref(true);
const displayRightChart = ref(true);
const displayStatistic = ref(false);
const [displayWordCloud, reloadWordCloud] = useToggle();
const [pieChartMode, togglePieChartMode] = useToggle(true);

const upVotes = ref(0);
const likes = ref(0);
const collects = ref(0);
const shares = ref(0);
const upVoteValue = useTransition(upVotes, { duration: 1500 });
const likeValue = useTransition(likes, { duration: 1500 });
const collectValue = useTransition(collects, { duration: 1500 });
const shareValue = useTransition(shares, { duration: 1500 });

function toggle_right_panel() {
  rotation.value = 0.5 - rotation.value;
  expansion.value = 10 - expansion.value;
  transitionToLeft.value = !(pageMode.value === 0);
  if (pageMode.value === 0) {
    pageMode.value = 1 - pageMode.value;
    togglePieChartMode();
    displayRightChart.value = false;
  } else {
    displayStatistic.value = false;
  }
}
function transitionFinished() {
  if (transitionToLeft.value) {
    transitionToLeft.value = false;
    pageMode.value = 0;
    displayRightChart.value = true;
    nextTick(() => {
      reloadWordCloud();
      togglePieChartMode();
    });
  } else if (pageMode.value === 1) {
    displayStatistic.value = true;

    // 测试数据
    upVotes.value = 100;
    likes.value = 150;
    collects.value = 10;
    shares.value = 23;
  }
}
setTimeout(() => {
  datasource.value.push({ value: 29, name: "Redmi", happy: 16, anger: 13 });
  setTimeout(() => {
    loading.value = false;
  }, 200);
}, 2000);
</script>

<style scoped lang="scss">
@import "./index.scss";
.expend {
  flex-grow: v-bind("expansion");
}
.collapse_button {
  transition: all 0.5s ease-in-out;
  transform: v-bind('"rotate(" + rotation + "turn)"');
}
::v-deep .el-tabs__content {
  display: flex;
  flex: none;
  flex-direction: column;
  flex-grow: 1;
  align-self: stretch;
}
</style>
