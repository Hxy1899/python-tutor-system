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
        <h1 class="text-xl md:text-2xl font-display text-[var(--color-text-primary)] tracking-tight">Python Tutor</h1>
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
    
    <main class="flex-1 flex overflow-hidden relative">
      <!-- Mobile Sidebar Overlay -->
      <div 
        v-if="isMobileMenuOpen" 
        @click="isMobileMenuOpen = false"
        class="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 md:hidden transition-opacity"
      ></div>

      <!-- Sidebar: Assignments -->
      <aside 
        :class="['fixed inset-y-0 left-0 z-40 w-80 bg-[var(--color-bg-raised)] border-r border-[var(--color-border-subtle)] flex flex-col p-6 shadow-xl md:shadow-sm overflow-y-auto transition-transform duration-300 md:static md:translate-x-0', 
                isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full']"
      >
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-lg font-display text-[var(--color-text-primary)] flex items-center tracking-tight">
            <ClipboardList class="w-5 h-5 mr-2 text-[var(--color-accent-orange)]" /> 作业列表
          </h2>
          <span class="bg-orange-50 text-[var(--color-accent-orange)] text-xs font-heading font-bold px-2.5 py-1 rounded-full border border-orange-100">
            {{ assignments.length }}
          </span>
        </div>
        
        <div class="space-y-4">
          <button 
            v-for="item in assignments" 
            :key="item.id"
            @click="selectAssignment(item); isMobileMenuOpen = false"
            :class="['w-full text-left p-5 rounded-2xl border-2 transition-all duration-300 group relative overflow-hidden', 
                    selectedAssignment?.id === item.id 
                      ? 'border-[var(--color-accent-orange)] bg-orange-50/30 shadow-md shadow-orange-100/20' 
                      : 'border-transparent bg-[var(--color-bg-base)] hover:bg-white hover:border-[var(--color-border-subtle)] hover:shadow-sm']"
          >
            <div class="flex flex-col relative z-10">
              <span :class="['font-heading font-bold text-base mb-1.5 transition-colors', selectedAssignment?.id === item.id ? 'text-[var(--color-text-primary)]' : 'text-[var(--color-text-primary)] group-hover:text-[var(--color-accent-orange)]']">
                {{ item.title }}
              </span>
              <p class="text-xs text-[var(--color-text-secondary)] font-body line-clamp-2 leading-relaxed">
                {{ item.description }}
              </p>
            </div>
            <div v-if="selectedAssignment?.id === item.id" class="absolute right-4 top-1/2 -translate-y-1/2">
              <ChevronRight class="w-5 h-5 text-[var(--color-accent-orange)]" />
            </div>
          </button>
        </div>
      </aside>

      <!-- Main: Editor + Diagnosis -->
      <div class="flex-1 flex flex-col relative bg-[var(--color-bg-base)]/50 overflow-y-auto md:overflow-hidden">
        <div class="flex-1 flex flex-col xl:flex-row overflow-hidden p-4 md:p-8 gap-6 md:gap-8">
          <!-- Editor Area -->
          <div class="flex-[3] min-h-[500px] flex flex-col bg-white rounded-3xl shadow-sm border border-[var(--color-border-subtle)] overflow-hidden group hover:shadow-md transition-shadow">
            <div class="px-6 py-4 border-b border-[var(--color-border-subtle)] flex flex-wrap justify-between items-center bg-[var(--color-bg-raised)] gap-4">
              <div class="flex items-center space-x-2">
                <Code2 class="w-4 h-4 text-[var(--color-text-secondary)]" />
                <span class="text-xs font-heading font-bold text-[var(--color-text-secondary)] uppercase tracking-widest">代码编辑器</span>
              </div>
              <div class="flex items-center space-x-3 ml-auto">
                <span v-if="isSubmitting" class="hidden sm:flex text-xs font-heading font-bold text-[var(--color-accent-orange)] animate-pulse items-center">
                  <RefreshCw class="w-3 h-3 mr-1 animate-spin" /> 正在诊断中...
                </span>
                <button 
                  @click="handleSubmit" 
                  :disabled="isSubmitting || !selectedAssignment"
                  class="btn-primary flex items-center px-6 py-2.5 text-sm"
                >
                  <Send class="w-4 h-4 mr-2" /> 提交诊断
                </button>
              </div>
            </div>
            <div class="flex-1 overflow-hidden relative">
              <CodeEditor 
                v-model="code" 
                :is-submitting="isSubmitting" 
                :errors="staticIssues" 
                class="h-full"
              />
            </div>
          </div>
          
          <!-- Diagnosis Panel Area -->
          <div class="flex-[2] min-h-[300px] flex flex-col bg-white rounded-3xl shadow-sm border border-[var(--color-border-subtle)] overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-6 py-4 border-b border-[var(--color-border-subtle)] flex items-center space-x-2 bg-[var(--color-bg-raised)]">
              <Sparkles class="w-4 h-4 text-[var(--color-accent-orange)]" />
              <span class="text-xs font-heading font-bold text-[var(--color-text-secondary)] uppercase tracking-widest">智能诊断结果</span>
            </div>
            <div class="flex-1 overflow-y-auto p-6">
              <div v-if="!hasDiagnosed" class="h-full flex flex-col items-center justify-center text-center p-8">
                <div class="bg-orange-50 p-6 rounded-full mb-6">
                  <Cpu class="w-12 h-12 text-[var(--color-accent-orange)] opacity-40" />
                </div>
                <h3 class="text-lg font-display text-[var(--color-text-primary)] mb-2">准备就绪</h3>
                <p class="text-sm text-[var(--color-text-secondary)] font-body leading-relaxed max-w-[200px]">
                  在上方编写代码后点击提交，AI 助手将为你提供引导式纠错建议。
                </p>
              </div>
              <HintPanel 
                v-else
                :error-type="diagnosisResult.error_type" 
                :hint="diagnosisResult.hint" 
                :is-correct="diagnosisResult.is_correct" 
                :dynamic-error="diagnosisResult.dynamic_error" 
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  BookOpen, LogOut, User, ClipboardList, 
  ChevronRight, Code2, Send, Sparkles, Cpu, RefreshCw, Menu
} from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';
import { getAssignments } from '../api/assignment';
import { submitCode } from '../api/code';
import CodeEditor from '../components/CodeEditor.vue';
import HintPanel from '../components/HintPanel.vue';

