import { createRouter, createWebHistory } from 'vue-router'
import Menu from '../views/Menu.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'menu',
      component: Menu,
      props: true,
    }, 
    {
      path: '/train-list',
      name: 'train-list',
      component: () => import('../views/TrainList.vue'),
      props: true,
    }, 
    {
      path: '/train-list/:id',
      name: 'train',
      component: () => import('../views/Train.vue'),
      props: true,
    }, 
    {
      path: '/settings',
      name: 'settings',
      props: true,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Settings.vue'),
    },
  ],
})

export default router
