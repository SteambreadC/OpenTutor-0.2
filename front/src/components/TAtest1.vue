<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="material">Material (PDF):</label>
        <input type="file" id="material" name="material" accept="application/pdf" @change="handleFileUpload">
      </div>
      <div>
        <label for="text">Your Text:</label>
        <textarea id="text" name="text" v-model="userText"></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HelloWorld',
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
form > div {
  margin-bottom: 20px;
}
</style>
