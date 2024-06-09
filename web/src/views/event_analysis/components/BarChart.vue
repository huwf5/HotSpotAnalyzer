<template>
  <v-chart class="chart" v-loading="props.isLoading" :option="barOption" autoresize />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import { GridComponent, DatasetComponent } from "echarts/components";
import { computed, ref, watch } from "vue";
import VChart from "vue-echarts";

use([GridComponent, BarChart, DatasetComponent]);

interface BarChartData {
  name: string;
  [key: string]: any;
}

const props = defineProps<{
  data: BarChartData[];
  isLoading: boolean;
}>();

const dataSetOptions = computed(() => {
  let series: any[] = [];
  let dimensions: string[] = [];
  let legends: string[] = [];
  if (props.data.length > 0) {
    for (const key of Object.keys(props.data[0])) {
      dimensions.push(key);
      if (key !== "name" && key !== "value") {
        series.push({
          type: "bar",
          stack: "total",
          label: {
            show: true
          },
          emphasis: {
            focus: "series"
          },
          encode: {
            x: "name",
            y: key
          },
          name: key // 添加名称以供legend使用
        });
        legends.push(key);
      }
    }
  }

  return { series, dimensions, legends };
});

const barOption = ref({
  tooltip: {
    trigger: "axis"
  },
  dataset: {
    dimensions: dataSetOptions.value.dimensions,
    source: props.data
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
  newVal => {
    barOption.value.dataset.source = newVal;
  }
);
</script>

<style scoped lang="scss">
.chart {
  display: flex;
  flex: none;
  flex-grow: 1;
  align-self: stretch;
}
</style>
