import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/register',
      name:'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path:'/login',
      name:'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path:'/',
      name:'project',
      component: () => import('../views/ProjectView.vue')
    },
    {
      path:'/milestones',
      name:'milestone',
      component: () => import('../views/MilestoneView.vue')
    },
    {
      path:'/mentorship',
      name:'mentorship',
      component: () => import('../views/MentorshipView.vue')
    },
    {
      path:'/chatUsers',
      name:'chatUsers',
      component: () => import('../views/ChatUsersView.vue')
    },
    {
      path:'/ta-chat',
      name:'chatInterface',
      component: () => import('../views/ChatInterfaceView.vue')
    }
  ]
})

export default router
