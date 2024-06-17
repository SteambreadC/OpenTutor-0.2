<template>
  <transition name="fade" mode="out-in">
    <div v-if="!courseId" class="upload-page">
      <h1 class="upload-title">创建课程</h1>
      <form @submit.prevent="submitCourse" class="upload-form">
        <div class="form-group">
          <label for="courseName">课程名称:</label>
          <input type="text" id="courseName" class="file-input" v-model="courseData.courseName">
        </div>
        <div class="form-group">
          <label for="school">学校:</label>
          <input type="text" id="school" class="file-input" v-model="courseData.school">
        </div>
        <div class="form-group">
          <label for="professor">教授名称:</label>
          <input type="text" id="professor" class="file-input" v-model="courseData.professor">
        </div>
        <div class="form-group">
          <label for="year">年份:</label>
          <input type="text" id="year" class="file-input" v-model="courseData.year">
        </div>
        <div class="form-group">
          <label for="info">其他信息:</label>
          <input type="text" id="info" class="file-input" v-model="courseData.info">
        </div>
        <div class="button-group">
          <button type="submit" class="submit-button">提交</button>
          <button type="button" class="skip-button" @click="skipCourse">跳过</button>
        </div>
      </form>
    </div>
      <upload-material v-else="courseId" :courseId="courseId"></upload-material>
  </transition>
</template>

<script>
import axios from "axios";
import UploadMaterial from './UploadMaterial.vue';

export default {
  name: 'CreateCourse',
  components: {
    UploadMaterial
  },
  data() {
    return {
      courseData: {
          courseName: '',
          school: '',
          professor: '',
          year: '',
          info: '',
          skip: false
      },
      courseId: '' // 用于存储生成的课程ID
    };
  },
  methods: {
    async submitCourse() {
      const formData = new FormData();
      for (let key in this.courseData) {
        if (this.courseData[key]) {
          formData.append(key, this.courseData[key]);
        }
      }
      try {
        const response = await axios.post('/api/register-course', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(response.data);
        this.courseId = response.data.course_id; // 存储生成的课程ID
        console.log("Course id =", this.courseId)
        this.$emit('courseCreated', this.courseId); // 触发 courseCreated 事件

      } catch (error) {
        console.error("There was an error creating the course", error);
      }
    },
    skipCourse() {
      this.courseData.skip = true;
      this.submitCourse();
    }
  }
};
</script>

<style scoped>
.upload-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  color: white;
  text-align: center;
}

.upload-title {
  margin-top: 40px;
  margin-bottom: 20px;
}

.upload-form {
  width: 100%;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 15px;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.file-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: none;
  box-sizing: border-box;
}

.button-group {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 20px;
}

.submit-button, .skip-button {
  width: 45%;
  padding: 10px;
  background: #2b61c4;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease, color 0.3s ease;
}

.submit-button:hover {
  background: #118a0d;
  color: #ffffff;
}

.skip-button:hover {
  background: #d25a2d;
  color: #ffffff;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.7s;


}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
