<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 flex items-center justify-center p-6">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md p-10 transform transition-all hover:scale-[1.01]">
      <div class="flex flex-col items-center mb-10 text-center">
        <div class="bg-indigo-600 p-4 rounded-2xl mb-4 shadow-lg shadow-indigo-200">
          <BookOpen class="w-10 h-10 text-white" />
        </div>
        <h2 class="text-3xl font-black text-gray-900 tracking-tight">Python Tutor</h2>
        <p class="text-gray-500 mt-2 font-medium italic">加入我们，一起探索 Python 的奥秘</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2 tracking-wide uppercase">用户名</label>
          <div class="relative">
            <User class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="form.username" 
              type="text" 
              required
              class="w-full pl-10 pr-4 py-3.5 border border-gray-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-medium"
              placeholder="请输入用户名"
            >
          </div>
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2 tracking-wide uppercase">真实姓名</label>
          <div class="relative">
            <UserCircle class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="form.name" 
              type="text" 
              required
              class="w-full pl-10 pr-4 py-3.5 border border-gray-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-medium"
              placeholder="请输入您的姓名"
            >
          </div>
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2 tracking-wide uppercase">密码</label>
          <div class="relative">
            <Lock class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="form.password" 
              type="password" 
              required
              class="w-full pl-10 pr-4 py-3.5 border border-gray-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-medium"
              placeholder="请输入密码"
            >
          </div>
        </div>
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2 tracking-wide uppercase">身份角色</label>
          <div class="flex space-x-4">
            <label class="flex-1 cursor-pointer">
              <input type="radio" v-model="form.role" value="student" class="hidden peer">
              <div class="p-4 border border-gray-200 rounded-xl text-center font-bold peer-checked:bg-indigo-50 peer-checked:border-indigo-600 peer-checked:text-indigo-600 transition-all">
                学生
              </div>
            </label>
            <label class="flex-1 cursor-pointer">
              <input type="radio" v-model="form.role" value="teacher" class="hidden peer">
              <div class="p-4 border border-gray-200 rounded-xl text-center font-bold peer-checked:bg-indigo-50 peer-checked:border-indigo-600 peer-checked:text-indigo-600 transition-all">
                教师
              </div>
            </label>
          </div>
        </div>
        
        <div v-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl text-sm font-bold border border-red-100">
          {{ error }}
        </div>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-indigo-600 text-white py-4 rounded-xl font-black text-lg shadow-xl shadow-indigo-200 hover:bg-indigo-700 disabled:opacity-50 transition-all active:scale-95"
        >
          {{ loading ? '注册中...' : '立即注册' }}
        </button>
      </form>
      
      <div class="mt-8 text-center">
        <p class="text-sm text-gray-500 font-medium">已有账号? <router-link to="/login" class="text-indigo-600 font-bold hover:underline">去登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { BookOpen, User, UserCircle, Lock } from 'lucide-vue-next';
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
