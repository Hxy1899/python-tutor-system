<template>
  <div class="code-editor-container" :class="{ 'has-errors': hasErrors }">
    <div class="editor-header">
      <div class="header-left">
        <span class="editor-title">Python 编辑器</span>
        <div class="status-indicator" :class="statusClass"></div>
      </div>
      <div class="header-right">
        <button class="btn-primary" @click="handleSubmit" :disabled="isSubmitting">
          <span v-if="isSubmitting">提交中...</span>
          <span v-else>提交诊断</span>
        </button>
      </div>
    </div>
    <div class="editor-body" ref="editorRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { EditorState } from "@codemirror/state";
import { EditorView, keymap, lineNumbers, highlightActiveLineGutter } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { linter, lintGutter } from "@codemirror/lint";

const props = defineProps({
  modelValue: { type: String, default: "" },
  isSubmitting: { type: Boolean, default: false },
  errors: { type: Array, default: () => [] }
});

const emit = defineEmits(['update:modelValue', 'submit']);

const editorRef = ref(null);
let view = null;

const hasErrors = ref(false);
const statusClass = ref('idle');

onMounted(() => {
  const startState = EditorState.create({
    doc: props.modelValue,
    extensions: [
      lineNumbers(),
      highlightActiveLineGutter(),
      history(),
      lintGutter(),
      python(),
      oneDark,
      keymap.of([...defaultKeymap, ...historyKeymap]),
      EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          emit('update:modelValue', update.state.doc.toString());
        }
      }),
      linter(() => {
        return props.errors.map(err => ({
          from: getPos(err.line, err.column),
          to: getPos(err.line, err.column + 5), // Rough estimate
          severity: "error",
          message: err.message
        }));
      })
    ]
  });

  view = new EditorView({
    state: startState,
    parent: editorRef.value
  });
});

onBeforeUnmount(() => {
  if (view) view.destroy();
});

const getPos = (line, col) => {
  if (!view) return 0;
  try {
    const lineObj = view.state.doc.line(line);
    return lineObj.from + col;
  } catch {
    return 0;
  }
};

const handleSubmit = () => {
  emit('submit');
};

watch(() => props.modelValue, (newVal) => {
  if (view && newVal !== view.state.doc.toString()) {
    view.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: newVal }
    });
  }
});

watch(() => props.errors, (newErrors) => {
  hasErrors.value = newErrors.length > 0;
  statusClass.value = newErrors.length > 0 ? 'error' : 'success';
}, { deep: true });
</script>

<style scoped>
.code-editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--color-border-subtle);
  background: #282c34; /* Dark background for editor area */
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-raised);
  border-bottom: 1px solid var(--color-border-subtle);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.editor-title {
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-secondary);
}

.status-indicator.idle { background: var(--color-text-secondary); }
.status-indicator.success { background: var(--color-success); }
.status-indicator.error { background: var(--color-error); }

.editor-body {
  flex: 1;
  overflow: auto;
}

:deep(.cm-editor) {
  height: 100%;
}
</style>
