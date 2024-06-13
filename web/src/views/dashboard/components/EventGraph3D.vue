<template>
  <div class="eventgraph3d-wrapper">
    <div id="graph"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed, watch } from "vue";
import ForceGraph3D from "3d-force-graph";
import * as THREE from "three"; // 引入THREE库
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer";
import SpriteText from "three-spritetext";
import { useStore } from "vuex";

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);
const date = ref("");

const fetchGraphData = async selectedDateValue => {
  if (selectedDateValue === "earlier") {
    date.value = "history";
  } else {
    date.value = selectedDateValue;
  }

  const graphContainer = document.getElementById("graph");
  const response = await fetch(`http://127.0.0.1:8000/fetch-graph?date=${date.value}`);
  const graphData = ref(null);
  const cache = {}; // 缓存对象
  if (cache[date.value]) {
    // 如果缓存中有数据，直接使用缓存数据
    graphData.value = cache[date.value];
  } else {
    graphData.value = await response.json();
    // 将数据存入缓存
    cache[date.value] = graphData.value;
  }
  if (graphContainer) {
    const Graph = ForceGraph3D({
      extraRenderers: [new CSS2DRenderer()]
    })(graphContainer)
      .backgroundColor("#000003")
      .graphData(graphData.value)
      .nodeAutoColorBy("group")
      .linkDirectionalArrowLength(3.5)
      .linkDirectionalArrowRelPos(1)
      .linkWidth(2)
      .linkColor(link => {
        const sourceNode = graphData.value.nodes.find(node => node.id === link.source);
        const targetNode = graphData.value.nodes.find(node => node.id === link.target);
        if (sourceNode.group === targetNode.group) {
          return sourceNode.color;
        } else {
          return "rgba(200, 200, 200, 0.5)";
        }
      })
      .linkThreeObjectExtend(true)
      .linkThreeObject(link => {
        const sprite = new SpriteText(`${link.description}`);
        sprite.color = "lightgrey";
        sprite.textHeight = 3;
        sprite.layers.enable(1); // 启用发光图层
        return sprite;
      })
      .linkPositionUpdate((sprite, { start, end }) => {
        const middlePos = Object.assign(
          ...["x", "y", "z"].map(c => ({
            [c]: start[c] + (end[c] - start[c]) / 2
          }))
        );
        Object.assign(sprite.position, middlePos);
      })
      .nodeThreeObject(node => {
        const nodeEl = document.createElement("div");
        nodeEl.textContent = node.id.split("-")[0];
        nodeEl.style.color = node.color;
        nodeEl.className = "node-label";
        return new CSS2DObject(nodeEl);
      })
      .onNodeClick(node => {
        // Aim at node from outside it
        const distance = 40;
        const distRatio = 1 - distance / Math.hypot(node.x, node.y, node.z);

        const newPos =
          node.x || node.y || node.z
            ? { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }
            : { x: 0, y: 0, z: -distance }; // special case if node is in (0,0,0)

        Graph.cameraPosition(
          newPos, // new position
          node, // lookAt ({ x, y, z })
          3000 // ms transition duration
        );
      })
      .nodeThreeObjectExtend(true);
    const bloomPass = new UnrealBloomPass();
    bloomPass.strength = 2;
    bloomPass.radius = 0.5;
    bloomPass.threshold = 0;

    // 设置Bloom只影响边（图层 1）
    const bloomLayer = new THREE.Layers();
    bloomLayer.set(1); // 图层 1 为边
    Graph.scene().traverse(object => {
      if (object instanceof THREE.Line) {
        // 确保只有边添加到图层 1
        object.layers.enable(1);
      }
    });
    bloomPass.layers = bloomLayer;

    Graph.postProcessingComposer().addPass(bloomPass);
  } else {
    console.error("Failed to find the container element for the 3D graph.");
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
  display: flex;
  align-items: center; /* Center the content vertically */
  justify-content: center; /* Center the content horizontally */
  width: 100%; /* Full width of the parent container */
  height: 100%; /* Full height of the parent container */
  padding: 20px;
  margin-top: 10px;
  overflow: hidden; /* Prevents any overflow from the 3D graph */
  background-color: #ffffff; /* White background */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 0 10px rgb(0 0 0 / 10%); /* Subtle shadow */
}
#graph {
  box-sizing: border-box; /* 包括边界和内边距在内的总宽度和高度 */
  width: 100%; /* Adjusted to 80% of its parent container */
  height: 100%; /* Height set to 600px for better visibility */
}
</style>
