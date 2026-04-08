<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-8 py-4 flex justify-between items-center sticky top-0 z-40 shadow-sm">
      <div class="flex items-center space-x-4">
        <div class="bg-indigo-600 p-2.5 rounded-2xl shadow-lg shadow-indigo-100">
          <BookOpen class="w-7 h-7 text-white" />
        </div>
        <h1 class="text-2xl font-black text-gray-900 tracking-tight">Python Tutor</h1>
      </div>
      
      <div class="flex items-center space-x-6">
        <div class="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-xl border border-gray-200">
          <User class="w-4 h-4 text-gray-500" />
          <span class="text-sm font-bold text-gray-700">{{ userStore.user?.name || userStore.user?.username }}</span>
        </div>
        <button @click="logout" class="text-sm font-bold text-red-600 hover:text-red-700 transition-colors flex items-center">
          <LogOut class="w-4 h-4 mr-1.5" /> 退出
        </button>
      </div>
    </header>
    
    <main class="flex-1 flex overflow-hidden">
      <!-- Sidebar: Assignments -->
      <aside class="w-80 bg-white border-r border-gray-200 flex flex-col p-6 shadow-sm overflow-y-auto">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-lg font-black text-gray-900 flex items-center tracking-tight">
            <ClipboardList class="w-5 h-5 mr-2 text-indigo-600" /> 作业列表
          </h2>
          <span class="bg-indigo-100 text-indigo-700 text-xs font-black px-2.5 py-1 rounded-full">{{ assignments.length }}</span>
        </div>
        
        <div class="space-y-4">
          <button 
            v-for="item in assignments" 
            :key="item.id"
            @click="selectAssignment(item)"
            :class="['w-full text-left p-5 rounded-2xl border-2 transition-all duration-200 group relative overflow-hidden', 
                    selectedAssignment?.id === item.id 
                      ? 'border-indigo-600 bg-indigo-50/50 shadow-md shadow-indigo-50' 
                      : 'border-transparent bg-gray-50 hover:bg-white hover:border-gray-200 hover:shadow-sm']"
          >
            <div class="flex flex-col relative z-10">
              <span :class="['font-bold text-base mb-1.5 transition-colors', selectedAssignment?.id === item.id ? 'text-indigo-900' : 'text-gray-900 group-hover:text-indigo-600']">
                {{ item.title }}
              </span>
              <p class="text-xs text-gray-500 font-medium line-clamp-2 leading-relaxed">
                {{ item.description }}
              </p>
            </div>
            <div v-if="selectedAssignment?.id === item.id" class="absolute right-4 top-1/2 -translate-y-1/2">
              <ChevronRight class="w-5 h-5 text-indigo-600" />
            </div>
          </button>
        </div>
      </aside>

      <!-- Main: Editor + Diagnosis -->
      <div class="flex-1 flex flex-col relative bg-gray-50/30">
        <div class="flex-1 flex overflow-hidden p-8 gap-8">
          <!-- Editor Area -->
          <div class="flex-[3] flex flex-col bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden group hover:shadow-md transition-shadow">
            <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
              <div class="flex items-center space-x-2">
                <Code2 class="w-4 h-4 text-gray-400" />
                <span class="text-xs font-black text-gray-500 uppercase tracking-widest">代码编辑器</span>
              </div>
              <div class="flex items-center space-x-3">
                <span v-if="isSubmitting" class="text-xs font-bold text-indigo-600 animate-pulse flex items-center">
                  <RefreshCw class="w-3 h-3 mr-1 animate-spin" /> 正在诊断中...
                </span>
                <button 
                  @click="handleSubmit" 
                  :disabled="isSubmitting || !selectedAssignment"
                  class="bg-indigo-600 text-white px-6 py-2.5 rounded-xl font-black text-sm hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-indigo-100 transition-all active:scale-95 flex items-center"
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
          <div class="flex-[2] flex flex-col bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-6 py-4 border-b border-gray-100 flex items-center space-x-2 bg-gray-50/50">
              <Sparkles class="w-4 h-4 text-indigo-500" />
              <span class="text-xs font-black text-gray-500 uppercase tracking-widest">智能诊断结果</span>
            </div>
            <div class="flex-1 overflow-y-auto p-6">
              <div v-if="!hasDiagnosed" class="h-full flex flex-col items-center justify-center text-center p-8">
                <div class="bg-indigo-50 p-6 rounded-full mb-6">
                  <Cpu class="w-12 h-12 text-indigo-300" />
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">准备就绪</h3>
                <p class="text-sm text-gray-500 font-medium leading-relaxed max-w-[200px]">
                  在左侧编写代码后点击提交，AI 助手将为你提供引导式纠错建议。
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
import { 
  BookOpen, LogOut, User, ClipboardList, 
  ChevronRight, Code2, Send, Sparkles, Cpu, RefreshCw 
} from 'lucide-vue-next';
import { useUserStore } from '../stores/userStore';
import { getAssignments } from '../api/assignment';
import { submitCode } from '../api/code';
import CodeEditor from '../components/CodeEditor.vue';
import HintPanel from '../components/HintPanel.vue';

const userStore = useUserStore();
const assignments = ref([]);
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
  window.location.reload();
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
