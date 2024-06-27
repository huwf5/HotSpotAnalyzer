<template>
  <v-chart class="chart" v-loading="props.isLoading" :option="barOption" autoresize />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import { GridComponent, DatasetComponent } from "echarts/components";
import { onMounted, ref, watch } from "vue";
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

const dataSetOptions = ref<{ series: any[]; dimensions: string[]; legends: string[] }>({
  series: [],
  dimensions: [],
  legends: []
});

function processData() {
  // calculate chart data
  let number = 0;
  let chartData: BarChartData[] = [];
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
    chartData.push({ name: "post" + number.toString(), ...processed_post_data });
  }
  // calculate dimensions
  let series: any[] = [];
  let dimensions: string[] = [];
  let legends: string[] = [];
  if (chartData.length > 0) {
    for (const key of Object.keys(chartData[0])) {
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
  barOption.value.dataset.source = chartData;
  barOption.value.series = series;
  barOption.value.legend.data = legends;
  barOption.value.dataset.dimensions = dimensions;
}

onMounted(() => processData);

const barOption = ref({
  tooltip: {
    trigger: "axis"
  },
  dataset: {
    dimensions: [] as string[],
    source: [] as BarChartData[]
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
  series: [] as any[],
  barMaxWidth: 30,
  barMinHeight: 100,
  legend: {
    // 添加图例配置
    orient: "horizontal", // 设置图例为垂直布局，通常放在右侧更合适
    bottom: "5%",
    data: dataSetOptions.value.legends // 图例项对应柱状图的名称
  }
});

watch(() => props.data, processData);
</script>

<style scoped lang="scss">
.chart {
  height: 300px;
}
</style>
