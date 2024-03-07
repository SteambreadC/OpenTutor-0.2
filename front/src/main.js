import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

/*import 'mdb-vue-ui-kit/css/mdb.min.css'*/
import router from './router';

const app = createApp(App);

app.use(router);

app.mount('#app');
