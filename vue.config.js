const path = require('path');
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  publicPath: process.env.NODE_ENV === 'production' 
    ? '/furina-toolbox/' 
    : '/',
  
  // 使用 pages 配置作为主要入口点配置
  pages: {
    index: {
      entry: path.resolve(__dirname, 'src/index/main.js'),
      template: path.resolve(__dirname, 'src/index/index.html'),
      filename: 'index.html',
      title: '芙宁娜工具箱'
    }
  },
  
  // 使用 chainWebpack 添加额外配置
  chainWebpack: config => {
    // 不需要手动配置入口点，因为 pages 已经处理了
    
    // 设置别名
    config.resolve.alias
      .set('@', path.resolve(__dirname, 'src'))
      .set('@main', path.resolve(__dirname, 'src/index'));
    
    // 如果需要修改 HTML 插件配置（可选）
    config.plugin('html').tap(args => {
      args[0] = {
        ...args[0],
        // 可以在这里覆盖或添加额外的 HTML 插件选项
        minify: {
          removeComments: true,
          collapseWhitespace: true,
          removeAttributeQuotes: false
        }
      };
      return args;
    });
  },
  
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
      watch: true
    },
    hot: true,
    open: true,
    port: 8080,
    client: {
      overlay: {
        warnings: false,
        errors: true
      }
    }
  },
  
  productionSourceMap: false,
  
  // 添加其他 Vue CLI 配置选项
  css: {
    extract: true,
    sourceMap: false
  },
  
  configureWebpack: {
    // 可以在这里添加额外的 webpack 配置
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    }
  }
});