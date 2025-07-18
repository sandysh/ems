<template>
    <div id="leaves">
        <div class="row mb-3">
<!--          <div class="col-12 mb-3">-->
<!--            <input class="col-2 float-end form-control datepicker" placeholder="Please select date" type="text" onfocus="focused(this)" onfocusout="defocused(this)">-->
<!--          </div>-->
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
                                    {{ leavesStore.stats.total_leaves_pending}}
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
                                <p class="text-sm mb-0 text-uppercase font-weight-bold">Total Leave Approved</p>
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
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card mb-4">
                    <div class="card-header">
                        <div class="row">
                            <div class="col-1">
                                <h6>Filter Leaves</h6>
                            </div>
                            <div class="col-2">
                                <input v-model="leavesStore.filter.range" class="form-control datepicker" placeholder="Filter" type="text" onfocus="focused(this)" onfocusout="defocused(this)">
                            </div>
                            <div class="col-2">
                                <div class="form-group">
                                  <select v-model="leavesStore.filter.status" class="form-select" id="exampleFormControlSelect1">
                                    <option value="all">All</option>
                                    <option value="PENDING_SUPERVISOR">Pending Supervisor</option>
                                    <option value="APPROVED">Approved</option>
                                    <option value="PENDING_ADMIN">Pending Admin</option>
                                    <option value="REJECTED">Rejected</option>
                                    <option value="CANCELLED">Cancelled</option>
                                  </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-body px-0 pt-0 pb-2">
                        <div class="table-responsive p-0">
                            <table class="table align-items-center justify-content-center mb-0">
                                <thead>
                                    <tr>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">User</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Type</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">From</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">To</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Reason</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Status</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="leave in leavesStore.list" :key="leave.id">
                                        <td>
                                            <div class="d-flex px-2">
                                              <div class="my-auto">
                                                  <h6 class="mb-0 text-sm text-capitalize">{{ leave.user.first_name }}</h6>
                                              </div>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="d-flex px-2">
                                              <div class="my-auto">
                                                  <h6 class="mb-0 text-sm text-capitalize">{{ leave.leave_type.name }}</h6>
                                              </div>
                                            </div>
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
                                            <span v-if="leave.status=='PENDING_SUPERVISOR'" class="badge bg-gradient-warning">Pending</span>
                                            <span v-if="leave.status=='APPROVED_BY_SUPERVISOR'" class="badge bg-gradient-warning">Approved By Supervisor</span>
                                            <span v-else-if="leave.status=='APPROVED'" class="badge bg-gradient-success">Approved</span>
                                            <span v-else-if="leave.status=='PENDING_ADMIN'" class="badge bg-gradient-info">Awaiting Admin Approval</span>
                                            <span v-else-if="leave.status=='REJECTED'" class="badge bg-gradient-danger">Rejected</span>
                                            <span v-else-if="leave.status=='CANCELLED'" class="badge bg-gradient-secondary">Cancelled</span>
                                        </td>
                                        <td class="">
                                            <div v-if="leave.status === 'APPROVED_BY_SUPERVISOR'|| leave.status === 'PENDING_ADMIN'" class="d-flex gap-1">
                                                <button @click="approveLeave(leave)" class="btn btn-success btn-xs">
                                                    <i class="fa fa-check"></i> Approve
                                                </button>
                                                <button @click="rejectLeave(leave)" class="btn btn-danger btn-xs">
                                                    <i class="fa fa-times"></i> Reject
                                                </button>
                                            </div>
                                            <span v-else>-</span>
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
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { leavesStore } from '../../store/leavesStore';
import { put } from '../../kit';
import Swal from 'sweetalert2';
import pagination from '../pagination.vue';

function approveLeave(leave) {
    Swal.fire({
        title: 'Approve Leave',
        text: 'Add a comment (optional):',
        input: 'textarea',
        inputPlaceholder: 'Enter your comment...',
        showCancelButton: true,
        confirmButtonText: 'Approve',
        confirmButtonColor: '#28a745',
        cancelButtonText: 'Cancel'
    }).then(async (result) => {
        if (result.isConfirmed) {
            const response = await put(`${leave.id}/update/status`, {
                status: 'APPROVED',
                comment: result.value || ''
            });
            
            if (response.status === 200) {
                Swal.fire('Approved!', 'Leave has been approved.', 'success');
                leavesStore.getMyLeaves();
                leavesStore.getStats();
            }
        }
    });
}

function rejectLeave(leave) {
    Swal.fire({
        title: 'Reject Leave',
        text: 'Please provide a reason for rejection:',
        input: 'textarea',
        inputPlaceholder: 'Enter reason for rejection...',
        inputValidator: (value) => {
            if (!value) {
                return 'Please provide a reason for rejection';
            }
        },
        showCancelButton: true,
        confirmButtonText: 'Reject',
        confirmButtonColor: '#dc3545',
        cancelButtonText: 'Cancel'
    }).then(async (result) => {
        if (result.isConfirmed) {
            const response = await put(`${leave.id}/update/status`, {
                status: 'REJECTED',
                comment: result.value
            });
            
            if (response.status === 200) {
                Swal.fire('Rejected!', 'Leave has been rejected.', 'info');
                leavesStore.getMyLeaves();
                leavesStore.getStats();
            }
        }
    });
}

function updatePageNumber(page){
  leavesStore.current_page = page;
  leavesStore.getMyLeaves()
}

onMounted(() => {
    leavesStore.getStats();
    leavesStore.getMyLeaves();
});
</script>