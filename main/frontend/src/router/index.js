import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import StudentView from '../views/StudentView.vue';
import TeacherView from '../views/TeacherView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';

const routes = [
  {
    path: '/',
    name: 'StudentHome',
    component: StudentView,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/teacher',
    name: 'TeacherHome',
    component: TeacherView,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = userStore.isLoggedIn;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.role && userStore.user?.role !== to.meta.role) {
    // Role mismatch
    if (userStore.user?.role === 'teacher') {
      next('/teacher');
    } else {
      next('/');
    }
  } else {
    next();
  }
});

export default router;
