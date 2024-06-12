<template>
  <div class="eventgraph3d-wrapper">
    <div id="3d-graph"></div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from "vue";
import ForceGraph3D from "3d-force-graph";
import * as THREE from "three"; // 引入THREE库
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer";
import SpriteText from "three-spritetext";
import graphData from "../../views/dashboard/components/graph_dict.json";

// import { FontLoader } from "three/examples/jsm/loaders/FontLoader.js";
// import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry.js";
onMounted(() => {
  const graphContainer = document.getElementById("3d-graph");
  if (graphContainer) {
    const Graph = ForceGraph3D({
      extraRenderers: [new CSS2DRenderer()]
    })(graphContainer)
      .backgroundColor("#000003")
      .graphData(graphData)
      .nodeAutoColorBy("group")
      .linkDirectionalArrowLength(3.5)
      .linkDirectionalArrowRelPos(1)
      .linkWidth(2)
      .linkColor(link => {
        const sourceNode = graphData.nodes.find(node => node.id === link.source)!;
        const targetNode = graphData.nodes.find(node => node.id === link.target)!;
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
        // Focus on node
        Graph.cameraPosition(
          { x: node.x, y: node.y, z: node.z * 1.5 }, // new position
          node, // lookAt ({ x, y, z })
          1000 // ms transition duration
        );
      })
      .nodeThreeObjectExtend(true);

    // const loader = new FontLoader();
    // loader.load("fonts/helvetiker_regular.typeface.json", function (font) {
    //   const textGeometry = new TextGeometry("情感分析概览", {
    //     font: font,
    //     size: 8,
    //     height: 0.5
    //   });

    //   const textMaterial = new THREE.MeshBasicMaterial({ color: 0x007bff });
    //   const textMesh = new THREE.Mesh(textGeometry, textMaterial);

    //   // Position the text in the scene
    //   textMesh.position.set(-30, 50, 0);
    //   Graph.scene().add(textMesh);
    // });

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
#3d-graph {
  width: 80%; /* Adjusted to 80% of its parent container */
  height: 80%; /* Height set to 600px for better visibility */
  border: 10px solid #cccccc; /* Optional: adds a border around the graph area */
}
</style>
