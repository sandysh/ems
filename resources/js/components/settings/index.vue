<template>
  <div class="container self-style mt-5">
    <div class="grid-container">
      <div :key="index" class="grid-item" v-for="(setting, index) in settings.list">
        <card-modal :data="setting" @edit-setting="openEditModal" @refresh-table="getSettings"></card-modal>
      </div>
    </div>
    <update-setting-form-modal v-if="showEditSettingForm" :setting="editableSetting"
      :showEditSettingForm="showEditSettingForm" @close-edit-modal="closeEditModal"></update-setting-form-modal>
  </div>
  <snack-bar v-show="snackBarStore.snackbarMessage !== ''"></snack-bar>
</template>

<style scoped>
.self-style {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  margin: auto;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
  width: 100%;
  margin: 0 auto;
}

.grid-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .grid-container {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>

<script setup>
import { onMounted, reactive, ref } from "vue";
import cardModal from "./cardModal.vue";
import updateSettingFormModal from "./updateSettingFormModal.vue";
import snackBar from "../shared/snackBar.vue";
import { snackBarStore } from "../../store.js";

const settings = reactive({ list: [] });
const editableSetting = ref({});
const showEditSettingForm = ref(false);

async function getSettings() {
  try {
    const response = await axios.get("get_settings");
    settings.list = response.data;
  } catch (error) {
    console.error("Error fetching settings:", error);
  }
}

function openEditModal(setting) {
  editableSetting.value = { ...setting };
  showEditSettingForm.value = true;
}

function closeEditModal() {
  showEditSettingForm.value = false;
  getSettings();
}

onMounted(() => {
  getSettings();
});
</script>
