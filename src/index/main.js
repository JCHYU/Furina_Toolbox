import { createApp } from 'vue';
import App from './App.vue';

import AntDesignVue from 'ant-design-vue/es';
import 'ant-design-vue/dist/reset.css';

console.log('🚀 Vue应用开始初始化');

const app = createApp(App);

// 使用 Ant Design Vue
app.use(AntDesignVue); // 使用默认导出的模块

// 添加挂载事件方法
app.config.globalProperties.$appMounted = function() {
  console.log('✅ 触发挂载事件');
  const event = new Event('vue:mounted');
  document.getElementById('app').dispatchEvent(event);
};

app.mount('#app');