<template>
  <div class="upload-material">
    <h1 class="upload-title">上传相关资料</h1>
    <form @submit.prevent="submitForm" class="upload-form">
      <div class="form-group">
        <label for="material" class="form-label">课本: </label>
        <input type="file" class="form-control" id="course-materials" multiple @change="handleFileUpload('courseMaterials', $event)">
      </div>
      <div class="form-group">
        <label for="material" class="form-label">PPT: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('ppt', $event)">
      </div>
      <div class="form-group">
        <label for="material" class="form-label">课堂笔记/作业: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('notes', $event)">
      </div>
      <div class="form-group">
        <label for="material" class="form-label">测试题目/往年考试题目: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('tests', $event)">
      </div>
      <div class="form-group">
        <label for="material" class="form-label">模拟考试题目: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('mockTests', $event)">
      </div>
      <div class="form-group">
        <label>其他补充材料: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('others', $event)">
      </div>
      <button type="submit" class="btn btn-primary">提交</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UploadMaterial',
  props: {
    courseId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      files: {
        courseMaterials: null,
        ppt: null,
        notes: null,
        tests: null,
        mockTests: null,
        others: null
      }
    };
  },
  methods: {
      handleFileUpload(type, event) {
            this.files[type] = event.target.files[0];
      },
      async submitForm() {
          const formData = new FormData();
          formData.append('course_id', this.courseId);
          console.log("Course id =", this.courseId)
          for (let key in this.files) {
              if (this.files[key]) {
                  formData.append(key, this.files[key]);
              }
          }
          console.log("Submitting form with data:", formData);

          try {
              const response = await axios.post('http://localhost:8010/api/submit', formData); // Store the response
              console.log("Form submitted successfully:", response.data);
              alert(`Response: ${response.data.message}`);
              //this.$router.push('/waiting');
              this.$emit('materialUploaded'); // 触发 materialUploaded 事件
          } catch (error) {
              console.error('Error submitting form:', error);
              alert('Failed to submit. Check if there are missing files or wrong formats. Please try again.');
          }
      }
  }
};
</script>

<style scoped>
.upload-material {
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


button {
  margin-top: 20px;
  padding: 12px 30px;
  color: #471081;
  background: #fcfcfc;
  font-family: 'Arial', sans-serif; /* 设置字体系列 */
  font-size: 16px; /* 设置字体大小 */
  font-weight: bold; /* 设置字体粗细 */
}
</style>
