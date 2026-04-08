<template>
  <div class="space-y-6 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">作业管理</h2>
      <button 
        @click="showCreateModal = true" 
        class="bg-indigo-600 text-white px-5 py-2.5 rounded-xl hover:bg-indigo-700 flex items-center shadow-lg shadow-indigo-200 transition-all font-semibold"
      >
        <Plus class="w-5 h-5 mr-2" /> 新增作业
      </button>
    </div>

    <!-- Assignment List -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="assignment in assignments" :key="assignment.id" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl transition-all group">
        <div class="flex justify-between items-start mb-4">
          <div class="p-3 bg-indigo-50 rounded-xl group-hover:bg-indigo-600 transition-colors">
            <FileText class="w-6 h-6 text-indigo-600 group-hover:text-white transition-colors" />
          </div>
          <div class="flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button @click="editAssignment(assignment)" class="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors">
              <Edit class="w-4 h-4" />
            </button>
            <button @click="confirmDelete(assignment.id)" class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-2">{{ assignment.title }}</h3>
        <p class="text-sm text-gray-600 line-clamp-2 mb-4 font-medium">{{ assignment.description }}</p>
        <div class="flex items-center text-xs text-gray-400 font-semibold uppercase tracking-wider">
          <Calendar class="w-3 h-3 mr-1.5" />
          {{ new Date(assignment.created_at).toLocaleDateString() }}
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl w-full max-w-2xl p-10 shadow-2xl">
        <div class="flex justify-between items-center mb-8">
          <h3 class="text-2xl font-black text-gray-900">{{ editingId ? '编辑作业' : '发布新作业' }}</h3>
          <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <X class="w-6 h-6 text-gray-400" />
          </button>
        </div>
        <form @submit.prevent="saveAssignment" class="space-y-6">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">作业标题</label>
            <input 
              v-model="form.title" 
              type="text" 
              required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-medium"
              placeholder="例如: 实现冒泡排序算法"
            >
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">作业描述</label>
            <textarea 
              v-model="form.description" 
              rows="4" 
              required
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-medium"
              placeholder="详细描述作业要求和预期输出..."
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2">测试代码 (Pytest)</label>
            <textarea 
              v-model="form.test_code" 
              rows="6"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 transition-all font-mono text-sm bg-gray-50"
              placeholder="def test_function():\n    assert solution.func(1) == 2"
            ></textarea>
            <p class="mt-2 text-xs text-gray-500 font-medium italic">测试代码将在沙箱中运行，用于验证学生提交的 solution.py</p>
          </div>
          <div class="flex justify-end space-x-4 pt-4">
            <button 
              type="button" 
              @click="closeModal" 
              class="px-6 py-3 border border-gray-200 text-gray-600 rounded-xl hover:bg-gray-50 font-bold transition-colors"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="px-8 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 font-bold transition-all"
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
import { Plus, FileText, Edit, Trash2, Calendar, X } from 'lucide-vue-next';
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
