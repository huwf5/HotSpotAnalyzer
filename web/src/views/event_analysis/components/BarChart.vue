<template>
  <v-chart class="chart" v-loading="props.isLoading" :option="BarOption" autoresize />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import { GridComponent, DatasetComponent } from "echarts/components";
import { ref } from "vue";
import VChart from "vue-echarts";

use([GridComponent, BarChart, DatasetComponent]);

const props = defineProps<{
  data: any[];
  isLoading: boolean;
}>();

const BarOption = ref({
  tooltip: {
    trigger: "axis"
  },
  dataset: {
    dimensions: ["value", "name", "happy", "anger"],
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
  series: [
    {
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
        y: "happy",
        itemChildGroupId: "happy"
      },
      name: "Happy" // 添加名称以供legend使用
    },
    {
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
        y: "anger",
        itemChildGroupId: "anger"
      },
      name: "Anger" // 添加名称以供legend使用
    }
  ],
  legend: {
    // 添加图例配置
    orient: "horizontal", // 设置图例为垂直布局，通常放在右侧更合适
    bottom: "5%",
    data: ["Happy", "Anger"] // 图例项对应柱状图的名称
  }
});
</script>

<style scoped lang="scss">
.chart {
  display: flex;
  flex: none;
  flex-grow: 1;
  align-self: stretch;
}
</style>
