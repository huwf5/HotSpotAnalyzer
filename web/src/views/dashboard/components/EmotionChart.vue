<template>
  <div class="emotion-wrapper">
    <h1 class="emotion-title">👻情感分析</h1>
    <div ref="chartRef" class="emotion-chart"></div>
  </div>
</template>

<script setup lang="ts">
import { EChartsType } from "echarts";
import { onMounted, ref, onBeforeUnmount, computed, watch } from "vue";
import { getMainSentiment } from "@/api/modules/event_analysis";
import * as echarts from "echarts";
import { useStore } from "vuex";
// import axios from "axios";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);

const chartRef = ref(null);
// const chartInstance = ref(null);
const chartInstance = ref<EChartsType | null>(null);

const defaultEmotionData = [
  { emotion: "Joyful", percentage: 65.97 },
  { emotion: "Sad", percentage: 6.48 },
  { emotion: "Angry", percentage: 0.95 },
  { emotion: "Disgusted", percentage: 3.72 },
  { emotion: "Scared", percentage: 0 },
  { emotion: "Surprised", percentage: 10.77 },
  { emotion: "Calm", percentage: 11.25 },
  { emotion: "Disappointed", percentage: 0.86 }
];
const emotionData = ref(defaultEmotionData);

// 随机颜色生成函数
const getRandomColor = () => {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

async function fetchEmotionData(selectedDateValue) {
  const date = selectedDateValue === "earlier" ? "history" : selectedDateValue;
  try {
    // const response = await axios.get(`http://127.0.0.1:8000/api/emotion/fetch_emotions/?date=${date}`, {
    //   headers: {
    //     Authorization:
    //       "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NTY5MzI3LCJpYXQiOjE3MTk1NDc3MjcsImp0aSI6IjRiMzQxY2NhYmRiYjQ3YTA5NmUyNTJhYWU0NDA5MjlhIiwidXNlcl9lbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.SUWOSeM-Dq-cevFsq_rUCuSH5I3IG4Qi9alcp00DCXk", // 替换为你的JWT令牌
    //     accept: "application/json"
    //   }
    // });

    await getMainSentiment(date).then(response => {
      emotionData.value = response.data;
    });
  } catch (error) {
    console.error("Failed to fetch emotion data from server, using default data", error);
    emotionData.value = defaultEmotionData;
  }
  initChart(); // 初始化或更新图表
}

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
        data: emotionData.value.map(item => item.emotion),
        axisLabel: {
          interval: 0,
          rotate: 45, // 使标签倾斜45度
          formatter: "{value}"
        }
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
                Joyful: "#f5222d",
                Sad: "#fa8c16",
                Angry: "#52c41a",
                Disgusted: "#1890ff",
                Scared: "#eb2f96",
                Surprised: "#faad14",
                Calm: "#13c2c2",
                Disappointed: "#2f54eb"
              };
              return colors[emotionData.value[params.dataIndex].emotion] || getRandomColor();
            }
          },
          animationDuration: 2000,
          label: {
            show: true,
            position: "top",
            formatter: "{c}%" // 格式化标签为百分比
          }
        }
      ]
    });
  }
};

onMounted(() => {
  fetchEmotionData(selectedDate.value);
  // initChart();
  window.addEventListener("resize", () => {
    if (chartInstance.value) {
      chartInstance.value.resize();
    }
  });
});

watch(selectedDate, newDate => {
  fetchEmotionData(newDate);
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
