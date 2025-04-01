<template>
  <div class="app">
    <div id="clusterContainer">
      <div class="itemCont">
          <div
            v-for="(cluster, i) in selectClusters"
            :key="i">

            <selectCluster
            :cluster="cluster"
            :extentList="extentList"
            :clusterId="cluster.clusterId"
            :pathStr="cluster.pathStr"/>

          </div>
        <div id="addClusterIcon" @drop="addCluster" @dragover.prevent>
          <i class="el-icon-circle-plus-outline plus_big"></i>
        </div>
      </div>
      <div class="clustersShow" @click="showClusters">show</div>
    </div>
    <div id="areaContainer" class="areaContainer">
      <div class="areaPlotClose" @click="closeAreaPlot">x</div>
      <areaPlotView>
      
      </areaPlotView>
    </div>
    <div class="header">
      <header>
        <h2>Visual Analysis of Protein Pocket Dynamics</h2>
      </header>
    </div>
    <div class="container">
      <div>
        <el-row :gutter="5" class="con_top">
          <!-- <el-col :span="4"> -->
            <!-- <el-card shadow="hover" class="annotation"> -->
              <!-- <div>
                <h4>Protein Annotations</h4>
                &nbsp;&nbsp;PDB ENTY：<input
                  type="text"
                  value="4E46"
                  style="width: 60px"
                />
              </div>
              <div>
                <h4>PDB INFO</h4>
                Released:<br />
                &nbsp;&nbsp;2013-03-13
                <br /><br />
                Method:
                <br />
                &nbsp;&nbsp;XRAY DIFFRACTION 1.26 Å
                <br /><br />
                Unique Ligands:
                <br />
                &nbsp;&nbsp;ACT,CL,IPA
              </div> -->
              <!-- <uploadView></uploadView>
            </el-card>
          </el-col> -->
          <!-- <el-col :span="12">
            <el-card shadow="hover">
              <div slot="header" class="card_header">
                <span>Heat Map</span>
              </div>
              <heatmap />
            </el-card>
          </el-col> -->
          <el-col :span="8">
            <el-card shadow="hover">
              <div slot="header" class="card_header">
                <span>Protein three-dimensional structure view</span>
              </div>
              <molstar ref="molPlot" />
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div>
        <el-row :gutter="5" class="con_center">
          
          <!-- <el-col :span="2"> -->
            <!-- <el-card shadow="hover" class="center_left">
              <div slot="header" class="card_header">
                <span>Chord Diagram</span>
              </div> -->
              <!-- <div class="card_content">
             
                <div
                  class="center_left_child"
                  v-for="(chord, i) in chords"
                  :key="i"
                >
                  <chordPlotView
                    @chordScatterLinkLine="scatterLinkLine"
                    :chordID="chord.chordID"
                    :chordData="chord.chordData"
                    :chordColor="chord.chordColor"
                  />
                </div>
                <div
                  class="center_left_add"
                  ref="addChord"
                  @drop="addChord"
                  @dragover.prevent
                > -->
                  <!-- <img src="@/assets/img/add-circle.svg" alt="添加数据" /> -->
                  <!-- <i class="el-icon-circle-plus-outline plus_big"></i> -->
                <!-- </div>
              </div>
            </el-card> -->
          <!-- </el-col> -->
          <el-col :span="14">
            <el-card shadow="hover" class="center_scatter">
              <div slot="header" class="card_header">
                <span>Scatter Plot</span>
              </div>
              <!-- <scatterPlotView
                @scatterShowMol="scatterShowMol"
                @scatterShowRadar="scatterShowRadar"
                ref="scatterPlot"
              /> -->
              <scatterPlotView
                @scatterShowMol="scatterShowMol"
                ref="scatterPlot"
              />
            </el-card>
          </el-col>
          <el-col :span="10">
            <el-card shadow="hover" class="center_right">
              <div slot="header" class="card_header">
                <span>Histogram of Volume</span>
                <div class="aniFlagBtn" @click="changeAni">Animation</div>
              </div>
              <div class="card_content">
                <barPlot
                  v-for="(bar, index) in bars"
                  :bar="bar"
                  @barSlider="barSlider"
                  @barClick="barClick"
                  ref="barPlot"
                  :key="index"
                />
                <div @drop="addBar" @dragover.prevent>
                  <img src="@/assets/img/addBar.svg" alt="添加数据" />
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <!-- <div>
        <el-row :gutter="5" class="con_bottom">
          <el-col :span="12">
            <el-card>
              <div slot="header" class="card_header">
                <span>Parallel Coordinate Plot</span>
              </div>
              <parallelPlotView
                @parallelScatterLinkLine="scatterLinkLine"
                @parallelShowMol="parallelShowMol"
                ref="parallelPlot"
              />
            </el-card>
            <el-card>
              <div slot="header" class="card_header">
                <span>Box Plot</span>
              </div>
              <boxPlotView />
            </el-card>
          </el-col>
          <el-col :span="12">
            <singleAxisScatter></singleAxisScatter>
          </el-col>
        </el-row>
      </div> -->
    </div>
  </div>
