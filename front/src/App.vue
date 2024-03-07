<template>
    <div class="app-container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">I'm your GPT study assistant :D</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="nav nav-tabs">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/ta-test">TA Test</router-link>
          </li>
          <!-- 更多导航项 -->
        </ul>
      </div>
    </div>
    </nav>

    <div class="content">
    <img alt="logo of Redpanda" src="./assets/winterRedpanda.jpg" class="logo" />
    <!-- TAtest1 msg="TA test here:" / -->
    <router-view class="view main-content"></router-view>
    </div>
    <footer class="footer">
      © 2024 My Website
    </footer>
    </div>
</template>

<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TAtest1 from './components/TAtest1.vue'

// This starter template is using Vue 3 experimental <script setup> SFCs
// Check out https://github.com/vuejs/rfcs/blob/script-setup-2/active-rfcs/0000-script-setup.md
</script>

<style>
#app {
  font-family: Montserrat, Avenir, Helvetica, Arial, Roboto, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: wheat;
  font-weight: 500;
  margin-top: 0;
}

.app-container{
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.content{
    flex:1 auto;
}

.logo{
  align-content: center;
  width: 400px; /* 例如，设置宽度为100px */
  height: auto; /* 高度自适应 */
  max-height: 400px;
  border-radius: 30px;
}

body {
  background: linear-gradient(to right, #6a11cb 0%, #2575fc 200%);
}
/* 自定义导航栏样式 */
.navbar {
  margin-bottom: 30px;
}

ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 30px;
}

li:not(:last-of-type) {
  margin-right: 1rem;
}

.footer {
  text-align: center;
  padding: 10px 0;
  background-color: #f8f9fa; /* Light grey background, adjust as needed */
  border-top: 1px solid #e7e7e7; /* Light grey border, adjust as needed */
}

/* 调整下拉菜单容器的样式 */
.navbar-nav .dropdown-menu {
  background-color: #f8f9fa; /* 修改背景颜色 */
}

/* 调整下拉菜单项的样式 */
.navbar-nav .dropdown-item {
  color: #007bff; /* 修改文字颜色 */
  text-align: center; /* 文字居中 */
}
</style>
