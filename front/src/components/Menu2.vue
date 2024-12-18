<template>
  <div class="layout">
    <div class="menu">
      <div class="logo">
        <img src="../pictures/logo.png" alt="Logo" class="logo-image" />
        <span class="logo-text">浙江工商大学古籍标注平台</span>
      </div>
      <ul class="button-list">
        <li>
          <router-link to="/" class="button">
            <el-icon><Operation /></el-icon>
            <span class="button-text">结构标注</span>
          </router-link>
        </li>
        <li>
          <router-link to="/entitytagging" class="button">
            <el-icon><Aim /></el-icon>
            <span class="button-text">实体标注</span>
          </router-link>
        </li>
        <li>
          <router-link to="/relationshipannotation" class="button">
            <el-icon><Rank /></el-icon>
            <span class="button-text">关系标注</span>
          </router-link>
        </li>
        <li>
          <router-link to="/map" class="button">
            <el-icon><Film /></el-icon>
            <span class="button-text">知识图谱</span>
          </router-link>
        </li>
        <li>
          <router-link to="/" class="button">
            <el-icon><ArrowRightBold /></el-icon>
            <span class="button-text">导出数据</span>
          </router-link>
        </li>
      </ul>
      <div class="exit">
        <button class="tobutton" title="个人信息">
          <el-icon style="font-size: 24px"><User /></el-icon>
        </button>
        <button class="tobutton" title="返回项目">
          <el-icon style="font-size: 24px"><Folder /></el-icon>
        </button>
        <button class="tobutton" title="退出">
          <el-icon style="font-size: 24px"><Right /></el-icon>
        </button>
      </div>
    </div>
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden; /* 防止内容溢出滚动 */
}
.menu {
  display: flex; /* 使用 Flexbox 布局 */
  height: 70px;
  align-items: center; /* 垂直居中对齐 */
  background-color: white; /* 背景色 */
}
.logo {
  display: flex;
  align-items: center;
}

.logo-image {
  left: 0%;
  height: 40px;
  margin-right: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.button-list {
  display: flex; /* 使用 Flexbox 布局 */
  width: 700px;
  margin-left: 100px;
  justify-content: space-around; /* 元素之间均匀分布 */
  align-items: center; /* 垂直居中对齐 */
  list-style-type: none; /* 去掉列表项的项目符号 */
}

.button {
  display: flex; /* 使用 Flexbox 布局 */
  align-items: center; /* 垂直居中对齐 */
  padding: 10px 15px; /* 内边距 */
  background-color: #fff; /* 背景颜色为白色 */
  color: #000;
  border-radius: 50px; /* 圆角，使按钮呈现为圆框 */
  cursor: pointer; /* 鼠标悬停时显示为手指形状 */
  transition:
    background-color 0.3s,
    color 0.3s; /* 添加过渡效果 */
  text-decoration: none; /* 去掉默认的下划线 */
  outline: none; /* 去掉焦点轮廓 */
}

.button:hover {
  background-color: black; /* 悬停时的背景色 */
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
}

.button:active {
  background-color: #1c598a; /* 按下时的背景色 */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3); /* 内阴影效果 */
  transform: translateY(2px); /* 按下时稍微下移 */
}

.exit {
  display: flex; /* 使用 Flexbox 布局 */
  align-items: center; /* 垂直居中对齐 */
  width: 300px;
  margin-left: 100px;
  justify-content: space-around; /* 元素之间均匀分布 */
}

.tobutton {
  display: flex; /* 使用 Flexbox 使图标居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  width: 50px; /* 设置按钮宽度 */
  height: 50px; /* 设置按钮高度 */
  border: none; /* 去掉边框 */
  border-radius: 50%; /* 使按钮成为圆形 */
  background-color: #f3f6f7; /* 背景色 */
  color: black; /* 图标颜色 */
  cursor: pointer; /* 鼠标悬停时显示手指光标 */
  transition:
    background-color 0.3s,
    box-shadow 0.2s; /* 添加过渡效果 */
}

.tobutton:hover {
  background-color: black; /* 悬停时的背景色 */
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
}

.tobutton:active {
  background-color: #1c598a; /* 按下时的背景色 */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3); /* 内阴影效果 */
  transform: translateY(2px); /* 按下时稍微下移 */
}
.content {
  flex: 1; /* 占据剩余空间 */
  overflow: auto; /* 如果子路由内容过多，内部区域滚动 */
  background-color: #f9f9f9;
}
</style>
