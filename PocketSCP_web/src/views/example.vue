<template>
  <div id="chart">
    <svg width="800" height="600">
      <g id="content" transform="translate(10,10)">
        <!-- 这里可以放置你的图形元素 -->
        <circle cx="687.8247649262615" cy="534.2200409133739" r="1" fill="rgba(72,117,207,1)"></circle>
      </g>
    </svg>
  </div>
</template>


<script>
import * as d3 from 'd3';

export default {
  name: 'ScatterPlotsvgView',
  mounted() {
    this.initPan();
  },
  methods: {
    initPan() {
      const svg = d3.select('#chart').select('svg');
      const g = svg.select('#content');

      // 创建缩放行为
      const zoom = d3.zoom()
        .on('zoom', (event) => {
          g.attr('transform', event.transform);
        });

      // 应用缩放行为到 SVG 元素
      svg.call(zoom);
    }
  }
};
</script>

<style scoped>
svg {
  border: 1px solid black;
}
</style>