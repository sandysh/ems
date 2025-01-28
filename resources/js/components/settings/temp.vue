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
            <div>
              <div class="mb-3">
                <label for="settingName" class="form-label">Setting Name</label>
                <input type="text" class="form-control" id="settingName" v-model="editableSetting.name" readonly />
              </div>
              <div class="mb-3">
                <label for="settingValue" class="form-label">Setting Value</label>
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
import { ref, watch } from "vue";
import { defineEmits, defineProps } from "vue";
import { post } from "../../kit.js";
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



<div class="modal">
        <div class="modal-header">
            <h5>Create Poll</h5>
            <button class="close" @click="closeCreateModal">&times;</button>
        </div>
<div class="modal-body">
            <input v-model="newPoll.name" class="form-control mb-3" placeholder="Poll Name" />
            <textarea v-model="newPoll.description" class="form-control mb-3" placeholder="Poll Description"></textarea>

            <h6 class="mt-3">Options</h6>
            <div v-for="(option, index) in newPoll.options" :key="index" class="d-flex align-items-center mb-2">
                <input v-model="newPoll.options[index]" class="form-control me-2" placeholder="Option Name" />
                <button class="btn btn-danger btn-sm" @click="removeOption(index)">Remove</button>
            </div>

<button class="btn btn-outline-primary btn-sm mt-2" @click="addOption">+ Add Option</button>
</div>
<div class="modal-footer">
            <button class="btn btn-secondary" @click="closeCreateModal">Cancel</button>
            <button class="btn btn-primary" @click="createPoll">Create</button>
        </div>
</div>