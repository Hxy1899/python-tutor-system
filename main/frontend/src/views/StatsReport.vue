<template>
  <div class="space-y-8 max-w-7xl mx-auto font-body">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-3xl font-display text-[var(--color-text-primary)] tracking-tight">学情统计报表</h2>
      <button @click="fetchStats" class="flex items-center text-sm font-heading font-bold text-[var(--color-accent-orange)] hover:text-orange-700 transition-colors">
        <RefreshCw class="w-4 h-4 mr-2" /> 刷新数据
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div v-for="card in statCards" :key="card.label" class="anthropic-card group hover:shadow-xl transition-all duration-300">
        <div class="flex items-center justify-between mb-6">
          <div :class="`p-3 rounded-2xl border border-transparent group-hover:border-white transition-all duration-300 ${card.bg}`">
            <component :is="card.icon" :class="`w-6 h-6 ${card.color}`" />
          </div>
          <span class="text-xs font-heading font-bold px-2.5 py-1 rounded-full bg-[var(--color-bg-base)] text-[var(--color-text-secondary)] uppercase tracking-widest">总计</span>
        </div>
        <p class="text-sm font-heading font-bold text-[var(--color-text-secondary)] mb-2 uppercase tracking-tighter">{{ card.label }}</p>
        <h3 class="text-4xl font-display text-[var(--color-text-primary)] tracking-tight">{{ card.value }}</h3>
      </div>
    </div>

    <!-- Error Distribution -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 mt-10">
      <div class="anthropic-card p-10">
        <div class="flex items-center justify-between mb-8">
          <h3 class="text-xl font-display text-[var(--color-text-primary)]">错误类型分布</h3>
          <div class="p-2 bg-orange-50 rounded-lg">
            <PieChart class="w-5 h-5 text-[var(--color-accent-orange)]" />
          </div>
        </div>
        <div class="space-y-6">
          <div v-for="error in stats?.error_distribution" :key="error.error_type" class="space-y-3">
            <div class="flex justify-between text-sm font-heading font-bold text-[var(--color-text-primary)]">
              <span class="flex items-center">
                <div class="w-2.5 h-2.5 rounded-full mr-3 shadow-sm" :style="{ backgroundColor: getErrorColor(error.error_type) }"></div>
                {{ error.error_type }}
              </span>
              <span class="text-[var(--color-text-secondary)]">{{ error.count }} <span class="text-xs ml-1 opacity-60">({{ getPercentage(error.count) }}%)</span></span>
            </div>
            <div class="w-full bg-[var(--color-bg-base)] rounded-full h-3 overflow-hidden border border-[var(--color-border-subtle)]/50">
              <div 
                class="h-full rounded-full transition-all duration-1000 ease-out" 
                :style="{ width: getPercentage(error.count) + '%', backgroundColor: getErrorColor(error.error_type) }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div class="anthropic-card p-10 flex flex-col">
        <div class="flex items-center justify-between mb-8">
          <h3 class="text-xl font-display text-[var(--color-text-primary)]">系统状态摘要</h3>
          <div class="p-2 bg-orange-50 rounded-lg">
            <Info class="w-5 h-5 text-[var(--color-accent-orange)]" />
          </div>
        </div>
        <div class="space-y-8 flex-1 flex flex-col justify-center">
          <div class="flex items-start p-6 rounded-2xl bg-orange-50/30 border border-orange-100/50 group hover:bg-orange-50/50 transition-colors">
            <div class="p-3 bg-white rounded-xl mr-5 shadow-sm">
              <CheckCircle class="w-6 h-6 text-[var(--color-success)]" />
            </div>
            <div>
              <p class="text-xs font-heading font-bold text-[var(--color-text-secondary)] uppercase tracking-widest mb-1">平均正确率</p>
              <p class="text-4xl font-display text-[var(--color-success)] tracking-tighter">{{ (stats?.average_correct_rate * 100).toFixed(1) }}%</p>
              <p class="text-xs text-[var(--color-text-secondary)] mt-2 font-body italic opacity-70">所有提交的综合通过率</p>
            </div>
          </div>
          <div class="flex items-start p-6 rounded-2xl bg-[var(--color-bg-base)]/50 border border-[var(--color-border-subtle)] group hover:bg-[var(--color-bg-base)] transition-colors">
            <div class="p-3 bg-white rounded-xl mr-5 shadow-sm">
              <AlertTriangle class="w-6 h-6 text-[var(--color-accent-orange)]" />
            </div>
            <div>
              <p class="text-xs font-heading font-bold text-[var(--color-text-secondary)] uppercase tracking-widest mb-1">最高频错误</p>
              <p class="text-3xl font-display text-[var(--color-text-primary)] tracking-tighter">{{ mostFrequentError?.error_type || 'N/A' }}</p>
              <p class="text-xs text-[var(--color-text-secondary)] mt-2 font-body italic opacity-70">出现次数: {{ mostFrequentError?.count || 0 }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Users, BookOpen, Send, CheckCircle, RefreshCw, PieChart, Info, AlertTriangle } from 'lucide-vue-next';
import { getOverallStats } from '../api/stats';

const stats = ref(null);
const loading = ref(false);

const statCards = computed(() => [
  { label: '注册学生', value: stats.value?.total_students || 0, icon: Users, bg: 'bg-blue-100', color: 'text-blue-600' },
  { label: '作业总数', value: stats.value?.total_assignments || 0, icon: BookOpen, bg: 'bg-indigo-100', color: 'text-indigo-600' },
  { label: '提交次数', value: stats.value?.total_submissions || 0, icon: Send, bg: 'bg-emerald-100', color: 'text-emerald-600' },
  { label: '通过次数', value: Math.round((stats.value?.total_submissions || 0) * (stats.value?.average_correct_rate || 0)), icon: CheckCircle, bg: 'bg-green-100', color: 'text-green-600' },
]);

const mostFrequentError = computed(() => {
  if (!stats.value?.error_distribution?.length) return null;
  return [...stats.value.error_distribution].sort((a, b) => b.count - a.count)[0];
});

const getPercentage = (count) => {
  if (!stats.value?.total_submissions) return 0;
  return ((count / stats.value.total_submissions) * 100).toFixed(1);
};

const getErrorColor = (type) => {
  const colors = {
    'SyntaxError': '#ef4444',
    'IndentationError': '#f97316',
    'NameError': '#f59e0b',
    'TypeError': '#8b5cf6',
    'ZeroDivisionError': '#ec4899',
    'LogicalError': '#3b82f6',
    'Correct': '#10b981'
  };
  return colors[type] || '#94a3b8';
};

const fetchStats = async () => {
  loading.value = true;
  try {
    stats.value = await getOverallStats();
  } catch (error) {
    console.error('Failed to fetch stats:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchStats);
</script>
