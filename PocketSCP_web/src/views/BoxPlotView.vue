<template>
  <div
    id="boxPlot"
    ref="boxPlotRef"
    @drop="boxPlotDrop"
    @dragover.prevent
    @mousemove="mouseXY"
    style="width: 100%; height: 140px"
  ></div>
</template>

<script>
import { request } from "@/network/request";
import axios from "axios";
let parallel_frame_pocket = [
  "2_4",
  "3_3",
  "4_6",
  "4_11",
  "5_4",
  "6_3",
  "8_11",
  "9_2",
  "11_7",
  "12_9",
  "13_3",
  "16_8",
  "19_8",
  "22_7",
  "23_9",
  "24_9",
  "25_5",
  "27_1",
  "29_1",
];
export default {
  name: "BoxPlotView",
  data() {
    return {
      charts: null, //

      pocketData: [], // 请求数据
      frameData: [],
      columnName: [], // 列名
      rangeData: [], // 范围
      mapIndex: [], // 下标映射
      arrs: [],
      mouseX: 0, // 鼠标位置
    };
  },
  mounted() {
    this.pocketData = parallel_frame_pocket;
    this.initData();
    // this.myEcharts()
  },
  methods: {
    async initData() {
      let that = this;
      await axios({
        url: "api/parallelPlot/index",
        method: "post",
        data: {
          frame_pocket: that.pocketData,
        }
      }).then((res) => {
          if (res.status === 200) {
            let volumes = res.data.data["frame_pocket_data"].map(
              (item) => item.volume
            );
            that.arrs.push(volumes);
            let frame_pockets = res.data.data["frame_pocket_data"].map(
              (item) => item.frame_pocket
            );

            that.frameData = res.data.data["frame_pocket_data"]; // 每一帧的各个属性值
            that.columnName = res.data.data["columnName"]; // 显示的列名
            that.rangeData = res.data.data["rangeData"]; // 返回属性范围
            that.mapIndex = res.data.data["mapIndex"]; // 下标映射
            that.myEcharts();
          }
        })
        .catch((err) => {
          console.log(err);
        });
      // that.drawChart();
    },
    myEcharts() {
      let that = this;
      let myChart = echarts.init(document.getElementById("boxPlot"));
      let data = echarts.dataTool.prepareBoxplotData(that.arrs);
      console.log("echarts_data", data);

      var option = {
        tooltip: {
          position: "right",
          trigger: "item",
          axisPointer: {
            type: "shadow", //鼠标悬停在箱上会显示阴影
          },
        },
        grid: {
          left: "5%", //可视化网格距离左部百分比位置
          right: "5%", //可视化网格距离右部百分比位置
          top: "5%", //可视化网格距离底部百分比位置
          bottom: "15%", //可视化网格距离底部百分比位置
        },
        xAxis: {
          type: "category",
          data: data.axisData, //使用data处理后的axisData数据
          axisLabel: {
            formatter: function (params) {
              return "pocket set " + (1 + parseInt(params));
            }, //x轴名称模板
          },
        },
        yAxis: {
          type: "value",
          name: "",
          splitArea: {
            show: true, //y轴网格间阴影区分显示
          },
        },
        series: [
          {
            type: "boxplot",
            data: data.boxData, //使用data的处理后的boxData数据
            tooltip: {
              //以下是设置tooltip的显示数据和显示格式
              formatter: function (param) {
                return [
                  "pocket set " + (parseInt(param.name) + 1) + ": ",
                  "max: " + param.data[5].toFixed(2),
                  "Q1: " + param.data[4].toFixed(2),
                  "median: " + param.data[3].toFixed(2),
                  "Q3: " + param.data[2].toFixed(2),
                  "min: " + param.data[1].toFixed(2),
                ].join("<br/>");
              },
            },
          },
          {
            name: "outlier",
            type: "scatter", //使用散点图显示异常值
            data: data.outliers, //异常值数据
          },
        ],
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
      myChart.on("click", function () {
        console.log(111);
      });
    },

    mouseXY(e) {
      this.mouseX = e.offsetX;
    },

    boxPlotDrop(event) {
      // console.log(event.dataTransfer.getData("framePocket"));
      this.pocketData = event.dataTransfer
        .getData("framePocket")
        .trim()
        .split(",");
      this.initData();
    },
    parallelClick(node) {
      console.log(node);
      this.$emit("parallelShowMol", node);
      this.$emit("parallelScatterLinkLine", node["frame_pocket"]);
      this.highlightScatter(node["frame_pocket"]);
    },
  },
};
</script>

<style scoped>
#boxPlot {
  /* width: 800px;
  height: 200px; */
}
</style>
