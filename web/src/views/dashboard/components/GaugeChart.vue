<template>
  <div class="gaugechart-wrapper">
    <h1 class="gaugechart-title">👻热度仪表</h1>
    <div ref="gaugeChartRef" class="gauge-chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, computed, watch, defineProps } from "vue";
import { EventAnalysis } from "@/api/interface";
import { getStatistics } from "@/api/modules/event_analysis";
import * as echarts from "echarts";
import { useStore } from "vuex";

const props = defineProps({
  statistics: Object as () => EventAnalysis.ResStatistics | null
});

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const gaugeChartRef = ref(null);
const myChart = ref<echarts.ECharts | null>(null);

const calculateHotnessIndex = data => {
  const likePerPost = data.like_counts / data.posts;
  const commentPerPost = data.comment_counts / data.posts;
  const forwardPerPost = data.forward_counts / data.posts;
  return likePerPost + commentPerPost + forwardPerPost;
};

async function fetchGaugeData() {
  const date = selectedDate.value === "earlier" ? "history" : selectedDate.value;
  let stats = props.statistics;
  if (!stats) {
    try {
      stats = await getStatistics();
    } catch (error) {
      initChart(50);
      return;
    }
  }

  const lastMonthHotness = calculateHotnessIndex(stats.last_month);
  const historyHotness = calculateHotnessIndex(stats.history);
  const maxHotness = Math.max(lastMonthHotness, historyHotness);
  const hotnessIndex = date === "history" ? (historyHotness / maxHotness) * 100 : (lastMonthHotness / maxHotness) * 100;

  initChart(hotnessIndex);
}

const initChart = hotnessIndex => {
  if (gaugeChartRef.value) {
    myChart.value = echarts.init(gaugeChartRef.value);

    const option = {
      tooltip: {
        formatter: function (params) {
          return `${params.seriesName} <br/>${params.name} : ${params.value.toFixed(1)}%`;
        },
        confine: true,
        position: function (pos, params, dom, rect, size) {
          const obj = { top: pos[1] };
          obj[["left", "right"][+(pos[0] < size.viewSize[0] / 2)]] = 15;
          return obj;
        }
      },
      series: [
        {
          name: "热度指数",
          type: "gauge",
          radius: "100%",
          startAngle: 180,
          endAngle: 0,
          axisLine: {
            lineStyle: {
              width: 30,
              color: [
                [0.2, "#91c7ae"],
                [0.8, "#63869e"],
                [1, "#c23531"]
              ]
            }
          },
          pointer: {
            width: 6,
            length: "80%",
            itemStyle: {
              color: "auto"
            }
          },
          axisTick: {
            show: false
          },
          splitLine: {
            length: 15,
            lineStyle: {
              width: 2,
              color: "#fff"
            }
          },
          axisLabel: {
            distance: 25,
            fontSize: 12,
            color: "#fff"
          },
          detail: {
            formatter: "{value}%",
            fontSize: 20,
            fontWeight: "bold",
            color: "#fff"
          },
          data: [{ value: hotnessIndex, name: "热度指数" }]
        }
      ]
    };

    myChart.value.setOption(option);
    window.addEventListener("resize", () => {
      if (myChart.value) {
        myChart.value.resize();
      }
    });
  }
};

watch(
  () => [selectedDate.value, props.statistics],
  () => {
    fetchGaugeData();
  },
  { immediate: true }
);

window.addEventListener("resize", () => {
  if (myChart.value) {
    myChart.value.resize();
  }
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", () => {
    if (myChart.value) {
      myChart.value.resize();
    }
  });
  if (myChart.value) {
    myChart.value.dispose();
  }
});
</script>

<style scoped>
.gaugechart-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin-bottom: 10px;
  overflow: hidden;
  background-color: #ffffff;
}
.gaugechart-title {
  margin-bottom: 20px;
  font-size: 18px;
  color: #007bff;
  text-align: center;
}
.gauge-chart {
  width: 100%;
  max-width: 500px;
  height: 250px;
  margin: 0 auto;
}
.echarts-tooltip {
  max-width: 90%;
  padding: 10px !important;
  overflow: hidden;
  color: white !important;
  text-overflow: ellipsis;
  word-wrap: break-word;
  background-color: rgb(0 0 0 / 70%) !important;
  border-radius: 4px !important;
}
</style>
