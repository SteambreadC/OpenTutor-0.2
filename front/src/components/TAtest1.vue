<template>
  <div class="container mt-5">
    <h1 class="mb-4">{{ msg = 'Input' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="material" class="form-label">Material (PDF):</label>
        <input type="file" class="form-control" id="material" name="material" accept="application/pdf" @change="handleFileUpload">
      </div>
      <div class="mb-3">
        <label for="text" class="form-label">Your Text:</label>
        <textarea class="form-control" id="text" name="text" rows="3" v-model="userText"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'TAtest1',
  props: {
    msg: String,
  },
  data() {
    return {
      materialFile: null,
      userText: '',
    };
  },
  methods: {
    handleFileUpload(event) {
      this.materialFile = event.target.files[0];
    },
    async submitForm() {
      if (!this.materialFile || !this.userText) {
        alert('Please fill in all fields.');
        return;
      }

      const formData = new FormData();
      formData.append('material', this.materialFile);
      formData.append('text', this.userText);

      try {
        /*
        const response = await axios.post('http://localhost:8010/api/submit', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        */
        const response = await axios.post('http://localhost:8010/api/submit', formData)
        alert(`Response: ${response.data.message}`);
        // Handle PDF file download if response contains a file
      } catch (error) {
        console.error('Error submitting form:', error);
        alert('Failed to submit. Please try again.');
      }
    },
  },
};
</script>

<style scoped>

/* 限制输入框和文件选择框长度 */
input[type="file"],
textarea {
  max-width: 700px; /* 或其他适当的长度 */
  margin: 0 auto;
  display: block;
}

h1{
    font-weight: 600;
}
.form-label {
  font-family: 'Montserrat', sans-serif;
  font-optical-sizing: auto;
  font-weight: 600; /* 例如，使用正常字重 */
  color: wheat; /* 对于特定元素使用不同的字体颜色 */
  font-size: 120%;
  font-style: normal;
}
.btn-primary{
    margin-bottom: 50px;
}
</style>
