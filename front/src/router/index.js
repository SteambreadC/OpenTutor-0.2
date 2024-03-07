import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '../components/HelloWorld.vue';
import TAtest1 from '../components/TAtest1.vue';
import Leftsidebar from "../components/leftsidebar.vue";

const routes = [
  {
    path: '/',
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