</template>
<script>
import { nanoid } from "nanoid";
import { mapState } from "vuex";

const { mapMutations } = require("vuex");
export default {
  name: "app",
  props: {},
  data() {
    return {
      chords: [],
      clusters: [
        {
          clusterClass: "asdf", //
          clusterName: "Pocket1",
          clusterData: [
            "20_1",
            "78_1",
            "32_3",
            "63_3",
            "94_2",
            "24_8",
            "68_1",
            "85_1",
            "6_2",
            "89_2",
            "55_1",
            "22_11",
            "90_7",
            "34_6",
            "84_7",
            "77_6",
            "49_2",
            "15_1",
            "86_1",
            "13_9",
            "21_4",
            "37_6",
            "12_4",
            "19_5",
            "54_5",
            "95_5",
            "97_6",
            "57_6",
            "71_5",
            "61_6",
            "72_3",
            "55_6",
            "53_7",
            "33_5",
            "9_5",
            "90_5",
            "87_6",
            "39_8",
            "41_4",
            "98_8",
            "24_5",
            "69_2",
            "8_5",
            "90_8",
            "66_10",
            "29_7",
            "43_7",
            "71_3",
            "37_7",
            "91_4",
            "28_5",
            "61_4",
            "88_5",
            "63_4",
            "99_7",
            "59_1",
            "32_5",
            "98_4",
            "40_2",
            "41_5",
            "15_3",
            "73_4",
            "81_3",
            "46_4",
            "68_6",
            "39_5",
            "52_4",
            "99_3",
            "38_7",
            "74_5",
            "75_3",
            "25_5",
            "84_8",
            "100_2",
            "69_7",
          ].join(","),
          childTree: [],
        },
      ],
      dropData: [],
      classes: [],
      bars: [], // 柱状图信息
      activeName: "first", // 中间底部的tab默认项
      activeNameRight: "first", // 右侧底部的tab默认项
      selectClusters: [],
      colorList: [],
      showFlag: false,
      extentList: [],
    };
  },
  mounted() {
    // 监听页面销毁
    window.addEventListener("unload", this.pocketUnload);
    // 获取数据
    let chordsData = localStorage.getItem("chords"); // 弦图
    let clusterData = localStorage.getItem("clusters"); // 簇
    let barData = localStorage.getItem("bars"); // 柱状图
    let parallelData = localStorage.getItem("parallel"); // 平行坐标
  },
  computed:{
    ...mapState([
      "lineAniFlag",
    ]),
  },
  components: {
    scatterPlotView: () => import("./views/ScatterPlotView"), // 散点图
    chordPlotView: () => import("./views/ChordPlotView"), // 弦图
    clusterPlotView: () => import("./views/ClusterPlotView"), // 口袋簇
    pdbPlotView: () => import("./views/PDBPlotView"), // PDB文件展示
    parallelPlotView: () => import("./views/ParallelPlotView"), // 平行坐标图
    boxPlotView: () => import("./views/BoxPlotView"), // 盒图
    // radarChart: () => import("./views/RadarChart"), // 雷达图
    molPlot: () => import("./views/MolPlotView"),
    barPlot: () => import("./views/BarPlotView"),
    heatmap: () => import("./views/Heatmap"),
    // heatmap: () => import("@/components/heatmap"),
    molstar: () => import("@/components/molstar"),
    chord: () => import("@/components/chord"),
    parallel: () => import("@/components/parallel"),
    box: () => import("@/components/box"),
    singleAxisScatter: () => import("@/components/singleAxisScatter"),
    selectCluster: () => import("./views/selectCluster"),
    UploadView: () => import("./views/uploadView"),
    areaPlotView: () => import("./views/AreaPlotView"),
  },
  methods: {
    ...mapMutations([
      "changeLineAniFlag",
    ]),
    addChord(e) {
      let that = this;
      that.dropData = e.dataTransfer.getData("framePocket");
      this.pathStr = e.dataTransfer.getData('pathStr');
      if(this.extentList.length == 0){
        e.dataTransfer.getData('valueExtent').slice(1,e.dataTransfer.getData('valueExtent').length + 1).trim().split(",").forEach((item,index) => {
          if(index % 2 == 0){
            this.extentList.push([]);
          }
          this.extentList[parseInt(index / 2)].push(parseFloat(item));
        });
      }
      
      // framePocket = that.dropData;
      // console.log("app add chord ", this.$refs.addChord.classList[0], e.dataTransfer.getData("identify"))
      // 创建新元素
      if (
        e.dataTransfer.getData("identify") &&
        e.dataTransfer.getData("identify") !== this.$refs.addChord.classList[0]
      ) {
        that.chords.push({
          chordID: nanoid(10).replace(/-/g, "").replace(/_/g, ""),
          chordData: that.dropData.trim().split(","),
          chordColor: e.dataTransfer.getData("color"),
        });
      }
      console.log(that.chords);
    },
    // cluster 拖拽
    clusterDrop(e) {
      let that = this;
      console.log(e);
      that.dropData = e.dataTransfer.getData("framePocket"); // 接收数据
      // 表示不存在
      if (that.classes.indexOf(e.dataTransfer.getData("identify")) === -1) {
        $("#appModalDIV").modal("show");
        $("#appModalSubmit").on("click", that.clusterModalClick);
      }
    },
    clusterModalClick() {
      // 添加数据
      let that = this;
      $("#appModalDIV").modal("hide");
      let modalInputValue = $("#modalInput").val().trim(); // 输入列表名称
      let randomClass = nanoid(10).replace(/-/g, "").replace(/_/g, "");
      that.clusters.push({
        clusterClass: randomClass, //
        clusterName: modalInputValue,
        clusterData: that.dropData,
        childTree: [],
      });
      that.classes.push(randomClass);
      $("#modalInput").val(""); // 更改为空
      $("#appModalSubmit").unbind("click", that.clusterModalClick);
    },
    // 平行坐标图自定义事件 显示三维结构
    parallelShowMol(node) {
      this.$refs.molPlot.barClick(node);
    },
    changeAni(event){
      let item = document.getElementsByClassName('aniFlagBtn')[0];
      if(this.lineAniFlag){
        item.style.backgroundColor = 'deepskyblue';
      }else{
        item.style.backgroundColor = 'darkblue';
      }
      this.changeLineAniFlag();
    },
    scatterplotShow(event){
      let item = document.getElementsByClassName('aniFlagBtn')[2];
      if(this.lineAniFlag){
        item.style.backgroundColor = 'deepskyblue';
      }else{
        item.style.backgroundColor = 'darkblue';
      }
      this.changeLineAniFlag();
    },
    lineShow(event){
      let item = document.getElementsByClassName('aniFlagBtn')[1];
      if(this.lineAniFlag){
        item.style.backgroundColor = 'deepskyblue';
      }else{
        item.style.backgroundColor = 'darkblue';
      }
      this.changeLineAniFlag();
    },

    // 散点中的自定义事件 显示三维结构
    scatterShowMol(node) {
      this.$refs.molPlot.barClick(node);
    },
    // 绘制雷达图
    scatterShowRadar(node) {
      console.log("展示雷达图", node);
      this.$refs.radarChart.radarClick(node);
    },


    closeAreaPlot(event){
      
      event.target.parentNode.style.display = 'none';
    },

    addBar(e) {
      this.bars.push({
        barClass: nanoid(10).replace(/-/g, "").replace(/_/g, ""),
        barData: e.dataTransfer.getData("framePocket").trim().split(","),
        barName: nanoid(10).replace(/-/g, "").replace(/_/g, ""),
        barColor: e.dataTransfer.getData("color"),
      });
      console.log(this.bars);
    },
    // 滑动块结束事件,显示
    barSlider(node) {
      // 显示三维结构
      this.$refs.molPlot.lineSlider(node);
      // 高亮
    },
    barClick(node) {
      console.log("App barClick ", node);
      this.$refs.molPlot.barClick(node);
    },

    scatterLinkLine(nodes) {
      // 调用绘线方法
      this.$refs.scatterPlot.circleLinkLine(nodes);
    },
    // 页面销毁
    pocketUnload() {
      // 数据存储
    },
    addCluster(e){
      
        this.selectClusters.push({
          frameList: e.dataTransfer.getData("framePocket").trim().split(","),
          color: e.dataTransfer.getData("color"),
          clusterId: nanoid(10).replace(/-/g, "").replace(/_/g, ""),
          pathStr: e.dataTransfer.getData('pathStr'),
        });
        this.colorList.push(e.dataTransfer.getData("color"));
        if(this.extentList.length == 0){
          e.dataTransfer.getData('valueExtent').slice(1,e.dataTransfer.getData('valueExtent').length + 1).trim().split(",").forEach((item,index) => {
            if(index % 2 == 0){
              this.extentList.push([]);
            }
            this.extentList[parseInt(index / 2)].push(parseFloat(item));
          });
        }
      
      
    },
    showClusters(e){
      if(this.showFlag){
        document.getElementById('clusterContainer').style.left = '-199px';
      }else{
        document.getElementById('clusterContainer').style.left = '0px';
      }
      this.showFlag = !this.showFlag;
      
    },
  },
};
</script>
<style lang="less">
// svg {
//   border: 1px solid rgba(31, 31, 31, 0.99);
// }

