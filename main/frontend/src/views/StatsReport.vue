<template>
  <div class="space-y-6 max-w-7xl mx-auto">
    <div class="flex items-center justify-between mb-2">
      <h2 class="text-2xl font-bold text-gray-900">学情统计报表</h2>
      <button @click="fetchStats" class="flex items-center text-sm text-indigo-600 hover:text-indigo-700 font-medium">
        <RefreshCw class="w-4 h-4 mr-1" /> 刷新数据
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div v-for="card in statCards" :key="card.label" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <div :class="`p-3 rounded-xl ${card.bg}`">
            <component :is="card.icon" :class="`w-6 h-6 ${card.color}`" />
          </div>
          <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-gray-50 text-gray-500 uppercase tracking-wider">总计</span>
        </div>
        <p class="text-sm font-medium text-gray-500 mb-1">{{ card.label }}</p>
        <h3 class="text-3xl font-extrabold text-gray-900 tracking-tight">{{ card.value }}</h3>
      </div>
    </div>

    <!-- Error Distribution -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-gray-900">错误类型分布</h3>
          <PieChart class="w-5 h-5 text-gray-400" />
        </div>
        <div class="space-y-4">
          <div v-for="error in stats?.error_distribution" :key="error.error_type" class="space-y-2">
            <div class="flex justify-between text-sm font-semibold text-gray-700">
              <span class="flex items-center">
                <div class="w-2 h-2 rounded-full mr-2" :style="{ backgroundColor: getErrorColor(error.error_type) }"></div>
                {{ error.error_type }}
              </span>
              <span>{{ error.count }} ({{ getPercentage(error.count) }}%)</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
              <div 
                class="h-full rounded-full transition-all duration-1000" 
                :style="{ width: getPercentage(error.count) + '%', backgroundColor: getErrorColor(error.error_type) }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-gray-900">系统状态摘要</h3>
          <Info class="w-5 h-5 text-gray-400" />
        </div>
        <div class="space-y-6">
          <div class="flex items-start p-4 rounded-xl bg-green-50/50 border border-green-100">
            <div class="p-2 bg-green-100 rounded-lg mr-4">
              <CheckCircle class="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p class="text-sm font-bold text-green-900">平均正确率</p>
              <p class="text-2xl font-black text-green-600 mt-1">{{ (stats?.average_correct_rate * 100).toFixed(1) }}%</p>
              <p class="text-xs text-green-700/70 mt-1 font-medium">所有提交的综合通过率</p>
            </div>
          </div>
          <div class="flex items-start p-4 rounded-xl bg-amber-50/50 border border-amber-100">
            <div class="p-2 bg-amber-100 rounded-lg mr-4">
              <AlertTriangle class="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <p class="text-sm font-bold text-amber-900">最高频错误</p>
              <p class="text-2xl font-black text-amber-600 mt-1">{{ mostFrequentError?.error_type || 'N/A' }}</p>
              <p class="text-xs text-amber-700/70 mt-1 font-medium">出现次数: {{ mostFrequentError?.count || 0 }}</p>
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
