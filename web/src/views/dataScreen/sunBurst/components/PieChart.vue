<template>
  <!-- 年龄比例 -->
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
const colors_emo = ["#800000", "#FFA500", "#006400"];

const option: ECOption = {
  color: colors,
  tooltip: {
    // 提示框配置
    show: true,
    trigger: "item",
    formatter: "{b} <br/>占比：{d}%" // formatter函数在下方定义
  },
  legend: {
    // 图例配置（处于右方的图例）
    orient: "vertical",
    right: "20px",
    top: "15px",
    itemGap: 15,
    itemWidth: 14,
    // formatter：用于自定义图例项（上方的提示框用到）的显示内容，根据图例项的名称查找对应的数据项，并显示名称和百分比
    formatter: function (name: string) {
      let text = "";
      // data3.value.forEach((val: ChartProp) => {
      props.data.forEach((val: ChartProp) => {
        if (val.name === name) text = " " + name + "　 " + val.percentage;
      });
      return text;
    },
    textStyle: { color: "#fff" }
  },
  grid: { top: "bottom", left: 10, bottom: 10 }, // 饼状图的网格配置
  // 饼状图的系列配置
  series: [
    // 第一个系列
    {
      zlevel: 1,
      name: "年龄比例",
      type: "pie",
      selectedMode: "single",
      radius: [0, 410],
      center: ["35%", "50%"],
      startAngle: 60,
      label: {
        position: "inside",
        show: true,
        color: "#fff",
        formatter: function (params) {
          return (params.data as ChartProp).percentage;
        },
        rich: {
          b: {
            fontSize: 16,
            lineHeight: 30,
            color: "#fff"
          }
        }
      },
      itemStyle: {
        shadowColor: "rgba(0, 0, 0, 0.2)",
        shadowBlur: 10
      },
      data: props.data.map((val: ChartProp, index: number) => {
        return {
          value: val.value,
          name: val.name,
          percentage: val.percentage,
          itemStyle: {
            borderWidth: 1,
            shadowBlur: 2,
            borderColor: colors[index],
            borderRadius: 0
          }
        };
      })
    },
    // 第二个系列
    {
      name: "",
      type: "pie",
      selectedMode: "single",
      radius: [410, 470],
      center: ["35%", "50%"],
      label: {
        position: "inside",
        show: false,
        color: "#fff",
        formatter: function (params) {
          return (params.data as ChartProp).percentage;
        },
        rich: {
          b: {
            fontSize: 16,
            lineHeight: 30,
            color: "#fff"
          }
        }
      },
      startAngle: 60,
      data: props.data.flatMap((val: ChartProp) => {
        //, index: number
        return [
          {
            value: val.pos_value,
            name: "积极",
            itemStyle: {
              borderWidth: 1,
              shadowBlur: 2,
              color: colors_emo[0],
              borderColor: colors_emo[0],
              borderRadius: 0.5
            }
          },
          {
            value: val.neu_value,
            name: "中立",
            itemStyle: {
              borderWidth: 1,
              shadowBlur: 2,
              color: colors_emo[1],
              borderColor: colors_emo[1],
              borderRadius: 0.5
            }
          },
          {
            value: val.neg_value,
            name: "消极",
            itemStyle: {
              borderWidth: 1,
              shadowBlur: 2,
              color: colors_emo[2],
              borderColor: colors_emo[2],
              borderRadius: 0.5
            }
          }
        ];
      })
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
