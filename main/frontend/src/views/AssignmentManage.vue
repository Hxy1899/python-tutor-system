<template>
  <div class="space-y-8 max-w-7xl mx-auto font-body">
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-display text-[var(--color-text-primary)] tracking-tight">作业管理</h2>
      <button 
        @click="showCreateModal = true" 
        class="btn-primary flex items-center px-6 py-3 shadow-lg shadow-orange-100/50"
      >
        <Plus class="w-5 h-5 mr-2" /> 新增作业
      </button>
    </div>

    <!-- Assignment List -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="assignment in assignments" :key="assignment.id" class="anthropic-card group hover:shadow-xl transition-all duration-300 relative overflow-hidden">
        <!-- Background subtle accent -->
        <div class="absolute top-0 right-0 w-24 h-24 -mr-8 -mt-8 bg-orange-50 rounded-full group-hover:bg-orange-100 transition-colors duration-300"></div>
        
        <div class="flex justify-between items-start mb-6 relative z-10">
          <div class="p-3 bg-[var(--color-bg-base)] rounded-xl border border-[var(--color-border-subtle)] group-hover:bg-[var(--color-accent-orange)] transition-colors duration-300">
            <FileText class="w-6 h-6 text-[var(--color-accent-orange)] group-hover:text-white transition-colors duration-300" />
          </div>
          <div class="flex space-x-2 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-1 group-hover:translate-y-0">
            <button @click="editAssignment(assignment)" class="p-2 text-[var(--color-text-secondary)] hover:text-[var(--color-accent-orange)] hover:bg-orange-50 rounded-lg transition-colors">
              <Edit class="w-4 h-4" />
            </button>
            <button @click="confirmDelete(assignment.id)" class="p-2 text-[var(--color-text-secondary)] hover:text-[var(--color-error)] hover:bg-red-50 rounded-lg transition-colors">
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
        <h3 class="text-xl font-heading font-bold text-[var(--color-text-primary)] mb-3 relative z-10">{{ assignment.title }}</h3>
        <p class="text-sm text-[var(--color-text-secondary)] line-clamp-2 mb-6 font-body leading-relaxed relative z-10">{{ assignment.description }}</p>
        <div class="flex items-center text-xs text-[var(--color-text-secondary)] font-heading font-bold uppercase tracking-widest relative z-10">
          <Calendar class="w-3 h-3 mr-2 text-[var(--color-accent-orange)]" />
          {{ new Date(assignment.created_at).toLocaleDateString() }}
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-[var(--color-bg-inverted)]/20 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-in fade-in duration-300">
      <div class="anthropic-card w-full max-w-2xl p-10 shadow-2xl bg-white border-none animate-in zoom-in-95 duration-300">
        <div class="flex justify-between items-center mb-10">
          <h3 class="text-2xl font-display text-[var(--color-text-primary)]">{{ editingId ? '编辑作业' : '发布新作业' }}</h3>
          <button @click="closeModal" class="p-2 hover:bg-[var(--color-bg-base)] rounded-full transition-colors group">
            <X class="w-6 h-6 text-[var(--color-text-secondary)] group-hover:text-[var(--color-text-primary)]" />
          </button>
        </div>
        <form @submit.prevent="saveAssignment" class="space-y-8">
          <div>
            <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">作业标题</label>
            <input 
              v-model="form.title" 
              type="text" 
              required
              class="w-full px-5 py-4 bg-[var(--color-bg-base)]/50 border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="例如: 实现冒泡排序算法"
            >
          </div>
          <div>
            <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">作业描述</label>
            <textarea 
              v-model="form.description" 
              rows="4" 
              required
              class="w-full px-5 py-4 bg-[var(--color-bg-base)]/50 border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-body text-[var(--color-text-primary)]"
              placeholder="详细描述作业要求和预期输出..."
            ></textarea>
          </div>
          <div>
            <label class="block text-xs font-heading font-bold text-[var(--color-text-secondary)] mb-2 tracking-widest uppercase">测试代码 (Pytest)</label>
            <textarea 
              v-model="form.test_code" 
              rows="6"
              class="w-full px-5 py-4 bg-[var(--color-bg-base)] border border-[var(--color-border-subtle)] rounded-xl focus:ring-4 focus:ring-orange-100/50 focus:border-[var(--color-accent-orange)] outline-none transition-all font-mono text-sm"
              placeholder="def test_function():\n    assert solution.func(1) == 2"
            ></textarea>
            <p class="mt-3 text-xs text-[var(--color-text-secondary)] font-body italic flex items-center">
              <Info class="w-3.5 h-3.5 mr-1.5 text-[var(--color-accent-orange)]" />
              测试代码将在沙箱中运行，用于验证学生提交的 solution.py
            </p>
          </div>
          <div class="flex justify-end space-x-4 pt-6">
            <button 
              type="button" 
              @click="closeModal" 
              class="px-8 py-3 border border-[var(--color-border-subtle)] text-[var(--color-text-secondary)] rounded-xl hover:bg-[var(--color-bg-base)] font-heading font-bold transition-colors"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="btn-primary px-10 py-3 shadow-lg shadow-orange-100/50"
            >
              {{ editingId ? '保存更改' : '立即发布' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Plus, FileText, Edit, Trash2, Calendar, X, Info } from 'lucide-vue-next';
import { getAssignments, createAssignment, updateAssignment, deleteAssignment } from '../api/assignment';

const assignments = ref([]);
const showCreateModal = ref(false);
const editingId = ref(null);
const form = ref({
  title: '',
  description: '',
  test_code: ''
});

const fetchAssignments = async () => {
  try {
    assignments.value = await getAssignments();
  } catch (error) {
    console.error('Failed to fetch assignments:', error);
  }
};

const editAssignment = (assignment) => {
  editingId.value = assignment.id;
  form.value = { ...assignment };
  showCreateModal.value = true;
};

const closeModal = () => {
  showCreateModal.value = false;
  editingId.value = null;
  form.value = { title: '', description: '', test_code: '' };
};

const saveAssignment = async () => {
  try {
    if (editingId.value) {
      await updateAssignment(editingId.value, form.value);
    } else {
      await createAssignment(form.value);
    }
    fetchAssignments();
    closeModal();
  } catch (error) {
    console.error('Failed to save assignment:', error);
  }
};

const confirmDelete = async (id) => {
  if (confirm('确定要删除这个作业吗？此操作不可撤销。')) {
    try {
      await deleteAssignment(id);
      fetchAssignments();
    } catch (error) {
      console.error('Failed to delete assignment:', error);
    }
  }
};

onMounted(fetchAssignments);
</script>
