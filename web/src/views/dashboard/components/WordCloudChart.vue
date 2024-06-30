<template>
  <div class="word-cloud-wrapper">
    <h1 class="word-cloud-title">👻词云分析</h1>
    <div ref="refChart" class="word-cloud-container"></div>
  </div>
</template>

<script setup lang="ts">
import { init as initECharts, EChartsType } from "echarts";
import { getWordCloud } from "@/api/modules/event_analysis";
import "echarts-wordcloud";
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { useStore } from "vuex";
// import axios from "axios";
const refChart = ref(null);
const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const defaultWordCloudData = [
  { name: "Example", value: 300 },
  { name: "Word", value: 260 },
  { name: "Cloud", value: 220 },
  { name: "Data", value: 180 },
  { name: "Analysis", value: 160 },
  { name: "Visualization", value: 140 },
  { name: "Vue.js", value: 120 },
  { name: "JavaScript", value: 100 },

  { name: "ECharts", value: 80 },
  { name: "Project", value: 60 }
];

const wordCloudData = ref(defaultWordCloudData);
const chartInstance = ref<EChartsType | null>(null);

async function fetchWordCloudData(selectedDateValue: string) {
  const date = selectedDateValue === "earlier" ? "history" : selectedDateValue;
  try {
    await getWordCloud(date).then(response => {
      wordCloudData.value = response.data.map(item => ({
        name: item.name,
        value: Math.sqrt(item.value) * 10
      }));
    });
  } catch (error) {
    console.error("Failed to fetch word cloud data from server, using default data", error);
    wordCloudData.value = defaultWordCloudData;
  }
  initChart();
}

const initChart = () => {
  if (refChart.value) {
    const chartInstance = initECharts(refChart.value, null, {
      devicePixelRatio: 2
    });
    chartInstance.setOption({
      tooltip: {
        show: true,
        formatter: function (params) {
          return `${params.name}: ${params.value}`;
        }
      },
      series: [
        {
          type: "wordCloud",
          shape: "ellipse",
          gridSize: 8,
          sizeRange: [12, 50], // 设置初始文字大小范围
          rotationRange: [-60, 60],
          textStyle: {
            fontFamily: "sans-serif",
            fontWeight: "bold",
            color: function () {
              return (
                "rgb(" +
                [Math.round(Math.random() * 200) + 50, Math.round(Math.random() * 50), Math.round(Math.random() * 50 + 50)].join(
                  ","
                ) +
                ")"
              );
            }
          },
          data: wordCloudData.value
        }
      ]
    });
  }
};

onMounted(() => {
  fetchWordCloudData(selectedDate.value);
});

watch(selectedDate, newDate => {
  fetchWordCloudData(newDate);
});

onUnmounted(() => {
  if (chartInstance.value) {
    (chartInstance.value as EChartsType).dispose(); // 使用类型断言
  }
});
</script>
<style scoped>
@keyframes fade-in-scale-up {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.word-cloud-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ffffff; /* 背景颜色调整为白色 */
}
.word-cloud-title {
  position: absolute; /* 使标题定位到左上角 */
  top: 0;
  left: 10px;
  margin: 0;
  font-size: 18px; /* 调整字体大小为较小的尺寸 */
  color: #007bff; /* 字体颜色改为蓝色 */
}
.word-cloud-container {
  width: 100%;
  height: 350px;
  animation: fade-in-scale-up 1s ease-out forwards;
}
</style>
