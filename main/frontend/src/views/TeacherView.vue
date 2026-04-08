<template>
  <div class="min-h-screen bg-[var(--color-bg-base)] flex flex-col font-body">
    <!-- Header -->
    <header class="bg-[var(--color-bg-raised)] border-b border-[var(--color-border-subtle)] px-8 py-4 flex justify-between items-center sticky top-0 z-40 shadow-sm">
      <div class="flex items-center space-x-4">
        <div class="bg-[var(--color-accent-orange)] p-2.5 rounded-2xl shadow-lg shadow-orange-100/50">
          <BookOpen class="w-7 h-7 text-white" />
        </div>
        <h1 class="text-2xl font-display text-[var(--color-text-primary)] tracking-tight">Python Tutor - ๆๅธ็ซฏ</h1>
      </div>
      <div class="flex items-center space-x-6">
        <div class="flex items-center space-x-3 bg-[var(--color-bg-base)] px-4 py-2 rounded-xl border border-[var(--color-border-subtle)]">
          <User class="w-4 h-4 text-[var(--color-text-secondary)]" />
          <span class="text-sm font-heading font-bold text-[var(--color-text-primary)]">
            ๆฌข่ฟ, {{ userStore.user?.name || userStore.user?.username }}
          </span>
        </div>
        <button @click="logout" class="text-sm font-heading font-bold text-[var(--color-error)] hover:text-red-700 transition-colors flex items-center">
          <LogOut class="w-4 h-4 mr-1.5" /> ้ๅบ
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-72 bg-[var(--color-bg-raised)] border-r border-[var(--color-border-subtle)] flex flex-col p-6 shadow-sm">
        <nav class="space-y-2">
          <button 
            @click="currentView = 'stats'"
            :class="['w-full flex items-center px-5 py-4 rounded-xl transition-all duration-300 font-heading text-sm', 
                    currentView === 'stats' 
                      ? 'bg-orange-50 text-[var(--color-accent-orange)] font-bold shadow-sm border border-orange-100' 
                      : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-base)] hover:text-[var(--color-text-primary)]']"
          >
            <BarChart2 class="w-5 h-5 mr-3" />
            ๅญฆๆๆฆ่ง
          </button>
          <button 
            @click="currentView = 'assignments'"
            :class="['w-full flex items-center px-5 py-4 rounded-xl transition-all duration-300 font-heading text-sm', 
                    currentView === 'assignments' 
                      ? 'bg-orange-50 text-[var(--color-accent-orange)] font-bold shadow-sm border border-orange-100' 
                      : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-base)] hover:text-[var(--color-text-primary)]']"
          >
            <ClipboardList class="w-5 h-5 mr-3" />
            ไฝไธ็ฎก็
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-10 bg-[var(--color-bg-base)] relative">
        <!-- Background texture or subtle gradient -->
        <div class="absolute inset-0 opacity-[0.03] pointer-events-none">
          <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" stroke-width="1"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
          </svg>
        </div>

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
import { BookOpen, BarChart2, ClipboardList, LogOut } from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';
import StatsReport from './StatsReport.vue';
import AssignmentManage from './AssignmentManage.vue';

const router = useRouter();
const userStore = useUserStore();
const currentView = ref('stats');

const logout = () => {
  userStore.logout();
  router.push('/login');
};
</script>
