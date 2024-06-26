<template>
  <div class="waiting">
    <img alt="logo of Redpanda" src="../assets/winterRedpanda.jpg" class="logo" />
    <h1>生成预测中...</h1>
    <img src="../assets/icons8-loading2.gif" alt="Loading..." class="loading" />

  </div>
</template>

<script>
import axios from "axios";
import {mapActions} from "vuex";

export default {
  name: 'Waiting',

  props: {
    courseId: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      processedFiles: []
    };
  },

  created() {
    this.checkProcessedFiles();
  },

methods: {
    ...mapActions(['updateResultFiles']),

    async checkProcessedFiles() {
        try {
            const response = await axios.get(`/api/processed-files?course_id=${this.courseId}`);
            if (response.data.status === "processing") {
                await this.pollTaskStatus(response.data.task_id);
            } else {
                this.handleProcessedFiles(response.data.processed_files);
            }
        } catch (error) {
            console.error('Error checking processed files:', error);
            setTimeout(this.checkProcessedFiles, 5000);
        }
    },

    async pollTaskStatus(taskId) {
        try {
            const response = await axios.get(`/api/task-status?task_id=${taskId}&course_id=${this.courseId}`);
            if (response.data.status === "completed") {
                this.handleProcessedFiles(response.data.processed_files);
            } else if (response.data.status === "error") {
                console.error('Error processing files:', response.data.message);
                // 处理错误情况，可能需要显示错误消息给用户
            } else {
                setTimeout(() => this.pollTaskStatus(taskId), 5000);
            }
        } catch (error) {
            console.error('Error polling task status:', error);
            setTimeout(() => this.pollTaskStatus(taskId), 5000);
        }
    },

    handleProcessedFiles(files) {
        if (!files){
          console.error("No processed files available.");
          alert("No processed files available.")
        }

        this.processedFiles = files;
        this.updateResultFiles({courseId: this.courseId, files: this.processedFiles});
        this.$router.push({name: 'Results', params: {courseId: this.courseId}});
    }
    /*
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
          this.processedFiles = response.data.processed_files;
          this.$store.commit("setResultFiles",{ courseId: this.courseId, files: this.processedFiles});
          setTimeout(()=>{
              this.$router.push({
                  name: 'Results',
                  params:{courseId: this.courseId}
              });
          },0);
        } else {
          setTimeout(this.checkProcessedFiles, 5000); // 5秒后再检查一次
        }
      })
      .catch(error => {
        console.error('Error checking processed files:', error);
        setTimeout(this.checkProcessedFiles, 5000); // 5秒后再检查一次
      });
    }
    */
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
