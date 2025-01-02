<template>
<<<<<<< HEAD
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
=======
  <div class="main">
    <div class="left">
      <!-- 关系类型列表 -->
      <div class="left-top">
        <div class="title">
          <el-icon style="font-size: 26px"><Rank /></el-icon>
          <div class="title-text">关系标注</div>
          <el-button class="add-button" @click="openAddRelationKindDialog">
            <el-icon><CirclePlus /></el-icon>
            <span class="add-text">添加关系类</span>
          </el-button>
        </div>
        <!-- 添加关系类对话框 -->
        <el-dialog title="添加关系类" v-model="dialogFormVisible">
          <el-form :model="newrelation">
            <el-form-item label="源实体" :label-width="formLabelWidth">
              <el-select
                v-model="newrelation.start_label"
                placeholder="请选择源实体"
                :loading="loading"
              >
                <el-option
                  v-for="(item, index) in data.enti"
                  :key="index"
                  :label="item.label"
                  :value="item.label"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="关系" :label-width="formLabelWidth">
              <el-input v-model="newrelation.type" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="目标实体" :label-width="formLabelWidth">
              <el-select
                v-model="newrelation.end_label"
                placeholder="请选择目标实体"
                :loading="loading"
              >
                <el-option
                  v-for="(item, index) in data.enti"
                  :key="index"
                  :label="item.label"
                  :value="item.label"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <template v-slot:footer>
            <div class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="addRelationKind">确 定</el-button>
            </div>
          </template>
        </el-dialog>
        <!-- 关系类型列表展示 -->
        <el-scrollbar height="190px">
          <div
            v-for="(item, index) in data.relation_types"
            :key="index"
            class="scrollbar-item-1"
            :style="{ backgroundColor: item.color }"
          >
            <div class="item-content">
              <div class="data1">
                （{{ item.start_label }},{{ item.type }},{{ item.end_label }}）
              </div>
              <div class="data2">{{ item.number }}个关系</div>
              <div class="item-content-buttonlist">
                <el-button
                  class="item-content-button"
                  title="删除"
                  plain
                  @click="openDeleteRelationKindDialog(index, item.type)"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
>>>>>>> dev
            </div>
          </div>
        </el-scrollbar>
      </div>
<<<<<<< HEAD
=======
      <!-- 关系实例列表 -->
>>>>>>> dev
      <div class="left-down">
        <div class="title">
          <el-icon style="font-size: 26px"><DataBoard /></el-icon>
          <div class="title-text">关系实例</div>
<<<<<<< HEAD
          <button class="add-button"></button>
        </div>
        <span class="instance-kind">人</span>
        <el-scrollbar height="260px">
          <p v-for="item in 20" :key="item" class="scrollbar-item-2">{{ item }}</p>
=======
        </div>
        <el-scrollbar height="260px">
          <div v-for="(relation, index) in data.relations" :key="relation.id">
            <h4>
              （{{ getEntityLabel(relation.from) }},{{ relation.type }},{{
                getEntityLabel(relation.to)
              }}）
            </h4>
            <p
              class="scrollbar-item-2"
              :style="{ backgroundColor: getRelationColor(relation.type) }"
            >
              （{{ getEntityText(relation.from) }},{{ relation.type }},{{
                getEntityText(relation.to)
              }}）
              <el-button
                size="mini"
                type="text"
                @click="handleDeleteRequest(relation.from, relation.type, relation.to)"
              >
                删除
              </el-button>
            </p>
          </div>
>>>>>>> dev
        </el-scrollbar>
      </div>
    </div>
    <div class="right">
<<<<<<< HEAD
      <div class="toolbar"></div>
      <el-divider />
      <Annotation :data="data" />
