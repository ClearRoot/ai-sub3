import Vue from 'vue';
import Router from 'vue-router';
import Chatbot from './views/Chatbot.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Chatbot',
      component: Chatbot
    },
  ],
});