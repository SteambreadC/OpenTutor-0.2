<template>
  <div class="upload-material">
    <h1 class="mb-4">{{ msg = '上传相关资料' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="material" class="form-label">课本: </label>
        <input type="file" class="form-control" id="course-materials" multiple @change="handleFileUp($event, 'courseMaterials')">
      </div>
      <div class="mb-3">
        <label for="material" class="form-label">PPT: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('ppt', $event)" />
      </div>
      <div>
        <label for="material" class="form-label">课堂笔记/作业: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('notes', $event)" />
      </div>
      <div>
        <label for="material" class="form-label">测试题目/往年考试题目: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('tests', $event)" />
      </div>
      <div>
        <label for="material" class="form-label">模拟考试题目: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('mockTests', $event)" />
      </div>
      <div for="material" class="form-label">
        <label>其他补充材料: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('others', $event)" />
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
        textbook: null,
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
              this.$router.push('/waiting');
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
form > div {
  margin-bottom: 20px;
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
