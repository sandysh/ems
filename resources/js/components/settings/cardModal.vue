<template>
  <div class="card mb-3">
    <div class="card-header">
      <div class="card-title">
        <p class="text-ss text-uppercase font-weight-bold mb-1">
          {{ data.name }}</p>
      </div>
      <div class="card-editor">
        <button @click="editSetting">
          <i class="fas fa-edit"></i>
        </button>
      </div>
    </div>
    <div class="card-body">
      <h6 class=" mb-0">{{ data.values }}</h6>
    </div>
  </div>
</template>

<style scoped>
.card {
  box-sizing: border-box;
  border-radius: 12px;
  width: 280px;
  height: 100px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card-header {
  display: flex;
  box-sizing: border-box;
  justify-content: space-between;
  height: max-content;
  padding: 12px 12px 0 12px;

}

button {
  border: none;
  background-color: white;
}

.card-body {
  height: max-content;
  box-sizing: border-box;

  padding: 12px 12px 0 12px;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}



.edit-btn:hover {
  color: #007bff;
}

@media (max-width: 768px) {
  .card {
    width: 100%;
    height: auto;
  }
}

@media (max-width: 480px) {
  .card {
    width: 100%;
    height: auto;
  }
}
</style>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["edit-setting", "refresh-table"]);

const editSetting = () => {
  emit("edit-setting", props.data);
  emit("refresh-table");
};
</script>
