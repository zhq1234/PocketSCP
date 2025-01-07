import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        zoomFactor: 1,    // 缩放比例
        radius: 4, // framePocket: [],
        similarMin: 0.1,   // 两个空腔的相似性下限
        similarMax: 1.0,   // 两个空腔的相似性上限
        scatterPlotFramePocketData: [], // 初始化散点图
        inOrOutDegree: 10,   // 度最大值
        colorIndex: 0,
        lineAniFlag: false,
        lineFlag: true,
        scatterPlotFlag: true,
        colorList: [
            ' rgb(139,0,0)',
             'rgb(30,144,255)',
             'rgb(0,100,0)',
             'rgb(0,255,0)',
            ' rgb(255,255,0)',
            ' rgb(205,92,92)',
             'rgb(245,245,220)',
             'rgb(	255,0,0)',
             'rgb(238,130,238)',
             'rgb(147,112,219)',
            ' rgb(255,127,0)',
            'rgb(0,139,139)',
            'rgb(139,0,139)',
            'rgb(128,0,128)',
            'rgb(255,255,255)',
            'rgb(255,255,0)',
            'rgb(255,0,255)',
            'rgb(139,139,0)',
            'rgb(238,210,238)',
            'rgb(156,156,156)',
            'rgb(244,164,96)',
           ],
        transformList: [],
        clusterColorList: [],
        currentColor: '',
        areaMsg: {
            'same_frame' : [],
            'tempArr1' : [],
            'tempArr2' : [],
            'frame_1': [],
            'frame_2': [],
        },
    }, getters: {
        //
    }, mutations: {
        initScatterPlotFramePocketData(state, framePocket) {
            state.scatterPlotFramePocketData = framePocket;
        }, //
        changeScatterPlotFramePocketData(state, framePocketMap) {
            state.scatterPlotFramePocketData["forceData"].map(d => {
                if (framePocketMap["pocket"].indexOf(d["frame_pocket"]) > -1) {
                    d["color"] = framePocketMap["color"]
                }
            })
        }, //
        changZoomFactor(state, k) {
            state.zoomFactor = k;
        }, //
        changePocketComparability(state, s) {
            state.pocketComparability = s;
        },  // 更改相似性
        changeSimilarMin(state, s) {
            state.similarMin = s
        },
        changeSimilarMax(state, s) {
            state.similarMax = s
        },// 更改度
        changeInOrOutDegree(state, d) {
            state.inOrOutDegree = d;
        },
        addColorIndex(state){
            state.colorIndex = state.colorIndex + 1;
        },
        subColorIndex(state){
            state.colorIndex = state.colorIndex - 1;
        },
        resetColorIndex(state){
            state.colorIndex = 0;
        },
        changeLineAniFlag(state){
            state.lineAniFlag = !state.lineAniFlag;
        },
        changeLineFlag(state){
            state.lineFlag = !state.lineFlag;
        },
        changeScatterplotFlag(state){
            state.scatterPlotFlag = !state.scatterPlotFlag;
        },
        popColor(state){
            state.currentColor = state.colorList.pop();
            state.clusterColorList.push(state.currentColor);
        },
        pushColor(state,color){
            console.log(state.clusterColorList,color);
            let index = state.clusterColorList.indexOf(color);
            console.log('index',index);
            console.log(state.transformList);
            state.clusterColorList.splice(index,1);
            state.transformList.splice(index,1);
            state.colorList.push(color);
        },
        removeTransformListByIndex(state,index){
            state.transformList.splice(index,1);
        },
        pushToTransformList(state,item){
            state.transformList.push(item);
        },
        updateAreaData(state,newData){
            state.areaMsg = newData;
        }

    }, actions: {
        highlightScatter(state, nodes) {
            let that = this;
            d3.selectAll("circle.scatterDot").style("opacity", 0.3).attr("r", that.state.radius / that.state.zoomFactor)
            nodes.trim().split(",").forEach(d => {
                d3.select(".c_" + d).attr("r", that.state.radius * 2 / that.state.zoomFactor).style("opacity", "1");
            })
        },//
        changeColor(state, data) {
            console.log(data["pocket"].trim().split(","))
            data["pocket"].trim().split(",").forEach(d => {
                console.log(d3.selectAll("circle").select(".c_" + d + "color"))
                d3.selectAll("circle").select(".c_" + d + "color").style("fill", data["color"])
            })
        },
        showAreaPlot(state, data) {
            d3.select('.areaContainer').style('display', 'block');
            state.areaMsg = data;
            
        }
    },
})
