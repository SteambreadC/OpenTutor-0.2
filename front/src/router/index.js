import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '../components/oldFiles/HelloWorld.vue';
import TAtest1 from '../components/oldFiles/TAtest1.vue';
import Welcome from '../components/Welcome.vue';
import CreateCourse from '../components/CreateCourse.vue';
import UploadMaterial from '../components/UploadMaterial.vue';
import Waiting from '../components/Waiting.vue';
import Results from '../components/Results.vue';
import Handle from "../components/Handle.vue";

const routes = [
  {
    path: '/',
    name: 'Welcome',
    components: {
      default: Welcome
    }
  },
  {
    path: '/handle',
    name: 'Handle',
    component: Handle
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
    path: '/results/:courseId',
    name: 'Results',
    component: Results
  },
  {
    path: '/hello',
    name: 'HelloWorld',
    components: {
      default: HelloWorld
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
