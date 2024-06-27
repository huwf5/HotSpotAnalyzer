<template>
  <div class="eventgraph3d-wrapper">
    <div id="graph-3d"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, onBeforeUnmount } from "vue";
import ForceGraph3D from "3d-force-graph";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer";
import SpriteText from "three-spritetext";
import * as THREE from "three";
import graphData from "../components/graph_dict.json";

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

onMounted(() => {
  const graphContainer = document.getElementById("3d-graph");

  if (!graphContainer) {
    console.error("Failed to find the container element for the 3D graph.");
    return;
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
});

onBeforeUnmount(() => {
  if (Graph) {
    Graph._destructor();
    Graph = null;
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
#graph-3d {
  width: 80%; /* Adjusted to 80% of its parent container */
  height: 80%; /* Height set to 600px for better visibility */
  border: 10px solid #cccccc; /* Optional: adds a border around the graph area */
}
</style>
