<template>
  <div class="row">
    <div class="col-12">
      <div class="card mb-4">
        <div class="card-header pb-0">
          <div class="d-flex align-items-center">
            <h6 class="mb-0">Metrices List</h6>
          </div>
          <div class="text-end">
             <div class="row">
               <div class="col-md-3 col-xs-12">
                 <div class="form-group">
                   <input v-model="searchText" type="email" class="form-control form-control-alternative" id="exampleFormControlInput1"
                          placeholder="search here.....">
                 </div>
               </div>
               <div class="col-md-3 offset-md-6 col-xs-12">
                 <button @click="metricStore.showAddMetricForm = true" type="button" class="btn btn-outline-primary btn-sm mb-0">Add New Metric</button>
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
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Score</th>
                  <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(metric, index) in metrices.list" :key="index">
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div>
                        <img src="/static/img/bg1.jpg" class="avatar avatar-sm me-3" alt="user1">
                      </div>
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">{{ metric.name }}</h6>
                      </div>
                    </div>
                  </td>
                   <td>
                    <p class="text-xs font-weight-bold mb-0">{{ metric.score }}</p>
                  </td>
                  <td class="align-middle text-center text-sm">
                    <span v-if="metric.is_active" class="badge badge-sm bg-gradient-success">Active</span>
                    <span v-else class="badge badge-sm bg-gradient-secondary">Suspended</span>
                  </td>
                  <td class="align-middle">
                    <a @click="edit(metric)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-info btn-xs mx-2"
                      data-toggle="tooltip" data-original-title="Edit metric">
                      Edit
                    </a>
                    <a @click="deleteMetric(metric)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-danger btn-xs"
                      data-toggle="tooltip" data-original-title="Edit metric">
                      Delete
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <pagination @updatePageNumber="updatePageNumber" :pagination="metrices.pagination"></pagination>
    </div>
    <delete-modal :data="metric" @refresh-table="getMetrices" v-show="deleteFormStore.showDeleteForm"></delete-modal>
    <add-new-metric-modal :entity="entity" @refresh-table="getMetrices" v-show="metricStore.showAddMetricForm"></add-new-metric-modal>
    <edit-metric-modal :data="entity"  @refresh-table="getMetrices" v-show="metricStore.showEditMetricForm"></edit-metric-modal>
    <snack-bar v-show="snackBarStore.snackbarMessage!==''"></snack-bar>
  </div>
</template>

<script setup>
import {onMounted, reactive, ref, watch} from 'vue';
import addNewMetricModal from './addNewMetricModal.vue';
import editMetricModal from './editMetricesModal.vue';
import deleteModal from '../shared/deleteModal.vue';
import snackBar from '../shared/snackBar.vue';
import pagination from '../pagination.vue';
import { metricStore, snackBarStore, deleteFormStore } from '../../store';
import { get } from '../../kit';
const metrices = reactive({ list: {}, pagination:{}});
const metric = ref({
  label: '',
  id: null,
  model: ''
})
const entity = ref({})
const editableMetric = ref({})
const searchText = ref('')
async function getMetrices() {
  let response;
  response = await get(`all?paginate=true&page=${metrices.pagination.page ? metrices.pagination.page : 1 }&searchText=${searchText.value}`);
  if (response.status === 200) {
    metrices.list = response.data.data
    metrices.pagination = response.data.pagination
  } else {

  }

}

function updatePageNumber(page){
  metrices.pagination.page = page;
  getMetrices();
}

function addSnackMessage(message){
  message = messsage
}

function deleteMetric(metric){
  console.log(metric)
  deleteFormStore.showDeleteForm = true
  this.metric.label = metric.name
  this.metric.id = metric.id
  this.metric.model = 'Metrices'
}

function edit(metric) {
  metricStore.showEditMetricForm = true
  this.entity = metric
}

watch(searchText, async (newValue, oldValue) => {
  getMetrices()
})
onMounted(() => {
  getMetrices();
})

</script>
