<template>
  <div id="app1">
    <h1>文本标注系统</h1>
    <Annotation :data="data" />
  </div>
</template>

<script>
import Annotation from './FabricCanvas.vue'
import data from '../data/annotations'

export default {
  components: {
    Annotation,
  },
  data() {
    return {
      data, // 导入标注数据
    }
  },
}
</script>

<style>
#app1 {
  font-family: Arial, sans-serif;
  margin: 20px;
  text-align: center;
}
</style>
