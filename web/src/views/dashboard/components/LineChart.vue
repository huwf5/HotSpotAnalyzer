<template>
  <div class="linechart-wrapper">
    <h1 class="linechart-title">👻热度趋势</h1>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, onUnmounted, ref, computed, watch } from "vue";
import { init as initECharts, ECharts, EChartsOption, graphic } from "echarts";
import { useStore } from "vuex";
import { getLineChart } from "@/api/modules/event_analysis";
// import axios from "axios";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const chartContainer = ref<HTMLDivElement | null>(null);
let myChart: ECharts | null = null;

// default data
const defaultLineChartData = {
  dates: ["2021-09-01", "2021-09-06", "2021-09-11", "2021-09-16", "2021-09-21", "2021-09-26"],
  values: [120, 200, 150, 80, 180, 230]
};
const lineChartData = ref<{ dates: string[]; values: number[] }>(defaultLineChartData);

async function fetchLineChartData(selectedDateValue) {
  const date = selectedDateValue === "earlier" ? "history" : selectedDateValue;
  try {
    const response = await getLineChart(date);
    const entries = Object.entries(response).sort((a, b) => new Date(a[0]).getTime() - new Date(b[0]).getTime());
    const dates = entries.map(entry => entry[0]);
    const values = entries.map(entry => entry[1]);
    lineChartData.value = { dates, values };
  } catch (error) {
    lineChartData.value = defaultLineChartData;
  }
  initChart(); // 初始化或更新图表
}

const initChart = () => {
  if (chartContainer.value) {
    myChart = initECharts(chartContainer.value);
    const option: EChartsOption = {
      tooltip: {
        trigger: "axis"
      },
      xAxis: {
        type: "category",
        data: lineChartData.value.dates,
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
      grid: {
        left: "3%",
        right: "3%",
        bottom: "3%",
        containLabel: true
      },
      series: [
        {
          data: lineChartData.value.values,
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
    };

    myChart.setOption(option);
    window.addEventListener("resize", () => {
      if (myChart) {
        myChart.resize();
      }
    });
  }
};

onMounted(() => {
  fetchLineChartData(selectedDate.value);
  window.addEventListener("resize", () => {
    myChart?.resize();
  });
});

watch(selectedDate, newDate => {
  fetchLineChartData(newDate);
});

onUnmounted(() => {
  myChart?.dispose();
});
</script>

<style scoped>
.chart-container {
  display: flex;
  justify-content: center;
  width: 100%; /* 使用100%宽度以适应父容器 */
  height: 375px; /* 保持图表为方形，可以调整为100%或固定尺寸 */
  margin: auto;
}
.linechart-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  overflow: hidden;
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
