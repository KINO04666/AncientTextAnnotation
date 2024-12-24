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
    ClickId: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const svgRef = ref(null)
    const svgWidth = 1000 // SVG 宽度
    const svgHeight = 500 // SVG 高度
    const maxLineWidth = 1000 // 最大行宽度，超出后换行
    let chosed = { start: 0, end: 0, text: '' } //被选中的文字的索引以及内容
    //选择标注区域
    const handleMouseUp = () => {
      const selection = window.getSelection()
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0)
        // 获取选中的文本
        chosed.text = range.toString()
        // 获取选中范围的起始和结束容器
        const startContainer = range.startContainer
        const endContainer = range.endContainer
        // 查找 char-group 并处理 <text> 元素
        const startTextGroup = getTextGroup(startContainer)
        const endTextGroup = getTextGroup(endContainer)
        //获取选择区域的前后两个字的索引
        if (startTextGroup) {
          const startTextElements = startTextGroup.getElementsByTagName('text')
          Array.from(startTextElements).forEach((startElement) => {
            chosed.start = startElement.getAttribute('data-index')
          })
        }
        if (endTextGroup) {
          const endTextElements = endTextGroup.getElementsByTagName('text')
          Array.from(endTextElements).forEach((endElement) => {
            chosed.end = endElement.getAttribute('data-index')
          })
        }
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
    //绘制界面
    const draw = () => {
      const svg = d3.select(svgRef.value)
      const textData = props.data.doc_content
      const entities = props.data.entities

      // 清空 SVG
      svg.selectAll('*').remove()

      // 绘制文本和实体框
      const textGroup = svg.append('g').attr('class', 'text-group')

      let cursorX = 20 // 初始光标 X 坐标
      let cursorY = 50 // 初始光标 Y 坐标
      let lineHeight = 30 // 行高

      // 绘制普通文本和实体
      const charGroups = []
      textData.split('').forEach((char, index) => {
        const entity = entities.find((e) => index >= e.start && index <= e.end)

        // 如果光标超出最大行宽，则换行
        if (cursorX + 15 > maxLineWidth) {
          cursorX = 20 // 重置 X 光标
          cursorY += lineHeight // 增加 Y 坐标
        }
        //如果实体在上下两行，进行换行处理
        if (entity && index == entity.start) {
          if (cursorX + (entity.end - entity.start + 1) * 17 >= maxLineWidth) {
            cursorX = 20 // 重置 X 光标
            cursorY += lineHeight // 增加 Y 坐标
          }
        }
        const charGroup = textGroup.append('g').attr('class', 'char-group')
        //绘制字体
        const text = charGroup
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
            .attr('rx', 5) // 设置水平圆角半径
            .attr('ry', 5) // 设置垂直圆角半径
            .lower()
          //由于实体框在文字下面，新建相同的透明框用以处理点击事件
          textGroup
            .append('rect')
            .attr('x', x - 2)
            .attr('y', y)
            .attr('width', width + 4)
            .attr('height', 20)
            .attr('fill', 'transparent')
            .attr('stroke', 'transparent') // 初始边框透明
            .attr('stroke-width', 2) // 设置边框宽度
            .attr('rx', 5) // 设置水平圆角半径
            .attr('ry', 5) // 设置垂直圆角半径
            .attr('role', 'button')
            .style('cursor', 'pointer') // 设置光标为手型
            .on('mouseover', function () {
              d3.select(this)
                .attr('fill', 'rgba(0, 0, 0, 0.1)') // 悬停时背景色
                .attr('stroke', 'black') // 悬停时边框变为黑色
            })
            .on('mouseout', function () {
              d3.select(this)
                .attr('fill', 'transparent') // 恢复背景透明
                .attr('stroke', 'transparent') // 恢复边框透明
            })
            .on('click', () => {
              emit('request-delete', entity.id) // 触发请求删除的事件
            })
        }
      })
    }
    //添加选中的为实体
    const add = () => {
      //有选中的文字
      if (chosed.text) {
        const newdata = JSON.parse(JSON.stringify(props.data)) // 深拷贝
        props.data.enti.forEach((Entity, index) => {
          //实体类++
          if (index === props.ClickId) {
            newdata.enti.forEach((entity) => {
              if (entity.color.background === Entity.color.background) {
                entity.number += 1
              }
            })
            const generateUniqueId = () => {
              // 当前时间戳（毫秒）加上一个随机数
              return Date.now() + Math.floor(Math.random() * 1000)
            }
            const uniqueId = generateUniqueId()
            newdata.entities.push({
              id: uniqueId,
              start: chosed.start,
              end: chosed.end,
              label: Entity.label,
              color: Entity.color,
              text: chosed.text,
            })
            emit('update-data', newdata) //更新data
            const e = []
            e.push({
              id: uniqueId,
              start: chosed.start,
              end: chosed.end,
              label: Entity.label,
              color: Entity.color,
              text: chosed.text,
            })
            emit('update-entity', e) //更新data
          }
        })
        //选择区域清空
        chosed.start = 0
        chosed.end = 0
        chosed.text = ''
        const newClickId = -1
        emit('update-ClickId', newClickId) //重置按钮
      }
    }
    onMounted(() => {
      draw()
    })

    // 监听 data 的变化
    watch(
      () => props.data,
      (newData, oldData) => {
        draw()
      },
      { deep: true },
    ) // 如果 data 是嵌套对象，设置 deep 监听
    //监听按钮点击
    watch(
      () => props.ClickId,
      (newData, oldData) => {
        add()
      },
    )

    return {
      svgRef,
      svgWidth,
      svgHeight,
      handleMouseUp,
      draw,
      add,
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
