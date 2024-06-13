<template>
  <div class="waiting">
    <h1>生成预测中...</h1>
    <img src="../assets/icons8-loading2.gif" alt="Loading..." />

  </div>
</template>

<script>
import LottieAnimation from "./LottieAnimation.vue";
export default {
  name: 'Waiting',
    components: {LottieAnimation},
  mounted() {
    setTimeout(() => {
      this.$router.push('/results');
    }, 20000); // 模拟等待时间
  }
};
</script>

<style scoped>
.waiting {
  text-align: center;
  margin-top: 50px;
}
img {
  margin-top: 20px;
  width: 100px;
}
</style>
