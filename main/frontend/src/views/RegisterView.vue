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
        <p class="text-[var(--color-text-secondary)] font-body italic">加入我们，一起探索 Python 的奥秘</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">用户名</label>
          <div class="relative group">
            <User class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-secondary)] transition-colors group-focus-within:text-[var(--color-accent-orange)]" />
            <input 
              v-model="form.username" 
              type="text" 
              required
              class="w-full pl-10 pr-4 py-3.5 bg-white border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="请输入用户名"
            >
          </div>
        </div>
        <div>
          <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">真实姓名</label>
          <div class="relative group">
            <UserCircle class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-secondary)] transition-colors group-focus-within:text-[var(--color-accent-orange)]" />
            <input 
              v-model="form.name" 
              type="text" 
              required
              class="w-full pl-10 pr-4 py-3.5 bg-white border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="请输入您的姓名"
            >
          </div>
        </div>
        <div>
          <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">密码</label>
          <div class="relative group">
            <Lock class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-secondary)] transition-colors group-focus-within:text-[var(--color-accent-orange)]" />
            <input 
              v-model="form.password" 
              type="password" 
              required
              class="w-full pl-10 pr-4 py-3.5 bg-white border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="请输入密码"
            >
          </div>
        </div>
        <div>
          <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">身份角色</label>
          <div class="flex space-x-4">
            <label class="flex-1 cursor-pointer">
              <input type="radio" v-model="form.role" value="student" class="hidden peer">
              <div class="p-4 border border-[var(--color-border-subtle)] rounded-xl text-center font-heading font-bold peer-checked:bg-orange-50 peer-checked:border-[var(--color-accent-orange)] peer-checked:text-[var(--color-accent-orange)] transition-all bg-white">
                学生
              </div>
            </label>
            <label class="flex-1 cursor-pointer">
              <input type="radio" v-model="form.role" value="teacher" class="hidden peer">
              <div class="p-4 border border-[var(--color-border-subtle)] rounded-xl text-center font-heading font-bold peer-checked:bg-orange-50 peer-checked:border-[var(--color-accent-orange)] peer-checked:text-[var(--color-accent-orange)] transition-all bg-white">
                教师
              </div>
            </label>
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
          {{ loading ? '注册中...' : '立即注册' }}
        </button>
      </form>
      
      <div class="mt-8 text-center">
        <p class="text-sm text-[var(--color-text-secondary)] font-body">
          已有账号? <router-link to="/login" class="text-[var(--color-accent-orange)] font-heading font-bold hover:underline">去登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { BookOpen, User, UserCircle, Lock, AlertCircle } from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';

const router = useRouter();
const userStore = useUserStore();

const form = ref({
  username: '',
  name: '',
  password: '',
  role: 'student'
});
const error = ref('');
const loading = ref(false);

const handleRegister = async () => {
  loading.value = true;
  error.value = '';
  try {
    await userStore.register(form.value);
    router.push('/login');
  } catch (err) {
    error.value = err.response?.data?.detail || '注册失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};
</script>
