<template>
  <div id="app">
    <a-layout>
      <!-- 顶部导航栏 -->
      <a-layout-header class="header">
        <div class="logo">Logo</div>
        <a-menu
          theme="dark"
          mode="horizontal"
          :style="{ lineHeight: '64px' }"
          :selectedKeys="[current]"
          @click="handleMenuClick"
        >
          <a-menu-item key="1">首页</a-menu-item>
          <a-menu-item key="2">产品</a-menu-item>
          <a-menu-item key="3">关于</a-menu-item>
        </a-menu>
      </a-layout-header>
      
      <!-- 中间内容区域 -->
      <a-layout-content class="content">
        <div class="content-inner">
          <h1>主内容区域</h1>
          <p>当前选中的菜单: {{ current }}</p>
          <p class="success-message">✅ 成功使用自定义入口: src/index/index.html</p>
          <div class="features">
            <a-card title="Vite 优势" class="feature-card">
              <ul>
                <li>⚡️ 极快的冷启动（300ms 以内）</li>
                <li>🔥 即时热模块替换（HMR）</li>
                <li>🎨 开箱即用的 CSS 预处理器支持</li>
                <li>📦 优化的生产构建</li>
              </ul>
            </a-card>
          </div>
        </div>
      </a-layout-content>
      
      <a-layout-footer class="footer">
        © {{ new Date().getFullYear() }} Furina Web - 保留所有权利
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script>
import { 
  ALayout, 
  ALayoutHeader, 
  ALayoutContent, 
  ALayoutFooter,
  AMenu,
  AMenuItem,
  ACard
} from 'ant-design-vue';

export default {
name: 'App',
  components: {
    'a-layout': ALayout,
    'a-layout-header': ALayoutHeader,
    'a-layout-content': ALayoutContent,
    'a-layout-footer': ALayoutFooter,
    'a-menu': AMenu,
    'a-menu-item': AMenuItem,
    'a-card': ACard
  },
  data() {
    return {
      current: '1'
    }
  },
  methods: {
    handleMenuClick(e) {
      this.current = e.key;
    },
    
    // 触发挂载事件
    appMounted() {
      this.$appMounted();
    }
  },
  
  mounted() {
    this.appMounted();
  }
}
</script>

<style lang="less">
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: @text-color;
}

.header {
  display: flex;
  align-items: center;
  padding: 0 20px;
  background: @menu-dark-bg;
}

.logo {
  width: 120px;
  height: 31px;
  margin-right: 24px;
  color: white;
  font-size: 18px;
  font-weight: 600;
  line-height: 31px;
}

.content {
  padding: 24px;
  min-height: calc(100vh - 64px - 70px);
  background-color: @background-color-light;
}

.content-inner {
  background: #fff;
  padding: 24px;
  border-radius: @border-radius-base;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  min-height: 100%;
}

.footer {
  text-align: center;
  background: #f0f2f5;
  padding: 24px 50px;
  color: lighten(@text-color, 20%);
  font-size: 14px;
}

/* 菜单样式 */
.ant-menu-dark {
  background-color: @menu-dark-bg !important;
  
  .ant-menu-item:hover {
    background-color: @menu-dark-item-hover-bg !important;
  }
  
  .ant-menu-item-selected {
    background-color: @menu-dark-item-active-bg !important;
    color: @menu-dark-highlight-color !important;
  }
}

.success-message {
  color: #52c41a;
  font-weight: bold;
  margin: 15px 0;
}

.features {
  margin-top: 20px;
}

.feature-card {
  max-width: 500px;
  margin-top: 15px;
  
  ul {
    padding-left: 20px;
    
    li {
      margin: 8px 0;
      line-height: 1.6;
    }
  }
}
</style>