<template>
  <div class="gaugechart-wrapper">
    <h1 class="gaugechart-title">👻热度仪表</h1>
    <div ref="gaugeChartRef" class="gauge-chart"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onBeforeUnmount, computed, watch } from "vue";
import { getStatistics } from "@/api/modules/event_analysis";
import { EventAnalysis } from "@/api/interface";
import * as echarts from "echarts";
import { useStore } from "vuex";
// import axios from "axios";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const gaugeChartRef = ref(null);
const myChart = ref<echarts.ECharts | null>(null);

async function fetchGaugeData(selectedDateValue) {
  const date = selectedDateValue === "earlier" ? "history" : selectedDateValue;
  try {
    const response: EventAnalysis.ResStatistics = await getStatistics();
    // const response = await axios.get(`http://127.0.0.1:8000/api/cardlist/fetch_card_list/`, {
    //   headers: {
    //     Authorization:
    //       "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NTk3MjE1LCJpYXQiOjE3MTk1NzU2MTUsImp0aSI6ImQ0NTZkMjI5OTIxMzRlOWJiMDAzYmU2NThlMGFlYjBmIiwidXNlcl9lbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.x5kyqhscJ-nOrUi9pf-H4G5EogifkB_ftUvsq2-sIUc", // 替换为你的JWT令牌
    //     accept: "application/json"
    //   }
    // });
    // 计算热度指数
    const lastMonth = response.last_month;
    const history = response.history;

    const calculateHotnessIndex = data => {
      const likePerPost = data.like_counts / data.posts;
      const commentPerPost = data.comment_counts / data.posts;
      const forwardPerPost = data.forward_counts / data.posts;
      const rawIndex = likePerPost + commentPerPost + forwardPerPost;
      return rawIndex;
    };

    const lastMonthHotness = calculateHotnessIndex(lastMonth);
    const historyHotness = calculateHotnessIndex(history);

    // 标准化热度指数
    const maxHotness = Math.max(lastMonthHotness, historyHotness);
    const lastMonthHotnessNormalized = (lastMonthHotness / maxHotness) * 100;
    const historyHotnessNormalized = (historyHotness / maxHotness) * 100;

    // 选择合适的热度指数
    const hotnessIndex = date === "history" ? historyHotnessNormalized : lastMonthHotnessNormalized;
    // 初始化或更新图表
    initChart(hotnessIndex);
  } catch (error) {
    console.error("Failed to fetch gauge data from server, using default data", error);
    initChart(50);
  }
}

const initChart = hotnessIndex => {
  if (gaugeChartRef.value) {
    myChart.value = echarts.init(gaugeChartRef.value);

    const option = {
      tooltip: {
        formatter: function (params) {
          return `${params.seriesName} <br/>${params.name} : ${params.value.toFixed(3)}%`;
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

onMounted(() => {
  fetchGaugeData(selectedDate.value);
});

watch(selectedDate, newDate => {
  fetchGaugeData(newDate);
});

onBeforeUnmount(() => {
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
  padding: 10px !important;
  color: white !important;
  background-color: rgb(0 0 0 / 70%) !important;
  border-radius: 4px !important;
}
</style>
