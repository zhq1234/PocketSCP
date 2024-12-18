<template>
  <div :class="barClass" @drop="timeLineDrop" @dragover.prevent>
    <div :id="barClass + '_text'" style="margin-left: 10px;">The current frame is: 0</div>
    <div class="load" v-if="loading">loading...</div>
  </div>
</template>

<script>
import { request } from "@/network/request";
import axios from "axios";

const { mapActions, mapState,mapMutations } = require("vuex");

export default {
  name: "BarPlotView",
  // bars=[{barClass,barData,barName,barColor}]
  props: { bar: undefined },

  data() {
    let width = 450,
      height = 230,
      margin = 10;
    return {
      barClass: "bar" + this.bar.barClass,
      frame: [], // 接收拖入的数据
      // framePocket: "1_1",
      framePocketStr: "", // 滑块数据
      barColors: [],
      width,
      height,
      margin,
      chartWidth: width - margin * 2,
      chartHeight: height - margin,
      barWidth: 10,
      legend: null, // 图例
      loading: true,
      svg: "",
      chart: "",
      frameVolume: [],
      tempColor: '',
      index: 0,
      linePathList: [],
      lineEnable: true,
      dotEnable: true,
      barEnabel: true,
      frame_pocketTemp: [],
      tempData: [],
      dataList: [],
      same_frame: []
    };
  },
  created() {
    let that = this;
    that.frame.push(that.bar.barData);
    that.frame_pocketTemp = that.bar.barData;
    that.barColors.push(that.bar.barColor);
  },
  mounted() {
    this.initData();
  },
  computed:{
    ...mapState([
      "lineAniFlag",
      "lineFlag",
      "scatterPlotFlag",
      
    ]),
  },
  methods: {
    ...mapActions(["highlightScatter","changeLineFlag","changeScatterplotFlag","showAreaPlot"]),
    ...mapMutations(["updateAreaData"]),
    initData() {
      let that = this;
      // that.cross = "M0,0 L15,15 M15,0 L0,15";
      // that.zoomStr =
      //   "M919.264 905.984l-138.912-138.912C851.808 692.32 896 591.328 896 480c0-229.376-186.624-416-416-416S64 250.624 64 480s186.624 416 416 416c95.008 0 182.432-32.384 252.544-86.208l141.44 141.44a31.904 31.904 0 0 0 45.248 0 32 32 0 0 0 0.032-45.248zM128 480C128 285.92 285.92 128 480 128s352 157.92 352 352-157.92 352-352 352S128 674.08 128 480z M625.792 448H512v-112a32 32 0 0 0-64 0V448h-112a32 32 0 0 0 0 64H448v112a32 32 0 1 0 64 0V512h113.792a32 32 0 1 0 0-64z";
      that.initRequire();
    },
    // 数据请求
    async initRequire() {
      let that = this;
      console.log('yuyuyu',that.frame);
      await axios({
        method: 'post',
        url: 'api/molStar/frame_bar',
        data: {
          'frame_pocket': that.frame
          
        }
      }).then((res) => {
          if (res.status === 200) {
            that.frameMap = res.data.data["frameMap"]; // frame_framePocket_dict 帧——口袋的映射 一帧可能对应几个不同的口袋
            that.clusterBar = res.data.data["clusterBar"]; // 表示有多少簇 clusterBar : 1

            that.frameExtent = res.data.data["frameExtent"]; // 数据帧范围 frameExtent : [2, 86]
            that.maxValue = res.data.data["maxVolume"]; // maxVolume: 353.147
            that.maxDis = res.data.data["maxDis"]; // 质心——阿尔法球的最大距离 中的最大值
            that.barData = res.data.data["barData"]; // 每一帧的各个属性值
            
            that.tempData = [];
            that.barData.forEach(item => {
              if(that.frame_pocketTemp.indexOf(item.frame_pocket) != -1){
                
                that.tempData.push(item)
              }
            });
            
            that.dataList.push(that.tempData);
            
            //找出重复帧
            function compare(arr1, arr2) {
              return arr1.filter((v) => {
                return arr2.indexOf(v) !== -1;
              });
            }

            if(that.dataList.length > 1){
              let arr1 = [];
              let arr2 = [];
              that.same_frame = [];
              that.dataList[0].forEach(item => {
                arr1.push(item.frame_pocket.split('_')[0]);
              });
              that.dataList[1].forEach(item => {
                arr2.push(item.frame_pocket.split('_')[0]);
              });
              that.same_frame = compare(arr1,arr2);
              
            }
            console.log(that.same_frame);
            
            // 表示每组的宽度
            that.barWidth =
              (that.width - that.margin * 4.5) /
              (that.frameExtent[1] - that.frameExtent[0]);
            // console.log("that.frameExtent ", that.frameExtent)
            that.drawChart();
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    findItem(frameStr){
      let tempItem;
      this.barData.forEach(item => {
        if(item.frame_pocket == frameStr){
          console.log(item,'iiii');
          tempItem = item;
          return;
        }
      });
      return tempItem;
    },
    drawChart() {
      // if(d3.selectAll('circle')){
      //   d3.selectAll('circle').remove();
      // }
      let that = this;
      // console.log(that.maxValue, that.maxDis);
      that.svg = d3
        .select("." + that.barClass)
        .selectAll("svg." + that.barClass + "timeLineSvg")
        .data([1])
        .join("svg")
        .attr("class", that.barClass + "timeLineSvg")
        .attr("width", that.width)
        .attr("height", that.height)
        .style("border-radius", "10px");

      // .attr("transform", `translate(${[that.margin, 0]})`)

      that.chart = that.svg
        .selectAll("g.timeLineChart")
        .data([1])
        .join("g")
        .attr("transform", `translate(${[that.margin * 2 - 10, that.margin]})`)
        .attr("class", "timeLineChart");
      // that.chart.append("rect").attr("width", that.chartWidth - that.margin * 2).attr("height", that.chartHeight - that.margin * 2).style("fill", "#a83f3f")
      let timeLineScaleLinearAxisBottom = d3
        .scaleLinear()
        .range([0, that.chartWidth - that.margin * 2])
        .domain(d3.extent(that.frameExtent)); // 线性比例尺
      let timeLineScaleLinearAxisLeft = d3
        .scaleLinear()
        .range([0, that.chartHeight - that.margin * 2])
        .domain([that.maxValue, 0]); // 用于绘制体积柱状图的比例尺
      let timeLineScaleLinearAxisRight = d3
        .scaleLinear()
        .range([0, that.chartHeight - that.margin * 2])
        .domain([that.maxDis, 0]); // 用于绘制最大距离柱状图的比例尺
      let timeLineAxisBottom = d3
        .axisBottom(timeLineScaleLinearAxisBottom)
        .tickValues(d3.extent(that.frameExtent))
        .tickSize(that.margin / 2); // 刻度点
      let timeLineAxisLeft = d3
        .axisLeft(timeLineScaleLinearAxisLeft)
        .tickSize(2); // 刻度点
      let timeLineAxisRight = d3
        .axisRight(timeLineScaleLinearAxisRight)
        .tickSize(2); // 刻度点
      // let timeLineAxisColorScale = d3.scaleSequential(d3.interpolateRainbow).domain([0, that.clusterBar]) // 填充颜色

      // 坐标轴位置
      that.chart
        .selectAll("g.axisBottom")
        .data([1])
        .join("g")
        .attr(
          "transform",
          `translate(${[15, that.chartHeight - that.margin * 2]})`
        )
        .attr("class", "axisBottom")
        .call(timeLineAxisBottom);
      that.chart
        .selectAll("g.axisLeft")
        .data([1])
        .join("g")
        .attr("class", "axisLeft")
        .call(timeLineAxisLeft)
        .attr("transform", `translate(${[15, 0]})`);
      // that.chart.selectAll("g.axisRight").data([1]).join("g").attr("transform", `translate(${[that.chartWidth - that.margin * 1.8, 0]})`).attr("class", "axisRight").call(timeLineAxisRight);
      // 边框
      that.chart
        .selectAll("g.timeLine_chart_border")
        .data([1])
        .join("g")
        .attr(
          "transform",
          `translate(${[15, that.chartHeight - that.margin * 2]})`
        )
        .attr("class", "timeLine_chart_border")
        .selectAll("rect")
        .data([1])
        .join("rect")
        .attr("id", "timeLine_chart_border")
        .attr("rx", that.margin / 2)
        .attr("width", that.chartWidth - that.margin * 2) // 滑动条宽度
        .attr("height", that.margin) // 滑动条高度
        .style("stroke-width", 1)
        .style("stroke", "black")
        .attr("fill", "none");
      let rectBarChart = that.chart
        .selectAll("g.rectBar")
        .data([1])
        .join("g")
        .attr("transform", `translate(${[0, 0]})`)
        .attr("class", "rectBar");
      // 绘制柱状图
      that.chart
        .selectAll("rect.bar")
        .data(that.barData)
        .join("rect")
        .attr(
          "class",
          (d) =>
            "bar " +
            "cluster" +
            that.bar.barClass +
            " cluster_" +
            d["j"] +
            that.bar.barClass
        )
        .attr("id", (d) => {
          return "bar_" + d["frame_pocket"];
        })
        .attr(
          "x",
          (d) =>
            d["i"] * that.barWidth +
            (that.barWidth / that.clusterBar) * d["j"] +
            15
        )
        .attr(
          "y",
          (d) =>
            that.chartHeight -
            timeLineScaleLinearAxisLeft(that.maxValue - d["volume"]) -
            that.margin * 2
        )
        .attr("width", that.barWidth / that.clusterBar) // 宽度为
        .attr("height", (d) =>
          timeLineScaleLinearAxisLeft(that.maxValue - d["volume"])
        )
        .style("fill", (d) => {
          return that.barColors[d["j"]];})
        .style("opacity", 1)
        .on("click", that.barClick)
        .on("mouseenter", "")
        .on("mouseleave", "");

      
        console.log('that.same_frame.length:',that.same_frame.length);
        

      if(that.same_frame.length != 0){
        //绘制下方重叠区域
        that.chart
        .selectAll(".same_bar")
          .data(that.same_frame)
          .enter().append("rect")
          .attr("class","same_bar")
          .attr(
            "x",
            (d) =>{
              
              return (parseInt(d) - that.frameExtent[0]) * that.barWidth +
              (that.barWidth / that.clusterBar) * 0 +
              15;
            }
              
          )
          .attr(
          "y",
          (d) => {
            console.log(that.chartHeight -
            timeLineScaleLinearAxisLeft(that.maxValue) -
            that.margin * 2);
            
            return that.chartHeight -
            timeLineScaleLinearAxisLeft(that.maxValue) -
            that.margin * 2;
          }
            
        )
          .attr("width", that.barWidth / that.clusterBar) // 宽度为
          .attr("height", (d) =>
            10
          )
          .style("fill", (d) => {
            return 'rgb(0,0,0)';
          })
          .style("opacity", 1);
      }
      
    
    


      // 绘制最大距离的折线图
      const line = d3.line()
        .x(d => {
          if(d['j'] == 0){
            return d["i"] * that.barWidth +
            (that.barWidth / that.clusterBar) * d["j"] +
            15;  
          }
          
          return d["i"] * that.barWidth +
            (that.barWidth / that.clusterBar) * d["j"] +
            15;
        })
        .y(d => {
          return that.chartHeight -
            timeLineScaleLinearAxisLeft(that.maxValue - d["volume"]) -
            that.margin * 2;
        })
        .curve(d3.curveMonotoneX);
      let pathLine;
      that.dataList.forEach(item => {
        pathLine = that.chart.append('path')
        .datum(item)
        .attr('class', 'line')
        .attr('fill', 'none')
        .attr('stroke', (d) => {
          let temp = that.barColors[that.index];
          that.index += 1;
          return temp;
        })
        .attr('stroke-width', 2)
        .attr('d', line);
        that.linePathList.push(pathLine);
      });
      that.index = 0; 
      

        if(that.lineAniFlag){
          for(var i =0;i < that.linePathList.length;i++){
            const totalLength = that.linePathList[i].node().getTotalLength();

            that.linePathList[i].attr('stroke-dasharray', totalLength + ' ' + totalLength)
              .attr('stroke-dashoffset', totalLength)
              .transition()
              .duration(10 * (that.frameExtent[1] - that.frameExtent[0]))
              .ease(d3.easeLinear)
              .attr('stroke-dashoffset', 0);
          }
        }


        

        // d3.selectAll('.dot').remove();

        that.chart.selectAll("circle.dot")
          .data(that.barData)
          .join("circle")
          .attr("class", "dot")
          .attr("cx", d => {
            return d["i"] * that.barWidth +
              (that.barWidth / that.clusterBar) * d["j"] +
              15;
          })
          .attr("cy", d => {
            return that.chartHeight -
              timeLineScaleLinearAxisLeft(that.maxValue - d["volume"]) -
              that.margin * 2;
          })
          .attr("r", 2)
          .attr("fill", d => {
            return that.barColors[d["j"]];
          });
          console.log('===================');
          // let len = 0;
          // console.log(that.barData);
          // that.chart.selectAll(".dot")
          // .data(that.barData)
          // .enter().append("circle")
          // .attr("class", "dot")
          // .attr("cx", d => {
          //   len++;
          //   return d["i"] * that.barWidth +
          //     (that.barWidth / that.clusterBar) * d["j"] +
          //     5;
          // })
          // .attr("cy", d => {
          //   console.log(d);
          //   return that.chartHeight -
          //     timeLineScaleLinearAxisLeft(that.maxValue - d["volume"]) -
          //     that.margin * 2;
          // })
          // .attr("r", 4)
          // .attr("fill", (d) => {
          //     return that.barColors[d["j"]];
          // });

          // console.log('len='+len);
        
        // let lineGen = d3.line()
        //       .x(function (d) {
        //         return (d["i"] * that.barWidth + (that.barWidth / that.clusterBar) * d["j"] + 5)
        //       })
        //       .y(function (d) {
        //         return that.chartHeight - timeLineScaleLinearAxisLeft(that.maxValue - d["volume"]) - that.margin * 2
        //       });

      // 绘制图例
      that.legend = that.chart
        .selectAll("g." + "cluster" + that.bar.barClass)
        .data(that.frame)
        .join("g")
        .attr("class", (d, i) => {
          return (
            "cluster" + that.bar.barClass + " cluster_" + i + that.bar.barClass
          );
        })
        .attr("transform", `translate(${[that.margin, that.margin]})`)
        .on("mouseenter", (d, i) => that.mouseEnterLegend(i))
        .on("mouseleave", that.mouseLeaveLegend)
        .each(function (d, i) {
          d3.select(this)
            .selectAll("rect")
            .data([1])
            .join("rect")
            .attr("x", i * 90 + 10)
            .attr("y", -8)
            .attr("height", 8)
            .attr("width", 20)
            .style("fill", that.barColors[i])
            .style("opacity", 1);
          d3.select(this)
            .selectAll("text")
            .data([1])
            .join("text")
            .attr("x", 22 + i * 90 + 10)
            .text("cluster_" + i)
            .style("font-size", 14);
        });

      // 添加叉号 关闭按钮
      that.chart
        .append("path")
        .attr("d", d3.arc()({
          innerRadius: 0,
          outerRadius: 7,
          startAngle: 0,
          endAngle: Math.PI * 2
        }))
        .attr("stroke", "#696969")
        .attr("stroke-width", 2)
        .attr("fill", "#BEBEBE")
        .attr('cursor','pointer')
        .attr("transform", `translate(${[that.width - 60, that.margin - 8]})`)
        .on("click", function () {
          console.log("移除柱状图");
          d3.select(this.parentNode.parentNode.parentNode).remove();
        });

      // that.chart
      //   .append("path")
      //   .attr("d", d3.arc()({
      //     innerRadius: 0,
      //     outerRadius: 7,
      //     startAngle: 0,
      //     endAngle: Math.PI * 2
      //   }))
      //   .attr("stroke", "red")
      //   .attr("stroke-width", 2)
      //   .attr("fill", "pink")
      //   .attr('cursor','pointer')
      //   .attr("transform", `translate(${[that.width - 80, that.margin - 8]})`)
      //   .on("click", function () {
      //     console.log('click');
      //     if(!this.lineEnable){
      //       this.parentNode.querySelector('.line').style.display = 'none';
      //     }else{
      //       this.parentNode.querySelector('.line').style.display = 'block';
      //     }
      //     this.lineEnable = !this.lineEnable;
          
      //   });

      //折线显示按钮
      that.chart.append("rect")
          .attr("x", 340)
          .attr("y", -6)
          .attr("width", 30)
          .attr("height", 15)
          .attr("fill", "deepskyblue")
          .attr('user-select', 'none')
          .attr('cursor','pointer')
          .on('click',function() {
              if(!this.lineEnable){
                this.parentNode.querySelectorAll('.line').forEach(item => {
                  item.style.display = 'none';
                });
              }else{
                this.parentNode.querySelectorAll('.line').forEach(item => {
                  item.style.display = 'block';
                });
              }
              this.lineEnable = !this.lineEnable;
        });

      that.chart.append("text")
      .attr("x", 355)
      .attr("y", 2)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .text("折线")
      .style("fill", "#ffffff")
      .style("font-family", "Arial")
      .style("font-size", "10px")
      .attr('cursor', 'pointer')
      .attr('user-select', 'none')
      .on('click',function() {
              if(!this.lineEnable){
                this.parentNode.querySelectorAll('.line').forEach(item => {
                  item.style.display = 'none';
                });
              }else{
                this.parentNode.querySelectorAll('.line').forEach(item => {
                  item.style.display = 'block';
                });
              }
              this.lineEnable = !this.lineEnable;
        });




        //散点显示按钮
        that.chart.append("rect")
          .attr("x", 300)
          .attr("y", -6)
          .attr("width", 30)
          .attr("height", 15)
          .attr("fill", "deepskyblue")
          .attr('user-select', 'none')
          .attr('cursor','pointer')
          .on('click',function() {
              if(!this.dotEnable){
                this.parentNode.querySelectorAll('.dot').forEach(item => {
                  item.style.display = 'none';
                });
              }else{
                this.parentNode.querySelectorAll('.dot').forEach(item => {
                  item.style.display = 'block';
                });
              }
              this.dotEnable = !this.dotEnable;
        });

      that.chart.append("text")
      .attr("x", 315)
      .attr("y", 2)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .text("散点")
      .style("fill", "#ffffff")
      .style("font-family", "Arial")
      .style("font-size", "10px")
      .attr('cursor', 'pointer')
      .attr('user-select', 'none')
      .on('click',function() {
              if(!this.dotEnable){
                this.parentNode.querySelectorAll('.dot').forEach(item => {
                  item.style.display = 'none';
                });
              }else{
                this.parentNode.querySelectorAll('.dot').forEach(item => {
                  item.style.display = 'block';
                });
              }
              this.dotEnable = !this.dotEnable;
        });


        //条状图显示按钮
        that.chart.append("rect")
          .attr("x", 260)
          .attr("y", -6)
          .attr("width", 30)
          .attr("height", 15)
          .attr("fill", "deepskyblue")
          .attr('user-select', 'none')
          .attr('cursor','pointer')
          .on('click',function() {
              if(!this.barEnabel){
                this.parentNode.querySelectorAll('.bar ').forEach(item => {
                  item.style.display = 'none';
                });
              }else{
                this.parentNode.querySelectorAll('.bar ').forEach(item => {
                  item.style.display = 'block';
                });
              }
              this.barEnabel = !this.barEnabel;
        });

      that.chart.append("text")
      .attr("x", 275)
      .attr("y", 2)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .text("条形")
      .style("fill", "#ffffff")
      .style("font-family", "Arial")
      .style("font-size", "10px")
      .attr('cursor', 'pointer')
      .attr('user-select', 'none')
      .on('click',function() {
              if(!this.barEnabel){
                this.parentNode.querySelectorAll('.bar ').forEach(item => {
                  item.style.display = 'none';
                });
              }else{
                this.parentNode.querySelectorAll('.bar ').forEach(item => {
                  item.style.display = 'block';
                });
              }
              this.barEnabel = !this.barEnabel;
        });





      //重叠帧显示按钮
      that.chart.append("rect")
          .attr("x", 220)
          .attr("y", -6)
          .attr("width", 30)
          .attr("height", 15)
          .attr("fill", "deepskyblue")
          .attr('user-select', 'none')
          .attr('cursor','pointer');

      that.chart.append("text")
      .attr("x", 235)
      .attr("y", 2)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .text("显示")
      .style("fill", "#ffffff")
      .style("font-family", "Arial")
      .style("font-size", "10px")
      .attr('cursor', 'pointer')
      .attr('user-select', 'none')
      .on('click',function() {    
            if(that.same_frame.length != 0){
              that.showCrossFrames();
            }else{
              alert('same frame is not exist!');
            }
            
        });


        // that.chart
        // .append("path")
        // .attr("d", d3.arc()({
        //   innerRadius: 0,
        //   outerRadius: 7,
        //   startAngle: 0,
        //   endAngle: Math.PI * 2
        // }))
        // .attr("stroke", "red")
        // .attr("stroke-width", 2)
        // .attr("fill", "pink")
        // .attr('cursor','pointer')
        // .attr("transform", `translate(${[that.width - 100, that.margin - 8]})`)
        // .on("click", function () {
        //   console.log('click');
        //   if(!this.lineEnable){
        //     this.parentNode.querySelector('.line').style.display = 'none';
        //   }else{
        //     this.parentNode.querySelector('.line').style.display = 'block';
        //   }
        //   this.lineEnable = !this.lineEnable;
          
        // });


      // 定义缩放zoom行为对象
      that.zoomBehavior = d3
        .zoom()
        .scaleExtent([1, 8]) // 设置缩放范围
        .on("zoom", function () {
          // 获取当前 Zoom 变换的状态
          var transform = d3.event.transform;

          // 应用变换到所有子元素上
          d3.select("." + that.barClass).attr("transform", transform);
        });
      // 添加放大镜 放大柱状图
      /* let histogram = d3.select("." + that.barClass)
      let cloneHis = null
      that.zoom = that.chart.append("g")
        .attr("transform", `translate(${[that.width - 85, that.margin - 12]})`)
        .append('svg')
        .attr("width", 20).attr('height', 20)
        .attr("viewBox", "0 0 1024 1024")
        .attr("pointer-events", "all")
        .append("path")
        .attr("d", that.zoomStr)
        .on("click", function () {
          if (cloneHis === null) {
            cloneHis = histogram.clone(true)
            console.log('柱状图', histogram.node());
            // let parent = d3.select(this.parentNode.parentNode);
            // console.log(parent);
            // 将克隆的 div 元素添加到 main 子元素中
            d3.select(".main").append(() => cloneHis.node());

            // 将 div 副本移动到居中位置
            cloneHis.style("position", "fixed")
              .style("z-index", 2)
              .style("left", "456px")
              .style("top", "378px")
              .style("transform", "scale(1.8)")
              .style("background", "rgba(227, 236, 250,0.9)")
              .on("dblclick", function () {
                console.log('点击的对象是', this);
                d3.select(this).remove();
                cloneHis = null
              })


            // histogram.transition().duration(500)
            //   .attr("style", "transform:translate(-100px,-100px) scale(2)")
          }

        }); */

      let timeLine_dragBehavior = d3
        .drag()
        .on("drag", function () {
          let dx = +d3.event.dx; // 移动坐标
          let x = +d3.select(this).attr("x"); // 当前选中节点
          let border = +d3.select("#timeLine_chart_border").attr("width") + 20;
          if (
            x >= 0 &&
            x + that.margin <= border &&
            x + dx >= 0 &&
            x + dx + that.margin <= border
          ) {
            d3.select(this).attr("x", x + dx);
          }
          // 更新标签数据
          let text = d3.select("#" + that.barClass + "_text"); // 标签数据
          let frame_num =
            Math.ceil(
              timeLineScaleLinearAxisBottom.invert(x + that.margin / 2)
            ) - 2; // 映射的键值
          if (that.frameMap[frame_num]) {
            that.framePocketStr =
              frame_num + "," + that.frameMap[frame_num].join("-");
            text.text("The current frame is: " + frame_num);
          }
        })
        .on("end", function () {
          let tempList = that.framePocketStr.split(",")[1].split('-');
          let endStr = that.framePocketStr.split(",")[0] + ',';
          tempList.forEach(item => {
            let tempItem = that.findItem(item);
            let colorTemp = that.barColors[tempItem.j];
            endStr += item + '/' + colorTemp + '-';
          });
          endStr = endStr.substring(0, endStr.length - 1);
          // let tempItem = that.findItem(that.framePocketStr.split(",")[1].replaceAll("-", ","));
          // 滑动结束事件
          that.$emit("barSlider", endStr);
          that.highlightScatter(
            that.framePocketStr.split(",")[1].replaceAll("-", ",")
          );
        });
      // 绘制滑块
      that.chart
        .selectAll("rect.timeLine_slider")
        .data([1])
        .join("rect")
        .attr("class", "timeLine_slider")
        .attr("x", 10)
        .attr("y", that.margin)
        .attr("rx", 5)
        .attr("width", that.margin)
        .attr("height", that.margin)
        .attr(
          "transform",
          `translate(${[0, that.chartHeight - that.margin * 3]})`
        )
        .style("stoke", "black")
        .style("stroke-width", 1)
        .attr("fill", "black")
        .call(timeLine_dragBehavior);
        that.loading = false;
    },
    mouseEnterLegend(index) {
      d3.selectAll(".cluster" + this.bar.barClass).style("opacity", 0.1);
      d3.selectAll(".cluster_" + index + this.bar.barClass).style(
        "opacity",
        0.5
      );
    },
    mouseLeaveLegend() {
      d3.selectAll(".cluster" + this.bar.barClass).style("opacity", 1);
    },

    timeLineDrop(event) {
      let that = this;
      that.frame_pocketTemp = event.dataTransfer.getData("framePocket").trim().split(",");
      that.frame.push(
        event.dataTransfer.getData("framePocket").trim().split(",")
      ); // 放入多维数据
      //移除之前存在折线图
      if(event.srcElement.querySelectorAll('.line')){
        event.srcElement.querySelectorAll('.line').forEach(item => {
        item.remove();
      });
    }
      that.barColors.push(event.dataTransfer.getData("color"));
      d3.select("#" + that.barClass + "_text").text("The current frame is: 1");
      // console.log("that.barColors ", that.barColors)
      // 请求数据
      that.initRequire();
    },
    barClick(node) {
      this.$emit("barClick", node);
    },
    lineChange(){
      console.log('click');
      console.log(d3.selectAll('.line').attr('display'));
      this.parentNode.querySelector('.line').display = 'none';
    },
    //展示重叠帧
    showCrossFrames(){
      let that = this;

      //数据处理
      let tempArr = []
      // console.log(this.dataList,this.same_frame);
      for(let i = 0 ;i < this.dataList.length;i++){
        tempArr.push([]);
        this.dataList[i].forEach(item => {
          if(this.same_frame.indexOf(item.frame_pocket.split('_')[0]) != -1){
            tempArr[item.j].push(item);
          }
        });
      }
      tempArr[0].sort((a,b) => {
        return b.volume - a.volume;
      });

      tempArr[0].sort((a,b) => {
        return b.volume - a.volume;
      });
      let strArr1 = []
      let strArr2 = []

      tempArr[0].forEach(item => {
        strArr1.push(item.frame_pocket.split('_')[0]);
      });

      
      tempArr[1].forEach(item => {
        strArr2.push(item.frame_pocket.split('_')[0]);
      });
      // console.log(strArr1,strArr2);
      
      let sortedFrames = tempArr[0].map(item => {
        return item.frame_pocket.split('_')[0];
      })

      tempArr[1].sort((a,b) => {
        let frameA = a.frame_pocket.split('_')[0];
        let frameB = b.frame_pocket.split('_')[0];
        return sortedFrames.indexOf(frameA) - sortedFrames.indexOf(frameB);
      })
     

      let areaMsg;
      areaMsg = {
            'same_frame' : that.same_frame,
            'tempArr1' : tempArr[0],
            'tempArr2' : tempArr[1],
            'frame_1': [],
            'frame_2': []
      };
      that.showAreaPlot(areaMsg);
      that.updateAreaData(areaMsg);


    }
  },
};
</script>

<style scoped>
/* svg {
  pointer-events: all;
} */
.load{
  position: relative;
  top: 120px;
  left: 30px;
  font-size: 2em;
  z-index: 2;
}
.barClass{
  position: absolute;
}
.btn{
  position: absolute;
  float: right;
  right: 70px;
  width: 60px;
  height: 25px;
  line-height: 12.5px;
  background-color: deepskyblue;
  color: white;
}
</style>
