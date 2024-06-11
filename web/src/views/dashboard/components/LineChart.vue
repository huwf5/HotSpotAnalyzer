<template>
  <div class="linechart-wrapper">
    <h1 class="linechart-title">👻热度趋势</h1>
    <v-chart ref="chartContainer" class="chart-container" :option="option" autoresize />
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { use } from "echarts/core";
import { ECharts, graphic } from "echarts";
import VChart from "vue-echarts";
import { LineChart } from "echarts/charts";

use([LineChart]);

const chartContainer = ref<ECharts>();
const option = ref({
  tooltip: {
    trigger: "axis"
  },
  xAxis: {
    type: "category",
    data: ["2021-09-01", "2021-09-06", "2021-09-11", "2021-09-16", "2021-09-21", "2021-09-26"],
    axisLabel: {
      rotate: 45, // 旋转标签以更好地适应
      color: "#6c757d" // 更改文字颜色
    }
  },
  yAxis: {
    type: "value",
    axisLabel: {
      color: "#6c757d"
    }
  },
  series: [
    {
      data: [120, 200, 150, 80, 180, 230],
      type: "line",
      smooth: true,
      lineStyle: {
        width: 3,
        shadowColor: "rgba(0,0,0,0.3)",
        shadowBlur: 10,
        shadowOffsetY: 8
      },
      itemStyle: {
        color: "#007bff", // 主颜色
        borderColor: "#007bff"
      },
      areaStyle: {
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: "#007bff" // 渐变色起始颜色
          },
          {
            offset: 1,
            color: "#fff" // 渐变色结束颜色
          }
        ])
      }
    }
  ]
});
</script>

<style scoped>
.chart-container {
  width: 100%; /* 使用100%宽度以适应父容器 */
  height: 375px; /* 保持图表为方形，可以调整为100%或固定尺寸 */
}
.linechart-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff; /* 背景颜色调整为白色 */
}
.linechart-title {
  margin: 0;

  /* position: absolute;
  top: 0;
  left: 10px; */
  font-size: 18px; /* 调整字体大小为较小的尺寸 */
  color: #007bff; /* 字体颜色改为蓝色 */
}
</style>
