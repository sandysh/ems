<template>
  <div v-if="showEditSettingForm" class="modal fade show" style="display: block">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Update Setting</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitUpdate">
            <div v-if="editableSetting.name === 'punch_in_time'">
              <time-picker :editable-setting="editableSetting" />
            </div>
            <div v-else>
              <div class="mb-3">
                <label for="settingValue" class="form-label">{{ editableSetting.name }}</label>
                <input type="text" class="form-control" id="settingValue" v-model="editableSetting.values"
                  placeholder="Enter new value" required />
              </div>

            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                Close
              </button>
              <button type="submit" class="btn btn-primary">
                Save changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import timePicker from "./timePicker.vue";
import { ref, watch } from "vue";
import { defineEmits, defineProps } from "vue";
import { post } from "../../kit";
import { snackBarStore } from "../../store.js";

const props = defineProps({
  setting: {
    type: Object,
    required: true,
  },
  showEditSettingForm: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["close-edit-modal"]);

const editableSetting = ref({ ...props.setting });

function closeModal() {
  emit("close-edit-modal");
}

async function submitUpdate() {
  if (!editableSetting.value.values) {
    snackBarStore.snackbarMessage = "Value cannot be empty!";
    return;
  }

  try {
    console.log(editableSetting.value.values);
    const response = await post(`update_setting/${editableSetting.value.id}`, {
      values: editableSetting.value.values,
    });

    if (response.status === 200) {
      snackBarStore.snackbarMessage = "Setting updated successfully!";
      closeModal();
    }
  } catch (error) {
    snackBarStore.snackbarMessage = "Failed to update setting.";
    console.error(error);
  }
}

watch(
  () => props.setting,
  (newSetting) => {
    editableSetting.value = { ...newSetting };
  },
  { immediate: true }
);
</script>