* {
  margin: 0;
}
.app {
  width: 100%;
  height: 100%;
  overflow: auto;
}
.annotation {
  width: 100%;
  height: 416px;
}
header {
  text-align: center;
  line-height: normal;
}
.container {
  /* height: 100%; */
  position: relative;
  top: 0;
  right: 0;
  z-index: 9;
  width: 100%;
  max-width: 1500px;
}
.con_top {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
}
.card_header {
  display: block;
  font-size: 10px;
  // height: 7px;
}

.con_center {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  .center_left {
    width: 100%;
    height: 100%;
    .card_content {
      display: flex;
      flex-direction: column;
      // justify-content: center;
      align-items: center;
      height: 480px;
      width: 100%;
      overflow-y: auto;
      overflow-x: hidden;
      .center_left_child {
        width: 210px;
        height: 200px;
        margin: 3px;
      }
      .center_left_add {
        .plus_big {
          font-size: 190px;
          color: #aaa;
        }
      }
    }
  }
  .center_scatter {
    width: 100%;
    height: 800px;
  }

  .aniFlagBtn{
    float: right;
    text-align: center;
    line-height: 20px;
    width: 70px;
    height: 20px;
    background-color: deepskyblue;
    color: #ffffff;
    cursor: pointer;
    margin: 0px 10px;
  }

  .center_right {
    width: 100%;
    height: 100%;
    .card_content {
      display: flex;
      flex-direction: column;
      // justify-content: center;
      align-items: center;
      width: 100%;
      height: 600px;
      overflow: auto;
      overflow-x: hidden;
    }
  }
}

