<template>
<<<<<<< HEAD
  <div id="app1">
=======
  <div id="app">
>>>>>>> origin/dev
    <h1>文本标注系统</h1>
    <Annotation :data="data" />
  </div>
</template>

<script>
<<<<<<< HEAD
import Annotation from './FabricCanvas.vue'
import data from '../data/annotations'
=======
import Annotation from "./FabricCanvas.vue";
import data from "../data/annotations";
>>>>>>> origin/dev

export default {
  components: {
    Annotation,
  },
  data() {
    return {
      data, // 导入标注数据
<<<<<<< HEAD
    }
  },
}
</script>

<style>
#app1 {
=======
    };
  },
};
</script>

<style>
#app {
>>>>>>> origin/dev
  font-family: Arial, sans-serif;
  margin: 20px;
  text-align: center;
}
</style>
