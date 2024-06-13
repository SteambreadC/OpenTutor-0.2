<template>
  <div class="create-course">
    <h1>创建课程</h1>
    <form @submit.prevent="submitCourse">
      <div v-if="!skip">
        <div>
          <label>课程名称:</label>
          <input v-model="courseName" />
        </div>
        <div>
          <label>学校:</label>
          <input v-model="school" />
        </div>
        <div>
          <label>教授名:</label>
          <input v-model="professor" />
        </div>
        <div>
          <label>年级:</label>
          <input v-model="grade" />
        </div>
        <div>
          <label>其他信息:</label>
          <input v-model="otherInfo" />
        </div>
        <button type="submit">提交</button>
      </div>
      <button @click="skipCourse">跳过</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'CreateCourse',
  data() {
    return {
      courseName: '',
      school: '',
      professor: '',
      grade: '',
      otherInfo: '',
      skip: false
    };
  },
  methods: {
    submitCourse() {
      // 这里你可以添加提交课程信息的逻辑
      this.$router.push('/upload-material');
    },
    skipCourse() {
      this.skip = true;
      this.$router.push('/upload-material');
    }
  }
};
</script>

<style scoped>
.create-course {
  text-align: center;
  margin-top: 50px;
}
form > div {
  margin-bottom: 20px;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
}
</style>
