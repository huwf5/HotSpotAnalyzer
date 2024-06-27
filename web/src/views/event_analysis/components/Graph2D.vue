<template>
  <v-chart class="chart" ref="chart" :option="graphOption" autoresize />
</template>

<script setup lang="ts">
import { use } from "echarts/core";
import { GraphChart } from "echarts/charts";
import { GridComponent } from "echarts/components";
import VChart from "vue-echarts";
import { ref, watch } from "vue";
import { ECharts } from "echarts";

use([GraphChart, GridComponent]);

const chart = ref<ECharts>();

interface GraphData {
  nodes: {
    id: number;
    name: string;
    attributes: {
      type: string;
      value: string;
    }[];
  }[];
  links: {
    source: number;
    target: number;
    type: string;
  }[];
}

const props = defineProps<{
  data: GraphData;
}>();

function process_data() {
  let category = 0;
  let event_map = new Map<number, number>();
  for (let index = 0; index < props.data.nodes.length; index++) {
    event_map.set(props.data.nodes[index].id, index);
  }
  let nodes = props.data.nodes.map(item => {
    return { ...item, category: category++ };
  });
  let links = props.data.links.map(link => {
    return {
      source: event_map.get(link.source)!,
      target: event_map.get(link.target)!,
      type: link.type,
      label: {
        show: true,
        formatter: (params: { data: { type: string } }) => params.data.type
      }
    };
  });
  let categories = props.data.nodes.map(node => {
    return { name: node.name };
  });
  let legends = categories.map(item => item.name);
  console.log(links);
  graphOption.value.series[0].data = nodes;
  graphOption.value.series[0].links = links;
  graphOption.value.series[0].categories = categories;
  graphOption.value.legend[0].data = legends;
}

function breakDownStr(input: string, stopStr = "<br />", tooltipTextLength = 14) {
  let processed_str = "";
  let len = input.length;
  for (let index = 0; index < len; index += tooltipTextLength) {
    processed_str += input.substring(index, Math.min(index + tooltipTextLength, len)) + stopStr;
  }
  return processed_str;
}

const graphOption = ref({
  tooltip: {},
  legend: [
    {
      data: [] as string[]
    }
  ],
  series: [
    {
      name: "关系图",
      type: "graph",
      layout: "force",
      data: props.data.nodes,
      links: props.data.links,
      categories: [] as { name: string }[],
      // roam: true,
      draggable: true,
      label: {
        show: true,
        position: "top",
        formatter: (params: { data: { name: string } }) => breakDownStr(params.data.name, "\n", 20)
      },
      labelLayout: {
        hideOverlap: true
      },
      edgeSymbol: ["none", "arrow"],
      tooltip: {
        formatter: (params: {
          data: {
            type?: string;
            name?: string;
            attributes?: {
              type: string;
              value: string;
            }[];
          };
        }) => {
          if (params.data.type) return params.data.type;
          else if (params.data.attributes && params.data.attributes.length > 0) {
            let result = {};
            let ret = breakDownStr(params.data.name!);
            for (const attr of Object.values(params.data.attributes)) {
              if (result[attr.type]) {
                result[attr.type] = result[attr.type] + " " + attr.value;
              } else {
                result[attr.type] = attr.value;
              }
            }
            for (const entry of Object.entries(result)) {
              ret += breakDownStr(entry[0] + "：" + (entry[1] as string));
            }
            return ret;
          } else return "";
        }
      },
      force: {
        repulsion: 100,
        edgeLength: 100
      }
    }
  ]
});

watch(() => props.data, process_data);
</script>

<style scoped lang="scss">
.chart {
  width: 100%;
  height: 500px;
}
</style>