const router = useRouter();
const userStore = useUserStore();
const assignments = ref([]);
const isMobileMenuOpen = ref(false);
const selectedAssignment = ref(null);
const code = ref('# 在此输入你的 Python 代码\n\ndef main():\n    print("Hello, Python!")\n\nif __name__ == "__main__":\n    main()');
const isSubmitting = ref(false);
const hasDiagnosed = ref(false);
const staticIssues = ref([]);
const diagnosisResult = reactive({
  error_type: "",
  hint: "",
  is_correct: false,
  dynamic_error: ""
});

const logout = () => {
  userStore.logout();
  router.push('/login');
};

const selectAssignment = (assignment) => {
  selectedAssignment.value = assignment;
  // If assignment has a template, we could load it here
};

const handleSubmit = async () => {
  if (isSubmitting.value || !selectedAssignment.value) return;
  
  isSubmitting.value = true;
  hasDiagnosed.value = true;
  try {
    const data = await submitCode({
      user_id: userStore.user?.id || 1,
      assignment_id: selectedAssignment.value.id,
      code: code.value,
      test_code: selectedAssignment.value.test_code || ""
    });
    
    diagnosisResult.error_type = data.error_type;
    diagnosisResult.hint = data.hint;
    diagnosisResult.is_correct = data.is_correct;
    diagnosisResult.dynamic_error = data.dynamic_error;
    staticIssues.value = data.static_issues || [];
    
  } catch (error) {
    console.error("Submission error:", error);
    diagnosisResult.error_type = "ConnectionError";
    diagnosisResult.hint = "无法连接到后端诊断服务器，请稍后重试。";
    diagnosisResult.is_correct = false;
  } finally {
    isSubmitting.value = false;
  }
};

const fetchAssignments = async () => {
  try {
    assignments.value = await getAssignments();
    if (assignments.value.length > 0) {
      selectedAssignment.value = assignments.value[0];
    }
  } catch (error) {
    console.error("Failed to fetch assignments:", error);
  }
};

onMounted(fetchAssignments);
</script>

<style scoped>
/* Any additional custom styles if tailwind doesn't cover it */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>
