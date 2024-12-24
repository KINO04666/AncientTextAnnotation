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
    //绘制
    const draw = () => {
      svg = d3.select(svgRef.value)
      const textData = props.data.doc_content
      const entities = props.data.entities
      const relations = props.data.relations
      const ClickId = props.ClickId
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
            .attr('rx', 5) // 设置水平圆角半径
            .attr('ry', 5) // 设置垂直圆角半径
            .lower()

          if (entity.id === ClickId.ClickId1) {
            //此时为第一个被选中的实体，设置虚线边框
            textGroup
              .append('rect')
              .attr('x', x - 2)
              .attr('y', y)
              .attr('width', width + 4)
              .attr('height', 20)
              .attr('fill', 'transparent')
              .attr('rx', 5) // 设置水平圆角半径
              .attr('ry', 5) // 设置垂直圆角半径
              .attr('stroke', 'black') // 确保边框颜色为黑色
              .attr('stroke-width', 2) // 设置边框宽度
              .attr('stroke-dasharray', '5, 5') // 点击后设置边框为虚线
              .on('click', function () {
                //再次点击取消选中
                ClickId.ClickId1 = 0
                emit('update-ClickId', ClickId)
              })
          } else {
            textGroup
              .append('rect')
              .attr('x', x - 2)
              .attr('y', y)
              .attr('width', width + 4)
              .attr('height', 20)
              .attr('fill', 'transparent')
              .attr('rx', 5) // 设置水平圆角半径
              .attr('ry', 5) // 设置垂直圆角半径
              .attr('stroke', 'transparent') // 初始边框透明
              .attr('stroke-width', 2) // 设置边框宽度
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
              .on('click', function () {
                if (ClickId.ClickId1 === 0) {
                  ClickId.ClickId1 = entity.id
                } else {
                  ClickId.ClickId2 = entity.id
                }
                emit('update-ClickId', ClickId)
              })
          }

          // 保存实体位置
          entityBoxes[entity.id] = { x, y, width, height: 20 }
        }
      })

      relations.forEach((relation) => {
        // 绘制关系箭头
        const relationGroup = svg
          .append('g')
          .attr('class', 'relation-group')
          .attr('role', 'button')
          .style('cursor', 'pointer') // 设置光标为手型
          .on('click', () => {
            // 点击事件处理
            emit('request-delete', relation.from, relation.type, relation.to) // 触发请求删除的事件
          })
        // 定义箭头
        const defs = svg.append('defs')
        const fromBox = entityBoxes[relation.from]
        const toBox = entityBoxes[relation.to]

        if (fromBox && toBox) {
          const startX = fromBox.x + fromBox.width / 2
          const startY = fromBox.y - 5 // 起点上方
          const endX = toBox.x + toBox.width / 2
          const endY = toBox.y - 5 // 终点上方
          // 动态计算关系文本位置
          // 动态计算关系文本位置
          // 动态计算文本位置
          // 动态计算关系文本位置
          const middleX = (startX + endX) / 2 // 箭头中间点的 X 坐标
          let labelY

          // 动态调整 label 的 Y 坐标
          if (endX > startX && endY > startY) {
            // 右下方
            labelY = startY - 10 // 文本在箭头上方
          } else if (endX < startX && endY > startY) {
            // 左下方
            labelY = startY - 10 // 文本在箭头上方
          } else if (endX > startX && endY < startY) {
            // 右上方
            labelY = endY - 10 // 文本在箭头上方
          } else if (endX < startX && endY < startY) {
            // 左上方
            labelY = endY - 10 // 文本在箭头上方
          } else {
            // 默认（水平或垂直箭头）
            labelY = startY - 10 // 文本在箭头上方
          }

          // 为每种关系定义独立的箭头
          const markerId = `arrowhead-${relation.type}`
          if (!svg.select(`#${markerId}`).node()) {
            defs
              .append('marker')
              .attr('id', markerId)
              .attr('markerWidth', 4) // 更小的箭头宽度
              .attr('markerHeight', 3) // 更小的箭头高度
              .attr('refX', 0) // 调整箭头位置
              .attr('refY', 1.5)
              .attr('orient', 'auto')
              .append('polygon')
              .attr('points', '0 0, 4 1.5, 0 3') // 更小的箭头形状
              .attr('fill', relation.color) // 动态箭头颜色
          }

          let d = `M${startX},${startY} ` // 起始点

          // 动态判断箭头方向
          if (endX > startX && endY > startY) {
            // 右下方
            d += `L${startX},${startY - 5} L${endX},${startY - 5} L${endX},${endY}`
          } else if (endX < startX && endY > startY) {
            // 左下方
            d += `L${startX},${startY - 5} L${endX},${startY - 5} L${endX},${endY}`
          } else if (endX > startX && endY < startY) {
            // 右上方
            d += `L${startX},${endY - 5} L${endX},${endY - 5} L${endX},${endY}`
          } else if (endX < startX && endY < startY) {
            // 左上方
            d += `L${startX},${endY - 5} L${endX},${endY - 5} L${endX},${endY}`
          } else {
            // 默认（水平或垂直）
            d += `L${endX},${endY}`
          }

          // 绘制箭头路径
          relationGroup
            .append('path')
            .attr('d', d)
            .attr('stroke', relation.color) // 统一箭身颜色
            .attr('stroke-width', 2)
            .attr('fill', 'none')
            .attr('marker-end', `url(#${markerId})`)

          // 添加关系类型文字
          relationGroup
            .append('text')
            .attr('x', middleX)
            .attr('y', labelY)
            .attr('font-size', '12px')
            .attr('text-anchor', 'middle') // 居中对齐
            .attr('fill', relation.color)
            .text(relation.type)
        }
      })
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
    watch(
      () => props.ClickId,
      (newData, oldData) => {
        draw()
      },
      { deep: true },
    )
    return {
      svgRef,
      svgWidth,
      svgHeight,
      draw,
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
