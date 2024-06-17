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
if (!token) {
  axios.get('/generate-token').then(response => {
    const newToken = response.data.token;
    localStorage.setItem('token', newToken);
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    app.use(router);
    app.use(VueAxios, axios);
    app.mount('#app');
  });
} else {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  app.use(router);
  app.use(VueAxios, axios);
  app.mount('#app');
}