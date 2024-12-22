<template>
  <div class="layout-container">
    <!-- 左半部分：地图 -->
    <div class="map-container">
      <div id="container"></div>
    </div>

    <!-- 右半部分：网络关系图 -->
    <div class="network-panel">
      <RelationGraph />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import axios from 'axios'
import RelationGraph from './RelationGraph.vue' // 引入网络关系图组件
import { useRoute } from 'vue-router'
import { ref } from 'vue'
let map = null
let markers = []
const route = useRoute()
// 获取地点经纬度并标注
const getLocationData = async (placeName) => {
  try {
    // 使用地点名称调用后端接口获取经纬度
    const response = await axios.post(
      '/gateway/gateway/geom-name/placename-object/home/placename',
      {
        limit: 3,
        name: placeName,
        page: 0,
        type: '',
      },
    )

    const records = response.data.datas.records
    if (records.length > 0) {
      // 遍历所有的 records，标注每一个地点
      records.forEach((record) => {
        const x = parseFloat(record?.spatial?.xcoord) // 经度
        const y = parseFloat(record?.spatial?.ycoord) // 纬度
        const realname = record?.spellings[2]?.writtenForm || '未命名'
        if (!isNaN(x) && !isNaN(y)) {
          const marker = new AMap.Marker({
            position: new AMap.LngLat(x, y),
            title: realname,
            icon: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
            anchor: 'bottom-center',
            offset: new AMap.Pixel(0, -10),
          })
          map.add(marker)
          markers.push(marker)
        }
      })
      if (markers.length > 0) {
        map.setFitView(markers) // 确保所有标注都显示在视图内
      }
    }
  } catch (error) {
    console.error(`获取地点 ${placeName} 经纬度失败:`, error)
  }
}

// 更新地图，获取地点信息并标注
const updateMap = (entities) => {
  // 清除已有标注
  if (markers.length > 0) {
    map.remove(markers)
    markers = []
  }

  // 遍历所有实体，筛选出 label 为 "地点" 的实体
  const locationEntities = entities.filter((ent) => ent.label === '地点')

  // 对每个地点名称进行接口请求
  locationEntities.forEach((entity) => {
    const placeName = entity.text
    getLocationData(placeName) // 获取经纬度并标注
  })
}

onMounted(() => {
  window._AMapSecurityConfig = {
    securityJsCode: '10be78e31e3ec6925dcd033c2a3dd25a',
  }

  AMapLoader.load({
    key: 'f43b5453e7738f22c4ecd6cd8914dbf7',
    version: '2.0',
    plugins: ['AMap.TileLayer.Satellite'],
  })
    .then((AMap) => {
      map = new AMap.Map('container', {
        zoom: 8,
        center: [116.397428, 39.90923], // 默认中心点
        viewMode: '3D',
        features: [],
      })

      const terrainLayer = new AMap.TileLayer.Satellite({ zIndex: 0 })
      map.add(terrainLayer)
      const doc_id = ref(route.query.doc_id)
      // 假设从后端获取到 entities 数据
      axios
        .get(`http://127.0.0.1:5000/get/${doc_id.value}`) // 假设获取文档ID为26的数据
        .then((response) => {
          const entities = response.data.entities // 获取 entities 数据
          updateMap(entities) // 更新地图
        })
        .catch((error) => {
          console.error('获取实体数据失败:', error)
        })
    })
    .catch((e) => console.error('地图加载失败:', e))
})

onUnmounted(() => {
  if (map) {
    map.destroy()
  }
})
</script>

<style scoped>
.layout-container {
  height: 100%;
  width: 100%;
  display: flex;
  background-color: #fff;
}

/* 左侧：地图区域 */
.map-container {
  flex: 1;
  display: flex;
  padding: 10px;
  box-sizing: border-box;
}

#container {
  flex: 1;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  border: 1px solid #ddd;
}

/* 右侧：网络关系图区域 */
.network-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  padding: 10px;
  box-sizing: border-box;
  border-left: 1px solid #ddd;
}
</style>
