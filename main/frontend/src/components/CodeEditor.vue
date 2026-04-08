<template>
  <div class="flex flex-col h-full bg-[#282c34] overflow-hidden" :class="{ 'ring-2 ring-red-500/30': hasErrors }">
    <div class="flex-1 overflow-hidden" ref="editorRef"></div>
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

const emit = defineEmits(['update:modelValue']);

const editorRef = ref(null);
let view = null;

const hasErrors = ref(false);

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
      }),
      EditorView.theme({
        "&": { height: "100%" },
        ".cm-scroller": { overflow: "auto" },
        ".cm-content, .cm-gutter": { minHeight: "100%" }
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

watch(() => props.modelValue, (newVal) => {
  if (view && newVal !== view.state.doc.toString()) {
    view.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: newVal }
    });
  }
});

watch(() => props.errors, (newErrors) => {
  hasErrors.value = newErrors.length > 0;
}, { deep: true });
</script>

<style>
.cm-editor {
  height: 100%;
}
.cm-editor.cm-focused {
  outline: none;
}
</style>
