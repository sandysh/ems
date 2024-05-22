<template>
<div class="row mt-5">
  <div class="col-12">
     <div class="card mb-4">
        <div class="card-header pb-0">
          <div class="row">
            <div class="col-9">
              <h6>Attendance History</h6>
            </div>
            <div class="col-2">
              <input v-model="filter.range" class="form-control datepicker" placeholder="Please select date" type="text" onfocus="focused(this)" onfocusout="defocused(this)">
            </div>
            <div class="col-1">
              <button @click="getSummary" class="btn btn-primary">Submit</button>
            </div>
          </div>
        </div>
        <div class="card-body px-0 pt-0 pb-2">
           <div class="table-responsive p-0">
              <table class="table align-items-center justify-content-center mb-0">
                 <thead>
                    <tr>
                       <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Date</th>
                       <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Punch In</th>
                       <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Punch Out</th>
                       <th class="text-uppercase text-secondary text-xxs font-weight-bolder text-center opacity-7 ps-2">Notes</th>
                    </tr>
                 </thead>
                 <tbody>
                    <tr v-for="attendance in summaries.list" :key="attendance.id">
                       <td>
                          <div class="d-flex px-2">
                             <div class="my-auto">
                                <h6 class="mb-0 text-sm">{{ attendance.punch_in_date }}</h6>
                             </div>
                          </div>
                       </td>
                       <td>
                          <span class="text-sm font-weight-bold mb-0">{{ attendance.punch_in_time }}</span>
                       </td>
                       <td>
                          <span class="text-sm font-weight-bold">{{ attendance.punch_out_time ? attendance.punch_out_time : "Missed" }}</span>
                       </td>
                       <td class="align-middle text-center">
                          <div class="d-flex align-items-center justify-content-center">
                             <span class="me-2 font-weight-bold">{{ attendance.notes }}</span>
                          </div>
                       </td>
                    </tr>
                 </tbody>
              </table>
           </div>
        </div>
     </div>
  </div>
</div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';
import { get, post } from '../../kit';
const summaries = reactive({list:{}})
const filter = reactive({range: ''})
async function getSummary() {
    let response = await post('summary', {filter: filter});
    summaries.list = response.data
}

onMounted(() => {
    getSummary();
})


</script>