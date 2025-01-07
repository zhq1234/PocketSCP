<template>
    <div class="mainDiv">
        <div class="tip" v-if="tipFalse">loading...</div>
        <div :class="clusterIdEnd"  @dragstart="dragStart" draggable="true" @dragover.prevent></div>
    </div>
</template>
<script>
    import { request } from "@/network/request";
import axios from "axios";
    const { mapMutations } = require("vuex");
    export default {
        name: "cluster",
        props: { cluster: undefined,extentList: undefined,clusterId: undefined,pathStr: ''},
        data(){
            return {
                color: '',
                dataList: [],
                frameList: [],
                avgList: [],
                sdList: [],
                clusterIdEnd: 'itemDiv' + this.clusterId,
                tipFalse: true,
                nameList: ['volume','alphanum','totalsasa','polarsasa','apolarsasa','mlohyden','malspra','msoacc','hydropscore','propolatoms','alspdensity','alphaspmaxdist','polarityscore'],
                maxSDList: [],
                clusterExtent: [],
                maxSD: 0,
            }
        },
        created() {
            let that = this;
            that.frameList.push(that.cluster.frameList);
            that.color = that.cluster.color;
            
        },
        mounted() {
            this.initData();
        },
        methods: {
            ...mapMutations([
                "popColor",
                "pushColor",
            ]),
            initData(){
                this.initRequire();
            },
            async initRequire() {
                let that = this;
                console.log('init');
                console.log(that.frameList);
                await axios({
                    url: 'api/molStar/frame_bar',
                    method: 'post',
                    data: {
                        frame_pocket: that.frameList
                    }
                }).then((res) => {
                    if (res.status === 200) {
                        console.log('init end');
                        // that.frameMap = res.data.data["frameMap"]; // frame_framePocket_dict 帧——口袋的映射 一帧可能对应几个不同的口袋
                        // that.clusterBar = res.data.data["clusterBar"]; // 表示有多少簇 clusterBar : 1

                        // that.frameExtent = res.data.data["frameExtent"]; // 数据帧范围 frameExtent : [2, 86]
                        // that.maxValue = res.data.data["maxVolume"]; // maxVolume: 353.147
                        // that.maxDis = res.data.data["maxDis"]; // 质心——阿尔法球的最大距离 中的最大值
                        // that.barData = res.data.data["barData"]; // 每一帧的各个属性值
                        that.dataList = res.data.data["barData"];
                        that.getExtent();
                        that.computeAvg();
                        console.log(that.extentList);
                        console.log('init');
                        that.computeSD();
                        that.drawCircle();
                        that.tipFalse = false;
                        console.log(that.dataList);


                        that.enventBinding();
                        console.log(that.pathStr);
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
            },
            getExtent(){
                let that = this;
                for(var i = 0;i < 13;i++){
                    that.clusterExtent.push([]);
                    that.clusterExtent[i].push(9999);
                    that.clusterExtent[i].push(-1);
                }
                that.dataList.forEach((item,index) => {
                    that.clusterExtent[0][0] = that.clusterExtent[0][0] < item.volume ? that.clusterExtent[0][0] : item.volume;
                    that.clusterExtent[0][1] = that.clusterExtent[0][1] > item.volume ? that.clusterExtent[0][1] : item.volume;
                    that.clusterExtent[1][0] = that.clusterExtent[1][0] < item.alphanum ? that.clusterExtent[1][0] : item.alphanum;
                    that.clusterExtent[1][1] = that.clusterExtent[1][1] > item.alphanum ? that.clusterExtent[1][1] : item.alphanum;
                    that.clusterExtent[2][0] = that.clusterExtent[2][0] < item.totalsasa ? that.clusterExtent[2][0] : item.totalsasa;
                    that.clusterExtent[2][1] = that.clusterExtent[2][1] > item.totalsasa ? that.clusterExtent[2][1] : item.totalsasa;
                    that.clusterExtent[3][0] = that.clusterExtent[3][0] < item.polarsasa ? that.clusterExtent[3][0] : item.polarsasa;
                    that.clusterExtent[3][1] = that.clusterExtent[3][1] > item.polarsasa ? that.clusterExtent[3][1] : item.polarsasa;
                    that.clusterExtent[4][0] = that.clusterExtent[4][0] < item.apolarsasa ? that.clusterExtent[4][0] : item.apolarsasa;
                    that.clusterExtent[4][1] = that.clusterExtent[4][1] > item.apolarsasa ? that.clusterExtent[4][1] : item.apolarsasa;
                    that.clusterExtent[5][0] = that.clusterExtent[5][0] < item.mlohyden ? that.clusterExtent[5][0] : item.mlohyden;
                    that.clusterExtent[5][1] = that.clusterExtent[5][1] > item.mlohyden ? that.clusterExtent[5][1] : item.mlohyden;
                    that.clusterExtent[6][0] = that.clusterExtent[6][0] < item.malspra ? that.clusterExtent[6][0] : item.malspra;
                    that.clusterExtent[6][1] = that.clusterExtent[6][1] > item.malspra ? that.clusterExtent[6][1] : item.malspra;
                    that.clusterExtent[7][0] = that.clusterExtent[7][0] < item.msoacc ? that.clusterExtent[7][0] : item.msoacc;
                    that.clusterExtent[7][1] = that.clusterExtent[7][1] > item.msoacc ? that.clusterExtent[7][1] : item.msoacc;
                    that.clusterExtent[8][0] = that.clusterExtent[8][0] < item.hydropscore ? that.clusterExtent[8][0] : item.hydropscore;
                    that.clusterExtent[8][1] = that.clusterExtent[8][1] > item.hydropscore ? that.clusterExtent[8][1] : item.hydropscore;
                    that.clusterExtent[9][0] = that.clusterExtent[9][0] < item.propolatoms ? that.clusterExtent[9][0] : item.propolatoms;
                    that.clusterExtent[9][1] = that.clusterExtent[9][1] > item.propolatoms ? that.clusterExtent[9][1] : item.propolatoms;
                    that.clusterExtent[10][0] = that.clusterExtent[10][0] < item.alspdensity ? that.clusterExtent[10][0] : item.alspdensity;
                    that.clusterExtent[10][1] = that.clusterExtent[10][1] > item.alspdensity ? that.clusterExtent[10][1] : item.alspdensity;
                    that.clusterExtent[11][0] = that.clusterExtent[11][0] < item.alphaspmaxdist ? that.clusterExtent[11][0] : item.alphaspmaxdist;
                    that.clusterExtent[11][1] = that.clusterExtent[11][1] > item.alphaspmaxdist ? that.clusterExtent[11][1] : item.alphaspmaxdist;
                    that.clusterExtent[12][0] = that.clusterExtent[12][0] < item.polarityscore ? that.clusterExtent[12][0] : item.polarityscore;
                    that.clusterExtent[12][1] = that.clusterExtent[12][1] > item.polarityscore ? that.clusterExtent[12][1] : item.polarityscore;

                });

                console.log('clusterExtent',that.clusterExtent);
            },
            computeAvg(){
                console.log('begin compute');
                let that = this;
                let len = 13;
                let tempAvg = [];
                for(var i = 0;i < len ;i++){
                    tempAvg.push(0);
                }
                that.dataList.forEach((item,index) => {
                    tempAvg[0] += item.volume;
                    tempAvg[1] += item.alphanum;
                    tempAvg[2] += item.totalsasa;
                    tempAvg[3] += item.polarsasa;
                    tempAvg[4] += item.apolarsasa;
                    
                    tempAvg[5] += item.mlohyden;
                    tempAvg[6] += item.malspra;
                    tempAvg[7] += item.msoacc;
                    tempAvg[8] += item.hydropscore;
                    tempAvg[9] += item.propolatoms;
                    tempAvg[10] += item.alspdensity;
                    tempAvg[11] += item.alphaspmaxdist;
                    tempAvg[12] += item.polarityscore;
                });
                console.log(tempAvg[4]);
                for(var i = 0;i < len ;i++){
                    tempAvg[i] /= that.dataList.length;
                }
                console.log(tempAvg);
                that.avgList = tempAvg;
                console.log('end compute');
            },
            dragStart(event){
                let that = this;
                console.log('drag start');
                event.dataTransfer.setData("framePocket", that.frameList);
                event.dataTransfer.setData("color", that.color);
                event.dataTransfer.setData("identify", "clusterTree"); 
            },
            drawCircle(){
                let that = this;
                const width = 200;
                const height = 160;
                const margin = { top: 10, right: 10, bottom: 10, left: 10 };

                // The radius of the radar chart
                const radius = Math.min(width / 2.2, height / 2.2);
                console.log(this.extentList);
                // The data for the radar chart
                const data = [];

                for(var i = 0;i < 13;i++){
                    // console.log(that.nameList[i],that.extentList[i][0],that.extentList[i][1],Math.log(1 + Math.exp(Math.pow(that.avgList[i],1/4))),Math.log(1 + Math.exp(Math.pow(that.extentList[i][0],1/4))),Math.log(1 + Math.exp(Math.pow(that.extentList[i][1],1/4))));
                    data.push({
                        axis: that.nameList[i],
                        value: Math.log(1 + that.avgList[i]),
                        minValue: Math.log(1 + that.extentList[i][0]),
                        maxValue: Math.log(1 + that.extentList[i][1]),
                    });
                }   

                let sdData = [];
                for(var i = 0;i < 13;i++){
                    sdData.push({
                        axis: that.nameList[i],
                        value: Math.log(1 + that.sdList[i]) ,
                        minValue: 0,
                        maxValue: Math.log(1 + that.maxSDList[i]),
                    });
                }

                console.log('sdData',sdData);



                console.log(data);
                // Create the svg element
                const svg = d3.select('.'+this.clusterIdEnd).append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .append("g")
                    .attr("transform", `translate(${width / 2},${height / 2 + 5})`);

                // Create the scales
                const angleScale = d3.scaleLinear()
                    .domain([0, data.length])
                    .range([0, 2 * Math.PI]);

                // Create the radar chart
                const radarLine = d3.lineRadial()
                    .radius(d => d.radiusScale(d.value))
                    .angle((d, i) => angleScale(i))
                    .curve(d3.curveLinearClosed);

                // Draw the background circles
                const levels = 5;
                for (let i = 0; i <= levels; i++) {
                    svg.append("circle")
                        .attr("r", radius / levels * i)
                        .attr("fill", "none")
                        .attr("stroke", "#ddd");
                }

                // Draw the axes
                const axis = svg.selectAll(".axis")
                    .data(data)
                    .enter()
                    .append("g")
                    .attr("class", "axis");

                axis.append("line")
                    .attr("x1", 0)
                    .attr("y1", 0)
                    .attr("x2", (d, i) => radius * Math.cos(angleScale(i) - Math.PI / 2))
                    .attr("y2", (d, i) => radius * Math.sin(angleScale(i) - Math.PI / 2))
                    .attr("stroke", "#ddd");

                axis.append("text")
                    .attr("x", (d, i) => (radius) * Math.cos(angleScale(i) - Math.PI / 2))
                    .attr("y", (d, i) => (radius) * Math.sin(angleScale(i) - Math.PI / 2))
                    .attr("dy", "0.1em")
                    .attr('font-size','0.5rem')
                    .style("text-anchor", "middle")
                    .text(d => d.axis);

                // Create individual scales for each axis
                data.forEach(d => {
                    d.radiusScale = d3.scaleLinear()
                        .domain([d.minValue, d.maxValue])
                        .range([0, radius]);
                });

                // Draw the radar area
                svg.append("path")
                    .datum(data)
                    .attr("d", radarLine)
                    .attr("fill", this.color)
                    .attr("fill-opacity", 0.3)
                    .attr("stroke", this.color)
                    .attr("stroke-width", 2);

                // Draw the dots
                svg.selectAll(".radarCircle")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("class", "radarCircle")
                    .attr("r", 3)
                    .attr("cx", (d, i) => d.radiusScale(d.value) * Math.cos(angleScale(i) - Math.PI / 2))
                    .attr("cy", (d, i) => d.radiusScale(d.value) * Math.sin(angleScale(i) - Math.PI / 2))
                    .attr("fill", this.color);



                //绘制标准差雷达图
                sdData.forEach(d => {
                    d.radiusScale = d3.scaleLinear()
                        .domain([d.minValue, d.maxValue])
                        .range([0, radius]);
                });


                svg.append("path")
                    .datum(sdData)
                    .attr("d", radarLine)
                    .attr("fill", 'black')
                    .attr("fill-opacity", 0)
                    .attr("stroke", 'black')
                    .attr('stroke-dasharray','2,2')
                    .attr("stroke-width", 2);


                //添加关闭按钮
                svg.append("path")
                .attr("d", d3.arc()({
                innerRadius: 0,
                outerRadius: 7,
                startAngle: 0,
                endAngle: Math.PI * 2,
                }))
                .attr("stroke", "#696969")
                .attr("stroke-width", 2)
                .attr("fill", "#BEBEBE")
                .attr("transform", `translate(${[width / 2 - 10, -height / 2 + 10]})`)
                .attr('cursor','pointer')
                .on("click", function () {
                    // console.log(d3.select('.'+that.clusterIdEnd)._groups[0][0].parentNode);
                // 点击移除对应的弦图 center_top_child
                    d3.select('.'+that.clusterIdEnd)._groups[0][0].parentNode.remove();
                    // console.log(d3.selectAll('.svgArea'+that.color.slice(5,-1).replaceAll(',','')));
                    d3.selectAll('.svgArea'+that.color.slice(5,-1).replaceAll(',','')).remove();
                    that.pushColor(that.color);
                    
                });




                //添加隐藏按钮
                svg.append("path")
                .attr("d", d3.arc()({
                innerRadius: 0,
                outerRadius: 7,
                startAngle: 0,
                endAngle: Math.PI * 2,
                }))
                .attr("stroke", "darkblue")
                .attr("stroke-width", 2)
                .attr('class','show'+that.color.slice(5,-1).replaceAll(',',''))
                .attr("fill", "skyblue")
                .attr("transform", `translate(${[-width / 2 + 10, -height / 2 + 10]})`)
                .attr('cursor','pointer')
                .on("click", function () {
                    // console.log(d3.select('.'+that.clusterIdEnd)._groups[0][0].parentNode);
                // 点击移除对应的弦图 center_top_child
                    // console.log(d3.selectAll('.svgArea'+that.color.slice(5,-1).replaceAll(',','')));
                    if(d3.selectAll('.svgArea'+that.color.slice(5,-1).replaceAll(',',''))._groups[0][0].style.display == 'none'){
                        d3.selectAll('.svgArea'+that.color.slice(5,-1).replaceAll(',',''))._groups[0][0].style.display = 'block';
                        d3.selectAll('.show'+that.color.slice(5,-1).replaceAll(',','')).attr('fill','skyblue');
                    }else{
                        d3.selectAll('.svgArea'+that.color.slice(5,-1).replaceAll(',',''))._groups[0][0].style.display = 'none';
                        d3.selectAll('.show'+that.color.slice(5,-1).replaceAll(',','')).attr('fill','SteelBlue');
                    }
                    
                    
                });

                
            },
            //事件绑定
            enventBinding(){
                let that = this;
                const scatterSvg = d3.select('.haha');
                d3.select('.'+that.clusterIdEnd).on('mouseenter',(e) => {
                    // scatterSvg.append("path")
                    // .attr('fill','red')
                    // .attr('class','tempCluster')
                    // .attr('stroke-dasharray','5,5')
                    // .attr('stroke',that.color)
                    // .attr('stroke-width',2)
                    // .attr('d',that.pathStr);
                });
                d3.select('.'+that.clusterIdEnd).on('mouseleave',(e) => {
                    // d3.select('.tempCluster').remove();
                })
            },
            //计算标准差
            computeSD(){
                let that = this;
                let tempSD = [];
                for(var i = 0;i < 13;i++){
                    tempSD.push(0);
                }
                that.dataList.forEach((item,index) => {
                    tempSD[0] += Math.pow(item.volume - that.avgList[0],2);
                    tempSD[1] += Math.pow(item.alphanum - that.avgList[1],2);
                    tempSD[2] += Math.pow(item.totalsasa - that.avgList[2],2);
                    tempSD[3] += Math.pow(item.polarsasa - that.avgList[3],2);
                    tempSD[4] += Math.pow(item.apolarsasa - that.avgList[4],2);
                    tempSD[5] += Math.pow(item.mlohyden - that.avgList[5],2);
                    tempSD[6] += Math.pow(item.malspra - that.avgList[6],2);
                    tempSD[7] += Math.pow(item.msoacc - that.avgList[7],2);
                    tempSD[8] += Math.pow(item.hydropscore - that.avgList[8],2);
                    tempSD[9] += Math.pow(item.propolatoms - that.avgList[9],2);
                    tempSD[10] += Math.pow(item.alspdensity - that.avgList[10],2);
                    tempSD[11] += Math.pow(item.alphaspmaxdist - that.avgList[11],2);
                    tempSD[12] += Math.pow(item.polarityscore - that.avgList[12],2);
                });
                // let maxSdTemp = 0;
                for(var i = 0;i < 13;i++){
                    tempSD[i] = Math.sqrt(tempSD[i] / that.dataList.length);
                    that.maxSDList[i] = Math.sqrt(Math.max(Math.pow(that.extentList[i][0] - that.avgList[i],2),Math.pow(that.extentList[i][1] - that.avgList[i],2)));
                    // maxSdTemp = maxSdTemp > that.maxSDList[i]?maxSdTemp:that.maxSDList[i];
                }
                that.sdList = tempSD;
                // that.maxSD = maxSdTemp;
                // console.log(that.maxSD);
                console.log(that.sdList);
                console.log('maxSDList',that.maxSDList);
            },
        },
        components: {},
    }
</script>


<style scoped>
    .mainDiv{
        margin-bottom: 0px;
        width: 220px;
        height: 180px;
        border-bottom: 1px solid black;
    }

    .itemDiv{
        width: 220px;
        height: 150px;
    }
    .axis line {
        stroke: #ddd;
    }
    .axis text {
        fill: #555;
    }
    .area {
        fill-opacity: 0.3;
    }

    .tip{
        position: relative;
        top: 80px;
        left: 60px;
    }

</style>