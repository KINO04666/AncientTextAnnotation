<template>
  <Menu />
  <div class="main">
    <div class="left">
      <div class="left-top">
        <div class="title">
          <el-icon style="font-size: 26px"><Aim /></el-icon>
          <div class="title-text">关系标注</div>
          <button class="add-button">
            <el-icon><CirclePlus /></el-icon>
            <span class="add-text">添加关系类</span>
          </button>
        </div>
        <el-scrollbar height="190px">
          <div v-for="item in 20" :key="item" class="scrollbar-item-1">
            <div class="item-content">
              <div class="data1">数据 1 - {{ item }}</div>
              <div class="data2">数据 2 - {{ item }}</div>
              <div class="data3">数据 3 - {{ item }}</div>
            </div>
          </div>
        </el-scrollbar>
      </div>
      <div class="left-down">
        <div class="title">
          <el-icon style="font-size: 26px"><DataBoard /></el-icon>
          <div class="title-text">关系实例</div>
          <button class="add-button"></button>
        </div>
        <span class="instance-kind">人</span>
        <el-scrollbar height="260px">
          <p v-for="item in 20" :key="item" class="scrollbar-item-2">{{ item }}</p>
        </el-scrollbar>
      </div>
    </div>
    <div class="right">
      <div class="toolbar"></div>
      <el-divider />
      <Annotation :data="data" />
    </div>
  </div>
</template>

<script>
import Annotation from './EntityTaggingText.vue'
import data from '../data/annotations'
import Menu from './Menu.vue'
export default {
  components: {
    Annotation,
    Menu,
  },
  data() {
    return {
      data, // 导入标注数据
    }
  },
  methods: {
    navigateToRelationAnnotation() {
      this.$router.push({ name: 'RelationshipAnnotation' }) // 跳转到指定名称的路由
    },
  },
  beforeCreate() {
    this.$nextTick(() => {
      document.body.setAttribute('style', 'background:#f3f6f7')
    })
  },
  //实例销毁之前钩子--移除body 标签的属性style
  beforeUnmount() {
    document.body.removeAttribute('style')
  },
}
</script>

<style scoped>
.main {
  display: flex;
}

.left {
  display: flex; /* 使用 Flexbox 布局 */
  flex-direction: column;
}

.left-top {
  margin-top: 20px;
  background-color: white;
  height: 240px;
  width: 400px;
  border-radius: 10px;
}

.title {
  display: flex;
  align-items: center;
  height: 30px;
  margin: 5px;
}

.title-text {
  margin-left: 10px;
  font-weight: bold;
}

.add-button {
  margin-left: 180px;
  border: none; /* 去掉边框 */
  background-color: #fff; /* 背景色 */
  color: #333; /* 文字颜色 */
  padding: 10px 15px; /* 内边距 */
  border-radius: 5px; /* 圆角 */
  cursor: pointer; /* 鼠标悬停时显示手指光标 */
  transition:
    background-color 0.3s,
    box-shadow 0.2s; /* 平滑过渡效果 */
}

.add-button:hover {
  background-color: #f0f0f0; /* 鼠标悬停时背景色 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 鼠标悬停时添加阴影 */
}

.add-button:active {
  background-color: #e0e0e0; /* 按下时背景色 */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3); /* 按下时的内阴影 */
  transform: translateY(2px); /* 按下时稍微下移 */
}

.left-down {
  background-color: white;
  margin-top: 30px;
  height: 350px;
  border-radius: 10px;
}

.scrollbar-item-1 {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.item-content {
  display: flex;
}

.data2 {
  margin-left: 80px;
}

.data3 {
  margin-left: 40px;
}

.scrollbar-item-2 {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.right {
  margin-top: 20px;
  margin-left: 50px;
  width: 1500px;
  background-color: white;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
}

.toolbar {
  display: flex;
  align-items: center;
  margin-top: 10px;
  width: 200px;
}
</style>
