<template>
  <!-- 热点旭日图 -->
  <div class="echarts">
    <ECharts :option="option" :resize="false" />
  </div>
</template>

<script setup lang="ts">
import ECharts from "@/components/ECharts/index.vue";
import { ECOption } from "@/components/ECharts/config";
// import { ref } from "vue";
// 数据接口 ChartProp
interface ChartProp {
  value: number;
  name: string;
  percentage: string;
  pos_value: number;
  neu_value: number;
  neg_value: number;
}

// 从父组件接收数据
const props = defineProps({
  msg: String,
  data: {
    type: Array as () => ChartProp[],
    required: true
  }
});

// 定义了一些颜色值和图表配置选项 option，包括颜色配置、提示框、图例、网格以及两个饼状图系列
const colors = ["#F6C95C", "#EF7D33", "#1F9393", "#184EA1", "#81C8EF", "#9270CA"];
const colors_emo = ["#006400", "#FFA500", "#800000"];

const option: ECOption = {
  color: colors,
  tooltip: {
    // 提示框
    show: true,
    trigger: "item",
    formatter: function (params) {
      return `${params.name}: ${(params.data as ChartProp).percentage}`;
    }
  },
  series: [
    {
      name: "热点事件",
      type: "sunburst",
      // percentage: "100%",
      radius: [0, "100%"],
      center: ["35%", "50%"],
      label: {
        // 扇形内的文字
        show: true,
        color: "#fff",
        formatter: function (params) {
          // params是下面定义的data
          return `${params.name}: ${(params.data as ChartProp).percentage}`;
        }
      },
      itemStyle: {
        borderWidth: 1,
        borderColor: "#fff"
      },
      data: props.data.map((val: ChartProp) => {
        return {
          name: val.name,
          value: val.value,
          percentage: val.percentage,
          children: [
            {
              name: "Positive",
              value: val.pos_value,
              percentage: ((val.pos_value / val.value) * 100).toFixed(2) + "%",
              itemStyle: {
                color: colors_emo[0]
              }
            },
            {
              name: "Neutral",
              value: val.neu_value,
              percentage: ((val.neu_value / val.value) * 100).toFixed(2) + "%",
              itemStyle: {
                color: colors_emo[1]
              }
            },
            {
              name: "Negative",
              value: val.neg_value,
              percentage: ((val.neg_value / val.value) * 100).toFixed(2) + "%",
              itemStyle: {
                color: colors_emo[2]
              }
            }
          ]
        };
      }),
      // 扇形厚度
      levels: [
        {}, // 少不了
        // 事件热度比例
        {
          r0: 0,
          r: "70%"
          // label: {
          //   rotate: 0
          // }
        },
        // 感情色彩比例
        {
          r0: "70%",
          r: "100%"
          // label: {
          //   rotate: 0
          // }
        }
      ]
    }
  ]
};
</script>

<style lang="scss" scoped>
.echarts {
  width: 100%;
  height: 100%;
}
</style>
