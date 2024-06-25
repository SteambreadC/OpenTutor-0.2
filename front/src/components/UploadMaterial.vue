<template>
  <div class="upload-material">
    <img alt="logo of Redpanda" src="../assets/winterRedpanda.jpg" class="logo" />
    <h1 class="upload-title">{{ msg = '上传相关资料' }}</h1>
    <form @submit.prevent="submitForm" class="upload-form">
      <div v-for="(field, index) in fields" :key="index" class="form-group">
        <label :for="field.id" class="form-group-label">{{ field.label }}:</label>
        <div>
          <!--<label :for="field.id" class="file-input-label">选择文件</label> -->
          <input type="file" :id="field.id" class="form-control" multiple @change="handleFileUpload(field.key, $event)">
        </div>
        <ul class="file-list" v-if="files[field.key].length > 0">
          <li v-for="(file, fileIndex) in files[field.key]" :key="fileIndex" class="file-item">
            <span class="file-name">{{ file.name }}</span>
            <button type="button" class="delete-btn" @click="removeFile(field.key, fileIndex)">×</button>
          </li>
        </ul>
      </div>
      <button type="submit" class="submit-button">提交</button>
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
      fields: [
        { label: '授课资料', key: 'textbook', id: 'textbook' },
        //{ label: 'PPT', key: 'ppt', id: 'ppt' },
        //{ label: '课堂笔记/作业', key: 'notes', id: 'notes' },
        { label: '作业题目/测试题目', key: 'homework', id: 'homework' },
        { label: '模拟考试/历年考试题目', key: 'mockTests', id: 'mock-tests' },
        { label: '其他补充材料', key: 'others', id: 'others' }
      ],
      files: {
        textbook: [],
        homework: [],
        mockTests: [],
        others: []
      }
    };
  },
  methods: {
    handleFileUpload(key, event) {
      this.files[key] = [...this.files[key], ...Array.from(event.target.files)];
    },
    removeFile(key, index) {
      this.files[key].splice(index, 1);
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('course_id', this.courseId);
      console.log("Course id =", this.courseId);

      for (let key in this.files) {
        for (let file of this.files[key]) {
          formData.append(key, file);
        }
      }

      console.log("Submitting form with data:", formData);

      try {
        const response = await axios.post('/api/submit', formData);
        console.log("Form submitted successfully:", response.data);
        //alert(`Response: ${response.data.message}`);
        this.$emit('materialUploaded');
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
  max-width: 700px;
  background: rgba(255, 255, 255, 0.1);
  padding: 50px;
  border-radius: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.file-input-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

.form-group label {
  margin: 5px 5px 15px;
  display: flex;
  align-items: flex-start;
  font-weight: bold;
}

.file-input-wrapper {
  position: relative;
  display: inline-block;
}

.file-input-label {
  display: inline-block;
  padding: 8px 12px;
  background-color: #1b95be;
  color: #ffffff;
  cursor: pointer;
  border-radius: 20px;
  margin: 8px;
  font-family: 'Arial', sans-serif; /* 自定义字体 */
  font-size: 16px; /* 自定义字体大小 */
  transition: background-color 0.3s ease;
}

.file-input-label:hover {
  background-color: #2980b9; /* 悬停效果 */
}

.file-input {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  width: 80%;
  height: 80%;
  cursor: pointer;
}

.file-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px; /* 添加间距 */
  list-style-type: none;
  padding: 0;
  margin: 10px 0 0;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(22, 229, 119, 0.54);
  padding: 10px;
  border-radius: 55px;
  margin-bottom: 5px;
  margin-left: 5px;
  font-size:12px;
  max-width: 170px;
  max-height: 50px;
}

.file-name {
  flex-grow: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 10px;
}

.delete-btn {
  display: flex;
  background-color: transparent;
  border: none;
  align-items: center;
  color: #ff6a6a;
  font-size: 18px;
  cursor: pointer;
  transition: color 0.3s;
}

.delete-btn:hover {
  color: #ff0000;
}

button {
  color: #471081;
  background: #fcfcfc;
  font-family: 'Arial', sans-serif; /* 设置字体系列 */
  font-size: 16px; /* 设置字体大小 */
  font-weight: bold; /* 设置字体粗细 */
}

.submit-button{
  margin-top:20px;
  width: 20%;
  padding: 10px;
  background: #3f76d5;
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

</style>
