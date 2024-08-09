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
                <h3 class="">New Task Form</h3>
                <hr class="border border-default border-1">
              </div>
              <div v-if="errorsStore.show" class="alert alert-danger mx-3" role="alert">
                <li class="text-white" v-for="(error,index) in errorsStore.list" :key="index">{{ error }}</li>
              </div>
              <div class="card-body">
                <form action="" method="post" autocomplete="false">
                  <div class="card-body px-0 pt-0 pb-2">
                    <div class="form-group">
                      <label class="form-control-label">title</label>
                      <input v-model="taskStore.taskData.title" class="form-control" type="text" value=""
                             required>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">Description</label>
                      <input v-model="taskStore.taskData.description" class="form-control"
                             type="text" value=""
                             required>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">Project</label>
                      <select v-model="taskStore.taskData.project" class="form-select form-select-md">
                        <option disabled value="">Please select Project</option>
                        <option v-for="(project, index) in projectStore.allProjects.list" :key="index"
                                :value="project.id">{{ project.name }}
                        </option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label  class="form-control-label">Status</label>
                      <select v-model="taskStore.taskData.status" class="form-select form-select-md">
                        <option disabled value="">Please select Status</option>
                        <option v-for="(status, index) in projectStatusStore.list" :key="index" :value="status.id">
                          {{ status.name }}
                        </option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">Assign To</label>
                      <select v-model="taskStore.taskData.assign_to" class="form-select form-select-md">
                        <option disabled value="">Please select User</option>
                        <option v-for="(user, index) in userStore.allUsers.list" :key="index" :value="user.id">
                          {{ user.username }}
                        </option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">Start Date</label>
                      <input v-model="taskStore.taskData.start_time" class="form-control"
                             type="datetime-local"
                             value=""
                             required>
                    </div>
                    <div class="form-group">
                      <label class="form-control-label">End Date</label>
                      <input v-model="taskStore.taskData.end_time" class="form-control"
                             type="datetime-local"
                             value=""
                             required>
                    </div>
                    <div class="form-group">
                      <label for="attachments" class="form-control-label">Attachments</label>
                      <input ref="attachments" name="attachments" class="form-control" type="file" id="attachments"
                             multiple accept="image/*">
                    </div>


                    <div class="d-flex justify-content-end">
                      <button @click="handleFileUpload" type="button"
                              class="btn btn-round bg-gradient-info w-20 mt-4 mb-0">Create
                      </button>
                      <button @click.prevent="taskStore.cancelNewTask" type="button"
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
import {projectStore} from "../../store/projectStore";
import {userStore} from "../../store/userStore";
import axios from 'axios';

const attachments = ref(null);

async function handleFileUpload() {
  const formData = new FormData();

  // Append files to formData

  if (attachments.value) {
    for (let i = 0; i < attachments.value.files.length; i++) {
      let file = attachments.value.files[i];
      formData.append('attachments', file);
    }
  }

  // Append other form data
  formData.append('title', taskStore.taskData.title);
  formData.append('description', taskStore.taskData.description);
  formData.append('project', taskStore.taskData.project);
  formData.append('status', taskStore.taskData.status);
  formData.append('assign_to', taskStore.taskData.assign_to);
  formData.append('start_time', taskStore.taskData.start_time);
  formData.append('end_time', taskStore.taskData.end_time);

  try {
    const response = await axios.post('create/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      taskStore.showAddTaskForm = false
      await taskStore.gettasks();
    }
  } catch (error) {
    errorsStore.list = error.response.data
    errorsStore.show = true
  }
}

watch(() => taskStore.taskData.project, async (newValue, oldValue) => {
  await projectStatusStore.statusData(taskStore.taskData.project)
})

onMounted(() => {
  projectStore.fetchAllProjects();
  userStore.FetchAllUser();
})

</script>
