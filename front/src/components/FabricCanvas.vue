<template>
    <div class="annotation-container">
      <svg ref="svgRef" :width="svgWidth" :height="svgHeight" class="annotation-svg"></svg>
    </div>
  </template>
  
  <script>
  import * as d3 from "d3";
  import { ref, onMounted } from "vue";
  
  export default {
    name: "ThreeSegmentArrow",
    props: {
      data: {
        type: Object,
        required: true,
      },
    },
    setup(props) {
      const svgRef = ref(null);
      const svgWidth = 800; // SVG 宽度
      const svgHeight = 400; // SVG 高度
      const maxLineWidth = 700; // 最大行宽度，超出后换行
  
      onMounted(() => {
        const svg = d3.select(svgRef.value);
        const textData = props.data.text;
        const entities = props.data.entities;
        const relations = props.data.relations;
  
        // 清空 SVG
        svg.selectAll("*").remove();
  
        // 绘制文本和实体框
        const textGroup = svg.append("g").attr("class", "text-group");
        const entityBoxes = {}; // 存储实体位置信息
  
        let cursorX = 20; // 初始光标 X 坐标
        let cursorY = 50; // 初始光标 Y 坐标
        let lineHeight = 30; // 行高
  
        // 绘制普通文本和实体
        const charGroups = [];
        textData.split("").forEach((char, index) => {
          const entity = entities.find((e) => index >= e.start && index < e.end);
  
          // 如果光标超出最大行宽，则换行
          if (cursorX + 10 > maxLineWidth) {
            cursorX = 20; // 重置 X 光标
            cursorY += lineHeight; // 增加 Y 坐标
          }
  
          const charGroup = textGroup.append("g").attr("class", "char-group");
          const text = charGroup
            .append("text")
            .attr("x", cursorX)
            .attr("y", cursorY)
            .text(char)
            .attr("font-size", "16px")
            .attr("fill", entity ? entity.color.text : "black");
  
          // 如果是实体，将字符分组
          if (entity) {
            charGroups.push({
              entity,
              x: cursorX,
              y: cursorY - 18,
              width: text.node().getBBox().width,
              height: 20,
              index,
            });
          }
  
          // 移动光标
          cursorX += text.node().getBBox().width;
        });
  
        // 绘制实体框
        //const entityGroups = [];
        entities.forEach((entity) => {
          const entityChars = charGroups.filter((c) => c.entity.id === entity.id);
          if (entityChars.length > 0) {
            const firstChar = entityChars[0];
            const lastChar = entityChars[entityChars.length - 1];
            const x = firstChar.x;
            const y = firstChar.y;
            const width = lastChar.x + lastChar.width - x;
  
            // 合并实体框
            textGroup
              .append("rect")
              .attr("x", x - 2)
              .attr("y", y)
              .attr("width", width + 4)
              .attr("height", 20)
              .attr("fill", entity.color.background)
              .attr("stroke", entity.color.border)
              .attr("stroke-width", 1)
              .lower();
  
            // 保存实体位置
            entityBoxes[entity.id] = { x, y, width, height: 20 };
          }
        });
  
        // 绘制关系箭头
        const relationGroup = svg.append("g").attr("class", "relation-group");
  
        // 定义箭头
        const defs = svg.append("defs");
  
        relations.forEach((relation) => {
          const fromBox = entityBoxes[relation.from];
          const toBox = entityBoxes[relation.to];
  
          if (fromBox && toBox) {
            const startX = fromBox.x + fromBox.width / 2;
            const startY = fromBox.y - 5; // 起点上方
            const endX = toBox.x + toBox.width / 2;
            const endY = toBox.y - 5; // 终点上方
            const middleX = (startX + endX) / 2; // 中间点 X 坐标
            const labelY = startY - 5; // 关系类型文字 Y 坐标（箭身正上方）
  
            // 为每种关系定义独立的箭头
            const markerId = `arrowhead-${relation.type}`;
            if (!svg.select(`#${markerId}`).node()) {
              defs
                .append("marker")
                .attr("id", markerId)
                .attr("markerWidth", 4) // 更小的箭头宽度
                .attr("markerHeight", 3) // 更小的箭头高度
                .attr("refX", 0) // 调整箭头位置
                .attr("refY", 1.5)
                .attr("orient", "auto")
                .append("polygon")
                .attr("points", "0 0, 4 1.5, 0 3") // 更小的箭头形状
                .attr("fill", relation.color); // 动态箭头颜色
            }
  
            const d = `
              M${startX},${startY} 
              L${startX},${startY-2} 
              L${endX},${startY-2} 
              L${endX},${endY}
            `;
  
            // 绘制箭头路径
            relationGroup
              .append("path")
              .attr("d", d)
              .attr("stroke", relation.color) // 统一箭身颜色
              .attr("stroke-width", 2)
              .attr("fill", "none")
              .attr("marker-end", `url(#${markerId})`);
  
            // 添加关系类型文字
            relationGroup
              .append("text")
              .attr("x", middleX)
              .attr("y", labelY)
              .attr("font-size", "12px")
              .attr("text-anchor", "middle") // 居中对齐
              .attr("fill", "black")
              .text(relation.type);
          }
        });
      });
  
      return {
        svgRef,
        svgWidth,
        svgHeight,
      };
    },
  };
  </script>
  
  <style>
  .annotation-container {
    width: 800px;
    margin: auto;
    border: 1px solid #ddd;
    position: relative;
  }
  .annotation-svg {
    width: 100%;
    height: 100%;
  }
  </style>
  