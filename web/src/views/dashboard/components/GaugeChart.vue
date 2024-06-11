<template>
  <div class="gaugechart-wrapper">
    <h1 class="gaugechart-title">👻热度仪表</h1>
    <div id="gauge-chart"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from "vue";
import * as echarts from "echarts";

const myChart = ref<echarts.ECharts | null>(null);

const resizeChart = () => {
  if (myChart.value) {
    myChart.value.resize();
  }
};

onMounted(() => {
  const chartDom = document.getElementById("gauge-chart");
  if (chartDom) {
    myChart.value = echarts.init(chartDom);

    const option = {
      tooltip: {
        formatter: "{a} <br/>{b} : {c}%"
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
          data: [{ value: 50, name: "热度指数" }]
        }
      ]
    };

    myChart.value.setOption(option);
    window.addEventListener("resize", resizeChart);
  }
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeChart);
  if (myChart.value) {
    myChart.value.dispose();
  }
});
</script>

<style scoped>
.gaugechart-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* Center the content vertically */
  background-color: #fff;
  padding: 0;
  position: relative;
  margin-bottom: 10px;
  height: 100%; /* Ensure the wrapper takes full height */
}

.gaugechart-title {
  font-size: 18px;
  color: #007bff;
  margin-bottom: 50px; /* Adjust this value to control the distance from the chart */
}

#gauge-chart {
  width: 100%;
  height: 250px; /* Adjust the height as needed */
}

.echarts-tooltip {
  background-color: rgba(0, 0, 0, 0.7) !important;
  color: white !important;
  border-radius: 4px !important;
  padding: 10px !important;
}
</style>