=======
      <div class="toolbar">
        <button class="automatic" title="自动标注" @click="automaticAnnotation">
          <el-icon><MagicStick /></el-icon>
        </button>
        <div v-if="loading" class="spinner">
          <!-- 这是一个简单的加载动画示例 -->
          <div class="loader"></div>
        </div>
      </div>
      <el-divider />
      <Annotation
        :data="data"
        @update-data="updateData"
        :ClickId="ClickId"
        @update-ClickId="updateClickId"
        @request-delete="handleDeleteRequest"
      />
      <!-- 添加关系实例的对话框 -->
      <el-dialog
        :title="`请选择${newrelation.starttext}和${newrelation.endtext}之间的关系`"
        v-model="adddialogFormVisible"
      >
        <el-form :model="newrelation">
          <el-form-item label="关系" :label-width="formLabelWidth">
            <el-select v-model="newrelation.type" placeholder="请选择新建关系类型">
              <el-option
                v-for="(item, index) in type"
                :key="index"
                :label="item"
                :value="item"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <template v-slot:footer>
          <div class="dialog-footer">
            <el-button @click="adddialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="addRelationInstance">确 定</el-button>
          </div>
        </template>
      </el-dialog>
      <!-- 编辑关系类的对话框 -->
      <el-dialog title="编辑关系类" v-model="editRelationDialogVisible">
        <el-form :model="editRelation">
          <el-form-item label="新关系名称" :label-width="formLabelWidth">
            <el-input v-model="editRelation.newType" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <template v-slot:footer>
          <div class="dialog-footer">
            <el-button @click="editRelationDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="updateRelationKind">确 定</el-button>
          </div>
        </template>
      </el-dialog>
      <!-- 删除关系类的确认对话框 -->
      <el-dialog
        title="确认删除"
        v-model="deleteRelationDialogVisible"
        width="30%"
        @close="relationToDelete = null"
      >
        <span>
          您确定要删除关系类 "{{ relationToDelete?.type }}" 吗？此操作将删除所有相关的关系实例。
        </span>
        <template v-slot:footer>
          <span class="dialog-footer">
            <el-button @click="deleteRelationDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="deleteRelationKind">确 定</el-button>
          </span>
        </template>
      </el-dialog>
>>>>>>> dev
    </div>
  </div>
</template>

<script>
<<<<<<< HEAD
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
=======
import Annotation from './RelationshipAnnotationText.vue'
import api from '@/axios/axios'
import { Rank, CirclePlus, Edit, Delete, DataBoard, MagicStick } from '@element-plus/icons-vue'

