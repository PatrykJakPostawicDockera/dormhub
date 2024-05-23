import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: () => import('../views/Auth/LoginView.vue'),
      meta: {
        public: true,
        skipIfAuth: true,
      },
    },
    {
      path: '/register/:suiteId?',
      name: 'Register',
      component: () => import('../views/Auth/RegisterView.vue'),
      meta: {
        public: true,
        skipIfAuth: true,
      },
      props: true,
    },
    {
      path: '/app',
      name: 'Homepage',
      component: () => import('../views/AppView.vue'),
      meta: {
        public: false,
        skipIfAuth: false,
      },
      children: [
        {
          path: '',
          name: 'Homepage',
          component: () => import('../views/HomeView.vue'),
        },
        {
          path: 'posts',
          name: 'Posts',
          component: () => import('../views/PostsView.vue'),
        },
        {
          path: 'todos',
          name: 'Todos',
          component: () => import('../views/TodosView.vue'),
        },
        {
          path: 'guests',
          name: 'Guests',
          component: () => import('../views/GuestsView.vue'),
        },
        {
          path: 'settings',
          name: 'Settings',
          component: () => import('../views/SettingsView.vue'),
        },
        {
          path: 'settings/edit-profile',
          name: 'Edit Profile',
          component: () => import('../views/EditProfileView.vue'),
        },
      ],
    },
    {
      path: '/debug/users',
      name: 'Debug Create Users',
      component: () => import('../views/Debug/CreateUser.vue'),
    },
    {
      path: '/debug/dorms',
      name: 'Debug Dorm Control',
      component: () => import('../views/Debug/DormControl.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'Login' },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.access == 'admin' || (to.meta.skipIfAuth && authStore.isAuthenticated)) {
    return next({ path: '/app' });
  }
  if (!to.meta.public && !authStore.isAuthenticated && to.name !== 'login') {
    return next({ path: '/' });
  }

  document.title = (to.name as string) + ' | ' + 'DormHub';
  next();
});

export default router;
