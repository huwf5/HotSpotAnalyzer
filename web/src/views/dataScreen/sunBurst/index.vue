<template>
  <div class="dataScreen-container">
    <div class="dataScreen-content" ref="dataScreenRef">
      <div class="dataScreen-header">
        <div class="header-lf">
          <span class="header-screening" @click="router.push(HOME_URL)">首页</span>
        </div>
        <div class="header-ct">
          <div class="header-ct-title">
            <span>热点事件概览</span>
            <div class="header-ct-warning">热点预警信息（2条）</div>
          </div>
        </div>
        <div class="header-ri">
          <span class="header-download">统计报告</span>
          <span class="header-time">当前时间：{{ time }}</span>
        </div>
      </div>
      <div class="dataScreen-main">
        <div class="dataScreen-lf">
          <div class="dataScreen-top">
            <div class="dataScreen-main-title">
              <span>热点事件统计</span>
              <img src="./images/dataScreen-title.png" alt="" />
            </div>
            <div class="dataScreen-main-chart">
              <!-- <RealTimeAccessChart /> -->
            </div>
          </div>
          <div class="dataScreen-bottom">
            <div class="dataScreen-main-title">
              <span>热点比例</span>
              <img src="./images/dataScreen-title.png" alt="" />
            </div>
            <div class="dataScreen-main-chart">
              <!-- <AgeRatioChart /> -->
            </div>
          </div>
        </div>
        <div class="dataScreen-ct">
          <div class="dataScreen-map">
            <div class="dataScreen-main-title">
              <span>旭日图</span>
              <img src="./images/dataScreen-title.png" alt="" />
            </div>
            <SunburstChart :msg="'asb'" :data="data" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="dataScreenSun">
import { HOME_URL } from "@/config";
import { useRouter } from "vue-router";
import { ref, onMounted, onBeforeUnmount } from "vue";
import dayjs from "dayjs";
import SunburstChart from "./components/SunburstChart.vue";

const router = useRouter();
const dataScreenRef = ref<HTMLElement | null>(null);
// 数据接口 ChartProp
interface ChartProp {
  value: number;
  name: string;
  percentage: string;
  pos_value: number;
  neu_value: number;
  neg_value: number;
}
// 数据数组 data（模拟传给子组件PieChart.vue的数据）
let data: ChartProp[] = [
  { value: 200, name: "校园外卖", percentage: "16%", pos_value: 80, neu_value: 30, neg_value: 90 },
  { value: 110, name: "草坪修缮", percentage: "8%", pos_value: 40, neu_value: 30, neg_value: 40 },
  { value: 150, name: "共享单车", percentage: "12%", pos_value: 30, neu_value: 30, neg_value: 90 },
  { value: 310, name: "课程安排", percentage: "24%", pos_value: 100, neu_value: 50, neg_value: 160 },
  { value: 250, name: "实验求助", percentage: "20%", pos_value: 180, neu_value: 40, neg_value: 30 },
  { value: 260, name: "勤工俭学", percentage: "20%", pos_value: 200, neu_value: 40, neg_value: 20 }
];

onMounted(() => {
  if (dataScreenRef.value) {
    dataScreenRef.value.style.transform = `scale(${getScale()}) translate(-50%, -50%)`;
    dataScreenRef.value.style.width = `1920px`;
    dataScreenRef.value.style.height = `1080px`;
  }
  window.addEventListener("resize", resize);
});

// 设置响应式
const resize = () => {
  if (dataScreenRef.value) {
    dataScreenRef.value.style.transform = `scale(${getScale()}) translate(-50%, -50%)`;
  }
};

// 根据浏览器大小推断缩放比例
const getScale = (width = 1920, height = 1080) => {
  let ww = window.innerWidth / width;
  let wh = window.innerHeight / height;
  return ww < wh ? ww : wh;
};

// 获取当前时间
let timer: NodeJS.Timer | null = null;
let time = ref<string>(dayjs().format("YYYY年MM月DD HH:mm:ss"));
timer = setInterval(() => {
  time.value = dayjs().format("YYYY年MM月DD HH:mm:ss");
}, 1000);

onBeforeUnmount(() => {
  window.removeEventListener("resize", resize);
  clearInterval(timer as unknown as number);
});
</script>

<style lang="scss" scoped>
@import "./index.scss";
</style>
