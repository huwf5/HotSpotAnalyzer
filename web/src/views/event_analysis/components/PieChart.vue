<template>
  <v-chart
    class="chart"
    :option="pieOption"
    ref="chart"
    autoresize
    v-loading="props.isLoading"
    @finished="stratRotation"
    @mouseover="stopRotation"
    @mouseout="restartRotation"
    @click="rotateEnabled = !rotateEnabled"
    @highlight="stopRotation"
    @downplay="restartRotation"
  />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import { TitleComponent, TooltipComponent, LegendComponent, DatasetComponent } from "echarts/components";
import VChart from "vue-echarts";
import { ref, watch } from "vue";
import { ECharts } from "echarts";

use([CanvasRenderer, PieChart, TitleComponent, DatasetComponent, TooltipComponent, LegendComponent]);

const rotateEnabled = ref(true);
const rotate = ref(0);
const timer = ref<NodeJS.Timeout>();
const coldBoot = ref(true);
const chart = ref<ECharts>();

interface PieChartData {
  name: string;
  value: number;
  [key: string]: any;
}

const props = withDefaults(
  defineProps<{
    displayMode?: number;
    isLoading: boolean;
    chartTitle?: string;
    data: PieChartData[];
  }>(),
  {
    displayMode: 0
  }
);

const seriesArray = [
  [
    // Minimize Mode
    {
      name: props.chartTitle !== undefined ? props.chartTitle : "PieChart",
      type: "pie",
      startAngle: 0,
      endAngle: "auto",
      animation: true,
      radius: ["35%", "40%"],
      center: ["50%", "50%"],
      padAngle: 2,
      avoidLabelOverlap: false,
      showEmptyCircle: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: "#fff"
      },
      label: {
        formatter: "{b}\n{d}%"
      }
    }
  ],
  [
    // Maximize Mode
    {
      name: props.chartTitle !== undefined ? props.chartTitle : "PieChart",
      type: "pie",
      startAngle: 180,
      endAngle: 360,
      animation: true,
      radius: ["65%", "70%"],
      center: ["50%", "80%"],
      padAngle: 2,
      avoidLabelOverlap: false,
      showEmptyCircle: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: "#fff"
      },
      label: {
        formatter: "{b}\n{d}%"
      }
    }
  ]
];

const pieOption = ref({
  tooltip: {
    trigger: "item"
  },
  legend: {
    top: "center",
    left: "5%",
    orient: "vertical"
  },
  dataset: {
    source: props.data
  },
  series: seriesArray[props.displayMode]
});

watch(
  () => props.displayMode,
  newVal => {
    coldBoot.value = true;
    if (newVal === 1) {
      stopRotation();
    }
    pieOption.value.series = seriesArray[newVal];
    chart.value?.setOption(pieOption.value);
  }
);
watch(
  () => props.data,
  newVal => {
    pieOption.value.dataset.source = newVal;
  }
);

function stratRotation() {
  if (coldBoot.value) {
    coldBoot.value = false;
    restartRotation();
  }
}

function stopRotation() {
  timer.value && clearInterval(timer.value);
  timer.value = undefined;
  pieOption.value.series[0].animation = true;
}

function restartRotation() {
  if (timer.value === undefined && rotateEnabled.value && props.displayMode === 0) {
    pieOption.value.series[0].animation = false;
    timer.value = setInterval(() => {
      rotate.value = (rotate.value + 0.1) % 360;
      pieOption.value.series[0].startAngle = 360 - rotate.value;
    }, 100);
  }
}
</script>

<style scoped lang="scss">
.chart {
  width: 100%;
  height: 200px;
}
</style>
