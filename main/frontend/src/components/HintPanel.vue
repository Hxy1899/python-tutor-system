<template>
  <div class="hint-panel anthropic-card" :class="{ 'has-error': errorType }">
    <div class="panel-header">
      <h3 class="panel-title">诊断报告</h3>
      <div v-if="errorType" class="error-badge" :class="errorClass">{{ errorType }}</div>
    </div>
    
    <div v-if="!errorType && !isCorrect" class="empty-state">
      <p>编写你的 Python 代码，并点击「提交诊断」来获得帮助。</p>
    </div>
    
    <div v-else-if="isCorrect" class="success-state">
      <div class="success-icon">?</div>
      <p class="success-msg">太棒了！你的代码运行正确，没有发现错误。</p>
    </div>
    
    <div v-else class="hint-content">
      <div class="hint-section">
        <h4 class="section-title">引导提示</h4>
        <div class="hint-text" v-html="hintHtml"></div>
      </div>
      
      <div v-if="dynamicError" class="error-details">
        <h4 class="section-title">错误详情</h4>
        <pre class="error-log">{{ dynamicError }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  errorType: { type: String, default: "" },
  hint: { type: String, default: "" },
  isCorrect: { type: Boolean, default: false },
  dynamicError: { type: String, default: "" }
});

const errorClass = computed(() => {
  if (props.errorType === "SyntaxError" || props.errorType === "IndentationError") return "critical";
  return "warning";
});

const hintHtml = computed(() => {
  if (!props.hint) return "";
  // Simple markdown-like list to HTML
  return props.hint.split('\n').map(line => {
    if (line.startsWith('- ')) {
      return `<li>${line.substring(2)}</li>`;
    }
    return `<p>${line}</p>`;
  }).join('');
});
</script>

<style scoped>
.hint-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  background: white;
  min-height: 200px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.panel-title {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: var(--space-2);
}

.error-badge {
  font-family: var(--font-heading);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

.error-badge.critical {
  background: rgba(192, 69, 58, 0.1);
  color: var(--color-error);
  border: 1px solid var(--color-error);
}

.error-badge.warning {
  background: rgba(217, 119, 87, 0.1);
  color: var(--color-accent-orange);
  border: 1px solid var(--color-accent-orange);
}

.empty-state, .success-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--color-text-secondary);
  padding: var(--space-8);
}

.success-icon {
  font-size: 3rem;
  margin-bottom: var(--space-4);
}

.success-msg {
  color: var(--color-success);
  font-weight: 500;
}

.section-title {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}

.hint-text {
  font-family: var(--font-body);
  line-height: 1.6;
}

.hint-text :deep(li) {
  margin-bottom: var(--space-2);
  list-style: none;
  position: relative;
  padding-left: var(--space-4);
}

.hint-text :deep(li)::before {
  content: "?";
  position: absolute;
  left: 0;
  color: var(--color-accent-orange);
}

.error-details {
  margin-top: var(--space-4);
}

.error-log {
  background: #f8f9fa;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  font-family: var(--font-mono);
  font-size: 12px;
  overflow-x: auto;
  color: var(--color-error);
  border: 1px dashed var(--color-border-subtle);
}
</style>
