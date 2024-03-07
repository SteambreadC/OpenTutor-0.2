<template>
  <div class="left-sidebar">
    <ul>
      <li><router-link to="/">首页</router-link></li>
      <li><router-link to="/about">关于我们</router-link></li>
      <li><router-link to="/contact">联系方式</router-link></li>
      <!-- 添加更多链接 -->
    </ul>
  </div>
</template>

<script>
export default {
  name: 'LeftSidebar',
  // 组件逻辑
}
</script>

<style>
.left-sidebar {
  /* 样式 */
  width: 100px;
  background-color: cadetblue;
}
</style>
