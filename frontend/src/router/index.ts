import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    // }
    
    {
      path: '/train-list',
      name: 'train-list',
      component: () => import('../views/TrainList.vue'),
      props: true,
    }, 
    {
      path: '/settings',
      name: 'settings',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Settings.vue'),
    },
  ],
})

export default router
