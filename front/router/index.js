import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import ProjectManagement from '@/components/ProjectManagement.vue'
import Layout_Top from '@/components/Layout_Top.vue'
import CreateProject from '@/components/CreateProject.vue'
import DocumentManagement from '@/components/DocumentManagement.vue'
import CreateDocument from '@/components/CreateDocument.vue'
// import CreateDocument from '@/components/CreateDocument.vue' // 如果有创建文档页面

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
          name: 'ProjectManagement',
          component: ProjectManagement,
        },
        {
          path: '/create-project',
          name: 'CreateProject',
          component: CreateProject,
        },
        {
          path: '/documents/:projectId',
          name: 'DocumentManagement',
          component: DocumentManagement,
          props: true,
        },
        {
          path: '/create-document',
          name: 'CreateDocument',
          component: CreateDocument,
        },
      ],
    },
  ],
})

export default router
