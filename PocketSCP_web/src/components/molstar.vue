<template>
  <div ref="molstar" class="molstar"></div>
</template>

<script>
export default {
  name: "molstar",
  data() {
    return {
      viewerInstance: null,
      frame: [], // 接收拖入的数据
      framePocket: "1_1",
      colors:['#FF8C00','#98F5FF','#98F5FF'],
      changecolor:[
          //   {
            
          //     struct_asym_id: 'C',
          //     start_residue_number: 4,
          //     end_residue_number: 4,
          //     color: '#BBFFFF',
          //   },
           ],
    };
  },
  mounted() {
    this.initMolstar();
  },
  methods: {
    initMolstar() {
      this.viewerInstance = new PDBeMolstarPlugin();
      let options = {
        customData: {
          url:
            "api/molStar/molStarInit?frame_pocket=" +
            this.framePocket,
          format: "pdb",
        },
        // visualStyle: "cartoon",//卡通
        visualStyle: "molecular-surface", // 分子表面
        // visualStyle: "carbohydrate",             // 碳水化合物
        // visualStyle: 'distance-restraint',
        // visualStyle:"putty",                     // 线
        // visualStyle: "mesh",                        // 球
        bgColor: { r: 255, g: 255, b: 255 },
        hideControls: true,
        landscape: false,
        selection: {
          data: [
            {
           
              struct_asym_id: 'C',
              start_residue_number: 1,
              end_residue_number: 13,
              color:this.colors[0],
             
            },
            
        //     {
           
        //    struct_asym_id: 'C',
        //    start_residue_number: 2,
        //    end_residue_number: 10,
        //    color: this.colors[1],
         
        //  },
          ],
        
          // nonSelectedColor: '#ddcbbc',
        },

      };

      String.prototype.colorHex = function () {
  // RGB颜色值的正则
      var reg = /^(rgb|RGB)/;
      var color = this;
      if (reg.test(color)) {
        var strHex = "#";
        // 把RGB的3个数值变成数组
        var colorArr = color.replace(/(?:\(|\)|rgb|RGB)*/g, "").split(",");
        // 转成16进制
        for (var i = 0; i < colorArr.length; i++) {
          var hex = Number(colorArr[i]).toString(16);
          if (hex === "0") {
            hex += hex;
          }
          strHex += hex;
        }
        return strHex;
      } else {
        return String(color);
      }
    };


      this.viewerInstance.render(this.$refs.molstar, options);
    },
    colorHex(color) {
      var that = color;
      //十六进制颜色值的正则表达式
      var reg = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/;
      // 如果是rgb颜色表示
      if (/^(rgb|RGB)/.test(that)) {
          var aColor = that.replace(/(?:\(|\)|rgb|RGB)*/g, "").split(",");
          var strHex = "#";
          for (var i=0; i<aColor.length; i++) {
              var hex = Number(aColor[i]).toString(16);
              if (hex.length < 2) {
                  hex = '0' + hex;    
              }
              strHex += hex;
          }
          if (strHex.length !== 7) {
              strHex = that;    
          }
          return strHex;
      } else if (reg.test(that)) {
          var aNum = that.replace(/#/,"").split("");
          if (aNum.length === 6) {
              return that;    
          } else if(aNum.length === 3) {
              var numHex = "#";
              for (var i=0; i<aNum.length; i+=1) {
                  numHex += (aNum[i] + aNum[i]);
              }
              return numHex;
          }
      }
      return that;
    },
     lineSlider(pocketData) {
      let that=this;
      this.changecolor=[];
      that.colors = [];
      let endStr = '';
      endStr = pocketData.split(',')[0] + ',';
      let tempList = pocketData.replace(endStr,'').split('-');
      tempList.forEach(item => {
        endStr += item.split('/')[0] + '-';
        let tempColor = item.split('/')[1].replace(' ','');
        that.colors.push(String(that.colorHex(tempColor)));
      });
      endStr = endStr.substring(0, endStr.length - 1);
      // Update data to create new visual ,第二个参数代表什么？
      fetch('api/molStar/caculatecolor?frame_pocket=' + endStr)
      .then(response => response.json())
      .then(data=>{
        for (let i = 0; i < data.length; i++) {
          let newObj={
            struct_asym_id: 'C',
            start_residue_number: parseInt(data[i]),
            end_residue_number: parseInt(data[i]),
            color: that.colors[i],
          }
          this.changecolor.push(newObj)
        }
        this.viewerInstance.visual.update(
        {
          customData: {
            // 返回的数据是由frameinfo和pocketinfo组成的pdb文件
            url:
              "api/molStar/slider?frame_pocket=" + endStr,
            format: "pdb",
          },
          bgColor: { r: 255, g: 255, b: 255 },
          visualStyle: "molecular-surface",
          selection: {
          data: this.changecolor,       
        
          // nonSelectedColor: '#ddcbbc',
        },

        },
        true
      );
      })
      // this.viewerInstance.visual.update(
      //   {
      //     customData: {
      //       // 返回的数据是由frameinfo和pocketinfo组成的pdb文件
      //       url:
      //         "http://127.0.0.1:5000/molStar/slider?frame_pocket=" + pocketData,
      //       format: "pdb",
      //     },
      //     bgColor: { r: 255, g: 255, b: 255 },
      //     visualStyle: "molecular-surface",
      //     selection: {
      //     data: this.changecolor,       
        
      //     // nonSelectedColor: '#ddcbbc',
      //   },

      //   },
      //   true
      // );
    },
    // 兄弟组件点击时调用
    barClick(node) {
      this.viewerInstance.visual.update(
        {
          customData: {
            url:
              "api/molStar/framePocket?frame_pocket=" +
              node["frame_pocket"],
            format: "pdb",
          },
          bgColor: { r: 255, g: 255, b: 255 },
          visualStyle: "molecular-surface",
        },
        true
      );
    },
  },
};
</script>

<style scoped>
.molstar {
  float: left;
  position: relative;
  left: 13%;
  width: 355px;
  height: 355px;
  position: relative;
}
</style>
