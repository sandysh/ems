<template>
  <div class="col-md-4">
    <div class="modal fade show" style="display: block;" id="modal-form" tabindex="-1" aria-modal="true" role="dialog"
         aria-labelledby="modal-form"
         aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-body p-0">
            <div class="card card-plain">
              <div class="card-header pb-0 text-left">
                <h3 class="">Edit Task Form</h3>
                <hr class="border border-default border-1">
              </div>
              <div v-if="errorsStore.show" class="alert alert-danger mx-3" role="alert">
                <li class="text-white" v-for="(error,index) in errorsStore.list" :key="index">{{ error }}</li>
              </div>
              <div class="card-body">
                <form action="" method="post" autocomplete="false">
                  <div class="card-body px-0 pt-0 pb-2">
                    <div class="form-group">
                      <label for="title" class="form-control-label">title</label>
                      <input v-model="taskStore.entity.title" class="form-control" type="text" value=""
                             id="title" required>
                    </div>
                    <div class="form-group">
                      <label for="description" class="form-control-label">Description</label>
                      <input v-model="taskStore.entity.description" class="form-control"
                             type="text" value=""
                             id="description" required>
                    </div>
                    <div class="form-group">
                      <label for="project" class="form-control-label">Project</label>
                      <input v-model="taskStore.entity.project.name" class="form-control"
                             type="text" value=""
                             id="project" required>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">Status</label>
                      <select v-model="taskStore.entity.status.id" class="form-select form-select-md">
                        <option v-for="(status, index) in projectStatusStore.list" :key="index" :value="status.id">
                          {{ status.name }}
                        </option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">Assign To</label>
                      <select v-model="taskStore.entity.assigned_to.id" class="form-select form-select-md">
                        <option v-for="(user, index) in userStore.allUsers.list" :key="index" :value="user.id">
                          {{ user.username }}
                        </option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="start_time" class="form-control-label">Start Date</label>
                      <input class="form-control"
                             type="datetime-local"
                             :value="formatDateTime(taskStore.entity.start_time)"
                             @input="updateStartTime"
                             id="start_time" required>
                    </div>
                    <div class="form-group">
                      <label for="end_time" class="form-control-label">End Date</label>
                      <input :value="formatDateTime(taskStore.entity.end_time)" class="form-control"
                             type="datetime-local"
                             @input="updateEndTime"
                             id="end_time" required>
                    </div>
                    <div class="form-group">
                      <label for="attachments" class="form-control-label">Attachments
                        <p v-for="(attach, index) in taskStore.entity.attachment_urls" :key="index"
                           style="line-height: 4px;">{{ attach }}</p></label>

                      <input ref="attachments" name="attachments" class="form-control" type="file" id="attachments"
                             multiple accept="image/*">
                    </div>


                    <div class="d-flex justify-content-end">
                      <button @click="handleFileUpdate" type="button"
                              class="btn btn-round bg-gradient-info w-20 mt-4 mb-0">Update
                      </button>
                      <button @click.prevent="taskStore.cancelEditTask" type="button"
                              class="btn btn-round bg-gradient-danger w-20 mt-4 mb-0">Cancel
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import {taskStore} from "../../store/taskStore";
import {errorsStore} from "../../store";
import {onMounted, watch, ref} from "vue";
import {projectStatusStore} from "../../store/projectStatusStore";
import {userStore} from "../../store/userStore";
import axios from 'axios';

const attachments = ref(null);

async function handleFileUpdate() {
  const formData = new FormData();

  // Append files to formData

  if (attachments.value) {
    for (let i = 0; i < attachments.value.files.length; i++) {
      let file = attachments.value.files[i];
      formData.append('attachments', file);
    }
  }

  // Append other form data
  formData.append('title', taskStore.entity.title);
  formData.append('description', taskStore.entity.description);
  formData.append('project', taskStore.entity.project.id);
  formData.append('status', taskStore.entity.status.id);
  formData.append('assign_to', taskStore.entity.assigned_to.id);
  formData.append('start_time', taskStore.entity.start_time);
  formData.append('end_time', taskStore.entity.end_time);

  try {
    const response = await axios.post(`update/${taskStore.entity.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      taskStore.showEditTaskForm = false
      await taskStore.gettasks();
    }
  } catch (error) {
    errorsStore.list = error.response.data
    errorsStore.show = true
  }
}

function formatDateTime(datetime) {
  const date = new Date(datetime);
  let formatted = null

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  formatted = `${year}-${month}-${day}T${hours}:${minutes}`;
  return formatted
}

function updateStartTime(event) {
  taskStore.entity.start_time = event.target.value;
}

function updateEndTime(event) {
  taskStore.entity.end_time = event.target.value;
}

onMounted(() => {
  projectStatusStore.statusData(taskStore.entity.project.id)
  userStore.FetchAllUser();
})

</script>
