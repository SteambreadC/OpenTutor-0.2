<template>
  <div class="waiting">
    <h1>生成预测中...</h1>
    <img src="../assets/icons8-loading2.gif" alt="Loading..." />

  </div>
</template>

<script>
export default {
  name: 'Waiting',
  data() {
    return {
      resultReady: false,
      timer: null,
    };
  },
  mounted() {
    this.checkResult();
  },
  methods: {
      checkResult() {
        this.timer = setInterval(async () => {
          // 在这里调用后端 API 来检查结果是否准备好
          // 如果结果准备好了,将 `this.resultReady` 设为 `true`
          // 例如:
          // const response = await axios.get('/api/check-result');
          // this.resultReady = response.data.ready;
        }, 1000); // 每秒检查一次
      },
    },
  watch: {
      resultReady(newValue) {
        if (newValue) {
          clearInterval(this.timer);
          this.$router.push('/results');
        }
      },
    },
    beforeUnmount() {
      clearInterval(this.timer);
    },
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
