<template>
  <div id="container"></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Highcharts from "highcharts";
import Networkgraph from "highcharts/modules/networkgraph";
import Exporting from "highcharts/modules/exporting";

// 引入 networkgraph 和 exporting 模块到 Highcharts
Networkgraph(Highcharts);
Exporting(Highcharts);

const graphData = ref({
  nodes: [
    {
      id: "林斌刘向东夫妇向中山大学捐赠1亿元",
      group: 1
    },
    {
      id: "2024年5月30日",
      group: 2
    },
    {
      id: "中山大学广州校区南校园怀士堂",
      group: 2
    },
    {
      id: "1亿元人民币",
      group: 2
    },
    {
      id: "林斌刘向东文体中心建设、林斌刘向东奖学金、洪淡华奖学金等",
      group: 2
    },
    {
      id: "中山大学校长高松院士授予林斌首位名誉校董荣衔",
      group: 1
    },
    {
      id: "高松院士",
      group: 2
    },
    {
      id: "林斌",
      group: 2
    },
    {
      id: "林斌在签约仪式上致辞",
      group: 1
    },
    {
      id: "深情告白母校",
      group: 2
    },
    {
      id: "雷军称小米独特企业文化如同仙丹",
      group: 1
    },
    {
      id: "雷军",
      group: 2
    }
  ],
  links: [
    {
      source: "林斌刘向东夫妇向中山大学捐赠1亿元",
      target: "2024年5月30日",
      description: "时间"
    },
    {
      source: "林斌刘向东夫妇向中山大学捐赠1亿元",
      target: "中山大学广州校区南校园怀士堂",
      description: "地点"
    },
    {
      source: "林斌刘向东夫妇向中山大学捐赠1亿元",
      target: "1亿元人民币",
      description: "捐赠金额"
    },
    {
      source: "林斌刘向东夫妇向中山大学捐赠1亿元",
      target: "林斌刘向东文体中心建设、林斌刘向东奖学金、洪淡华奖学金等",
      description: "捐赠项目"
    },
    {
      source: "中山大学校长高松院士授予林斌首位名誉校董荣衔",
      target: "高松院士",
      description: "人物"
    },
    {
      source: "中山大学校长高松院士授予林斌首位名誉校董荣衔",
      target: "林斌",
      description: "人物"
    },
    {
      source: "林斌在签约仪式上致辞",
      target: "林斌",
      description: "人物"
    },
    {
      source: "林斌在签约仪式上致辞",
      target: "深情告白母校",
      description: "态度"
    },
    {
      source: "雷军称小米独特企业文化如同仙丹",
      target: "雷军",
      description: "人物"
    },
    {
      source: "林斌刘向东夫妇向中山大学捐赠1亿元",
      target: "中山大学校长高松院士授予林斌首位名誉校董荣衔",
      description: "包含关系"
    },
    {
      source: "林斌刘向东夫妇向中山大学捐赠1亿元",
      target: "林斌在签约仪式上致辞",
      description: "因果关系"
    },
    {
      source: "雷军称小米独特企业文化如同仙丹",
      target: "林斌刘向东夫妇向中山大学捐赠1亿元",
      description: "共指关系"
    }
  ]
});

const groupColors = ["#FF6347", "#4682B4"];

onMounted(() => {
  const nodes = graphData.value.nodes.map(node => ({
    id: node.id,
    color: groupColors[node.group - 1],
    marker: {
      radius: 12 // 节点大小
    }
  }));

  const links = graphData.value.links.map(link => ({
    from: link.source,
    to: link.target,
    description: link.description // 连接的描述信息
  }));

  Highcharts.chart("container", {
    chart: {
      type: "networkgraph",
      height: "600px", // 设置高度
      zoomType: "xy", // 启用 x 和 y 方向的缩放
      panning: {
        enabled: true,
        type: "xy" // 启用 x 和 y 方向的拖动
      },
      panKey: "shift" // 拖动时需按住 Shift 键
    },
    tooltip: {
      useHTML: true,
      headerFormat: "<b>{point.key}</b><br>",
      pointFormat: "{point.description}"
    },
    credits: {
      enabled: false
    },
    exporting: {
      enabled: false
    },
    title: {
      text: "事件图谱2D"
    },
    subtitle: {
      text: "事件节点"
    },
    plotOptions: {
      networkgraph: {
        keys: ["from", "to"],
        layoutAlgorithm: {
          enableSimulation: true
        },
        point: {
          events: {
            mouseOver: function () {
              this.linksTo.forEach(function (link) {
                link.graphic.attr({
                  stroke: "red", // 高亮颜色
                  strokeWidth: 5 // 高亮时的线宽
                });
              });
              this.linksFrom.forEach(function (link) {
                link.graphic.attr({
                  stroke: "red",
                  strokeWidth: 5
                });
              });
            },
            mouseOut: function () {
              this.linksTo.forEach(function (link) {
                link.graphic.attr({
                  stroke: "#cccccc", // 默认颜色
                  strokeWidth: 1 // 默认线宽
                });
              });
              this.linksFrom.forEach(function (link) {
                link.graphic.attr({
                  stroke: "#cccccc",
                  strokeWidth: 1
                });
              });
            }
          }
        }
      }
    },
    series: [
      {
        dataLabels: {
          enabled: true,
          linkFormat: "{point.description}",
          format: "{point.id}",
          style: {
            width: "100px", // 限制标签的最大宽度
            color: "#333", // 文本颜色
            textOverflow: "ellipsis",
            whiteSpace: "nowrap", // 不允许文本换行
            overflow: "hidden" // 隐藏溢出的文本
          }
        },
        nodes: nodes,
        data: links
      }
    ]
  });
});
</script>

<style scoped>
#container {
  width: 100%; /* 响应式宽度 */
  height: 500px; /* 固定高度 */
}
.highcharts-data-table table {
  min-width: 320px;
  max-width: 800px;
  margin: 1em auto;
}
.highcharts-figure,
.highcharts-data-table table {
  min-width: 320px;
  max-width: 800px;
  margin: 1em auto;
}

.highcharts-data-table table {
  font-family: Verdana, sans-serif;
  border-collapse: collapse;
  border: 1px solid #ebebeb;
  margin: 10px auto;
  text-align: center;
  width: 100%;
  max-width: 500px;
}
.highcharts-data-table caption {
  padding: 1em 0;
  font-size: 1.2em;
  color: #555;
}
.highcharts-data-table th {
  font-weight: 600;
  padding: 0.5em;
}
.highcharts-data-table td,
.highcharts-data-table th,
.highcharts-data-table caption {
  padding: 0.5em;
}
.highcharts-data-table thead tr,
.highcharts-data-table tr:nth-child(even) {
  background: #f8f8f8;
}
.highcharts-data-table tr:hover {
  background: #f1f7ff;
}
/* Additional CSS here */
</style>
