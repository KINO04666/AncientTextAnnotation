<template>
  <div class="main">
    <!-- 添加加载遮罩 -->
    <el-loading v-if="loading" :fullscreen="true" text="加载中..." />

    <div class="left">
      <div class="structure-panel">
        <div class="panel-header">
          <el-icon><Document /></el-icon>
          <span class="panel-title">结构</span>
        </div>
        <div class="structure-content">
          <el-tree :data="structureTree" :props="defaultProps" default-expand-all node-key="id">
            <template #default="{ node, data }">
              <span class="custom-tree-node">
                <span>{{ data.text }}</span>
              </span>
            </template>
          </el-tree>
        </div>
      </div>
    </div>

    <div class="right">
      <div class="toolbar">
        <!-- 自动标点按钮 -->
        <el-tooltip content="自动标点" placement="bottom">
          <el-button type="primary" circle @click="handleAutoPunctuation" :loading="loading">
            <el-icon><SemiSelect /></el-icon>
          </el-button>
        </el-tooltip>

        <el-divider direction="vertical" />

        <!-- 结构标注按钮组 -->
        <el-button-group>
          <el-button
            v-for="type in structureTypes"
            :key="type.value"
            :type="selectedType === type.value ? 'primary' : ''"
            @click="handleAnnotation(type.value)"
          >
            {{ type.label }}
          </el-button>
        </el-button-group>

        <div class="save-status" :class="saveStatus === '保存失败' ? 'error' : ''">
          <el-icon v-if="saveStatus === '已保存'"><Check /></el-icon>
          <el-icon v-else-if="saveStatus === '保存中...'"><Loading /></el-icon>
          <el-icon v-else><Warning /></el-icon>
          {{ saveStatus }}
        </div>
      </div>

      <!-- 文本编辑区域 -->
      <div
        ref="editableDiv"
        class="editable-content"
        contenteditable="true"
        @input="handleTextChange"
        @mouseup="handleTextSelection"
        @contextmenu.prevent="handleContextMenu"
        spellcheck="false"
      >
        {{ content }}
      </div>
    </div>
  </div>

  <!-- 右键菜单 -->
  <div
    v-if="showContextMenu"
    class="context-menu"
    :style="{ left: menuPosition.x + 'px', top: menuPosition.y + 'px' }"
  >
    <div class="menu-group">
      <div
        v-for="type in structureTypes"
        :key="type.value"
        class="menu-item"
        @click="handleAnnotation(type.value)"
      >
        {{ type.label }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Edit, SemiSelect, Check, Loading, Warning } from '@element-plus/icons-vue'
import api from '@/axios/axios'
import { useRoute } from 'vue-router'
// 响应式状态
const route = useRoute()
const doc_id = route.query.doc_id
const content = ref('')
const selectedType = ref('')
const loading = ref(false) // 只用于自动标点的加载状态
const structureTree = reactive([])
const editorRef = ref(null)

// 结构类型定义
const structureTypes = [
  { label: '卷', value: '卷' },
  { label: '篇', value: '篇' },
  { label: '章', value: '章' },
  { label: '节', value: '节' },
  { label: '小节', value: '小节' },
]

