import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import axios from 'axios';
import VueAxios from 'vue-axios';
import router from './router';



const app = createApp(App);

axios.defaults.baseURL = 'http://localhost:8010'

const token = localStorage.getItem('token');

// 初始化 Vue 应用
const initializeApp = (token) => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  app.use(router);
  app.use(VueAxios, axios);
  app.mount('#app');
};


if (!token) {
  axios.get('http://localhost:8010/generate-token').then(response => {
    const newToken = response.data.token;
    localStorage.setItem('token', newToken);
    initializeApp(newToken);
    axios.get('http://localhost:8010/jwt-test');
  })
    .catch(error => {
    console.error('Error generating token:', error);
    alert('Failed to generate token. Please try again later.');
  });
} else {
  initializeApp(token);
}