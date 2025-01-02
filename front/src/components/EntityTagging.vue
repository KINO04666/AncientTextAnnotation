<template>
<<<<<<< HEAD
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
=======
  <div class="main">
    <div class="left">
      <div class="left-top">
        <div class="title">
          <el-icon style="font-size: 26px"><Aim /></el-icon>
          <div class="title-text">实体标注</div>
          <el-button class="add-button" @click="openadd">
            <el-icon><CirclePlus /></el-icon>
            <span class="add-text">添加实体类</span>
          </el-button>
        </div>
        <el-scrollbar height="190px">
          <div
            v-for="(item, index) in data.enti"
            :key="index"
            class="scrollbar-item-1"
            :style="{ backgroundColor: item.color.background }"
          >
            <div class="item-content">
              <div class="data1">{{ item.label }}</div>
              <div class="data2">{{ item.number }}个实体</div>
              <div class="item-content-buttonlist">
                <el-button
                  class="item-content-button"
                  title="删除"
                  plain
                  @click="openDeleteDialog(index, item.label)"
                  ><el-icon><Delete /></el-icon
                ></el-button>
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>
      <div class="left-down">
        <div class="title">
          <el-icon style="font-size: 26px"><DataBoard /></el-icon>
          <div class="title-text">实体实例</div>
        </div>
        <el-scrollbar height="260px">
          <div v-for="(entity, index) in data.enti" :key="index">
            <h4>{{ entity.label }}</h4>
            <!-- 显示 label -->
            <p
              v-for="ent in filteredEntities(entity.label)"
              :key="ent.id"
              class="scrollbar-item-2"
              :style="{ backgroundColor: entity.color.background }"
            >
              {{ ent.label }}: {{ ent.text }}
              <!-- 显示筛选后的 text 和 label -->
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
            @click="handleButtonClick(index)"
          >
            <span class="entity-label">{{ entity.label }}</span>
            <div class="color-box" :style="{ backgroundColor: entity.color.background }"></div>
          </button>
          <button class="automatic" title="自动标注" @click="autoAnnotation">
            <el-icon><MagicStick /></el-icon>
          </button>
          <!-- 转圈动画 -->
          <div v-if="loading" class="spinner">
            <!-- 这是一个简单的加载动画示例 -->
            <div class="loader"></div>
          </div>
        </div>
      </div>
      <el-divider />
      <Annotation
        :data="data"
        :ClickId="ClickId"
        @update-entity="updateEntity"
        @update-ClickId="updateClickId"
        @request-delete="handleDeleteRequest"
        @update-data="updateData"
      />
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
import Annotation from './EntityTaggingText.vue'
import api from '@/axios/axios'

