<template>
  <div id="chart-container">
    <!-- <div class="header" @click="resetColorIndexFun">清空</div> -->
    <div class="colorSelect">
      <select id="colorSelectOpt" @change="changeColorShow"  v-model="colorSelect">
        <option value="1">volume</option>
        <option value="2">alphanum</option>
        <option value="3">totalsasa</option>
        <option value="4">polarsasa</option>
        <option value="5">apolarsasa</option>
        <option value="6">mlohyden</option>
        <option value="7">malspra</option>
        <option value="8">msoacc</option>
        <option value="9">hydropscore</option>
        <option value="10">propolatoms</option>
        <option value="11">alspdensity</option>
        <option value="12">alphaspmaxdist</option>
        <option value="13">polarityscore</option>
        <option value="14">frame</option>
      </select>
    </div>

    <el-tooltip :content="'minOpacity: ' + minOpacity" placement="top">
      <el-switch
        @change="changeColorShow"
        class="opacitySwitch"
        v-model="minOpacity"
        active-color="#13ce66"
        inactive-color="#ff4949"
        active-value="0.5"
        inactive-value="1">
      </el-switch>
    </el-tooltip>

    <el-slider
      class="sliderClass"
      v-model="opacityK"
      @input="changeColorShow"
      >
    </el-slider>

    <div id="colorTip" class="colorTip">
      volume->
    </div>
    <el-button icon="el-icon-search" circle @click="handleChange"></el-button>
    <!-- <el-input v-model="input" placeholder="请输入内容" class="custom-input"></el-input> -->
    <div
        class="sub_center_center"
        draggable="true"
        @dragstart="scatterSubDragStart"
        v-if="subPlot"
      >
      <svg class="sub_svg">
        <path class="subPath" :d="subPlotPathEnd" fill="rgba(0, 0, 255, 0.5)"></path>
      </svg>
    </div>
    <div id="chart"></div>
    <div id="loading" v-if="loading"><span>loading...</span></div>
    

  </div>
</template>
<script>
import { request } from "@/network/request";
import axios from "axios";
import { quadtree } from "d3";
import { mapState } from "vuex";

