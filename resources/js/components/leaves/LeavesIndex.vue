<template>
    <div id="leaves">
<!--      <div class="d-flex justify-content-end">-->
<!--        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">-->
<!--          <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked>-->
<!--          <label class="btn btn-outline-primary" for="btnradio1">Today</label>-->

<!--          <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off">-->
<!--          <label class="btn btn-outline-primary" for="btnradio2">Yesterday</label>-->

<!--          <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off">-->
<!--          <label class="btn btn-outline-primary" for="btnradio3">This Month</label>-->

<!--          <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off">-->
<!--          <label class="btn btn-outline-primary" for="btnradio3">Last Month</label>-->
<!--        </div>-->
<!--      </div>-->
        <div class="row mb-3">
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
                <div class="card">
                    <div class="card-body p-3">
                        <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-uppercase font-weight-bold">Total Leaves Applied</p>
                                <h5 class="font-weight-bolder">
                                    {{ leavesStore.stats.total_leaves_applied }}
                                </h5>
                                <!-- <p class="mb-0">
                                    <span class="text-success text-sm font-weight-bolder">+55%</span>
                                    since yesterday
                                </p> -->
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-primary shadow-primary text-center rounded-circle">
                                <i class="ni ni-money-coins text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
                <div class="card">
                    <div class="card-body p-3">
                        <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-uppercase font-weight-bold">Total Leaves Pending </p>
                                <h5 class="font-weight-bolder">
                                    {{ leavesStore.stats.total_leaves_pending }}
                                </h5>
                                <!-- <p class="mb-0">
                                    <span class="text-success text-sm font-weight-bolder">+3%</span>
                                    since last week
                                </p> -->
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-danger shadow-danger text-center rounded-circle">
                                <i class="ni ni-world text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
                <div class="card">
                    <div class="card-body p-3">
                        <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-uppercase font-weight-bold">Total Leaves Approved</p>
                                <h5 class="font-weight-bolder">
                                    {{ leavesStore.stats.total_leaves_approved }}
                                </h5>
                                <!-- <p class="mb-0">
                                    <span class="text-danger text-sm font-weight-bolder">-2%</span>
                                    since last quarter
                                </p> -->
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-success shadow-success text-center rounded-circle">
                                <i class="ni ni-paper-diploma text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-sm-6">
                <div class="card">
                    <div class="card-body p-3">
                        <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-uppercase font-weight-bold">Total Leaves Rejected</p>
                                <h5 class="font-weight-bolder">
                                    {{ leavesStore.stats.total_leaves_rejected }}
                                </h5>
                                <!-- <p class="mb-0">
                                    <span class="text-success text-sm font-weight-bolder">+5%</span> than last month
                                </p> -->
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-warning shadow-warning text-center rounded-circle">
                                <i class="ni ni-cart text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-sm-6 mt-3" v-for="(g,i) in leavesStore.stats.general" :key="i">
                <div class="card">
                    <div class="card-body p-3">
                        <div class="row">
                        <div class="col-8">
                            <div class="numbers">
                                <p class="text-sm mb-0 text-uppercase font-weight-bold">{{ g.name }} Leaves</p>
                                <h5 class="font-weight-bolder">
                                    {{ g.approved }} / {{ g.total }}
                                </h5>
                                  <p class="mb-0">
                                    <span class="text-success text-sm font-weight-bolder">{{g.total-g.approved }}</span> remaining
                                  </p>
                            </div>
                        </div>
                        <div class="col-4 text-end">
                            <div class="icon icon-shape bg-gradient-warning shadow-warning text-center rounded-circle">
                                <i class="ni ni-cart text-lg opacity-10" aria-hidden="true"></i>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card mb-4">
                    <div class="card-header pb-0">
                        <div class="row">
                            <div class="col-1">
                                <h6>My Leaves</h6>
                            </div>
                            <div class="col-2">
                                <input v-model="leavesStore.filter.range" class="form-control datepicker" placeholder="Filter" type="text" onfocus="focused(this)" onfocusout="defocused(this)">
                            </div>
                            <div class="col-2 offset-7">
                                <button @click="showForm" class="btn btn-success">Apply Leave </button>
                            </div>
                        </div>
                    </div>
                    <div class="card-body px-0 pt-0 pb-2">
                        <div class="table-responsive p-0">
                            <table class="table align-items-center justify-content-center mb-0">
                            <thead>
                                <tr>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Type</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Created At</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">From</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">To</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Reason</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Status</th>
                                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="leave in leavesStore.list" :key="leave.id">
                                    <td>
                                        <div class="d-flex px-2">
                                        <div class="my-auto">
                                            <h6 class="mb-0 text-sm text-capitalize">{{ leave.leave_type.name }}</h6>
                                        </div>
                                        </div>
                                    </td>
                                    <td>
                                        <p class="text-sm font-weight-bold mb-0">{{ leave.created_at }}</p>
                                    </td>
                                    <td>
                                        <p class="text-sm font-weight-bold mb-0">{{ leave.from_date }}</p>
                                    </td>
                                    <td>
                                        <span class="text-sm font-weight-bold">{{ leave.to_date }}</span>
                                    </td>
                                    <td>
                                        <span class="text-sm font-weight-bold">{{ leave.reason }}</span>
                                    </td>
                                    <td>
                                        <span v-if="leave.status=='APPROVED'" class="badge bg-gradient-success">{{ leave.status }}</span>
                                        <span v-if="leave.status=='PENDING'" class="badge bg-gradient-info">{{ leave.status }}</span>
                                        <span v-if="leave.status=='REJECTED'" class="badge bg-gradient-danger">{{ leave.status }}</span>
                                        <span v-if="leave.status=='CANCELLED'" class="badge bg-gradient-warning">{{ leave.status }}</span>
                                    </td>
                                    
                                    <td class="">
                                      <span v-if="leave.status==='PENDING'">
                                         <button @click="edit(leave)" class="btn btn-success btn-xs m-2">
                                            <i class="fa fa-edit"></i>
                                        </button>
                                        <button @click="cancel(leave)" class="btn btn-danger btn-xs m-2" :class="{'disabled': leave.status == 'CANCELLED'}">
                                            <i class="fa fa-close"></i>
                                        </button>
                                      </span>
                                       <span v-else>N/A</span>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <pagination @updatePageNumber="updatePageNumber" :pagination="leavesStore.pagination"></pagination>
            </div>
        </div>
        <Transition>
            <add-edit-leaves v-if="leavesStore.showLeavesForm"></add-edit-leaves>
        </Transition>
    </div>

