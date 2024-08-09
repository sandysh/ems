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
                <div class="d-flex justify-content-between">
                  <h3 class="">Task Details</h3>
                  <button @click.prevent="taskStore.cancelTaskDetails" type="button"
                          class="btn btn-round bg-gradient-danger w-10 mx-4">X
                  </button>
                </div>
                <hr class="border border-default border-1">
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
                      <div class="carousel-inner">
                        <div v-for="(img, index) in taskStore.entity.attachment_urls" :key="index"
                             class="carousel-item active">
                          <img :src="img" class="d-block w-100" alt="image" height="300" width="400">
                        </div>
                      </div>
                      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls"
                              data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                      </button>
                      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls"
                              data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                      </button>
                    </div>
                  </div>
                  <div class="card-body">
                    <h5 class="card-title">{{ taskStore.entity.title }}</h5>
                    <p class="card-text">{{ taskStore.entity.description }}</p>
                    <p class="card-text">Project:
                      {{ taskStore.entity.project ? taskStore.entity.project.name : null }}</p>
                    <p class="card-text">Task Status:
                      {{ taskStore.entity.status ? taskStore.entity.status.name : null }}</p>
                    <p class="card-text">Owner:
                      {{ taskStore.entity.owner ? taskStore.entity.owner.username : null }}</p>
                    <p class="card-text">Task Assign To:
                      {{ taskStore.entity.assigned_to ? taskStore.entity.assigned_to.username : null }}</p>
                    <p class="card-text">Start Date: {{ taskStore.entity.start_time }}</p>
                    <p class="card-text">End Date: {{ taskStore.entity.end_time }}</p>
                  </div>
                </div>
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
import {onMounted, watch, ref} from "vue";


onMounted(() => {
  taskStore.gettasks();
})

</script>