const { mapMutations } = require("vuex");
export default {
  name: 'ScatterPlotView',
  data(){
    return {
      value1: "1",
      margin: 10,
      width: 940,
      height: 600,
      data: [],
      quadtree: null,
      svg_item: null,
      nodeList: [],
      painting: false,
      lastPoint: {x:null,y:null},
      beginPoint: {x:null,y:null},
      doubleClick: false,
      pathElement: null,
      cuurentPath: '',
      selectNode: [],
      xScale:null,
      yScale:null,
      xScaleOriginal:null,
      yScaleOriginal:null,
      selectItemFlag: false,
      selectItem: null,
      pointSeries: null,
      zoomFun: null,
      firstMove: 1,
      zoom: null,
      annotations: [],
      ctrlFlag: false,
      pointer: null,
      annotationSeries: null,
      chart: null,
      loading: true,
      maxData: { maxX: 0, maxY: 0 },
      volumeMsg: {minV: 0, maxV: 999},
      chartDom : null,
      currentPath: '',
      subPlot: false,
      subPlotPath:'',
      subPlotPathEnd:'',
      color: '',
      rect: null,
      frameNode: '1_1,40_1,163_1,715_1,725_1,',
      pathList: [],
      pathLabel: '',
      lastTransform: {
        x: 0,
        y: 0,
        k: 1,
      },
      // startColor: 'green',
      // // startColor: 'skyblue',
      // endColor: 'red',
      colorScale: null,
      colorSelect: 1,
      colorNameList: ['','volume','alphanum','totalsasa','polarsasa','apolarsasa','mlohyden','malspra','msoacc','hydropscore','propolatoms','alspdensity','alphaspmaxdist','polarityscore','frame'],
      valueExtent: [[],],
      pointOpacity: 100,
      firstSlider: true,
      densityMap: [],
      opacityK: 50, //密度影响透明度因子
      opacityNear: 2, //邻近透明度因子
      minOpacity: 0.5, //最小透明度
      maxOpacity: 1,  //最大透明度
      maxDensity: 0,
      densityGirdSize: 3, //密度格大小
      input:'',
    }
  },
  mounted(){
    this.initRequire();
  },
  computed:{
    ...mapState([
      "zoomFactor",
      "radius",
      "similarMin",
      "similarMax",
      "scatterPlotFramePocketData",
      "inOrOutDegree",
      "colorIndex",
      "colorList",
      "transformList",
      "currentColor",
    ]),
  },
  methods:{
    ...mapMutations([
      "changZoomFactor",
      "initScatterPlotFramePocketData",
      "changeSimilarMin",
      "changeSimilarMax",
      "changeInOrOutDegree",
      "addColorIndex",
      "subColorIndex",
      "resetColorIndex",
      "popColor",
      "pushColor",
      "pushToTransformList",
    ]),

    async initRequire() {
      let that = this;
      await axios.post('api/forcePlot/index').then((res) => {
          if (res.status === 200) {
            console.log(res.data.data)
            // that.scatterPlotFramePocketData = res.data.data
            that.initScatterPlotFramePocketData(res.data.data); // 初始化数据
            that.maxData["maxX"] = res.data.data["maxX"];
            that.maxData["maxY"] = res.data.data["maxY"];
            that.valueExtent.push([res.data.data["minV"],res.data.data["maxV"]])
            for(var i = 2; i < that.colorNameList.length; i++){
              that.valueExtent.push([res.data.data["min_"+that.colorNameList[i]],res.data.data["max_"+that.colorNameList[i]]]);
            }
            console.log(that.valueExtent)
            that.quadtree = d3
              .quadtree()
              .x(d => d.x)
              .y(d => d.y)
              .addAll(res.data.data.forceData);
            




            
            that.initData();
            that.svg_item = d3.select('d3fc-svg').select('svg')._groups[0][0];
            this.svg_item.classList.add('haha')
            console.log('pop');
            d3.selectAll('svg')._groups[0][8].classList.add('removeItem')
            d3.selectAll('svg')._groups[0][9].classList.add('removeItem')
            document.getElementsByClassName('x-axis')[0].style.opacity = 0;
            document.getElementsByClassName('y-axis')[0].style.opacity = 0;
            that.pathElement = d3.select('.haha').append("path")
            .attr('fill','red')
            .attr('stroke','#ff0000')
            .attr('stroke-width',2);
            that.loading = false;


            that.rect = document.getElementsByClassName('haha')[0].getBoundingClientRect();
            
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async  handleChange(){
      let that = this;
      that.frameNode='1_1,40_1,163_1,715_1,725_1,'
      const inputValue=that.input;
      console.log(inputValue);
      await axios({
        method: 'post',
        url: 'api/forcePlot/select_residue_pocket',
        data: {
          'residue': inputValue
        }
      }).then((res) => {
       
        console.log(that.frameNode)
        console.log('111')
        console.log(res.data.data['select_pocket']);
       
        const language =d=>{
          
        // if(d.frame_pocket in res.data.data['select_pocket'])
        // if(d.frame_pocket in res.data.data['select_pocket']){
          if( res.data.data['select_pocket'].includes(d.frame_pocket)){
            // that.selectNode.push(d)
            // that.frameNode += (d.frame_pocket + ',')
            // console.log(that.frameNode)
            // console.log(that.frameNode)
          // console.log('true')
          console.log(that.frameNode)
          let color='rgb(0, 252, 200)';
          
        let tempColor = color.split('(')[1].split(')')[0].split(',');
        let temp = [];
        tempColor.forEach(item => {
          item = parseInt(item);
          item /= 255;
          // temp.push(item);
          temp.push(item);
        })
        let tempOpacity = ++that.densityMap[Math.floor(that.xScale(d.x) / that.densityGirdSize)][Math.floor(that.yScale(d.y) / that.densityGirdSize)] * that.opacityK / 1000 + parseFloat(that.minOpacity);
        tempOpacity = tempOpacity > that.maxOpacity? that.maxOpacity:tempOpacity;
        // console.log(that.densityMap[Math.floor(that.xScale(d.x))][Math.floor(that.yScale(d.y))] / that.maxDensity);
        // if(that.densityMap[Math.floor(that.xScale(d.x))][Math.floor(that.yScale(d.y))] / that.maxDensity > 0.01){
        //   tempOpacity = that.maxOpacity;
        // }else{
        //   tempOpacity = that.minOpacity;
        // }
        

        temp.push(tempOpacity);
        // console.log(temp);
        // console.log(temp);
        return temp;
        }
        let color = that.colorScale(Math.pow(d.volume,1/2));
        let tempColor = color.split('(')[1].split(')')[0].split(',');
        let temp = [];
        tempColor.forEach(item => {
          item = parseInt(item);
          item /= 255;
          // temp.push(item);
          temp.push(item);
        })
        let tempOpacity = ++that.densityMap[Math.floor(that.xScale(d.x) / that.densityGirdSize)][Math.floor(that.yScale(d.y) / that.densityGirdSize)] * that.opacityK / 1000 + parseFloat(that.minOpacity);
        tempOpacity = tempOpacity > that.maxOpacity? that.maxOpacity:tempOpacity;
     

        temp.push(tempOpacity);
        // console.log(temp);
        // console.log(temp);
        return temp;

      }
      
     
      //使用fc.weblFillColor()创建一个新的颜色访问器，并将其传递给点序列的 decorate() 方法。
      console.log(that.scatterPlotFramePocketData["forceData"])

      const fillColor = fc.webglFillColor().value(language).data(that.scatterPlotFramePocketData["forceData"]);
      
      // const fillColor1 = fc.webglFillColor().value(language).data(that.scatterPlotFramePocketData["forceData"]);
      //这行代码使用 .decorate() 方法修改 WebGL 点序列的绘制程序。这里的修改是将填充颜色设置为 fillColor 生成的颜色。
      that.pointSeries.decorate(program => {fillColor(program)});
      })
      console.log(that.frameNode)
    },
    
    initData(){
      
      let that = this;
      // 定义颜色范围
      // that.startColor = "#90EE90";
      that.startColor = "#1E90FF";
      // that.endColor = "#87CEEB";
      that.endColor = "red";
      // 创建颜色比例尺

      // that.colorScale = d3.scaleSequential(d3.interpolateHclLong("#1E90FF", "red"))
      // .domain([Math.log(1 + that.valueExtent[that.colorSelect][0]),Math.log(1 + that.valueExtent[that.colorSelect][1])]);


      that.colorScale = d3.scaleLinear()
      .domain([Math.pow(that.valueExtent[that.colorSelect][0],1/2),Math.pow(that.valueExtent[that.colorSelect][1],1/2)])
      .range([that.startColor, that.endColor]);
      that.chartDom = d3.select('#chart');



      const colorSvg = d3.select('#colorTip');
      // console.log(d3.range(that.volumeMsg['minV'], that.volumeMsg['maxV'], 10));
      // colorSvg.append("defs")
      //       .append("linearGradient")
      //       .attr("id", "gradient")
      //       .attr("x1", "0%")
      //       .attr("y1", "0%")
      //       .attr("x2", "100%")
      //       .attr("y2", "0%")
      //       .selectAll("stop")
      //       .data(d3.range(that.volumeMsg['minV'], that.volumeMsg['maxV'], 10))
      //       .enter().append("stop")
      //       .attr("offset", d => `${d * 100}%`)
      //       .attr("stop-color", d => colorScale(d));

      //   // Draw the rectangle filled with the gradient
      //   colorSvg.append("rect")
      //       .attr("width", 150)
      //       .attr("height", 50)
      //       .style("fill", "url(#gradient)");

      document.getElementById('chart').addEventListener("click",that.itemClick);
      // that.chartDom.attr('width',that.width - 2 * that.margin).attr('height',that.height - 2 * that.margin).attr('transform',`translate(${[that.margin, that.margin]})`)
      that.xScale = d3.scaleLinear().domain([-that.maxData["maxX"], that.maxData["maxX"]]).range([0,that.width]);
      that.yScale = d3.scaleLinear().domain([-that.maxData["maxY"], that.maxData["maxY"]]).range([0,that.height]);
      that.xScaleOriginal = that.xScale.copy();
      that.yScaleOriginal = that.yScale.copy();


      //初始化密度图
      that.initDensityMap();

      that.selectItemFlag = false;
      that.pointSeries = fc
        .seriesWebglPoint()
        .size(3)
        .crossValue(d => d.x)
        .mainValue(d => d.y);


      const languageFill = d =>{
        let color = that.colorScale(Math.pow(d.volume,1/2));
        let tempColor = color.split('(')[1].split(')')[0].split(',');
        let temp = [];
        tempColor.forEach(item => {
          item = parseInt(item);
          item /= 255;
          // temp.push(item);
          temp.push(item);
        })
        // let tempOpacity;
        //根据密度的透明度计算
        let tempOpacity = ++that.densityMap[Math.floor(that.xScale(d.x) / that.densityGirdSize)][Math.floor(that.yScale(d.y) / that.densityGirdSize)] * that.opacityK / 1000 + parseFloat(that.minOpacity);
        tempOpacity = tempOpacity > that.maxOpacity? that.maxOpacity:tempOpacity;
        // console.log(that.densityMap[Math.floor(that.xScale(d.x))][Math.floor(that.yScale(d.y))] / that.maxDensity);
        // if(that.densityMap[Math.floor(that.xScale(d.x))][Math.floor(that.yScale(d.y))] / that.maxDensity > 0.01){
        //   tempOpacity = that.maxOpacity;
        // }else{
        //   tempOpacity = that.minOpacity;
        // }
        

        temp.push(tempOpacity);
        // console.log(temp);
        return temp;
      };
      const fillColor = fc.webglFillColor().value(languageFill).data(that.scatterPlotFramePocketData["forceData"]);
      that.pointSeries.decorate(program => {fillColor(program)});

      that.zoomFun = (event) => {
        
        that.xScale.domain(d3.event.transform.rescaleX(that.xScaleOriginal).domain());
        that.yScale.domain(d3.event.transform.rescaleY(that.yScaleOriginal).domain());
        
        that.drawScatter();
        this.lastTransform = d3.event.transform;
        let i = -1;
        console.log(d3.selectAll('.highlightRoot')['_groups'][0].length);
        if(d3.selectAll('.highlightRoot')['_groups'][0].length != 0){
          d3.selectAll('.highlightRoot').attr('transform',d => {
            i += 1;
            return `translate(${d3.event.transform.x-this.transformList[i].x*(d3.event.transform.k/this.transformList[i].k)},${d3.event.transform.y-this.transformList[i].y*(d3.event.transform.k/this.transformList[i].k)}) scale(${d3.event.transform.k/this.transformList[i].k})`;
          });
        }
        
      }

      that.zoom = d3
        .zoom()
        .scaleExtent([0.01, 400])
        .on('zoom',that.zoomFun);

      that.pointer = fc.pointer().on('point',([coord]) => {
        if(!coord || !that.quadtree){
          return;
        }
        const x = that.xScale.invert(coord.x);
        const y = that.yScale.invert(coord.y);
        const radius = Math.abs(that.xScale.invert(coord.x) - that.xScale.invert(coord.x - 20));
        const closestDatum = that.quadtree.find(x, y, radius);
        if(closestDatum){
          that.selectItemFlag = true;
          that.selectItem = closestDatum;
          that.annotations[0] = that.createAnnotationData(closestDatum);
        }else{
          that.selectItemFlag = false;
        }
        that.drawScatter();
      });


      //切换圈选
      d3.select('body')
      .on('keydown',() => {
        if(d3.event.keyCode == 17){
          if(that.ctrlFlag){
            that.painting = false;
            that.nodeList = [];
            that.selectNode = [];
            console.log('on');
            that.zoom.on('zoom',that.zoomFun);
            that.svg_item.removeEventListener('mousedown',that.mouseDownFun);
            that.svg_item.removeEventListener('mousemove',that.mouseMoveFun);
            // svg_item.removeEventListener('mouseup',mouseUpFun);
            document.getElementById('chart').addEventListener("click",that.itemClick);
            that.currentPath = "";
            that.pathElement.attr('d',that.currentPath);
            // d3.selectAll('.highlightRoot')['_groups'][0].forEach(element => {
            //   element.remove();
            // });
          }else{
            console.log('close');
            that.svg_item.addEventListener('mousedown',that.mouseDownFun);
            that.svg_item.addEventListener('mousemove',that.mouseMoveFun);
            document.getElementById('chart').removeEventListener("click",that.itemClick);
            // svg_item.addEventListener('mouseup',mouseUpFun);
            that.zoom.on('zoom',null);
            
          }
          that.ctrlFlag =!that.ctrlFlag;
        }else if(d3.event.keyCode == 16){
          that.subPlot = !that.subPlot;
        }
      });

    //绑定元素点击事件



    that.annotationSeries = that.seriesSvgAnnotation()
      .notePadding(15)
      .type(d3.annotationCallout);
    
    that.chart = fc
      .chartCartesian(that.xScale,that.yScale)
      .webglPlotArea(
        fc
        .seriesWebglMulti()
        .series([that.pointSeries])
        .mapping(d => {
          return d.dat;
        })
      )
      .svgPlotArea(
        fc
        .seriesSvgMulti()
        .series([that.annotationSeries])
        .mapping(d => {
          return d.anno;})
      )
      .decorate(sel => {
        sel
        .enter()
        .select("d3fc-svg.plot-area")
        .on("measure.range",() => {
          that.xScaleOriginal.range([0, d3.event.detail.width]);
          that.yScaleOriginal.range([d3.event.detail.height, 0]);
        })
        .call(that.zoom)
        .call(that.pointer)
      });

      this.drawScatter();

    },
    drawScatter(){
      let anno = this.annotations;
      let dat = this.scatterPlotFramePocketData["forceData"];
      
      d3.select('#chart').datum({anno,dat}).call(this.chart);
      
    },
    createAnnotationData(dataPoint){
      let fp = dataPoint.frame_pocket;
      let px = dataPoint.x;
      let py = dataPoint.y;
      return {
        note: {
          label: fp,
          bgPadding: 5,
        },
        x: px,
        y: py,
        dx: 20,
        dy: 20
      }
    },
    webglColor(color){
      const { r, g, b, opacity } = d3.color(color).rgb();
      return [r / 255, g / 255, b / 255, opacity];
    },
    seriesSvgAnnotation(){
      // the underlying component that we are wrapping
      const d3Annotation = d3.annotation();

      let xScale = d3.scaleLinear();
      let yScale = d3.scaleLinear();

      const join = fc.dataJoin("g", "annotation");

      const series = selection => {
        selection.each((data, index, group) => {
          const projectedData = data.map(d => ({
            ...d,
            x: xScale(d.x),
            y: yScale(d.y)
          }));

          d3Annotation.annotations(projectedData);

          join(d3.select(group[index]), projectedData).call(d3Annotation);
        });
      };

      series.xScale = (...args) => {
        if (!args.length) {
          return xScale;
        }
        xScale = args[0];
        return series;
      };

      series.yScale = (...args) => {
        if (!args.length) {
          return yScale;
        }
        yScale = args[0];
        return series;
      };

      fc.rebindAll(series, d3Annotation);

      return series;
    },
    itemClick(e){
      if(e.button == 0){
        if(this.selectItemFlag){
          this.$emit("scatterShowMol", this.selectItem);
          this.selectItemFlag = false;
        }
      }
    },
    mouseDownFun(e){
      if(this.doubleClick){
      //绘制最后一段线
      this.currentPath += 'L' + this.beginPoint.x + ',' + this.beginPoint.y;
      this.subPlotPath += 'Z';
      this.pathLabel += 'Z';
      this.pathElement.attr('d',this.currentPath);


      this.painting = false;
      console.log('end');
      let x1,y1,x2,y2;
      x1=y1=9999;
      x2=y2=0;
      for(var i = 0;i < this.nodeList.length;i++){
        if(this.nodeList[i][0] < x1){
          x1 = this.nodeList[i][0];
        }
        if(this.nodeList[i][0] > x2){
          x2 = this.nodeList[i][0];
        }
        if(this.nodeList[i][1] < y1){
          y1 = this.nodeList[i][1];
        }
        if(this.nodeList[i][1] > y2){
          y2 = this.nodeList[i][1];
        }
      }
      x1 = this.xScale.invert(x1);
      x2 = this.xScale.invert(x2);
      y1 = this.yScale.invert(y1);
      y2 = this.yScale.invert(y2);

      for(var i = 0;i < this.nodeList.length;i++){
        this.nodeList[i][0] = this.xScale.invert(this.nodeList[i][0]);
        this.nodeList[i][1] = this.yScale.invert(this.nodeList[i][1]);
      }

      this.quadtree.visit((node,x3,y3,x4,y4) => {
        if(!node.length){
          do{
            let d = node.data;
            // if(d3.polygonContains(nodeList,[d['x'],d['y']])){
            //   selectNode.push(d)
            // }
            if(d['x'] >= x1 && d['x'] < x2 && d['y'] < y1 && d['y'] >= y2){
              this.selectNode.push(d)
            }

          }while(node = node.next);
        }
        return false;
      });
      let templist = [];
      let countMap = new Map();
      let mostColor = '';
      let maxCount = 0;
      for(var i  = 0;i < this.selectNode.length;i++){
        if(d3.polygonContains(this.nodeList,[this.selectNode[i]['x'],this.selectNode[i]['y']])){
          templist.push(this.selectNode[i])
          if(countMap.has(this.selectNode[i].color)){
            countMap.set(this.selectNode[i].color,countMap.get(this.selectNode[i].color) + 1);
          }else{
            countMap.set(this.selectNode[i].color,1);
          }
          if(countMap.get(this.selectNode[i].color) > maxCount){
            maxCount = countMap.get(this.selectNode[i].color);
            mostColor = this.selectNode[i].color;
          }

          this.frameNode += (this.selectNode[i].frame_pocket + ',')
        }
      }
      this.frameNode = this.frameNode.slice(0,-1);
      console.log(this.frameNode);
      this.color = mostColor;
      this.drawSubPlot();
      console.log(this.selectNode);
      }else{
        
        this.frameNode = '';
        this.nodeList = [];
        this.selectNode = [];
        console.log(this.selectNode)
        this.painting = true;
        // ctx.clearRect(0,0,svg_item.style.width,svg_item.style.height);
        console.log('clear');
     
        let x = e.clientX - document.getElementsByClassName('haha')[0].getBoundingClientRect().x;
        let y = e.clientY - document.getElementsByClassName('haha')[0].getBoundingClientRect().y;
        this.lastPoint.x = x;
        this.lastPoint.y = y;
        this.beginPoint.x = x;
        this.beginPoint.y = y;
        this.nodeList.push([x,y]);
        this.$alertselectNode = [];
        // drawCircle(x,y,3);

        //记录起始点并开始加载path
        this.currentPath = 'M' + x + ',' + y;
        this.subPlotPath = 'M' + parseInt(200 / this.rect.width * x) + ',' + parseInt(100 / this.rect.height * y);
        this.pathLabel = 'M' + x + ',' + y;
      }
      this.doubleClick = !this.doubleClick;
    },
    mouseMoveFun(e){
      if(this.painting){
        let x = e.clientX - document.getElementsByClassName('haha')[0].getBoundingClientRect().x;
        let y = e.clientY - document.getElementsByClassName('haha')[0].getBoundingClientRect().y;
        this.nodeList.push([x,y]);
        console.log('move');
        this.currentPath += 'L' + x + ',' + y;
        this.subPlotPath += 'L' + parseInt(200 / this.rect.width * x) + ',' + parseInt(100 / this.rect.height * y);
        this.pathLabel += 'L' + x + ',' + y;
        this.pathElement.attr('d',this.currentPath);
        this.lastPoint.x = e.clientX - document.getElementsByClassName('haha')[0].getBoundingClientRect().x;
        this.lastPoint.y = e.clientY - document.getElementsByClassName('haha')[0].getBoundingClientRect().y;
        this.currentPath += 'M' + this.lastPoint.x + ',' + this.lastPoint.y;
      }
    },
    drawSubPlot(){
      this.subPlotPathEnd = this.subPlotPath;

    },
    resetColorIndexFun(){
      this.resetColorIndex();
      this.transformList.length = 0;
      this.pathList.length = 0;
      d3.selectAll('.highlightRoot').remove();
    },
    async circleLinkLine(nodes) {
      let that = this;
      await request({
        url: "/forcePlot/linkLine", //
        method: "POST", //
        data: {
          frame_pocket: nodes, //
          similarMin: that.similarMin, // that.state.similar
          similarMax: that.similarMax, // that.state.similar
        },
      })
        .then((res) => {
          // 请求成功
          if (res.status === 200) {
            // 后端处理得到的 度data["degree"] 信息没用到
            // data["link"] 是包含 [source,target] 的二维数组
            // that.drawLinkLine(res.data.data["link"]);
            console.log(res.data.data["link"]);
            console.log(this.quadtree.find(1,1,20));
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    changeRgbToRgba(str){
      str = str.replace('rgb','rgba');
      str = str.slice(0,-1) + ',0.6' + str.slice(-1);
      return str;
    },
    scatterSubDragStart(event) {
      let that = this;
      
      //重设颜色
      // that.startColor = 'yellow';

      // that.colorScale = d3.scaleLinear()
      // .domain([that.volumeMsg['minV'], that.volumeMsg['maxV']])
      // .range([that.startColor, that.endColor]);

      // const languageFill = d =>{
      //   let color = that.colorScale(d.volume);
      //   let tempColor = color.split('(')[1].split(')')[0].split(',');
      //   let temp = [];
      //   tempColor.forEach(item => {
      //     item = parseInt(item);
      //     item /= 255;
      //     temp.push(item);
      //   })
      //   temp.push(1.0);
      //   // console.log(temp);
      //   return temp;
      // };
      // const fillColor = fc.webglFillColor().value(languageFill).data(that.scatterPlotFramePocketData["forceData"]);
      // that.pointSeries.decorate(program => {fillColor(program)});




      that.popColor();
      that.firstMove = 1;
      let rgbaColor = this.changeRgbToRgba(that.currentColor);
      that.pushToTransformList(that.lastTransform);
      let tempPath = d3.select('.haha').append("path")
      .attr('d',that.pathLabel)
      .attr('fill',rgbaColor)
      .attr('class','highlightRoot');
      tempPath._groups[0][0].classList.add('svgArea'+that.currentColor.slice(5,-1).replaceAll(',',''));
      that.pathList.push(tempPath);
      event.dataTransfer.setData('color',that.currentColor);
      event.dataTransfer.setData("identify", "scatter"); 
      event.dataTransfer.setData('valueExtent',that.valueExtent);
      
      event.dataTransfer.setData(
        "framePocket",
        this.frameNode
      );
      event.dataTransfer.setData('pathStr',that.currentPath);
    },
    changeColorShow(e){
      console.log('iioo'+this.minOpacity);
      let that = this;
      that.densityMap = [];
      that.initDensityMap();
      if(that.firstSlider){
        that.firstSlider = false;
        return;
      }
      document.getElementById('colorTip').innerHTML = that.colorNameList[that.colorSelect] + '->';


      if(parseInt(that.colorSelect) == 14 ){
        console.log('切换到体积了')
        that.colorScale = d3.scaleLinear()
        .domain([that.valueExtent[that.colorSelect][0],that.valueExtent[that.colorSelect][1]])
        .range([that.startColor,that.endColor]);
      }
      else if(parseInt(that.colorSelect) == 1){
        that.colorScale = d3.scaleLinear()
        .domain([Math.pow(that.valueExtent[that.colorSelect][0],1/2),Math.pow(that.valueExtent[that.colorSelect][1],1/2)])
        .range([that.startColor,that.endColor]);
      }
      else {
        console.log('此处做过更改,貌似疏水性有负值不太行')
        that.colorScale = d3.scaleLinear()
            .domain([1 + that.valueExtent[that.colorSelect][0] + Math.abs(that.valueExtent[that.colorSelect][0]),1 + that.valueExtent[that.colorSelect][1] + Math.abs(that.valueExtent[that.colorSelect][0])])
          //  .domain([Math.pow(that.valueExtent[that.colorSelect][0],1/2),Math.pow(that.valueExtent[that.colorSelect][1],1/2)])
        .range([that.startColor,that.endColor]);
      }
      
      





      // that.colorScale = d3.scaleSequential(d3.interpolateHclLong("#1E90FF", "red"))
      // .domain([Math.log( 1 + that.valueExtent[that.colorSelect][0] + Math.abs(that.valueExtent[that.colorSelect][0])),Math.log(1 + that.valueExtent[that.colorSelect][1] + Math.abs(that.valueExtent[that.colorSelect][0]))]);



      const languageFill = d =>{
        let tempValue;
        switch(parseInt(that.colorSelect)){
          case 1:
            tempValue = d.volume;
            break;
          case 2:
            tempValue = d.alphanum;
            break;
          case 3:
            tempValue = d.totalsasa;
            break;
          case 4:
            tempValue = d.polarsasa;
            break;
          case 5:
            tempValue = d.apolarsasa;
            break;
          case 6:
            tempValue = d.mlohyden;
            break;
          case 7:
            tempValue = d.malspra;
            break;
          case 8:
            tempValue = d.msoacc;
            break;
          case 9:
            tempValue = d.hydropscore;
            break;
          case 10:
            tempValue = d.propolatoms;
            break;
          case 11:
            tempValue = d.alspdensity;
            break;
          case 12:
            tempValue = d.alphaspmaxdist;
            break;
          case 13:
           tempValue = d.polarityscore;
            break;
          case 14:
            tempValue = d.frameID;
            break;
        }
        if(parseInt(that.colorSelect) == 14 ){
          tempValue = tempValue;
        }
         else if(parseInt(that.colorSelect) == 1){
           tempValue = Math.pow(tempValue,1/2)
         }

        else{
          //  tempValue = tempValue;
          tempValue = 1 + tempValue + Math.abs(that.valueExtent[that.colorSelect][0]);
        }
        
          //  let color = that.colorScale(Math.pow(tempValue,1/2));
               let color = that.colorScale(tempValue);
        let tempColor = color.split('(')[1].split(')')[0].split(',');
        let temp = [];
        tempColor.forEach(item => {
          item = parseInt(item);
          item /= 255;
          temp.push(item);
        })
        // let tempOpacity;
        //根据密度的透明度计算
        let tempOpacity = ++that.densityMap[Math.floor(that.xScaleOriginal(d.x) / that.densityGirdSize)][Math.floor(that.yScaleOriginal(d.y) / that.densityGirdSize)] * that.opacityK / 1000 + parseFloat(that.minOpacity);
        tempOpacity = tempOpacity > that.maxOpacity? that.maxOpacity:tempOpacity;
        // console.log(that.densityMap[Math.floor(that.xScale(d.x))][Math.floor(that.yScale(d.y))] / that.maxDensity);
        // if(that.densityMap[Math.floor(that.xScale(d.x))][Math.floor(that.yScale(d.y))] / that.maxDensity > 0.01){
        //   tempOpacity = that.maxOpacity;
        // }else{
        //   tempOpacity = that.minOpacity;
        // }
        temp.push(tempOpacity);
        // console.log(temp);
        return temp;
      };

      const fillColor = fc.webglFillColor().value(languageFill).data(that.scatterPlotFramePocketData["forceData"]);
      that.pointSeries.decorate(program => {fillColor(program)});

      that.drawScatter();


    },

    initDensityMap(){
      let that = this;
      let maxDensity = 0;
      if(that.densityMap.length == 0){
        //初始化密度图
        for(var i = 0;i < Math.floor(that.width / that.densityGirdSize);i++){
          that.densityMap.push([]);
          for(var j = 0;j < Math.floor(that.height / that.densityGirdSize);j++){
            that.densityMap[i].push(0);
          }
        }
        // that.scatterPlotFramePocketData.forceData.forEach((item,index) => {
        //   // console.log(item);
        //   // console.log(that.xScale(item.x),that.yScale(item.y));
        //   that.densityMap[Math.floor(that.xScale(item.x) / that.densityGirdSize)][Math.floor(that.yScale(item.y) / that.densityGirdSize)] += 1;
        //   // maxDensity = maxDensity > that.densityMap[Math.floor(that.xScale(item.x))][Math.floor(that.yScale(item.y))]?maxDensity:that.densityMap[Math.floor(that.xScale(item.x))][Math.floor(that.yScale(item.y))];
        // });
      }
      

      
      // that.maxDensity = maxDensity;
      // console.log('maxDensity',maxDensity);
    }

  }
}
</script>
<style scoped>
.custom-input {
  /* 你的自定义样式 */
  width: 200px;
  /* border: 2px solid #409EFF; */
  border-radius: 4px;
  padding: 10px;
}
  #chart-container{
    width: 740px;
    height: 430px;
    position: relative;
  }
  #chart{
    width: 900px;
    height: 600px;
  }
  .x-axis{
    display: none;
  }
  .sub_center_center{
    position: absolute;
    right: 40px;
    width:200px;
    height: 100px;
    border: 1px solid #000000;
    z-index: 2;
  }
  .sub_svg{
    width: 100%;
    height: 100%;
  }
  .header{
    position: relative;
    width: 50px;
    height: 30px;
    text-align: center;
    border: 1px solid #ffffff;
    background-color: cornflowerblue;
    color: #ffffff;
    cursor: pointer;
  }
  .colorTip{
    width: 300px;
    height: 20px;
    position: absolute;
    top: 0px;
    right: 50px;
    background: linear-gradient(to right, #1E90FF 0%,red 100%);
    line-height: 20px;
    padding-left: 2px;
    font-size: 0.7em;
    color: rgba(255,255,255,0.8);
  }
  .colorSelect{
    width: 130px;
    height: 30px;
    position: absolute;
    top: -5px;
    right: 370px;
  }
  #colorSelectOpt{
    width: 130px;
    height: 30px;
  }
  #colorSelectOpt option{
    line-height: 30px;
  }


  .sliderClass{
    position: relative;
    top: -9px;
    left: 50px;
    width: 150px;
  }
  .opacitySwitch{
    position: absolute;
  }


  #loading{

  }
</style>