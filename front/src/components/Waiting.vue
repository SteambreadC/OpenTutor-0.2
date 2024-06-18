<template>
  <div class="waiting">
    <img alt="logo of Redpanda" src="../assets/winterRedpanda.jpg" class="logo" />
    <h1>生成预测中...</h1>
    <img src="../assets/icons8-loading2.gif" alt="Loading..." class="loading" />

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'Waiting',

  props: {
    courseId: {
      type: String,
      required: true
    }
  },

  created() {
    // 检查处理结果，处理完成后跳转到结果页面
    this.checkProcessedFiles();
  },
  methods: {
    checkProcessedFiles() {
      const token = localStorage.getItem('token');
      //const courseId = this.courseId

      axios.get(`http://localhost:8010/api/processed-files?course_id=${this.courseId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        if (response.data.processed_files.length > 0) {
          setTimeout(()=>{
              this.$router.push({ name: 'Results', params: { courseId:this.courseId }});
          },2000);
        } else {
          setTimeout(this.checkProcessedFiles, 5000); // 5秒后再检查一次
        }
      })
      .catch(error => {
        console.error('Error checking processed files:', error);
        setTimeout(this.checkProcessedFiles, 5000); // 5秒后再检查一次
      });
    }
  }
};
</script>

<style scoped>
.waiting {
  text-align: center;
  margin-top: 50px;
}
.loading {
  margin-top: 20px;
  width: 100px;
}
</style>
