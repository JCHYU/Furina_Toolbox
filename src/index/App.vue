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
          <p>页面内容...</p>
          <!-- 这里可以放置页面主要内容 -->
        </div>
      </a-layout-content>
      
      <a-layout-footer class="footer">
        None
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
}
.header {
  display: flex;
  align-items: center;
  background: #001529;
  padding: 0 20px;
}
.logo {
  width: 120px;
  height: 31px;
  margin-right: 24px;
  color: white;
  font-size: 18px;
  line-height: 31px;
}
.content {
  padding: 24px;
  min-height: calc(100vh - 64px - 70px); /* 视口高度 - 头部高度 - 底部高度 */
}
.content-inner {
  background: #fff;
  padding: 24px;
  min-height: 100%;
}
.footer {
  text-align: center;
  background: #f0f2f5;
  padding: 24px 50px;
}
</style>