import Vue from 'vue';
import Router from 'vue-router';
import qa from '../components/Question.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/question',
      name: 'qa',
      component: qa,
    },
  ],
});
