<template>
  <div class="annotation-container" @mouseup="handleMouseUp">
    <svg ref="svgRef" :width="svgWidth" :height="svgHeight" class="annotation-svg"></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'
import { ref, onMounted, watch } from 'vue'

export default {
  name: 'ThreeSegmentArrow',
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit }) {
    const svgRef = ref(null)
    const svgWidth = 1000 // SVG 宽度
    const svgHeight = 500 // SVG 高度
    const maxLineWidth = 1000 // 最大行宽度，超出后换行
    let svg
    let text
    let textGroup
    const disabledBackgrounds = ref([]) // 记录 disabled 实体的背景颜色
    const disabledborder = ref([]) // 记录 disabled 实体的边框颜色
    const disabledfill = ref([]) // 记录 disabled 实体的字体颜色
    const disabledlabel = ref([]) //记录 disabled 标注种类

    const checkDisabledEntities = () => {
      disabledBackgrounds.value = [] // 清空
      disabledborder.value = []
      disabledfill.value = []
      disabledlabel.value = []
      props.data.enti.forEach((entity) => {
        if (entity.disabled === true) {
          disabledBackgrounds.value.push(entity.color.background)
          disabledborder.value.push(entity.color.border)
          disabledfill.value.push(entity.color.fill)
          disabledlabel.value.push(entity.label)
        }
      })
    }

    //选择标注区域
    const handleMouseUp = () => {
      const selection = window.getSelection()
      if (selection.rangeCount > 0 && disabledBackgrounds.value.length > 0) {
        const range = selection.getRangeAt(0)
        // 获取选中的文本
        const selectedText = range.toString()

        // 获取选中范围的起始和结束容器
        const startContainer = range.startContainer
        const endContainer = range.endContainer
        // 查找 char-group 并处理 <text> 元素
        const startTextGroup = getTextGroup(startContainer)
        const endTextGroup = getTextGroup(endContainer)
        let startindex
        let endindex
        let x
        let y
        let endx
        let endwidth
        if (startTextGroup) {
          const startTextElements = startTextGroup.getElementsByTagName('text')
          Array.from(startTextElements).forEach((startElement) => {
            // 在此处处理 <text> 元素
            startindex = startElement.getAttribute('data-index')
            x = parseFloat(startElement.getAttribute('x')) - 2
            y = parseFloat(startElement.getAttribute('y')) - 18
          })
        }

        if (endTextGroup) {
          const endTextElements = endTextGroup.getElementsByTagName('text')
          Array.from(endTextElements).forEach((endElement) => {
            endindex = endElement.getAttribute('data-index')
            endx = parseFloat(endElement.getAttribute('x'))
            endwidth = endElement.getBBox().width
          })
        }
        let width = endx + endwidth - x + 2
        textGroup
          .append('rect')
          .attr('x', x)
          .attr('y', y)
          .attr('width', width)
          .attr('height', 20)
          .attr('fill', disabledBackgrounds.value[0])
          .attr('stroke', disabledborder.value[0])
          .attr('stroke-width', 1)
          .lower()
        console.log(x)
        console.log(y)
        console.log(width)
        for (let i = startindex; i <= endindex; i++) {
          let selectedTextElement = d3.select(`.text-group .char-group text[data-index='${i}']`)
          selectedTextElement.attr('fill', disabledfill.value[0])
        }
        const newdata = props.data
        //更新data
        newdata.enti.forEach((entity) => {
          if (entity.color.background === disabledBackgrounds.value[0]) {
            entity.number += 1
          }
        })
        newdata.entities.push({
          id: 0,
          start: startindex,
          end: endindex,
          label: disabledlabel.value[0],
          color: {
            background: disabledBackgrounds.value[0],
            border: disabledborder.value[0],
            fill: disabledfill.value[0],
          },
          text: selectedText,
        })
        emit('update-data', newdata)
      }
    }

    // 获取节点的 char-group 值
    const getTextGroup = (node) => {
      while (node) {
        // 检查是否是 g 元素，并且类名包含 char-group
        if (
          node.nodeType === Node.ELEMENT_NODE &&
          node.tagName === 'g' &&
          node.classList.contains('char-group')
        ) {
          return node // 返回找到的 char-group 元素
        }
        node = node.parentNode // 向上遍历祖先节点
      }
      return null // 未找到
    }

    const cs = () => {
      svg = d3.select(svgRef.value)
      const textData = props.data.text
      const entities = props.data.entities

      // 清空 SVG
      svg.selectAll('*').remove()

      // 绘制文本和实体框
      textGroup = svg.append('g').attr('class', 'text-group')
      const entityBoxes = {} // 存储实体位置信息

      let cursorX = 20 // 初始光标 X 坐标
      let cursorY = 50 // 初始光标 Y 坐标
      let lineHeight = 30 // 行高

      // 绘制普通文本和实体
      const charGroups = []
      textData.split('').forEach((char, index) => {
        const entity = entities.find((e) => index >= e.start && index <= e.end)

        // 如果光标超出最大行宽，则换行
        if (cursorX + 10 > maxLineWidth) {
          cursorX = 20 // 重置 X 光标
          cursorY += lineHeight // 增加 Y 坐标
        }

        const charGroup = textGroup.append('g').attr('class', 'char-group')
        text = charGroup
          .append('text')
          .attr('x', cursorX)
          .attr('y', cursorY)
          .text(char)
          .attr('font-size', '16px')
          .attr('fill', entity ? entity.color.fill : 'black')
          .attr('data-index', index) // 添加索引值
        // 如果是实体，将字符分组

        if (entity) {
          charGroups.push({
            entity,
            x: cursorX,
            y: cursorY - 18,
            width: text.node().getBBox().width,
            height: 20,
          })
        }

        // 移动光标
        cursorX += text.node().getBBox().width
      })

      // 绘制实体框
      entities.forEach((entity) => {
        const entityChars = charGroups.filter((c) => c.entity.id === entity.id)
        if (entityChars.length > 0) {
          const firstChar = entityChars[0]
          const lastChar = entityChars[entityChars.length - 1]
          const x = firstChar.x
          const y = firstChar.y
          const width = lastChar.x + lastChar.width - x

          // 合并实体框
          textGroup
            .append('rect')
            .attr('x', x - 2)
            .attr('y', y)
            .attr('width', width + 4)
            .attr('height', 20)
            .attr('fill', entity.color.background)
            .attr('stroke', entity.color.border)
            .attr('stroke-width', 1)
            .lower()

          // 保存实体位置
          entityBoxes[entity.id] = { x, y, width, height: 20 }
        }
      })
    }
    onMounted(() => {
      cs()
    })

    // 监听 data 的变化
    watch(
      () => props.data,
      (newData, oldData) => {
        checkDisabledEntities() // 当 data 变化时重新检查
        cs()
      },
      { deep: true },
    ) // 如果 data 是嵌套对象，设置 deep 监听

    return {
      svgRef,
      svgWidth,
      svgHeight,
      handleMouseUp,
      disabledBackgrounds,
      disabledborder,
      disabledfill,
      disabledlabel,
      cs,
    }
  },
}
</script>

<style>
.annotation-container {
  width: 1000px;
  height: 500px;
  margin: auto;
  border: 1px solid #ddd;
  position: relative;
}
.annotation-svg {
  width: 100%;
  height: 500px;
}
</style>
