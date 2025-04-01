<template>
  <el-upload
          class="pop-upload"
          ref="upload"
          action=""
          :file-list="fileList"
          :auto-upload="false"
          :multiple="true"
          :on-change="handleChange"
          :on-remove="handleRemove"
          v-loading="loading"
  >
      <el-button slot="trigger" size="small" type="primary">select file</el-button>
      <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">upload</el-button>
  </el-upload>
</template>
  
  <script>
  import axios from "axios";
  import { request } from "@/network/request";
  export default {
    data() {
      return {
        fileList: [],
        search: "",
        file_list: "",
        loading: false,
      };
    },
    methods: {
      handleChange(file, fileList) {
                this.fileList = fileList
            },
            // 删除文件之前的钩子，参数为上传的文件和文件列表，若返回 false 或者返回 Promise 且被 reject，则停止删除。function(file, fileList)
            handleRemove(file, fileList) {
                this.fileList = fileList
            },
            //上传服务器
            submitUpload() {
                //判断是否有文件再上传
                if (this.fileList.length != 2) {
                    return this.$message.warning('Please select the correct file and upload it again.')
                }
                // 下面的代码将创建一个空的FormData对象:
                const formData = new FormData()
                // 你可以使用FormData.append来添加键/值对到表单里面；
                this.fileList.forEach((file) => {
                  console.log(file.name.split('.')[1]);
                    formData.append(file.name.split('.')[1], file.raw)
                })
                this.loading = true;
                //自定义的接口也可以用ajax或者自己封装的接口
                request({
                    method: 'POST',
                    url: 'http://localhost:5050/upload',   //填写自己的接口
                    data: formData        //填写包装好的formData对象
                }).then(res => {
                    if (res != null) {
                      this.$alert('upload success,the token is ' + res, 'tip', {
                        confirmButtonText: 'yes',
                        callback: action => {
                          this.$message({
                            type: 'info',
                            message: `action: ${ action }`
                          });
                        }
                      });
                      this.loading = false;
                    } else {
                        this.$message.error('upload failed.');
                    }
                    //清空fileList
                    this.fileList = []
                })
            },
    },
  };
  </script>
  
  <style>
  </style>
  