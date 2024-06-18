<template>
  <div class="welcome">
    <img alt="logo of Redpanda" src="../assets/winterRedpanda.jpg" class="logo" />
    <h1>欢迎使用AI个人学习助手</h1>
    <p>这个应用可以帮助你预测考试题目，生成模拟试卷，以及提供学习辅导。</p>
    <button type="submit" class="btn btn-primary" @click="start">开始</button>
  </div>
</template>

<script>
export default {
  name: 'Welcome',
  methods: {
    start() {
      this.$router.push('/handle');
    }
  }
};
</script>

<style scoped>
.logo{
  margin-bottom: 25px;
}

.welcome {
  text-align: center;
  margin-top: 50px;
}
button {
  margin-top: 20px;
  padding: 15px 30px;
  color: #471081;
  background: #fcfcfc;
  font-family: 'Arial', sans-serif; /* 设置字体系列 */
  font-size: 16px; /* 设置字体大小 */
  font-weight: bold; /* 设置字体粗细 */
}
</style>
