<template>
  <div class="hint-panel font-body" :class="{ 'has-error': errorType }">
    <div class="flex justify-between items-start mb-6">
      <h3 class="text-xl font-display text-[var(--color-text-primary)]">诊断报告</h3>
      <div v-if="errorType" class="px-3 py-1 rounded-full text-[10px] font-heading font-bold uppercase tracking-widest border" :class="errorClass">
        {{ errorType }}
      </div>
    </div>
    
    <div v-if="!errorType && !isCorrect" class="h-full flex flex-col items-center justify-center text-center p-8 bg-[var(--color-bg-base)]/30 rounded-2xl border border-dashed border-[var(--color-border-subtle)]">
      <p class="text-sm text-[var(--color-text-secondary)] italic">编写你的 Python 代码，并点击「提交诊断」来获得帮助。</p>
    </div>
    
    <div v-else-if="isCorrect" class="success-state p-8 bg-green-50/50 rounded-2xl border border-green-100 text-center animate-in zoom-in duration-500">
      <div class="text-5xl mb-4">{{ randomIcon }}</div>
      <p class="text-lg font-display text-[var(--color-success)] mb-2">太棒了！</p>
      <p class="text-sm text-[var(--color-text-secondary)]">你的代码运行正确，没有发现错误。</p>
    </div>
    
    <div v-else class="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div class="hint-section p-6 bg-orange-50/30 rounded-2xl border border-orange-100/50">
        <h4 class="text-xs font-heading font-bold text-[var(--color-accent-orange)] uppercase tracking-widest mb-4 flex items-center">
          <Sparkles class="w-3.5 h-3.5 mr-2" /> 引导提示
        </h4>
        <div class="space-y-3 text-[var(--color-text-primary)] leading-relaxed text-sm" v-html="hintHtml"></div>
      </div>
      
      <div v-if="dynamicError" class="error-details p-6 bg-[var(--color-bg-inverted)] rounded-2xl border border-gray-800 shadow-xl">
        <h4 class="text-xs font-heading font-bold text-gray-400 uppercase tracking-widest mb-4 flex items-center">
          <Terminal class="w-3.5 h-3.5 mr-2" /> 错误详情
        </h4>
        <pre class="font-mono text-[11px] text-red-400 overflow-x-auto whitespace-pre-wrap leading-relaxed">{{ dynamicError }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Sparkles, Terminal } from 'lucide-vue-next';

const props = defineProps({
  errorType: { type: String, default: "" },
  hint: { type: String, default: "" },
  isCorrect: { type: Boolean, default: false },
  dynamicError: { type: String, default: "" }
});

const errorClass = computed(() => {
  if (props.errorType === "SyntaxError" || props.errorType === "IndentationError") 
    return "bg-red-50 text-[var(--color-error)] border-red-200 shadow-sm shadow-red-100/50";
  return "bg-orange-50 text-[var(--color-accent-orange)] border-orange-200 shadow-sm shadow-orange-100/50";
});

const hintHtml = computed(() => {
  if (!props.hint) return "";
  // Simple markdown-like list to HTML
  return props.hint.split('\n').map(line => {
    const trimmed = line.trim();
    if (trimmed.startsWith('- ')) {
      return `<li class="ml-4 list-disc marker:text-[var(--color-accent-orange)]">${trimmed.substring(2)}</li>`;
    }
    return `<p>${trimmed}</p>`;
  }).join('');
});

const randomIcon = computed(() => {
  const emojis = ['🎉', '🥳', '✨', '⭐', '👍'];
  return emojis[Math.floor(Math.random() * emojis.length)];
});
</script>

<style scoped>
/* Remove existing styles as we use Tailwind now */
</style>