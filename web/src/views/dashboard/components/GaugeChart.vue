<template>
  <div class="gaugechart-wrapper">
    <h1 class="gaugechart-title">👻热度仪表</h1>
    <v-chart ref="myChart" class="gauge-chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import VChart from "vue-echarts";
import { ECharts } from "echarts";

const myChart = ref<ECharts>();

const option = ref({
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
});
</script>

<style scoped>
.gaugechart-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* Center the content vertically */
  height: 100%; /* Ensure the wrapper takes full height */
  padding: 0;
  margin-bottom: 10px;
}
.gaugechart-title {
  margin-bottom: 50px; /* Adjust this value to control the distance from the chart */
  font-size: 18px;
  color: #007bff;
}
.gauge-chart {
  width: 100%;
  height: 250px; /* Adjust the height as needed */
}
.echarts-tooltip {
  padding: 10px !important;
  color: white !important;
  background-color: rgb(0 0 0 / 70%) !important;
  border-radius: 4px !important;
}
</style>
