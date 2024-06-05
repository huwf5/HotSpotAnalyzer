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
import { ref, onMounted, onUnmounted } from "vue";

const refChart = ref(null);

onMounted(() => {
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
          data: [
            { name: "JavaScript", value: 1000 },
            { name: "Vue", value: 800 },
            { name: "React", value: 600 },
            { name: "Angular", value: 400 },
            { name: "Svelte", value: 200 },
            { name: "Python", value: 950 },
            { name: "Ruby", value: 300 },
            { name: "Java", value: 850 },
            { name: "C#", value: 500 },
            { name: "C++", value: 650 },
            { name: "JavaScript", value: 100 },
            { name: "Vue", value: 8000 },
            { name: "React", value: 6000 },
            { name: "Angular", value: 4000 },
            { name: "Svelte", value: 2000 },
            { name: "Python", value: 9050 },
            { name: "Ruby", value: 3000 },
            { name: "Java", value: 8050 },
            { name: "C#", value: 5000 },
            { name: "C++", value: 6500 }
          ].map(item => ({
            name: item.name,
            value: Math.sqrt(item.value) * 10
          }))
        }
      ]
    });
  }
});

onUnmounted(() => {
  if (chartInstance && chartInstance.dispose) {
    chartInstance.dispose();
  }
});
</script>
<style scoped>
@keyframes fadeInScaleUp {
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
  background-color: #fff; /* 背景颜色调整为白色 */
  position: relative;
}

.word-cloud-title {
  position: absolute; /* 使标题定位到左上角 */
  top: 0;
  left: 10px;
  font-size: 18px; /* 调整字体大小为较小的尺寸 */
  color: #007bff; /* 字体颜色改为蓝色 */
  margin: 0;
}

.word-cloud-container {
  width: 100%;
  height: 350px;
  animation: fadeInScaleUp 1s ease-out forwards;
}
</style>
