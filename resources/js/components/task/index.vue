<template>
  <div class="row">
    <div class="col-12">
      <div class="card mb-4">
        <div class="card-header pb-0">
          <div class="d-flex align-items-center">
            <h6 class="mb-0">Task List</h6>
          </div>
          <div class="text-end">
             <div class="row">
               <div class="col-md-3 col-xs-12">
                 <div class="form-group">
                   <input v-model="taskStore.filters.searchText" type="text" class="form-control form-control-alternative" id="searchInput"
                          placeholder="Search here...">
                 </div>
               </div>
               <div class="col-md-3 offset-md-6 col-xs-12">
                 <button @click="taskStore.showAddTaskForm = true" type="button" class="btn btn-outline-primary btn-sm mb-0">Add New Task</button>
               </div>
             </div>
          </div>
        </div>
        <div class="card-body px-0 pt-0 pb-2">
          <div class="table-responsive p-0">
            <table class="table align-items-center mb-0">
              <thead>
                <tr>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Task</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Description</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Project</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Owner</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Assign To</th>
                  <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(task, index) in taskStore.tasks.list" :key="index">
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">{{ task.title }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">{{ task.description }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm" v-if="task.project">{{ task.project.name }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm" v-if="task.status">{{ task.status.name }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm" v-if="task.owner">{{ task.owner.username }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm" v-if="task.assigned_to">{{ task.assigned_to.username }}</h6>
                      </div>
                    </div>
                  </td>
                  <td class="align-middle text-center text-sm">
                    <a @click="taskStore.showEditForm(task)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-info btn-xs mx-2"
                      data-toggle="tooltip" data-original-title="Edit project">
                      Edit
                    </a>
                    <a @click="taskStore.deleteTask(task)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-danger btn-xs me-2"
                      data-toggle="tooltip" data-original-title="Delete project">
                      Delete
                    </a>
                    <a @click="taskStore.viewClick(task)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-success btn-xs"
                      data-toggle="tooltip" data-original-title="view">
                      View
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <pagination @updatePageNumber="updatePageNumber" :pagination="taskStore.tasks.pagination"></pagination>
    </div>
    <delete-modal :data="taskStore.task" @refresh-table="taskStore.gettasks" v-show="deleteFormStore.showDeleteForm"></delete-modal>
    <add-new-task-modal v-if="taskStore.showAddTaskForm"></add-new-task-modal>
    <edit-task-modal  v-if="taskStore.showEditTaskForm"></edit-task-modal>
    <view-task-modal v-show="taskStore.showViewTask"></view-task-modal>
    <snack-bar v-show="snackBarStore.snackbarMessage !== ''"></snack-bar>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import addNewTaskModal from './addNewTaskModal.vue';
import editTaskModal from './editTaskModal.vue';
import deleteModal from '../shared/deleteModal.vue';
import viewTaskModal from './viewTaskModal.vue';
import snackBar from '../shared/snackBar.vue';
import pagination from '../pagination.vue';
import { taskStore } from '../../store/taskStore';
import {deleteFormStore} from "../../store";
import {snackBarStore} from "../../store";
import { get } from '../../kit';
import {leavesStore} from "../../store/leavesStore";


function updatePageNumber(page){
  taskStore.tasks.pagination.page = page;
  taskStore.gettasks();
}

watch(taskStore.filters, async (newFilter, oldFilter) => {
 await taskStore.gettasks()
})


onMounted(async () => {
  await taskStore.gettasks();

});
</script>
