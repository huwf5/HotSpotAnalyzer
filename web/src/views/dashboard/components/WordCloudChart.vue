<template>
  <div class="word-cloud-wrapper">
    <h1 class="word-cloud-title">👻词云分析</h1>
    <div ref="refChart" class="word-cloud-container"></div>
  </div>
</template>

<script setup>
// import * as echarts from "echarts";
import { init as initECharts } from "echarts";
import "echarts-wordcloud";
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { useStore } from "vuex";

const refChart = ref(null);
const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const fetchWordCloud = async selectedDateValue => {
  const date = ref("");
  if (selectedDateValue === "earlier") {
    date.value = "history";
  } else {
    date.value = selectedDateValue;
  }

  const response = await fetch(`http://127.0.0.1:8000/fetch-wordCloud?date=${date.value}`);
  const wordCloud = ref(null);
  wordCloud.value = await response.json();
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
          data: wordCloud.value["data"].map(item => ({
            name: item["name"],
            value: Math.sqrt(item["value"]) * 10
          }))
        }
      ]
    });
  }
};
watch(
  selectedDate,
  newDate => {
    fetchWordCloud(newDate);
  },
  { immediate: true }
);
onMounted(() => {
  fetchWordCloud(selectedDate.value);
});

onUnmounted(() => {
  if (chartInstance && chartInstance.dispose) {
    chartInstance.dispose();
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
