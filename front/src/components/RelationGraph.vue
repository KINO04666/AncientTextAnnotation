<template>
  <div class="network-container">
    <!-- 网络图容器 -->
    <div ref="networkContainer" class="network-graph"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
<<<<<<< HEAD
import axios from 'axios'
import { Network } from 'vis-network/standalone'

// 定义网络图容器的引用
const networkContainer = ref(null)

// 定义函数以获取数据并渲染网络图
const fetchDataAndRender = async () => {
  try {
    const response = await axios.get('http://localhost:5000/get/26')
=======
import api from '@/axios/axios'
import { Network } from 'vis-network/standalone'
import { useRoute } from 'vue-router'
// 定义网络图容器的引用
const networkContainer = ref(null)
const route = useRoute()
const doc_id = ref(route.query.doc_id)
// 定义函数以获取数据并渲染网络图
const fetchDataAndRender = async () => {
  try {
    const response = await api.get(`/get/${doc_id.value}`)
>>>>>>> dev
    const data = response.data

    const nodes = data.entities.map((entity) => ({
      id: entity.id,
      label: entity.text || entity.label,
      color: {
        background: entity.color.background || '#97C2FC', // 默认颜色
        border: entity.color.border || '#2B7CE9',
      },
    }))

    const edges = data.relations.map((rel) => ({
      from: rel.from,
      to: rel.to,
      label: rel.type,
      arrows: 'to',
      color: rel.color.color || '#848484',
      font: {
        color: rel.color.color || '#848484',
        size: 14,
      },
      smooth: { type: 'dynamic' },
    }))

    const options = {
      nodes: {
        shape: 'ellipse',
        borderWidth: 2,
        size: 30,
        font: { color: '#333', size: 16 },
      },
      edges: {
        smooth: { type: 'dynamic' },
        arrows: { to: { enabled: true, scaleFactor: 1.2 } },
        font: { align: 'middle' },
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -200,
          springLength: 120,
          springConstant: 0.05,
        },
        stabilization: { iterations: 100 },
      },
      interaction: {
        dragNodes: true,
        zoomView: true,
      },
    }

    new Network(networkContainer.value, { nodes, edges }, options)
  } catch (error) {
    console.error('Error fetching or rendering data:', error)
<<<<<<< HEAD
    alert('无法获取文档数据，请检查服务器是否运行或 API 是否正确')
=======
    alert('没有获取到实体和关系数据，请添加实体和关系！')
>>>>>>> dev
  }
}

onMounted(() => {
  fetchDataAndRender()
})
</script>

<style scoped>
.network-container {
  height: 100%; /* 占满整个视口 */
  width: 100%;
}

.network-graph {
  height: 100%; /* 容器内的图表元素占满父容器 */
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fafafa;
}
</style>
