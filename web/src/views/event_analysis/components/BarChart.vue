<template>
  <v-chart class="chart" v-loading="props.isLoading" :option="barOption" autoresize />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import { GridComponent, DatasetComponent } from "echarts/components";
import { ref, watch } from "vue";
import VChart from "vue-echarts";

use([GridComponent, BarChart, DatasetComponent]);

interface BarChartData {
  name: string;
  [key: string]: any;
}

const props = defineProps<{
  data: any[];
  isLoading: boolean;
}>();
const chartData = ref<BarChartData[]>([]);

const dataSetOptions = ref<{ series: any[]; dimensions: string[]; legends: string[] }>({
  series: [],
  dimensions: [],
  legends: []
});

function initDimensions() {
  let series: any[] = [];
  let dimensions: string[] = [];
  let legends: string[] = [];
  if (chartData.value.length > 0) {
    for (const key of Object.keys(chartData.value[0])) {
      dimensions.push(key);
      if (key !== "name") {
        series.push({
          type: "bar",
          stack: "total",
          emphasis: {
            focus: "series"
          },
          encode: {
            x: "name",
            y: key
          },
          name: key // 添加名称以供tooltip使用
        });
        legends.push(key);
      }
    }
  }
  dataSetOptions.value.series = series;
  dataSetOptions.value.dimensions = dimensions;
  dataSetOptions.value.legends = legends;
}

function processData() {
  let number = 0;
  chartData.value = [];
  for (const post_data of props.data) {
    number++;
    let total_val = 0;
    let processed_post_data = {};
    for (const val of Object.values(post_data)) total_val += val as number;
    if (total_val > 0) {
      for (const entry of Object.entries(post_data)) {
        processed_post_data[entry[0]] = ((entry[1] as number) / total_val) * 100;
      }
    } else processed_post_data = { ...post_data };
    chartData.value.push({ name: "post" + number.toString(), ...processed_post_data });
  }
}
processData();
initDimensions();

const barOption = ref({
  tooltip: {
    trigger: "axis"
  },
  dataset: {
    dimensions: dataSetOptions.value.dimensions,
    source: chartData.value
  },
  grid: {
    containLabel: true,
    left: "5%",
    right: "5%",
    top: "5%",
    bottom: "20%"
  },
  xAxis: {
    // 柱状图的x轴
    type: "category"
  },
  yAxis: {
    // 柱状图的y轴
    type: "value"
  },
  series: dataSetOptions.value.series,
  legend: {
    // 添加图例配置
    orient: "horizontal", // 设置图例为垂直布局，通常放在右侧更合适
    bottom: "5%",
    data: dataSetOptions.value.legends // 图例项对应柱状图的名称
  }
});

watch(
  () => props.data,
  () => {
    processData();
    initDimensions();
    barOption.value.dataset.source = chartData.value;
    barOption.value.dataset.dimensions = dataSetOptions.value.dimensions;
    barOption.value.series = dataSetOptions.value.series;
    barOption.value.legend.data = dataSetOptions.value.legends;
  }
);
</script>

<style scoped lang="scss">
.chart {
  height: 300px;
}
</style>
