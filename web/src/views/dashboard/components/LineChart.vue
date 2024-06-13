<template>
  <div class="linechart-wrapper">
    <h1 class="linechart-title">👻热度趋势</h1>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { init as initECharts, ECharts, graphic } from "echarts";
import { useStore } from "vuex";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const chartContainer = ref<HTMLDivElement | null>(null);
let myChart: ECharts | null = null;

const initChart = async selectedDateValue => {
  const date = ref("");
  if (selectedDateValue === "earlier") {
    date.value = "history";
  } else {
    date.value = selectedDateValue;
  }
  const response = await fetch(`http://127.0.0.1:8000/fetch-chartData?date=${date.value}`);
  const chartData = await response.json();
  const x_data = chartData["x"];
  const y_data = chartData["y"];

  if (chartContainer.value) {
    myChart = initECharts(chartContainer.value);
    const option: {
      yAxis: { axisLabel: { color: string }; type: string };
      xAxis: { axisLabel: { rotate: number; color: string }; data: any; type: string };
      grid: { left: string };
      series: {
        areaStyle: { color: LinearGradient };
        data: any;
        lineStyle: { shadowOffsetY: number; shadowBlur: number; width: number; shadowColor: string };
        itemStyle: { borderColor: string; color: string };
        type: string;
        smooth: boolean;
      }[];
      tooltip: { trigger: string };
    } = {
      grid: {
        left: "15%" // 增加左侧内边距
      },
      tooltip: {
        trigger: "axis"
      },
      xAxis: {
        type: "category",
        data: x_data,
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
          data: y_data,
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
  }
};
watch(
  selectedDate,
  newDate => {
    initChart(newDate);
  },
  { immediate: true }
);
onMounted(() => {
  initChart(selectedDate.value);
  window.addEventListener("resize", () => {
    myChart?.resize();
  });
});

onUnmounted(() => {
  myChart?.dispose();
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
  font-size: 18px; /* 调整字体大小为较小的尺寸 */
  color: #007bff; /* 字体颜色改为蓝色 */
}
</style>
