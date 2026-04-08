<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b px-6 py-4 flex justify-between items-center shadow-sm">
      <div class="flex items-center space-x-3">
        <div class="bg-indigo-600 p-2 rounded-lg">
          <BookOpen class="w-6 h-6 text-white" />
        </div>
        <h1 class="text-xl font-bold text-gray-900">Python Tutor - 教师端</h1>
      </div>
      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-600 font-medium">欢迎, {{ userStore.user?.name || userStore.user?.username }}</span>
        <button @click="logout" class="text-sm text-red-600 hover:text-red-700 flex items-center font-medium">
          <LogOut class="w-4 h-4 mr-1" /> 退出
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-64 bg-white border-r flex flex-col p-4 shadow-sm">
        <nav class="space-y-1">
          <button 
            @click="currentView = 'stats'"
            :class="['w-full flex items-center px-4 py-3 rounded-xl transition-all duration-200', 
                    currentView === 'stats' ? 'bg-indigo-50 text-indigo-700 font-semibold' : 'text-gray-600 hover:bg-gray-100']"
          >
            <BarChart2 class="w-5 h-5 mr-3" />
            学情概览
          </button>
          <button 
            @click="currentView = 'assignments'"
            :class="['w-full flex items-center px-4 py-3 rounded-xl transition-all duration-200', 
                    currentView === 'assignments' ? 'bg-indigo-50 text-indigo-700 font-semibold' : 'text-gray-600 hover:bg-gray-100']"
          >
            <ClipboardList class="w-5 h-5 mr-3" />
            作业管理
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-8 bg-gray-50/50">
        <div v-if="currentView === 'stats'">
          <StatsReport />
        </div>
        <div v-if="currentView === 'assignments'">
          <AssignmentManage />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { BookOpen, BarChart2, ClipboardList, LogOut } from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';
import StatsReport from './StatsReport.vue';
import AssignmentManage from './AssignmentManage.vue';

const userStore = useUserStore();
const currentView = ref('stats');

const logout = () => {
  userStore.logout();
  window.location.reload();
};
</script>
