import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import ProjectManagement from '@/components/ProjectManagement.vue'
import Layout_Top from '@/components/Layout_Top.vue'
import CreateProject from '@/components/CreateProject.vue'
import DocumentManagement from '@/components/DocumentManagement.vue'
import CreateDocument from '@/components/CreateDocument.vue'
<<<<<<< HEAD
import Annotation from '@/components/Annotation.vue'
=======
>>>>>>> dev
import LoginForm from '@/components/LoginForm.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import FileImport from '@/components/FileImport.vue'
import MapView from '@/components/MapView.vue'
import EntityTagging from '@/components/EntityTagging.vue'
import RelationshipAnnotation from '@/components/RelationshipAnnotation.vue'
import RelationGraph from '@/components/RelationGraph.vue'
<<<<<<< HEAD
import Menu2 from '@/components/Menu2.vue'
=======
import HeaderNav from '@/components/HeaderNav.vue'
import StructureTagging from '@/components/StructureTagging.vue'
>>>>>>> dev
// import CreateDocument from '@/components/CreateDocument.vue' // 如果有创建文档页面
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: LoginForm,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterForm,
    },
    {
      path: '/layout',
      component: Layout_Top,
      children: [
        {
          path: '/page',
          name: 'page',
          component: MainPage,
          meta: { requiresAuth: true },
        },
        {
          path: '/project-management',
          name: 'ProjectManagement',
          component: ProjectManagement,
          meta: { requiresAuth: true },
        },
        {
          path: '/create-project',
          name: 'CreateProject',
          component: CreateProject,
          meta: { requiresAuth: true },
        },
        {
          path: '/documents/:projectId',
          name: 'DocumentManagement',
          component: DocumentManagement,
          props: true,
          meta: { requiresAuth: true },
        },
        {
          path: '/create-document',
          name: 'CreateDocument',
          component: CreateDocument,
          meta: { requiresAuth: true },
        },
        {
          path: '/:pathMatch(.*)*',
          redirect: '/login',
        },
      ],
    },
    {
<<<<<<< HEAD
      path: '/annotation',
      name: 'Annotation',
      component: Annotation,
    },
    {
=======
>>>>>>> dev
      path: '/import',
      name: 'Import',
      component: FileImport,
    },
    {
      path: '/relationshipannotation',
      name: 'RelationshipAnnotation',
      component: RelationshipAnnotation,
    },
    {
      path: '/relationgraph',
      name: 'RelationGraph',
      component: RelationGraph,
    },
    {
<<<<<<< HEAD
      path: '/menu2',
      component: Menu2,
=======
      path: '/headernav',
      component: HeaderNav,
>>>>>>> dev
      children: [
        {
          path: '/map',
          name: 'Map',
          component: MapView,
        },
<<<<<<< HEAD
      ],
    },
    {
      path: '/entitytagging',
      name: 'EntityTagging',
      component: EntityTagging,
    },
    {
      path: '/relationshipannotation',
      name: 'RelationshipAnnotation',
      component: RelationshipAnnotation,
    },
=======
        {
          path: '/entitytagging',
          name: 'EntityTagging',
          component: EntityTagging,
        },
        {
          path: '/relationshipannotation',
          name: 'RelationshipAnnotation',
          component: RelationshipAnnotation,
        },
        {
          path: '/struct',
          name: 'StructureTagging',
          component: StructureTagging,
        },
      ],
    },
>>>>>>> dev
  ],
})
export default router
