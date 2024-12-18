<template>
    <Menu />
    <div class="main">
        <div class="left">
            <div class="left-top">
              <div class="title">
                <el-icon style="font-size: 26px;"><Aim /></el-icon>
                <div class="title-text">实体标注</div>
                <el-button class="add-button" type="link" @click="openadd">
                  <el-icon><CirclePlus /></el-icon>
                  <span class="add-text">添加实体类</span>
                </el-button>
              </div>
                <el-scrollbar height="190px">
                  <div v-for="(item, index) in data.enti" :key="index" class="scrollbar-item-1" :style="{ backgroundColor: item.color.background }">
                    <div class="item-content">
                      <div class="data1">{{ item.label }}</div>
                      <div class="data2">{{ item.number }}个实体</div>
                      <div class="item-content-buttonlist">
                        <button class="item-content-button" title="编辑"><el-icon><Edit /></el-icon></button>
                        <el-button class="item-content-button" title="删除" plain @click="openDeleteDialog(index,item.label)"><el-icon><Delete /></el-icon></el-button>
                      </div>
                    </div>
                  </div>
                </el-scrollbar>
            </div>
            <div class="left-down">
              <div class="title">
                <el-icon style="font-size: 26px;"><DataBoard /></el-icon>
                <div class="title-text">实体实例</div>
              </div>
                <el-scrollbar height="260px">
                  <div v-for="(entity, index) in data.enti" :key="index">
                    <h4>{{ entity.label }}</h4> <!-- 显示 label -->
                    <p v-for="ent in filteredEntities(entity.label)" :key="ent.id" class="scrollbar-item-2" :style="{ backgroundColor: entity.color.background }">
                    {{ ent.label }}: {{ ent.text }} <!-- 显示筛选后的 text 和 label -->
                    </p>
                   </div>
                </el-scrollbar>
            </div>
        </div>
        <div class="right">
          <div class="toolbar">
            <div class="tool-button-list">
              <button
                v-for="(entity, index) in data.enti"
                :key="entity.label"
                class="tool-button"
                :disabled="entity.disabled"
                @click="handleButtonClick(index)">
                  <span class="entity-label">{{ entity.label }}</span>
                  <div class="color-box" :style="{ backgroundColor: entity.color.background }"></div>
              </button>
            </div>
          </div>
          <el-divider />
          <Annotation :data="data" @update-data="updateData" />
        </div>
    </div>
</template>

<script>
import Annotation from "./EntityTaggingText.vue";
import data from "../data/annotations";
import Menu from "./Menu.vue"
export default{
  components: {
    Annotation,
    Menu,
  },
  data(){
    return {
      data,
    };
  },
  methods:{
    generateSimilarColors() {
    // 生成随机颜色
    const randomColor = this.getRandomColor();
    
    // 将 HEX 颜色转换为 RGB
    const rgb = this.hexToRgb(randomColor);
    
    // 生成较深和较浅的颜色
    const darkColor = this.rgbToHex(
      Math.max(rgb.r - 50, 0),
      Math.max(rgb.g - 50, 0),
      Math.max(rgb.b - 50, 0)
    );
    const lightColor = this.rgbToHex(
      Math.min(rgb.r + 50, 255),
      Math.min(rgb.g + 50, 255),
      Math.min(rgb.b + 50, 255)
    );

    return {
      darkColor,
      lightColor
    };
  },

  getRandomColor() {
    // 生成随机颜色
    const randomColor = Math.floor(Math.random() * 16777215).toString(16);
    return `#${randomColor.padStart(6, '0')}`; // 确保是 6 位的 HEX 颜色
  },

  hexToRgb(hex) {
    const bigint = parseInt(hex.slice(1), 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;

    return { r, g, b };
  },

  rgbToHex(r, g, b) {
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).padStart(6, '0')}`;
  },
    openadd() {
        this.$prompt('请输入邮箱', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /.+/,
          inputErrorMessage: '输入不能为空'
        }).then(({value}) => {
          const Color = this.generateSimilarColors();
          this.data.enti.push({
            label: value, number: 0,disabled: false,color: { background: Color.lightColor, border: Color.darkColor ,fill: Color.darkColor}
            }),
          this.$message({
            type: 'success',
            message: '添加成功',
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });       
        });
      },
    openDeleteDialog(index,label) {
        this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.data.enti.splice(index,1)
           // 删除 entities 中与 label 相等的项
          this.data.entities = this.data.entities.filter(entity => entity.label !== label);
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
      },
    updateData(newData) {
      // 根据需要更新数据
      this.data = newData; // 更新父组件的数据
    },
    handleButtonClick(index) {
      // 恢复其他按钮的状态
      this.data.enti.forEach((entity, i) => {
        if(i != index)
        entity.disabled = false;
      });
      // 设置当前按钮为禁用状态
      this.data.enti[index].disabled = true;
    },
    filteredEntities(label) {
      // 根据提供的 label 筛选 entities
      return this.data.entities.filter(entity => entity.label === label);
    },
    navigateToRelationAnnotation() {
      this.$router.push({ name: 'RelationshipAnnotation' }); // 跳转到指定名称的路由
    },
  },
  beforeCreate () {
    this.$nextTick(()=>{
      document.body.setAttribute('style', 'background:#f3f6f7')
    })
  },
  //实例销毁之前钩子--移除body 标签的属性style
  beforeDestroy () {
    document.body.removeAttribute('style')
  }
}
</script>


<style scoped>
.main{
  display: flex; 
}

.left{
    display: flex; /* 使用 Flexbox 布局 */
    flex-direction: column;
}

.left-top{
    margin-top: 20px;
    background-color: white;
    height: 240px;
    width: 400px;
    border-radius: 10px; 
}

.title{
  display: flex; 
  align-items: center;
  height: 30px;
  margin: 5px;
}

.title-text{
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
  transition: background-color 0.3s, box-shadow 0.2s; /* 平滑过渡效果 */
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

.left-down{
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
  color: black;
}


.item-content{
  display: flex;
}

.data2{
  margin-left: 80px;
}

.item-content-buttonlist{
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 80px;
  margin-left: 70px;
}

.item-content-button{
  background-color: transparent;
  cursor: pointer;
  border: none;
}

.item-content-button:hover {
  color: #0056b3; /* 悬停时的文本颜色 */
  background: none;
}

.scrollbar-item-2 {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  color: black;
}

.right{
  margin-top: 20px;
  margin-left: 50px;
  width: 1500px;
  background-color: white;
  display: flex;
  flex-direction: column;
  border-radius: 10px; 
}

.toolbar{
  display: flex;
  align-items: center;
  margin-top: 10px;
  width: 200px;
  height: 40px;
}

.tool-button-list{
  margin-left: 25px;
  display: flex;
}

.tool-button{
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 120px;
  border: none;
  background: none;
}

.tool-button:hover {
  background-color: #f0f0f0; /* 悬停时背景色变化 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 悬停时阴影效果 */
  border-radius: 10px; 
}

.tool-button:disabled{
  background-color: #f0f0f0; /* 悬停时背景色变化 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 悬停时阴影效果 */
  border-radius: 10px; 
}

.entity-label{
  font-size: 20px;
}

.color-box{
  width: 25px;
  height: 25px;
  border-radius: 10px; 
}

</style>