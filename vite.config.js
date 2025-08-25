import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  // 设置根目录为 src/index
  root: path.resolve(__dirname, 'src/index'),
  
  // 构建配置
  build: {
    outDir: path.resolve(__dirname, 'dist'),
    rollupOptions: {
      input: {
        // 入口文件位于 src/index/index.html
        main: path.resolve(__dirname, 'src/index/index.html')
      }
    }
  },
  
  plugins: [vue()],
  
  // 预览服务器配置
  preview: {
    port: 8080,
    strictPort: true,
    // 确保所有路由返回 index.html
    historyApiFallback: true
  },
  
  resolve: {
    alias: {
      // 设置别名，指向 src 目录
      '@': path.resolve(__dirname, 'src'),
      // 添加当前目录的别名
      '~': path.resolve(__dirname, 'src/index')
    }
  },
  
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        modifyVars: {
          'primary-color': '#0071FF',
          'menu-dark-bg': '#0071FF',
          'menu-dark-item-active-bg': '#0058d4',
          'menu-dark-item-hover-bg': '#0065eb',
          'menu-dark-item-color': 'rgba(255, 255, 255, 0.9)',
          'menu-dark-highlight-color': '#fff',
          'text-color': '#2c3e50',
          'border-color-base': '#ebedf0',
          'background-color-light': '#f8f9fa',
          'border-radius-base': '4px'
        }
      }
    }
  },

  // 开发服务器配置
  server: {
    port: 5173,
    strictPort: true,
    open: '/index.html' // 自动打开 index.html
  },

  optimizeDeps: {
    // 强制排除 Ant Design Vue 的预构建
    exclude: ['ant-design-vue']
  }
});