<template>
  <div class="student-view">
    <header class="app-header">
      <div class="header-content container">
        <h1 class="logo">Python Tutor System</h1>
        <div class="user-info">
          <span class="username">你好，学生</span>
        </div>
      </div>
    </header>
    
    <main class="main-content container">
      <div class="editor-section">
        <CodeEditor 
          v-model="code" 
          :is-submitting="isSubmitting" 
          :errors="staticIssues" 
          @submit="submitCode" 
        />
      </div>
      
      <div class="diagnosis-section">
        <HintPanel 
          :error-type="diagnosisResult.error_type" 
          :hint="diagnosisResult.hint" 
          :is-correct="diagnosisResult.is_correct" 
          :dynamic-error="diagnosisResult.dynamic_error" 
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import CodeEditor from '../components/CodeEditor.vue';
import HintPanel from '../components/HintPanel.vue';

const code = ref('# 在此输入你的 Python 代码\n\ndef main():\n    print("Hello, Python!")\n\nif __name__ == "__main__":\n    main()');
const isSubmitting = ref(false);
const staticIssues = ref([]);
const diagnosisResult = reactive({
  error_type: "",
  hint: "",
  is_correct: false,
  dynamic_error: ""
});

const submitCode = async () => {
  if (isSubmitting.value) return;
  
  isSubmitting.value = true;
  try {
    const response = await axios.post('http://localhost:8000/api/v1/code/submit', {
      user_id: 1,
      assignment_id: 1,
      code: code.value,
      test_code: "" // Optional test code for assignments
    });
    
    const data = response.data;
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
</script>

<style scoped>
.student-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.app-header {
  background: white;
  border-bottom: 1px solid var(--color-border-subtle);
  padding: var(--space-4) 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  color: var(--color-accent-orange);
}

.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: var(--space-6);
  padding-top: var(--space-8);
  padding-bottom: var(--space-8);
}

.editor-section {
  height: calc(100vh - 200px);
}

.diagnosis-section {
  position: sticky;
  top: var(--space-8);
  height: fit-content;
}

@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  .diagnosis-section {
    position: relative;
    top: 0;
  }
}
</style>
