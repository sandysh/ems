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
                <h3 class="">Add Status Form</h3>
                <hr class="border border-default border-1">
              </div>
              <div v-if="errorsStore.show" class="alert alert-danger mx-3" role="alert">
                <li class="text-white" v-for="(error,index) in errorsStore.list" :key="index">{{ error }}</li>
              </div>
              <div class="card-body">
                <form action="" method="post" autocomplete="false">
                  <div class="card-body px-0 pt-0 pb-2">
                    <div class="form-group">
                      <label for="status" class="form-control-label">Status</label>
                      <input v-model="projectStore.data.name" name="name" class="form-control" type="text" value=""
                             id="status" required>
                    </div>

                    <div class="d-flex justify-content-end">
                      <button @click.prevent="projectStore.statusSubmit" type="button"
                              class="btn btn-round bg-gradient-info w-20 mt-4 mb-0">Create
                      </button>
                      <button @click.prevent="projectStore.statusCancel" type="button"
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
import {projectStore} from '../../store/projectStore';
import {errorsStore} from "../../store";
const emit = defineEmits(['refresh-table'])
const props = defineProps(['data'])


</script>