.con_bottom {
  width: 100%;
  height: 100%;
  .bottom_right {
    width: 100%;
    height: 100%;
  }
}

.addCluster {
  overflow: auto;
}
.center_left_child{
  padding-right: 10px;
}
div::-webkit-scrollbar {
  width: 3px;
}
div::-webkit-scrollbar-track {
  background: rgb(239, 239, 239);
  border-radius: 2px;
}
div::-webkit-scrollbar-thumb {
  background: #40a0ff49;
  border-radius: 10px;
}
div::-webkit-scrollbar-thumb:hover {
  background: #40a0ff;
}


div::-moz-scrollbar {
  width: 3px;
}
div::-moz-scrollbar-track {
  background: rgb(239, 239, 239);
  border-radius: 2px;
}
div::-moz-scrollbar-thumb {
  background: #40a0ff49;
  border-radius: 10px;
}
div::-moz-scrollbar-thumb:hover {
  background: #40a0ff;
}
</style>

<style scoped>
.el-card__body {
  padding: 5px;
}
.clusterChild{
  width: 100%;
  height: 200px;
}

#clusterContainer{
  position: absolute;
  width: 200px;
  height: 100%;
  left: -200px;
  border: 1px solid #000000;
  transition: all 0.3s;
  -webkit-transition:all 0.3s;
  z-index: 999;
}


#addClusterIcon i{
  margin-left: 40px;
  line-height: 200px;
  font-size: 8rem;
}
.clustersShow{
  cursor: pointer;
  width: 50px;
  height: 50px;
  position: absolute;
  top: 45%;
  left: 199px;
  background-color: cornflowerblue;
  line-height: 50px;
  text-align: center;
  color: aliceblue;
  border-radius: 0px 10px 10px 0px;
  z-index: 9999;
}

.itemCont{
  width: 200px;
  height: 100%;
  margin-bottom: 20px;
  overflow: auto;
  overflow-x: hidden;
}
#areaContainer{
  display: none;
  position: absolute;
  width: 800px;
  height: 500px;
  background-color: aliceblue;
  top: 400px;
  left: 700px;
  border: 1px solid #000000;
  transition: all 0.3s;
  -webkit-transition:all 0.3s;
  z-index: 999;
}
.areaPlotClose{
  position: absolute;
  right: 20px;
  top: 5px;
  cursor: pointer;
  font-size: 2rem;
}

</style>
