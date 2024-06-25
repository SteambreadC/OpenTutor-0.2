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

/*
const initializeApp = () => {
  app.use(router);
  app.use(VueAxios, axios);
  app.mount('#app');
};

initializeApp()
*/


// 初始化 Vue 应用
const initializeApp = (token) => {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  app.use(router);
  app.use(VueAxios, axios);
  app.mount('#app');
};

// 获取新的 Token
const getNewToken = () => {
  return axios.get('http://localhost:8010/generate-token').then(response => {
    const newToken = response.data.access_token;
    localStorage.setItem('token', newToken);
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    return newToken;
  }).catch(error => {
    console.error('Error generating token:', error);
    alert('Failed to generate token. Please try again later.');
  });
};

if (!token) {
  getNewToken().then(newToken => {
    if (newToken) {
      initializeApp(newToken);
      axios.get('http://localhost:8010/jwt-test');
    }
  });
} else {
  initializeApp(token);
}

// Axios响应拦截器，用于处理401错误
axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await getNewToken();
      if (newToken) {
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return axios(originalRequest);
      }
    }
    return Promise.reject(error);
  }
);