export default {
  components: {
    Annotation,
    Rank,
    CirclePlus,
    Edit,
    Delete,
    DataBoard,
    MagicStick,
  },
  data() {
    return {
      loading: false,
      docId: this.$route.query.doc_id,
      data: {
        enti: [], // 实体类别
        entities: [], // 实体实例
        relation_types: [], // 关系类型
        relations: [], // 关系实例
        doc_name: '',
        doc_describe: '',
        doc_content: '',
        project_id: '',
      },
      ClickId: { ClickId1: 0, ClickId2: 0 }, // 选择的实体id
      dialogFormVisible: false,
      adddialogFormVisible: false,
      editRelationDialogVisible: false,
      deleteRelationDialogVisible: false,
      formLabelWidth: '120px',
      newrelation: {
        start_label: '',
        end_label: '',
        type: '',
        starttext: '',
        endtext: '',
      },
      type: [],
      editRelation: { oldType: '', newType: '' },
      relationToDelete: null,
      loading: false, // 添加加载状态
    }
  },
  methods: {
    // 获取初始数据
    async fetchData() {
      this.loading = true
      try {
        const response = await api.get(`/get/${this.docId}`)
        this.data = response.data
        console.log('Fetched data:', this.data)
        console.log('Fetched data.enti:', this.data.enti)
        console.log('Fetched data.entities:', this.data.entities)
        console.log('Fetched data.relation_types:', this.data.relation_types)
        console.log('Fetched data.relations:', this.data.relations)
      } catch (error) {
        console.error('获取关系数据失败:', error)
        this.$message({
          type: 'error',
          message: '获取关系数据失败，请稍后重试。',
        })
      } finally {
        this.loading = false
      }
    },
    // 添加关系类
    async addRelationKind() {
      try {
        if (
          !this.newrelation.start_label ||
          !this.newrelation.end_label ||
          !this.newrelation.type
        ) {
          throw new Error('请填写所有必填字段')
        }
        const payload = {
          doc_id: this.docId,
          start_label: this.newrelation.start_label,
          end_label: this.newrelation.end_label,
          type: this.newrelation.type,
          color: this.generateSimilarColors().lightColor, // 生成颜色
        }
        const response = await api.post('/add_relation', payload)
        if (response.data.status === 'success') {
          this.$message({
            type: 'success',
            message: '关系类添加成功',
          })
          this.dialogFormVisible = false
          this.fetchData() // 刷新数据
          // 重置 newrelation
          this.newrelation = {
            start_label: '',
            end_label: '',
            type: '',
            starttext: '',
            endtext: '',
          }
        } else {
          throw new Error(response.data.message || '添加失败')
        }
      } catch (error) {
        console.error('添加关系类失败:', error)
        this.$message({
          type: 'error',
          message: `添加关系类失败: ${error.message || '请稍后重试。'}`,
        })
      }
    },
    // 打开编辑关系类对话框
    openEditRelationKindDialog(type) {
      this.editRelation = { oldType: type, newType: '' }
      this.editRelationDialogVisible = true
    },
    // 更新关系类
    async updateRelationKind() {
      try {
        if (!this.editRelation.newType) {
          throw new Error('新关系名称不能为空')
        }
        const payload = {
          doc_id: this.docId,
          oldType: this.editRelation.oldType,
          newType: this.editRelation.newType,
        }
        const response = await api.put(`/relations/${this.editRelation.oldType}`, payload)
        if (response.data.status === 'success') {
          this.$message({
            type: 'success',
            message: '关系类更新成功',
          })
          this.editRelationDialogVisible = false
          this.fetchData() // 刷新数据
        } else {
          throw new Error(response.data.message || '更新失败')
        }
      } catch (error) {
        console.error('更新关系类失败:', error)
        this.$message({
          type: 'error',
          message: `更新关系类失败: ${error.message || '请稍后重试。'}`,
        })
      }
    },
    // 打开删除关系类对话框
    openDeleteRelationKindDialog(index, type) {
      this.relationToDelete = { index, type }
      this.deleteRelationDialogVisible = true
    },
    // 删除关系类
    async deleteRelationKind() {
      try {
        const { type } = this.relationToDelete
        const response = await api.delete(`/relations/${type}?doc_id=${this.docId}`)
        if (response.data.status === 'success') {
          this.$message({
            type: 'success',
            message: '关系类删除成功',
          })
          this.deleteRelationDialogVisible = false
          this.fetchData() // 刷新数据
        } else {
          throw new Error(response.data.message || '删除失败')
        }
      } catch (error) {
        console.error('删除关系类失败:', error)
        this.$message({
          type: 'error',
          message: `删除关系类失败: ${error.message || '请稍后重试。'}`,
        })
      } finally {
        this.relationToDelete = null
      }
    },
    // 添加关系实例
    async addRelationInstance() {
      try {
        if (!this.newrelation.type) {
          throw new Error('请选择关系类型')
        }

        // 根据选定的关系类型获取对应的颜色
        const relationType = this.data.relation_types.find(
          (rt) => rt.type === this.newrelation.type,
        )
        if (!relationType) {
          throw new Error('未找到选定关系类型的颜色')
        }
        await api.put('/update_relation_types', { type: this.newrelation.type, increment: true })
        const payload = {
          doc_id: this.docId,
          from_entity_id: this.ClickId.ClickId1,
          to_entity_id: this.ClickId.ClickId2,
          type: this.newrelation.type,
          color: relationType.color, // 添加颜色字段
        }

        const response = await api.post('/relations/instances', payload)
        if (response.data.status === 'success') {
          this.$message({
            type: 'success',
            message: '关系实例添加成功',
          })
          this.adddialogFormVisible = false
          this.fetchData() // 刷新数据
          // 重置 ClickId 和 newrelation
          this.ClickId = { ClickId1: 0, ClickId2: 0 }
          this.newrelation = {
            start_label: '',
            end_label: '',
            type: '',
            starttext: '',
            endtext: '',
          }
        } else {
          throw new Error(response.data.message || '添加失败')
        }
      } catch (error) {
        console.error('添加关系实例失败:', error)
        this.$message({
          type: 'error',
          message: `添加关系实例失败: ${error.message || '请稍后重试。'}`,
        })
      }
    },
    // 删除标注的关系实例
    async handleDeleteRequest(from, type, to) {
      try {
        await this.$confirm('是否要删除此处已标注的关系', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })

        // 假设有一个唯一的ID来标识关系实例
        const relationId = this.getRelationId(from, type, to)
        if (!relationId) {
          this.$message({
            type: 'error',
            message: '未找到要删除的关系实例。',
          })
          return
        }
        await api.put('/update_relation_types', { type: type, increment: false })

        await api.delete(`/relations/instances/${relationId}?doc_id=${this.docId}`)

        this.$message({
          type: 'success',
          message: '删除成功!',
        })

        this.fetchData() // 刷新数据
      } catch (error) {
        if (error !== 'cancel' && error !== undefined) {
          // 根据 Element Plus 的实现，取消操作不会传递错误
          console.error('删除关系实例失败:', error)
          this.$message({
            type: 'error',
            message: '删除失败，请稍后重试！',
          })
        } else {
          this.$message({
            type: 'info',
            message: '已取消删除',
          })
        }
      }
    },

    // 获取关系实例的唯一ID（需要根据实际数据结构实现）
    getRelationId(from, type, to) {
      const relation = this.data.relations.find(
        (rel) => rel.from === from && rel.type === type && rel.to === to,
      )
      return relation ? relation.id : null
    },
    // 更新data
    updateData(newData) {
      this.data = newData // 更新父组件的数据
    },
    // 更新选中的实体
    updateClickId(newClickId) {
      this.ClickId = newClickId
      if (this.ClickId.ClickId1 !== 0 && this.ClickId.ClickId2 !== 0) {
        // 选中两个实体，进行关系建立
        const fromEntity = this.data.entities.find((entity) => entity.id === this.ClickId.ClickId1)
        const toEntity = this.data.entities.find((entity) => entity.id === this.ClickId.ClickId2)
        if (fromEntity && toEntity) {
          this.newrelation.starttext = fromEntity.text
          this.newrelation.start_label = fromEntity.label
          this.newrelation.from_entity_id = fromEntity.id

          this.newrelation.endtext = toEntity.text
          this.newrelation.end_label = toEntity.label
          this.newrelation.to_entity_id = toEntity.id
        } else {
          this.$message({
            type: 'error',
            message: '选中的实体不存在，请重新选择。',
          })
          return
        }

        // 根据选中的实体类型，找到可用的关系类型
        this.type = [] // 重置类型列表
        this.data.relation_types.forEach((relationType) => {
          if (
            relationType.start_label === this.newrelation.start_label &&
            relationType.end_label === this.newrelation.end_label
          ) {
            this.type.push(relationType.type)
          }
        })

        // 如果没有可用的关系类型
        if (this.type.length === 0) {
          this.$message({
            type: 'info',
            message: '当前选中的实体类型之间没有可用的关系类型。',
          })
        } else {
          this.adddialogFormVisible = true
        }
      }
    },
    // 生成随机颜色
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
    // 根据提供的 type 筛选关系实例
    filteredEntities(type) {
      return this.data.relations.filter((relation) => relation.type === type)
    },
    // 获取实体的 label
    getEntityLabel(entityId) {
      const entity = this.data.entities.find((ent) => ent.id === entityId)
      return entity ? entity.label : '未知实体'
    },
    // 获取实体的 text
    getEntityText(entityId) {
      const entity = this.data.entities.find((ent) => ent.id === entityId)
      return entity ? entity.text : '未知文本'
    },
    // 获取关系类型的颜色
    getRelationColor(type) {
      const relationType = this.data.relation_types.find((rt) => rt.type === type)
      return relationType ? relationType.color : '#FFFFFF'
    },
    // 自动标注功能（根据您的需求实现）
    async automaticAnnotation() {
      this.loading = true // 开始加载动画
      try {
        await api.post('/analyze_relation', {
          doc_id: this.docId,
          doc_content: this.data.doc_content,
          entities: this.data.entities,
          relation_types: this.data.relation_types,
        })
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false // 结束加载动画
      }
      this.fetchData()
    },
    // 打开添加关系类对话框
    openAddRelationKindDialog() {
      this.dialogFormVisible = true
    },
  },
  created() {
    this.fetchData()
>>>>>>> dev
  },
  beforeCreate() {
    this.$nextTick(() => {
      document.body.setAttribute('style', 'background:#f3f6f7')
    })
  },
<<<<<<< HEAD
  //实例销毁之前钩子--移除body 标签的属性style
=======
>>>>>>> dev
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
<<<<<<< HEAD
=======
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
<<<<<<< HEAD
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
=======
  color: black;
  width: 380px;
>>>>>>> dev
}

.item-content {
  display: flex;
<<<<<<< HEAD
}

.data2 {
  margin-left: 80px;
}

.data3 {
  margin-left: 40px;
=======
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
  background-color: transparent;
  cursor: pointer;
  border: none;
}

.item-content-button:hover {
  color: #0056b3; /* 悬停时的文本颜色 */
  background: none;
>>>>>>> dev
}

.scrollbar-item-2 {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
<<<<<<< HEAD
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
=======
  color: black;
>>>>>>> dev
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
<<<<<<< HEAD
=======
  height: 40px;
}

.automatic {
  width: 30px;
  height: 30px;
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

/* 其他样式保持不变 */
.dialog-footer {
  text-align: right;
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
>>>>>>> dev
}
</style>
