<template>
  <div class="row mt-4">
        <div class="col-lg-7 mb-lg-0 mb-4">
            <div class="card ">
              <div class="card-header pb-0 p-3">
                  <div class="d-flex justify-content-between">
                    <h6 class="mb-2">Points Activities (Weekly)</h6>
                  </div>
              </div>
              <div class="table-responsive">
                  <table class="table align-items-center table-striped">
                    <tbody>
                        <tr v-for="(rating,index) in points.data.ratings" :key="index">
                          <td class="w-5">
                              <div class="d-flex px-2 py-1 align-items-center">
                                <div class="ms-4">
                                    <h6 class="text-sm mb-0">
                                      <span class="">{{ rating.rater.first_name }} {{ rating.rater.last_name }}</span>  
                                    </h6>
                                </div>
                              </div>
                            </td>
                            <td class="w-5">voted</td>
                            <td class="w-5"><span class="">{{ rating.rated.first_name }} {{ rating.rated.last_name }}</span></td>
                            <td class="w-5"><span class=""> on </span> </td>
                            <td class="w-5"><span class="">{{ rating.metric.name }}</span></td>
                          </tr>
                    </tbody>
                  </table>
              </div>
            </div>
        </div>
        <div class="col-lg-5">
          <div class="card">
            <div class="card-header pb-0 p-3">
              <h6 class="mb-0">Points Table (Weekly)</h6>
            </div>
            <div class="card-body p-3">
              <ul class="list-group">
                <li v-for="(user,index) in points.data.users" class="list-group-item border-0 d-flex justify-content-between ps-0 mb-2 border-radius-lg">
                  <div class="d-flex align-items-center">
                    <div class="icon icon-shape icon-sm me-3 bg-gradient-dark shadow text-center">
                      <i class="ni ni-mobile-button text-white opacity-10"></i>
                    </div>
                    <div class="d-flex flex-column">
                      <h6 class="mb-1 text-dark text-sm">{{ user.first_name }} {{ user.last_name }} ({{ user.sum_total.score}})</h6>
                      <span class="text-xs">A total of <span class="text-danger">{{ user.total_raters.total }}</span> person has voted for you.</span>
                      <!-- {% for metric in user.metric_scores %}
                        <span class="text-xs"> {{ metric.metric__name}} <span class="font-weight-bold">{{ metric.score }}</span></span>
                      {% endfor %} -->
                    </div>
                  </div>
                  <div class="d-flex">
                    <button @click="showModal(user)" class="btn btn-link btn-icon-only btn-rounded btn-sm text-dark icon-move-right my-auto"><i class="ni ni-bold-right" aria-hidden="true"></i></button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <points-description @close-modal="closeModal" v-if="modal.show" :data='modalData'></points-description>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';
import PointsDescription from './PointsDescription.vue';

const points = reactive({data:{}})
const modalData = reactive({user: {}})
const modal = reactive({show: false});
async function getPoints(){
    let response = await fetch('points')
    response = await response.json()
    points.data = response.data
}

function showModal(user) {
  modal.show = true;
  modalData.user = user
  modalData.metrices = points.data.metrices
}

function closeModal(){
  modal.show = false
}

onMounted(async () => {
    await getPoints()
})

</script>