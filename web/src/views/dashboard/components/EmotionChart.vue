<template>
  <div class="emotion-wrapper">
    <h1 class="emotion-title">👻情感分析</h1>
    <div ref="chartRef" class="emotion-chart"></div>
  </div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount } from "vue";
import * as echarts from "echarts";

const chartRef = ref(null);
const chartInstance = ref(null);
const emotionData = ref([
  { emotion: "Happy", percentage: 20 },
  { emotion: "Sad", percentage: 30 },
  { emotion: "Angry", percentage: 10 },
  { emotion: "Surprised", percentage: 15 },
  { emotion: "Fearful", percentage: 5 },
  { emotion: "Disgusted", percentage: 20 }
]);

const initChart = () => {
  if (chartRef.value) {
    // 对 emotionData 进行排序，根据需求选择升序或降序
    emotionData.value.sort((a, b) => b.percentage - a.percentage); // 降序排序

    chartInstance.value = echarts.init(chartRef.value);
    chartInstance.value.setOption({
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" }
      },
      xAxis: {
        type: "category",
        data: emotionData.value.map(item => item.emotion)
      },
      yAxis: {
        type: "value",
        boundaryGap: [0, 0.01]
      },
      series: [
        {
          type: "bar",
          data: emotionData.value.map(item => item.percentage),
          itemStyle: {
            color: params => {
              const colors = {
                Happy: "#fadb14",
                Sad: "#1890ff",
                Angry: "#ff4d4f",
                Surprised: "#9254de",
                Fearful: "#13c2c2",
                Disgusted: "#389e0d"
              };
              return colors[emotionData.value[params.dataIndex].emotion] || "#000";
            }
          },
          animationDuration: 2000,
          label: {
            show: true, // 显示标签
            position: "top", // 标签的位置
            formatter: "{c}%" // 标签内容格式器
          }
        }
      ]
    });
  }
};

onMounted(() => {
  initChart();
  window.addEventListener("resize", () => {
    if (chartInstance.value) {
      chartInstance.value.resize();
    }
  });
});

onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.dispose();
  }
  window.removeEventListener("resize", () => {
    if (chartInstance.value) {
      chartInstance.value.resize();
    }
  });
});
</script>

<style scoped>
.emotion-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ffffff; /* 背景颜色调整为白色 */
}
.emotion-title {
  position: absolute; /* 使标题定位到左上角 */
  top: 0;
  left: 10px;
  margin: 0;
  font-size: 18px;
  color: #007bff; /* 字体颜色改为蓝色 */
}
.emotion-chart {
  width: 90%;
  height: 350px;
  animation: fadeInScaleUp 1s ease-out forwards;
}
</style>