</template>

<script setup>
import { onMounted, reactive, watch } from 'vue';
import AddEditLeaves  from './AddEditLeaves.vue'
import { leavesStore } from '../../store/leavesStore';
import Swal from 'sweetalert2';
import { put } from '../../kit';
import pagination from '../pagination.vue';

watch(leavesStore.filter, async (newFilter, oldFilter) => {
 await  leavesStore.getMyLeaves()
})

function showForm(){
    leavesStore.showLeavesForm = true
}

function updatePageNumber(page){
  leavesStore.current_page = page;
  leavesStore.getMyLeaves()
}

function edit(leave) {
    leavesStore.showLeavesForm = true
    leavesStore.form = leave
    leavesStore.form.leave_date = leave.from_date + " to "  + leave.to_date
}

function cancel(leave){
        Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelButtonText: 'Nope',
        confirmButtonText: "Yes, cancel this leave!"
        }).then(async (result) => {
        if (result.isConfirmed) {
            let response = await put(leave.id + '/update/status',{status: "CANCELLED"})
            leavesStore.getMyLeaves()
            if(response.status === 200) {
                Swal.fire({
                title: "Cancelled!",
                text: "Your leave has been cancelled.",
                icon: "success"
                });
            }
        }
        });
}

// async function getMyLeaves() {
//     let response = await post('all')
//     leavesStore.list = response.data
// }

onMounted(() => {
    leavesStore.getMyLeaves()
    leavesStore.getStats()
})

</script>