import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '../components/oldFiles/HelloWorld.vue';
import TAtest1 from '../components/oldFiles/TAtest1.vue';
import Welcome from '../components/Welcome.vue';
import CreateCourse from '../components/CreateCourse.vue';
import UploadMaterial from '../components/UploadMaterial.vue';
import Waiting from '../components/Waiting.vue';
import Results from '../components/Results.vue';

const routes = [
  {
    path: '/',
    name: 'Welcome',
    components: {
      default: Welcome
    }
  },
      {
    path: '/create-course',
    name: 'CreateCourse',
    component: CreateCourse
  },
  {
    path: '/upload-material',
    name: 'UploadMaterial',
    component: UploadMaterial
  },
  {
    path: '/waiting',
    name: 'Waiting',
    component: Waiting
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  },
  {
    path: '/hello',
    name: 'HelloWorld',
    components: {
      default: HelloWorld
    }
  },
  {
    path: '/ta-test',
    name: 'TAtest1',
    msg: 'This is a test~',
    component: TAtest1
  }

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