export default {
  components: {
    Annotation,
  },
  data() {
    return {
      loading: false, // 控制加载动画
      new_entity_id: -1,
      data: {
        enti: [],
        entities: [],
        relations: [],
        doc_name: '',
        doc_describe: '',
        doc_content: '',
        project_id: '',
      },
      user_id: Cookies.get('userId'),
      ClickId: -1, // 选中的按钮实体类型
      entityToDelete: null,
      docId: this.$route.query.doc_id, // 您需要根据实际情况获取 doc_id
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async autoAnnotation() {
      this.loading = true // 开始加载动画
      try {
        await api.post('/analyze_entity', {
          doc_id: this.docId,
          doc_content: this.data.doc_content,
          enti: this.data.enti,
        })
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false // 结束加载动画
      }
      this.fetchData()
    },
    async openDeleteDialog(index, label) {
      try {
        // 弹出确认框
        await this.$confirm(`确认删除实体类 "${label}" 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })

        // 如果用户点击了 "确定"，执行删除逻辑
        await api.delete('/delete_enti', {
          data: {
            doc_id: this.docId,
            label: label,
          },
        })

        // 刷新数据
        this.fetchData()

        // 显示成功消息
        this.$message.success('删除成功')
      } catch (error) {
        // 用户点击 "取消"，会抛出异常，此时可以忽略
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          this.$message.error('删除失败，请稍后重试！')
        } else {
          console.log('删除已取消')
        }
      }
    },

    async fetchData() {
      try {
        const response = await api.get(`/get/${this.docId}`)
        const data = response.data
        delete data.doc_create
        delete data.doc_modify
        this.data = data
        console.log(this.data)
      } catch (error) {
        console.error('获取数据失败:', error)
        this.$message({
          type: 'error',
          message: '获取数据失败，请稍后重试。',
        })
      }
    },
    // 删除标注的实体
    async handleDeleteRequest(DeleteId) {
      try {
        // 弹出确认对话框
        await this.$confirm('是否要删除此处以标注的实体', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })

        // 查找要删除的实体
        const entityIndex = this.data.entities.findIndex((entity) => entity.id === DeleteId)
        if (entityIndex === -1) {
          this.$message({
            type: 'error',
            message: '未找到要删除的实体。',
          })
          return
        }
        const entityToDelete = this.data.entities[entityIndex]
        const label = entityToDelete.label

        // 先在后端删除实体
        await api.post('/delete_entity', {
          doc_id: this.docId,
          entity_id: DeleteId,
        })

        // 从前端数据中移除实体
        this.data.entities.splice(entityIndex, 1)

        // 查找并更新实体类别的计数
        const entiIndex = this.data.enti.findIndex((entity) => entity.label === label)
        if (entiIndex !== -1) {
          this.data.enti[entiIndex].number -= 1

          // 更新实体类别计数到后端
          try {
            await api.put('/update_enti', {
              doc_id: this.docId,
              number: this.data.enti[entiIndex].number,
              label: label,
            })
          } catch (error) {
            console.error('更新实体类别计数失败:', error)
            this.$message({
              type: 'error',
              message: '更新实体类别计数失败，请稍后重试。',
            })
            // 根据需要，您可以选择在此处回滚前端的数据更改
          }
        } else {
          console.warn(`未找到标签为 "${label}" 的实体类别`)
        }

        // 从前端数据中移除与该实体相关的关系
        const originalRelationsLength = this.data.relations.length
        this.data.relations = this.data.relations.filter(
          (relation) => relation.from !== DeleteId && relation.to !== DeleteId,
        )
        const removedRelations = originalRelationsLength - this.data.relations.length
        if (removedRelations > 0) {
          this.$message({
            type: 'info',
            message: `删除成功! 移除了 ${removedRelations} 个相关关系实例。`,
          })
        } else {
          this.$message({
            type: 'success',
            message: '删除成功!',
          })
        }
      } catch (error) {
        if (error !== 'cancel' && error !== undefined) {
          // 根据 Element Plus 的实现，取消操作不会传递错误
          console.error('删除失败:', error)
          this.$message({
            type: 'error',
            message: '删除失败，请稍后重试。',
          })
        } else {
          this.$message({
            type: 'info',
            message: '已取消删除',
          })
        }
      }
    },
    // 修改实体
    async openchange(label) {
      try {
        const { value } = await this.$prompt('请输入新实体名称', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /.+/,
          inputErrorMessage: '输入不能为空',
        })

        // 更新本地数据
        this.data.enti.forEach((entity) => {
          if (entity.label === label) {
            entity.label = value
          }
        })
        this.data.entities.forEach((entity) => {
          if (entity.label === label) {
            entity.label = value
          }
        })

        // 同步到后端
        await api.post('/upload', {
          user_id: this.user_id,
          project_id: this.data.project_id,
          doc_id: this.docId,
          doc_name: this.data.doc_name,
          doc_describe: this.data.doc_describe,
          text: this.data.doc_content,
          entities: this.data.entities,
          relations: this.data.relations,
          enti: this.data.enti,
        })

        this.$message({
          type: 'success',
          message: '修改成功',
        })
      } catch (error) {
        if (error !== 'cancel') {
          console.error('修改实体失败:', error)
          this.$message({
            type: 'error',
            message: '修改实体失败，请稍后重试。',
          })
        } else {
          this.$message({
            type: 'info',
            message: '取消输入',
          })
        }
      }
    },
    // 添加实体
    async openadd() {
      try {
        const { value } = await this.$prompt('请输入实体名称', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /.+/,
          inputErrorMessage: '输入不能为空',
        })

        const Color = this.generateSimilarColors()
        const newEntity = {
          label: value,
          number: 0,
          color: { background: Color.lightColor, border: Color.darkColor, fill: Color.darkColor },
        }
        const e = []
        e.push(newEntity)
        // 更新本地数据
        this.data.enti.push(newEntity)
        // 同步到后端
        await api.post('/add_enti', {
          doc_id: this.docId,
          color: newEntity.color,
          label: newEntity.label,
        })

        this.$message({
          type: 'success',
          message: '添加成功',
        })
      } catch (error) {
        if (error !== 'cancel') {
          console.error('添加实体失败:', error)
          this.$message({
            type: 'error',
            message: '添加实体失败，请稍后重试。',
          })
        } else {
          this.$message({
            type: 'info',
            message: '取消输入',
          })
        }
      }
    },
    // 生成一浅一深的颜色
    generateSimilarColors() {
      // 生成随机颜色
      const randomColor = this.getRandomColor()

      // 将 HEX 颜色转换为 RGB
      const rgb = this.hexToRgb(randomColor)

      // 生成较深和较浅的颜色
      const darkColor = this.rgbToHex(
        Math.max(rgb.r - 50, 0),
        Math.max(rgb.g - 50, 0),
        Math.max(rgb.b - 50, 0),
      )
      const lightColor = this.rgbToHex(
        Math.min(rgb.r + 50, 255),
        Math.min(rgb.g + 50, 255),
        Math.min(rgb.b + 50, 255),
      )

      return {
        darkColor,
        lightColor,
      }
    },
    getRandomColor() {
      // 生成随机颜色
      const randomColor = Math.floor(Math.random() * 16777215).toString(16)
      return `#${randomColor.padStart(6, '0')}` // 确保是 6 位的 HEX 颜色
    },
    hexToRgb(hex) {
      const bigint = parseInt(hex.slice(1), 16)
      const r = (bigint >> 16) & 255
      const g = (bigint >> 8) & 255
      const b = bigint & 255

      return { r, g, b }
    },
    rgbToHex(r, g, b) {
      return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).padStart(6, '0')}`
    },
    // 更新 data
    async updateEntity(newData) {
      // 验证 newData 的结构
      if (!Array.isArray(newData) || newData.length === 0) {
        this.$message({
          type: 'error',
          message: '更新数据格式错误，请重试。',
        })
        return
      }

      try {
        // 发送 API 请求
        const response = await api.post('/upload', {
          user_id: this.user_id,
          project_id: this.data.project_id,
          doc_id: this.docId,
          doc_name: this.data.doc_name,
          doc_describe: this.data.doc_describe,
          text: this.data.doc_content,
          entities: newData,
        })

        if (response.data.status === 'success') {
          const data = response.data
          // 假设每个实体都有一个唯一的 entity_id
          newData.forEach((entity) => {
            entity.id = data.entity_id // 确保后端返回的 `entity_id` 是对应的
            this.data.entities.push(entity)
          })

          this.$message({
            type: 'success',
            message: '数据更新成功',
          })

          // 更新实体计数
          const label = newData[0].label
          const entityToUpdate = this.data.enti.find((entity) => entity.label === label)
          if (entityToUpdate) {
            entityToUpdate.number += newData.length

            // 使用 for...of 循环处理异步请求
            for (const entity of this.data.enti) {
              if (entity.label === label) {
                try {
                  await api.put('/update_enti', {
                    doc_id: this.docId,
                    number: entity.number,
                    label: label,
                  })
                } catch (error) {
                  console.error('更新实体计数失败:', error)
                  this.$message({
                    type: 'error',
                    message: '更新实体计数失败，请稍后重试。',
                  })
                }
              }
            }
          } else {
            console.warn(`未找到标签为 "${label}" 的实体`)
          }
        } else {
          throw new Error(response.data.message || '更新失败')
        }
      } catch (error) {
        console.error('更新数据失败:', error)
        this.$message({
          type: 'error',
          message: `更新数据失败: ${error.message || '请稍后重试。'}`,
        })
      }
    },

    // 重置按钮状态
    updateClickId(newClickId) {
      this.ClickId = newClickId
    },
    // 选择标注的实体类型
    handleButtonClick(index) {
      this.ClickId = index
    },
    // 根据提供的 label 筛选 entities
    filteredEntities(label) {
      return this.data.entities.filter((entity) => entity.label === label)
    },
  },
  // 生成背景色
  beforeCreate() {
    this.$nextTick(() => {
      document.body.setAttribute('style', 'background:#f3f6f7')
    })
  },
  // 实例销毁之前钩子--移除 body 标签的属性 style
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
>>>>>>> dev
  align-items: center;
  height: 30px;
  margin: 5px;
}

<<<<<<< HEAD
.title-text{
  margin-left: 10px;
  font-weight: bold; 
=======
.title-text {
  margin-left: 10px;
  font-weight: bold;
  white-space: nowrap;
>>>>>>> dev
}

.add-button {
  margin-left: 180px;
  border: none; /* 去掉边框 */
  background-color: #fff; /* 背景色 */
  color: #333; /* 文字颜色 */
  padding: 10px 15px; /* 内边距 */
  border-radius: 5px; /* 圆角 */
  cursor: pointer; /* 鼠标悬停时显示手指光标 */
<<<<<<< HEAD
  transition: background-color 0.3s, box-shadow 0.2s; /* 平滑过渡效果 */
=======
  transition:
    background-color 0.3s,
    box-shadow 0.2s; /* 平滑过渡效果 */
>>>>>>> dev
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

<<<<<<< HEAD
.left-down{
    background-color: white;
    margin-top: 30px;
    height: 350px;
    border-radius: 10px; 
=======
.left-down {
  background-color: white;
  margin-top: 30px;
  height: 350px;
  border-radius: 10px;
>>>>>>> dev
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
<<<<<<< HEAD
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
=======
  width: 380px;
}

.item-content {
  display: flex;
  width: 100%;
}

.data1 {
  width: 33%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.data2 {
  width: 33%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-content-buttonlist {
  margin-left: 50px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.item-content-button {
>>>>>>> dev
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

<<<<<<< HEAD
.right{
=======
.right {
>>>>>>> dev
  margin-top: 20px;
  margin-left: 50px;
  width: 1500px;
  background-color: white;
  display: flex;
  flex-direction: column;
<<<<<<< HEAD
  border-radius: 10px; 
}

.toolbar{
=======
  border-radius: 10px;
}

.toolbar {
>>>>>>> dev
  display: flex;
  align-items: center;
  margin-top: 10px;
  width: 200px;
  height: 40px;
}

<<<<<<< HEAD
.tool-button-list{
=======
.tool-button-list {
>>>>>>> dev
  margin-left: 25px;
  display: flex;
}

<<<<<<< HEAD
.tool-button{
=======
.tool-button {
>>>>>>> dev
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
<<<<<<< HEAD
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
=======
  border-radius: 10px;
}

.automatic {
  width: 30px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border: none;
  background: none;
  margin-left: 20px;
  border-radius: 50px; /* 圆角，使按钮呈现为圆框 */
  cursor: pointer; /* 鼠标悬停时显示为手指形状 */
}

.automatic:hover {
  background-color: black; /* 悬停时的背景色 */
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
}

.entity-label {
  font-size: 20px;
}

.color-box {
  width: 25px;
  height: 25px;
  border-radius: 10px;
}
.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.loader {
  border: 4px solid #f3f3f3; /* 边框颜色 */
  border-top: 4px solid #3498db; /* 动画的颜色 */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
>>>>>>> dev
