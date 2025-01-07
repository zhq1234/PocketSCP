<template>
    <div id="areaMain">
        <div id="chartArea">
            <svg class="areaSvg"></svg>
        </div>
    </div>
</template>

<script>

import { style } from "d3";
import { selectAll } from "d3";
import { mapState } from "vuex";

const { mapMutations } = require("vuex");
export default {
        name: "areaPlot",
        props: { same_frame: [],tempArr1: [],tempArr2: []},
        data(){
            return {
              
            }
        },
        created() {
            this.draw()
        },
        mounted() { 
            
        },
        updated() {
            this.draw();
        },
        computed: {
            ...mapState([
             "areaMsg"
            ]),
        },
        watch: {
            areaMsg: {
                handler(newData) {
                    console.log('update');
                    
                    this.draw();
                },
                immediate: true,
            }
        },
        methods: {
            ...mapMutations([
                "updateAreaData"
            ]),
            initData(){
                console.log('in area');
            },
            draw(){
                let that = this;
                const width = 750;
                const height = 450;
                const margin = {top: 20, right: 30, bottom: 30, left: 40};
                // 创建 SVG 画布

                d3.select(".areaSvg").selectAll("*").remove();
                const svg = d3.select(".areaSvg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", `translate(${margin.left},${margin.top})`);
                    
                


                console.log(that.areaMsg);
                
                // 设置X轴的时间尺度
                const x = d3.scaleTime()
                    .domain([0,that.areaMsg['same_frame'].length - 1])
                    .range([0, width]);

                // 设置Y轴的数值尺度，根据两个数组的最大volume来设置范围
                const y = d3.scaleLinear()
                    .domain([0, d3.max([...that.areaMsg['tempArr1'], ...that.areaMsg['tempArr2']], d => d.volume)]) // 合并两个数组并找出最大值
                    .range([height, 0]);

                // 定义用于绘制面积图的函数
                const area1 = d3.area()
                    .x(d => x(that.areaMsg['tempArr1'].indexOf(d)))
                    .y0(height)
                    .y1(d => y(d.volume));

                const area2 = d3.area()
                    .x(d => x(that.areaMsg['tempArr2'].indexOf(d)))
                    .y0(height)
                    .y1(d => y(d.volume));

                // 添加第一个数组的面积图
                svg.append("path")
                    .datum(that.areaMsg['tempArr1'])
                    .attr("class", "area")
                    .attr("d", area1)
                    .style("fill", "steelblue");

                // 添加第二个数组的面积图
                svg.append("path")
                    .datum(that.areaMsg['tempArr2'])
                    .attr("class", "area")
                    .attr("d", area2)
                    .style("fill", "orange");

                // 添加X轴
                svg.append("g")
                    .attr("transform", `translate(0,${height})`)
                    .call(d3.axisBottom(x).ticks(6));

                // 添加Y轴
                svg.append("g")
                    .call(d3.axisLeft(y));
                
                d3.selectAll(".area").style('fill-opacity',0.6);
                d3.selectAll(".area").style('stroke-width',1);
                d3.selectAll(".area").style('stroke','black');
            }
                

            }

            
    

    }
</script>

<style scoped>
    #areaMain{
        width: 100%;
    }
    body {
        font-family: sans-serif;
    }

    .area {
        fill-opacity: 0.6; /* 设置透明度 */
        stroke-width: 1;
        stroke: #000; /* 边框颜色 */
    }

    .axis path,
    .axis line {
        fill: none;
        stroke: #000;
    }
</style>