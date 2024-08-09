<template>
  <div class="row">
    <div class="col-12">
      <div class="card mb-4">
        <div class="card-header pb-0">
          <div class="d-flex align-items-center">
            <h6 class="mb-0">Projects List</h6>
          </div>
          <div class="text-end">
             <div class="row">
               <div class="col-md-3 col-xs-12">
                 <div class="form-group">
                   <input v-model="projectStore.filters.searchText" type="text" class="form-control form-control-alternative" id="searchInput"
                          placeholder="Search here...">
                 </div>
               </div>
               <div class="col-md-3 offset-md-6 col-xs-12">
                 <button @click="projectStore.showAddProjectForm = true" type="button" class="btn btn-outline-primary btn-sm mb-0">Add New Project</button>
               </div>
             </div>
          </div>
        </div>
        <div class="card-body px-0 pt-0 pb-2">
          <div class="table-responsive p-0">
            <table class="table align-items-center mb-0">
              <thead>
                <tr>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Name</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Description</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                  <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(project, index) in projectStore.projects.list" :key="index">
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">{{ project.name }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">{{ project.description }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm" v-if="project.status">{{ project.status.name }}</h6>
                      </div>
                    </div>
                  </td>
                  <td class="align-middle text-center text-sm">
                    <a @click="projectStore.showEditForm(project)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-info btn-xs mx-2"
                      data-toggle="tooltip" data-original-title="Edit project">
                      Edit
                    </a>
                    <a @click="projectStore.showDelForm(project)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-danger btn-xs me-2"
                      data-toggle="tooltip" data-original-title="Delete project">
                      Delete
                    </a>
                    <a @click="projectStore.showStatusForm(project)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-success btn-xs"
                      data-toggle="tooltip" data-original-title="Add status">
                      Add Status
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <pagination @updatePageNumber="updatePageNumber" :pagination="projectStore.projects.pagination"></pagination>
    </div>
    <delete-modal :data="projectStore.project" @refresh-table="projectStore.getProjects" v-show="deleteFormStore.showDeleteForm"></delete-modal>
    <add-new-project-modal v-show="projectStore.showAddProjectForm"></add-new-project-modal>
    <edit-project-modal  v-if="projectStore.showEditProjectForm"></edit-project-modal>
    <add-status-modal v-show="projectStore.showAddStatusForm"></add-status-modal>
    <snack-bar v-show="snackBarStore.snackbarMessage !== ''"></snack-bar>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import addNewProjectModal from './addNewProjectModal.vue';
import editProjectModal from './editProjectModal.vue';
import deleteModal from '../shared/deleteModal.vue';
import snackBar from '../shared/snackBar.vue';
import pagination from '../pagination.vue';
import { projectStore } from '../../store/projectStore';
import {deleteFormStore} from "../../store";
import {snackBarStore} from "../../store";
import { get } from '../../kit';
import addStatusModal from "./addStatusModal.vue";
import {leavesStore} from "../../store/leavesStore";


function updatePageNumber(page){
  projectStore.projects.pagination.page = page;
  projectStore.getProjects();
}

watch(projectStore.filters, async (newFilter, oldFilter) => {
 await projectStore.getProjects()
})


onMounted(async () => {
  await projectStore.getProjects();

});
</script>
