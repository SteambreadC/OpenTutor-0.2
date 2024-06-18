<template>
  <div class="results">
    <img src="../assets/2renpandas.jpg" class="results-img">
    <h1>预测结果</h1>
    <p>这是预测的考试题目:</p>
    <!-- 文件下载列表 -->
    <div v-if="files.length > 0" class="download-page">
      <form class="download-form">
      <h2>下载文件</h2>
      <ul>
        <li v-for="file in files" :key="file.name">
          <a :href="file.url" class="download-link"
             @click.prevent="downloadFile(file.url, file.name)">{{ file.name }}</a>
        </li>
      </ul>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Results',
  data() {
    return {
      files: [],
    };
  },
  created() {
    const courseId = this.$route.params.courseId;
    const token = localStorage.getItem('token');

    // 获取处理后的文件数据
    axios.get(`http://localhost:8010/api/processed-files?course_id=${courseId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(response => {
        this.files = response.data.processed_files.map(file => ({
          name: file.split('\\').pop(),
          url: `http://localhost:8010/download/${file}`
        }));
      })
      .catch(error => {
        console.error('Error fetching processed files:', error);
      });
  },
  methods: {
    downloadFile(url, name) {
      const token = localStorage.getItem('token');

      axios.get(url, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      })
        .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', name);
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch(error => {
          console.error('Error downloading file:', error);
        });
    }
  }
};
</script>

<style scoped>

.download-link {
  display: inline-block;
  padding: 8px 16px;
  color: #fff;
  border-radius: 6px;
  font-weight: bold;
  transition: background-color 0.3s;
  margin: 9px;
  cursor: pointer;

}

.download-link:hover {
  background-color: rgba(201, 224, 200, 0.11);
}

.results-img {
  text-align: center;
  margin-top: 50px;
  margin-bottom: 50px;
  border-radius: 100px;
}

ul {
  list-style-type: none; /* 移除列表项的默认样式 */
  padding: 0;
  display: flex; /* 使用弹性盒子布局 */
  flex-wrap: wrap; /* 允许列表项换行 */
  justify-content: space-between; /* 列表项在一行内平均分布 */
}

li {
  flex-basis: 100%; /* 每个列表项占据一行的48%宽度 */
  margin-bottom: 10px; /* 列表项之间的垂直间距 */
}

a {
  text-decoration: none;
  color: #3498db;
}

a:hover {
  text-decoration: underline;
}

h1{
    margin: 20px;
}

p{
    margin: 15px;
    font-size: 17px;
}

.download-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  color: white;
  text-align: center;
}

.download-form {
  width: 700px;
  max-width: 100%;
  min-height: 400px;
  max-height: 100%;
  background: rgba(255, 255, 255, 0.1);
  padding: 50px;
  border-radius: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
