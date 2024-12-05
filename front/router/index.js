import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import ProjectManagement from '@/components/ProjectManagement.vue'
import Layout_Top from '@/components/Layout_Top.vue'
import CreateProject from '@/components/CreateProject.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout_Top,
      children: [
        {
          path: '/page',
          name: 'page',
          component: MainPage,
        },
        {
          path: '/project-management',
          name: 'projectManagement',
          component: ProjectManagement,
        },
        {
          path: '/create-project',
          name: 'createProject',
          component: CreateProject,
        },
      ],
    },
  ],
})

export default router
