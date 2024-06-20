<template>
  <div class="emotion-wrapper">
    <h1 class="emotion-title">👻情感分析</h1>
    <div ref="chartRef" class="emotion-chart"></div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import * as echarts from "echarts";
import { useStore } from "vuex";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);
const chartRef = ref(null);

const fetchEmotionData = async selectedDateValue => {
  const date = ref("");
  if (selectedDateValue === "earlier") {
    date.value = "history";
  } else {
    date.value = selectedDateValue;
  }

  const response = await fetch(`http://127.0.0.1:8000/fetch-emotionData?date=${date.value}`);
  const emotionData = ref(null);
  emotionData.value = await response.json();
  emotionData.value = emotionData.value["data"];

  if (chartRef.value) {
    // 对 emotionData 进行排序，根据需求选择升序或降序
    emotionData.value.sort((a, b) => b.percentage - a.percentage); // 降序排序

    const chartInstance = echarts.init(chartRef.value);
    chartInstance.setOption({
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" }
      },
      xAxis: {
        type: "category",
        data: emotionData.value.map(item => item["emotion"])
      },
      yAxis: {
        type: "value",
        boundaryGap: [0, 0.01]
      },
      series: [
        {
          type: "bar",
          data: emotionData.value.map(item => item["percentage"]),
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
              return colors[emotionData.value[params.dataIndex]["emotion"]] || "#000";
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
  fetchEmotionData(selectedDate.value);
});
watch(
  selectedDate,
  newDate => {
    fetchEmotionData(newDate);
  },
  { immediate: true }
);
</script>

<style scoped>
.emotion-wrapper {
  position: relative;
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
  width: 100%;
  height: 350px;
  animation: fadeInScaleUp 1s ease-out forwards;
}
</style>
