<template>
  <v-chart class="word_chart" ref="chart" v-loading="props.isLoading" :option="wordCloudOption" />
</template>

<script setup lang="ts">
import { ECharts } from "echarts";
import "echarts-wordcloud";
import { ref, watch } from "vue";
import VChart from "vue-echarts";

interface WordCloudData {
  name: string;
  value: number;
  [key: string]: any;
}

const props = defineProps<{
  data: WordCloudData[];
  reload: boolean;
  isLoading: boolean;
}>();

const chart = ref<ECharts>();
watch(
  () => props.reload,
  () => {
    chart.value!.resize();
  }
);

const wordCloudOption = ref({
  series: [
    {
      type: "wordCloud",
      shape: "square",
      keepAspect: true,
      center: ["50%", "50%"],
      sizeRange: [10, 60],
      rotationRange: [0, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      shrinkToFit: false,
      layoutAnimation: true,
      textStyle: {
        fontFamily: "sans-serif",
        fontWeight: "bold",
        color: function () {
          return (
            "rgb(" +
            [Math.round(Math.random() * 160), Math.round(Math.random() * 160), Math.round(Math.random() * 160)].join(",") +
            ")"
          );
        }
      },
      emphasis: {
        focus: "self",
        textStyle: {
          textShadowBlur: 10,
          textShadowColor: "#333"
        }
      },
      data: props.data
    }
  ]
});

watch(
  () => props.data,
  newVal => {
    wordCloudOption.value.series[0].data = newVal;
  }
);
</script>

<style scoped lang="scss">
.word_chart {
  width: 100%;
  height: 100%;
}
</style>
