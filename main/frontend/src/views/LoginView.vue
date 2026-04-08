<template>
  <div class="min-h-screen bg-[var(--color-bg-base)] flex items-center justify-center p-6 relative overflow-hidden font-body">
    <!-- Decorative background elements -->
    <div class="absolute top-0 left-0 w-full h-full opacity-5 pointer-events-none">
      <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-[var(--color-accent-orange)] blur-3xl"></div>
      <div class="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-indigo-500 blur-3xl"></div>
    </div>

    <div class="anthropic-card w-full max-w-md p-10 relative z-10">
      <div class="flex flex-col items-center mb-10 text-center">
        <div class="bg-[var(--color-accent-orange)] p-4 rounded-2xl mb-4 shadow-lg shadow-orange-100/50">
          <BookOpen class="w-10 h-10 text-white" />
        </div>
        <h2 class="text-3xl font-display text-[var(--color-text-primary)] tracking-tight mb-2">Python Tutor</h2>
        <p class="text-[var(--color-text-secondary)] font-body italic">开启你的智慧编程之旅</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">用户名</label>
          <div class="relative group">
            <User class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-secondary)] transition-colors group-focus-within:text-[var(--color-accent-orange)]" />
            <input 
              v-model="username" 
              type="text" 
              required
              class="w-full pl-10 pr-4 py-3.5 bg-white border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="请输入用户名"
            >
          </div>
        </div>
        <div>
          <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">密码</label>
          <div class="relative group">
            <Lock class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-secondary)] transition-colors group-focus-within:text-[var(--color-accent-orange)]" />
            <input 
              v-model="password" 
              type="password" 
              required
              class="w-full pl-10 pr-4 py-3.5 bg-white border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="请输入密码"
            >
          </div>
        </div>
        
        <div v-if="error" class="bg-red-50 text-[var(--color-error)] p-4 rounded-xl text-sm font-body border border-red-100 animate-shake flex items-center">
          <AlertCircle class="w-4 h-4 mr-2 shrink-0" />
          {{ error }}
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="btn-primary w-full py-4 rounded-xl font-heading font-bold text-lg shadow-xl shadow-orange-100 hover:shadow-orange-200/50 disabled:opacity-50 transition-all active:scale-95"
        >
          {{ loading ? '登录中...' : '进入系统' }}
        </button>
      </form>
      
      <div class="mt-8 text-center">
        <p class="text-sm text-[var(--color-text-secondary)] font-body">
          还没有账号? <router-link to="/register" class="text-[var(--color-accent-orange)] font-heading font-bold hover:underline">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { BookOpen, User, Lock, AlertCircle } from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    const user = await userStore.login({
      username: username.value,
      password: password.value
    });
    
    if (user.role === 'teacher') {
      router.push('/teacher');
    } else {
      router.push('/');
    }
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.animate-shake {
  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
</style>
