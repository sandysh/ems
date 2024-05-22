<template>
    <div class="row">
        <div class="card">
            <div class="table-responsive">
                <table class="table align-items-center mb-0">
                <thead>
                    <tr>
                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Users</th>
                    <th class="text-uppercase text-xs font-weight-bolder opacity-7 ps-2" v-for="metric in metrices.list">{{ metric.name }}</th>
                    <th class="text-secondary opacity-7"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users.list">
                        <td>
                            <div class="d-flex px-2 py-1">
                            <div>
                                <img src="https://demos.creative-tim.com/soft-ui-design-system-pro/assets/img/team-2.jpg" class="avatar avatar-sm me-3">
                            </div>
                            <div class="d-flex flex-column justify-content-center">
                                <h6 class="mb-0 text-xs">{{ user.first_name }} {{ user.last_name }}</h6>
                            </div>
                            </div>
                        </td>
                        <td v-for="metric in metrices.list">
                            <button @click="rate(user, metric)" class="btn btn-danger btn-xs mt-2 float-right">Vote</button> 
                        </td>
                    </tr>
                </tbody>
                </table>
            </div>
        </div>
        <!-- <div class="col-3 mb-5" v-for="user in users.list">
            <div class="card">
                <div class="card-header pb-0 p-3">
                    <h6 class="mb-0">{{ user.first_name }} {{ user.last_name }}</h6>
                </div>
                <div class="card-body p-3">
                    <ul class="list-group" v-for="metric in metrices.list">
                        <li class="list-group-item border-0 d-flex justify-content-between ps-0 mb-2 border-radius-lg">
                            <div class="d-flex align-items-center">
                                <div class="icon icon-shape icon-sm me-3 bg-gradient-dark shadow text-center">
                                    <i class="ni ni-mobile-button text-white opacity-10"></i>
                                </div>
                                <div class="d-flex flex-column">
                                    <h6 class="mb-1 text-dark text-sm">{{ metric.name }}</h6>
                                    <span class="text-xs">250 in stock, <span class="font-weight-bold">346+ sold</span></span>
                                </div>
                                <div class="d-flex">
                                    <button @click="rate(user, metric)" class="btn btn-danger btn-xs mt-2 float-right">Vote</button> 
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div> -->
    </div>
</template>  

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { get, post } from '../../kit';
import Swal from 'sweetalert2';

const users = reactive({ list: {}});
const metrices = reactive({ list: {}});
async function getUsers() {
    let response;
    response = await get('/users/all');
    users.list = response.data
}

async function getMetrices() {
  let response;
  response = await get('/metrices/all');
  metrices.list = response.data
}

async function rate(user, metric) {
    let response = await post('store',{user:user, metric: metric})
    console.log(response.data);
    if (response.data == 'success') {
        Swal.fire({
        title: "Awesome!",
        text: "You rated " + user.first_name + " on " + metric.name,
        icon: "success"
        });
    }
}

onMounted(() => {
    getUsers();
    getMetrices();
})
</script>