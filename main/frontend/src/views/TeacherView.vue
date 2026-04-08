<template>
  <div class="min-h-screen bg-[var(--color-bg-base)] flex flex-col font-body">
    <!-- Header -->
    <header class="bg-[var(--color-bg-raised)] border-b border-[var(--color-border-subtle)] px-4 md:px-8 py-4 flex justify-between items-center sticky top-0 z-40 shadow-sm">
      <div class="flex items-center space-x-3 md:space-x-4">
        <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="md:hidden p-2 text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-base)] rounded-lg transition-colors">
          <Menu class="w-6 h-6" />
        </button>
        <div class="bg-[var(--color-accent-orange)] p-2 md:p-2.5 rounded-xl md:rounded-2xl shadow-lg shadow-orange-100/50">
          <BookOpen class="w-6 h-6 md:w-7 md:h-7 text-white" />
        </div>
        <h1 class="text-xl md:text-2xl font-display text-[var(--color-text-primary)] tracking-tight">教师端</h1>
      </div>
      <div class="flex items-center space-x-3 md:space-x-6">
        <div class="hidden sm:flex items-center space-x-3 bg-[var(--color-bg-base)] px-4 py-2 rounded-xl border border-[var(--color-border-subtle)]">
          <User class="w-4 h-4 text-[var(--color-text-secondary)]" />
          <span class="text-sm font-heading font-bold text-[var(--color-text-primary)]">
            {{ userStore.user?.name || userStore.user?.username }}
          </span>
        </div>
        <button @click="logout" class="text-sm font-heading font-bold text-[var(--color-error)] hover:text-red-700 transition-colors flex items-center px-3 py-2 rounded-lg hover:bg-red-50/50">
          <LogOut class="w-4 h-4 md:mr-1.5" /> <span class="hidden md:inline">退出</span>
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden relative">
      <!-- Mobile Sidebar Overlay -->
      <div 
        v-if="isMobileMenuOpen" 
        @click="isMobileMenuOpen = false"
        class="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 md:hidden transition-opacity"
      ></div>

      <!-- Sidebar -->
      <aside 
        :class="['fixed inset-y-0 left-0 z-40 w-72 bg-[var(--color-bg-raised)] border-r border-[var(--color-border-subtle)] flex flex-col p-6 shadow-xl md:shadow-sm transition-transform duration-300 md:static md:translate-x-0', 
                isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full']"
      >
        <nav class="space-y-2">
          <button 
            @click="currentView = 'stats'; isMobileMenuOpen = false"
            :class="['w-full flex items-center px-5 py-4 rounded-xl transition-all duration-300 font-heading text-sm', 
                    currentView === 'stats' 
                      ? 'bg-orange-50 text-[var(--color-accent-orange)] font-bold shadow-sm border border-orange-100' 
                      : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-base)] hover:text-[var(--color-text-primary)]']"
          >
            <BarChart2 class="w-5 h-5 mr-3" />
            学情概览
          </button>
          <button 
            @click="currentView = 'assignments'; isMobileMenuOpen = false"
            :class="['w-full flex items-center px-5 py-4 rounded-xl transition-all duration-300 font-heading text-sm', 
                    currentView === 'assignments' 
                      ? 'bg-orange-50 text-[var(--color-accent-orange)] font-bold shadow-sm border border-orange-100' 
                      : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-base)] hover:text-[var(--color-text-primary)]']"
          >
            <ClipboardList class="w-5 h-5 mr-3" />
            作业管理
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-10 bg-[var(--color-bg-base)] relative">
        <div class="relative z-10 max-w-6xl mx-auto">
          <div v-if="currentView === 'stats'" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <StatsReport />
          </div>
          <div v-if="currentView === 'assignments'" class="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <AssignmentManage />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { BookOpen, BarChart2, ClipboardList, LogOut, User, Menu } from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';
import StatsReport from './StatsReport.vue';
import AssignmentManage from './AssignmentManage.vue';

const router = useRouter();
const userStore = useUserStore();
const currentView = ref('stats');
const isMobileMenuOpen = ref(false);

const logout = () => {
  userStore.logout();
  router.push('/login');
};
</script>
