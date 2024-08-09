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
                <h3 class="">Edit Project Form</h3>
                <hr class="border border-default border-1">
              </div>
              <div v-if="errorsStore.show" class="alert alert-danger mx-3" role="alert">
                <li class="text-white" v-for="(error,index) in errorsStore.list" :key="index">{{ error }}</li>
              </div>
              <div class="card-body">
                <form action="" method="post" autocomplete="false">
                  <div class="card-body px-0 pt-0 pb-2">
                    <div class="form-group">
                      <label for="first name" class="form-control-label">Name</label>
                      <input v-model="projectStore.entity.name" name="name" class="form-control" type="text" value=""
                             id="first-name">
                    </div>
                    <div class="form-group">
                      <label for="score" class="form-control-label">Description</label>
                      <input v-model="projectStore.entity.description" name="description" class="form-control" type="text"
                             value=""
                             id="score">
                    </div>
                    <div class="form-group">
                      <label class="form-control-label" for="status">Status</label>
                      <select v-model="projectStore.entity.status.id" name="status" class="form-select form-select-md"
                              id="status">
                        <option v-for="(status, index) in projectStatusStore.list" :key="index" :value="status.id">
                          {{ status.name }}
                        </option>
                      </select>
                    </div>

                    <div class="d-flex justify-content-end">
                      <button @click.prevent="projectStore.submit" type="button"
                              class="btn btn-round bg-gradient-info w-20 mt-4 mb-0">Update
                      </button>
                      <button @click.prevent="projectStore.cancel" type="button"
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
import {reactive, onMounted} from 'vue';
import {projectStore} from '../../store/projectStore';
import {projectStatusStore} from "../../store/projectStatusStore";
import {errorsStore} from "../../store";

onMounted(() => {
  projectStatusStore.statusData(projectStore.entity.id)
})

</script>
