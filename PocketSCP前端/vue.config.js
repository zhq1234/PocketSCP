const path = require('path');
function resolve (dir) {
    return path.join(__dirname, dir)
}
module.exports = {
    productionSourceMap: false,
    devServer: {
        port: 8080, //  配置端口号
        host: "127.0.0.1", // 访问地址
        open: true, //  自动打开浏览器
        historyApiFallback: true,
        allowedHosts: "all",
        proxy: {
            '/api': {
              target: 'http://127.0.0.1:5050',
              changeOrigin: true,
              pathRewrite: { '^/api': '' },
            },
        },
    }
}