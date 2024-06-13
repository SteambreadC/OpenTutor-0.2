import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import axios from 'axios';
import VueAxios from 'vue-axios';
import router from './router';


/*import 'mdb-vue-ui-kit/css/mdb.min.css'*/

const app = createApp(App);

app.use(router);
app.use(VueAxios, axios);
app.mount('#app');
