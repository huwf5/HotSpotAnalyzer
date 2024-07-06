<template>
  <div class="eventgraph3d-wrapper">
    <div id="graph-3d"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, onBeforeUnmount, computed, watch, ref } from "vue";
import ForceGraph3D from "3d-force-graph";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer";
import SpriteText from "three-spritetext";
import * as THREE from "three";
import { getGraph3D } from "@/api/modules/event_analysis";
import DefaultGraphData from "../components/history.json";

// import axios from "axios";
import { useStore } from "vuex";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);
const graphContainer = ref<HTMLElement | null>(null);

declare module "three-spritetext" {
  interface SpriteText extends THREE.Object3D {}
}

interface Coords {
  x: number;
  y: number;
  z: number;
}

interface Node extends Coords {
  id: string;
  group: number;
  color: string;
}

let Graph: ReturnType<typeof ForceGraph3D> | null = null;

// 创建对象池
const spriteTextPool: SpriteText[] = [];
const css2DObjectPool: CSS2DObject[] = [];

function getSpriteText(text: string, color: string = "lightgrey", textHeight: number = 3): SpriteText {
  const sprite = spriteTextPool.length > 0 ? spriteTextPool.pop()! : new SpriteText();
  sprite.text = text;
  sprite.color = color;
  sprite.textHeight = textHeight;
  (sprite as THREE.Object3D).layers.enable(1);
  return sprite;
}

function getCSS2DObject(node: Node): CSS2DObject {
  const nodeEl = document.createElement("div");
  nodeEl.textContent = node.id.split("-")[0];
  nodeEl.style.color = node.color;
  nodeEl.className = "node-label";
  const obj = css2DObjectPool.length > 0 ? css2DObjectPool.pop()! : new CSS2DObject(nodeEl);
  obj.element = nodeEl;
  return obj;
}

const fetchGraphData = async (selectedDateValue: string) => {
  const date = selectedDateValue === "earlier" ? "history" : selectedDateValue;

  try {
    const response = await getGraph3D(date);

    const graphData = response ? response : DefaultGraphData;
    initializeGraph(graphData);
  } catch (error) {
    //console.error("Failed to fetch graph data from server, using default data", error);
    initializeGraph(DefaultGraphData); // Fallback to default data on any error
  }
};

const initializeGraph = graphData => {
  const graphContainer = document.getElementById("graph-3d");
  if (!graphContainer) {
    console.error("Failed to find the container element for the 3D graph.");
    return;
  }

  if (Graph) {
    Graph._destructor(); // 清除当前图形
  }

  Graph = ForceGraph3D({
    extraRenderers: [new CSS2DRenderer()]
  })(graphContainer)
    .backgroundColor("#000003")
    .graphData(graphData)
    .nodeAutoColorBy("group")
    .linkDirectionalArrowLength(3.5)
    .linkDirectionalArrowRelPos(1)
    .linkWidth(2)
    .linkColor(link => {
      const sourceNode = graphData.nodes.find(node => node.id === link.source) as Node;
      const targetNode = graphData.nodes.find(node => node.id === link.target) as Node;
      return sourceNode && targetNode && sourceNode.group === targetNode.group ? sourceNode.color : "rgba(200, 200, 200, 0.5)";
    })
    .linkThreeObjectExtend(true)
    .linkThreeObject(link => {
      const sprite = getSpriteText(`${link.description}`);
      return sprite;
    })
    .linkPositionUpdate((sprite, { start, end }: { start: Coords; end: Coords }) => {
      const middlePos = {
        x: (start.x + end.x) / 2,
        y: (start.y + end.y) / 2,
        z: (start.z + end.z) / 2
      };
      Object.assign(sprite.position, middlePos);
    })
    .nodeThreeObject(node => getCSS2DObject(node))
    .onNodeClick((node: object) => {
      const actualNode = node as Node;
      Graph!.cameraPosition({ x: actualNode.x, y: actualNode.y, z: actualNode.z * 1.5 }, actualNode, 1000);
    })
    .nodeThreeObjectExtend(true);

  const bloomPass = new UnrealBloomPass();
  bloomPass.strength = 2;
  bloomPass.radius = 0.5;
  bloomPass.threshold = 0;

  const bloomLayer = new THREE.Layers();
  bloomLayer.set(1);
  Graph.scene().traverse(object => {
    if (object instanceof THREE.Line) {
      object.layers.enable(1);
    }
  });
  bloomPass.layers = bloomLayer;

  Graph.postProcessingComposer().addPass(bloomPass);
};

const handleResize = () => {
  if (Graph && graphContainer.value) {
    Graph.width(graphContainer.value.clientWidth).height(graphContainer.value.clientHeight);
    Graph.refresh();
  }
};

watch(
  selectedDate,
  newDate => {
    fetchGraphData(newDate);
  },
  { immediate: true }
);

onMounted(() => {
  fetchGraphData(selectedDate.value);
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  if (Graph) {
    Graph._destructor();
    Graph = null;
  }
  const graphContainer = document.getElementById("graph-3d");
  if (graphContainer) {
    graphContainer.innerHTML = ""; // 清空容器中的内容
  }
});
</script>
<style>
.node-label {
  z-index: 10;
  display: inline-block;
  max-width: 100px;
  padding: 2px 4px;
  font-size: 12px;
  color: white;
  text-overflow: ellipsis;
  overflow-wrap: break-word;
  white-space: nowrap;
  user-select: none;
  background-color: rgb(0 0 0 / 80%);
  border-radius: 4px;
}
.eventgraph3d-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  margin-top: 10px;
  overflow: hidden;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgb(0 0 0 / 10%);
}

/* .eventgraph3d-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;

  position: relative;
  height: 100%;
  padding: 20px;
  margin-top: 10px;
  overflow: hidden;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgb(0 0 0 / 10%);
} */
#graph-3d {
  width: 100%; /* Adjusted to 80% of its parent container */
  height: 100%; /* Height set to 600px for better visibility */
  padding: 0;
  margin: 0;
}
</style>
