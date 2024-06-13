<template>
  <div class="upload-material">
    <h1 class="mb-4">{{ msg = '上传相关资料' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="material" class="form-label">课本: </label>
        <input type="file" class="form-control" id="material" name="material" @change="handleFileUpload('textbook', $event)" />
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