// 自动标点处理
const handleAutoPunctuation = async () => {
  if (!content.value) {
    ElMessage.warning('请先输入文本')
    return
  }

  try {
    loading.value = true

    // 使用 fetch 调用 API
    const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer sk-3d5aa54bd21f40f5b6157cbb8cd3483d',
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          {
            role: 'system',
            content:
              '你是一个专门处理中文古籍标点的助手。请帮我为以下文本添加标点符号，只返回添加标点后的文本，不要有任何其他解释。',
          },
          {
            role: 'user',
            content: content.value,
          },
        ],
        temperature: 0.1,
      }),
    })

    const data = await response.json()

    // 更新文本内容
    content.value = data.choices[0].message.content

    ElMessage.success('自动标点完成')
  } catch (error) {
    console.error('自动标点失败:', error)
    ElMessage.error('自动标点失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 文本选择处理
const handleTextSelection = () => {
  const selection = window.getSelection()
  const text = selection.toString().trim()

  if (!text) return
}

// 处理引用标注
const handleQuoteAnnotation = (range, text) => {
  const container = document.createElement('span')
  container.className = 'special-annotation quote'
  container.textContent = `『${text}』`

  const label = document.createElement('span')
  label.className = 'annotation-label'
  label.textContent = '引'
  container.appendChild(label)

  range.deleteContents()
  range.insertNode(container)
}

// 处理结构标注
const handleStructureAnnotation = async (range, text, type) => {
  const id = Date.now().toString()

  // 不改变原文本样式，只添加标识
  const container = document.createElement('span')
  container.setAttribute('data-structure-id', id)
  container.setAttribute('data-structure-type', type)
  container.textContent = text

  // 替换选中内容
  range.deleteContents()
  range.insertNode(container)

  // 添加到结构树
  addToStructureTree({
    id,
    text,
    type,
    children: [],
  })

  // 实时保存
  saveToBackend(content.value, structureTree)
}

// 添加获取中文标签的函数
const getStructureLabel = (type) => {
  const typeMap = {
    volume: '卷',
    article: '篇',
    chapter: '章',
    section: '节',
    subsection: '小节',
  }
  return typeMap[type] || type
}

// 修改结构树相关代码
const typeOrder = {
  卷: 1,
  篇: 2,
  章: 3,
  节: 4,
  小节: 5,
}

// 修改添加到结构树的函数
const addToStructureTree = (node) => {
  // 如果是卷，直接添加到根节点
  if (node.type === '卷') {
    structureTree.push(node)
    return
  }

  // 找到合适的父节点
  const parent = findLastSuitableParent(structureTree, node.type)
  if (parent) {
    parent.children.push(node)
  } else {
    // 如果找不到合适的父节点，提示用户
    ElMessage.warning(`请先添加${getRequiredParentType(node.type)}`)
  }
}

// 获取需要的父节点类型
const getRequiredParentType = (type) => {
  const types = ['卷', '篇', '章', '节', '小节']
  const index = types.indexOf(type)
  return index > 0 ? types[index - 1] : null
}

// 查找最后一个合适的父节点
const findLastSuitableParent = (nodes, type) => {
  for (let i = nodes.length - 1; i >= 0; i--) {
    const node = nodes[i]
    // 检查当前节点是否可以作为父节点
    if (typeOrder[node.type] < typeOrder[type]) {
      // 先在当前节点的子节点中查找
      if (node.children && node.children.length > 0) {
        const found = findLastSuitableParent(node.children, type)
        if (found) return found
      }
      return node
    }
  }
  return null
}

// 替换选中内容
const replaceRangeWithNode = (range, node) => {
  range.deleteContents()
  range.insertNode(node)
}

// 处理文本变化
const handleTextChange = (event) => {
  content.value = event.target.innerHTML
  // 只在有内容时保存
  if (content.value) {
    saveToBackend(content.value, structureTree)
  }
}

// 树形结构数据
const defaultProps = {
  children: 'children',
  label(data) {
    return `${data.type}：${data.text}`
  },
}

// 右键菜单状态
const showContextMenu = ref(false)
const menuPosition = reactive({ x: 0, y: 0 })
const currentSelection = ref(null)

// 处理右键菜单
const handleContextMenu = (event) => {
  const selection = window.getSelection()
  const text = selection.toString().trim()

  if (!text) return

  // 保存选中内容
  currentSelection.value = {
    text,
    range: selection.getRangeAt(0).cloneRange(),
  }

  // 显示菜单
  showContextMenu.value = true
  menuPosition.x = event.clientX
  menuPosition.y = event.clientY

  // 点击其他地方关闭菜单
  document.addEventListener('click', closeContextMenu)
}

// 关闭右键菜单
const closeContextMenu = () => {
  showContextMenu.value = false
  document.removeEventListener('click', closeContextMenu)
}

// 处理标注选择
const handleAnnotation = (type) => {
  const selection = window.getSelection()
  const text = selection.toString().trim()

  if (!text) {
    ElMessage.warning('请先选择文本')
    return
  }

  const range = selection.getRangeAt(0)
  handleStructureAnnotation(range, text, type)
  selection.removeAllRanges()
}

// 添加保存状态
const saveStatus = ref('已保存') // 可能的状态：'已保存'、'保存中'、'保存失败'

// 修改实时保存函���
const saveToBackend = async (content, structures) => {
  try {
    saveStatus.value = '保存中...'
    await api.post('/update_document', {
      doc_id: doc_id,
      doc_content: content,
    })
    saveStatus.value = '已保存'
  } catch (error) {
    saveStatus.value = '保存失败'
  }
}

onMounted(async () => {
  try {
    // 组件加载时立即获取数据
    const response = await api(`/get/${doc_id}`)
    const data = response.data
    content.value = data.doc_content || '' // 设置到编辑器中
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
})
</script>

<style scoped>
.main {
  display: flex;
  padding: 20px;
  gap: 20px;
  background-color: #f5f7fa;
  height: calc(100vh - 60px);
}

.left {
  width: 300px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.structure-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #f8f9fb;
  border-radius: 8px 8px 0 0;
}

.panel-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.structure-content {
  padding: 15px;
  overflow-y: auto;
  flex: 1;
  height: calc(100% - 60px);
}

.structure-item {
  padding: 12px 15px;
  margin-bottom: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  color: #606266;
}

.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.toolbar {
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  background-color: white;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  border-bottom: 1px solid #e4e7ed;
}

.editable-content {
  flex: 1;
  padding: 20px 40px;
  background-color: white;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  overflow-y: auto;
  outline: none;
  white-space: pre-wrap;
  font-size: 16px;
  line-height: 2.2;
}

/* 树形结构样式 */
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  font-size: 14px;
  padding-right: 8px;
}

/* 按钮组样式 */
.el-button-group {
  display: flex;
  gap: 1px;
}

.el-button-group .el-button {
  margin-left: -1px;
}

.el-button-group .el-button:first-child {
  margin-left: 0;
}

/* 分隔线样式 */
.el-divider--vertical {
  height: 20px;
  margin: 0 15px;
}

/* 添加引用样式 */
.special-annotation.quote {
  color: #409eff;
}

/* 右键菜单样式 */
.context-menu {
  position: fixed;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 4px 0;
  z-index: 1000;
  min-width: 120px;
}

.menu-group {
  padding: 4px 0;
}

.menu-item {
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}

.menu-item:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

/* 添加保存状态样式 */
.save-status {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #67c23a; /* 成功状态的颜色 */
}

.save-status.error {
  color: #f56c6c; /* 失败状态的颜色 */
}

.save-status .el-icon {
  font-size: 16px;
}
</style>
