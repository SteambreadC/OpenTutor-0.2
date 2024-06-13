<template>
  <div class="welcome">
    <h1>欢迎使用AI个人学习助手</h1>
    <p>这个应用可以帮助你预测考试题目，生成模拟试卷，以及提供学习辅导。</p>
    <button @click="start">开始</button>
  </div>
</template>

<script>
export default {
  name: 'Welcome',
  methods: {
    start() {
      this.$router.push('/create-course');
    }
  }
};
</script>

<style scoped>
.welcome {
  text-align: center;
  margin-top: 50px;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
}
</style>
