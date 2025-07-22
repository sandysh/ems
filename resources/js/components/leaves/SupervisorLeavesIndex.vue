<template>
    <div id="supervisor-leaves">
        <div class="row mb-3">
            <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
                <div class="card">
                    <div class="card-body p-3">
                        <div class="row">
                            <div class="col-8">
                                <div class="numbers">
                                    <p class="text-sm mb-0 text-uppercase font-weight-bold">Pending My Review</p>
                                    <h5 class="font-weight-bolder">
                                        {{ leavesStore.stats.pending_supervisor }}
                                    </h5>
                                </div>
                            </div>
                            <div class="col-4 text-end">
                                <div class="icon icon-shape bg-gradient-warning shadow-warning text-center rounded-circle">
                                    <i class="ni ni-time-alarm text-lg opacity-10" aria-hidden="true"></i>
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
                                    <p class="text-sm mb-0 text-uppercase font-weight-bold">Approved by Me</p>
                                    <h5 class="font-weight-bolder">
                                        {{ leavesStore.stats.approved_by_supervisor }}
                                    </h5>
                                </div>
                            </div>
                            <div class="col-4 text-end">
                                <div class="icon icon-shape bg-gradient-success shadow-success text-center rounded-circle">
                                    <i class="ni ni-check-bold text-lg opacity-10" aria-hidden="true"></i>
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
                                    <p class="text-sm mb-0 text-uppercase font-weight-bold">Escalated to Admin</p>
                                    <h5 class="font-weight-bolder">
                                        {{ leavesStore.stats.escalated_to_admin }}
                                    </h5>
                                </div>
                            </div>
                            <div class="col-4 text-end">
                                <div class="icon icon-shape bg-gradient-danger shadow-danger text-center rounded-circle">
                                    <i class="ni ni-send text-lg opacity-10" aria-hidden="true"></i>
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
                        <div class="row align-items-center">
                            <div class="col">   
                                <h6 class="mb-0">Leave Applications for Review</h6>
                            </div>
                            <div class="col-auto d-flex gap-2">
                                <button
                                    class="btn btn-primary"
                                    :class="{'active': leavesStore.filter.only_mine}"
                                    @click="setOnlyMine"
                                >
                                    My Leaves
                                </button>
                                <button
                                    class="btn btn-secondary"
                                    :class="{'active': !leavesStore.filter.only_mine}"
                                    @click="setSupervised"
                                >
                                    Supervised Leaves
                                </button>
                                <button @click="showForm" class="btn btn-success">Apply Leave</button>
                            </div>
                        </div>
                    </div>
                    <div class="card-body px-0 pt-0 pb-2">
                        <div class="table-responsive p-0">
                            <table class="table align-items-center justify-content-center mb-0">
                                <thead>
                                    <tr>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Employee</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Type</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">From</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">To</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Reason</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="leave in leavesStore.list" :key="leave.id">
                                        <td>
                                            <div class="d-flex px-2">
                                                <div class="my-auto">
                                                    <h6 class="mb-0 text-sm text-capitalize">{{ leave.user.first_name }} {{ leave.user.last_name }}</h6>
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
                                            <span v-if="leave.status=='PENDING_SUPERVISOR'" class="badge bg-gradient-warning">Pending Review</span>
                                            <span v-else-if="leave.status=='APPROVED'" class="badge bg-gradient-success">Approved</span>
                                            <span v-else-if="leave.status=='APPROVED_BY_SUPERVISOR'" class="badge bg-gradient-success">Approved</span>
                                            <span v-else-if="leave.status=='REJECTED'" class="badge bg-gradient-info">Rejected</span>
                                            <span v-else-if="leave.status=='PENDING_ADMIN'" class="badge bg-gradient-info">Awaiting Admin Approval</span>
                                            <span v-else class="badge bg-gradient-secondary">{{ leave.status }}</span>
                                        </td>
                                        <td>
                                            <div v-if="leave.status === 'PENDING_SUPERVISOR'" class="d-flex gap-1">
                                                <button @click="approveLeave(leave)" class="btn btn-success btn-xs">
                                                    <i class="fa fa-check"></i> Approve
                                                </button>
                                                <button @click="rejectLeave(leave)" class="btn btn-danger btn-xs">
                                                    <i class="fa fa-times"></i> Reject
                                                </button>
                                            </div>
                                            <span v-else>N/A</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <Transition>
            <add-edit-leaves v-if="leavesStore.showLeavesForm"></add-edit-leaves>
        </Transition>
    </div>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { leavesStore } from '../../store/leavesStore';
import { put } from '../../kit';
import Swal from 'sweetalert2';
import AddEditLeaves  from './AddEditLeaves.vue'

watch(leavesStore.filter, async (newFilter, oldFilter) => {
 await  leavesStore.getMyLeaves()
})

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
                status: 'APPROVED_BY_SUPERVISOR',
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
        text: 'This will escalate to admin. Please provide a reason:',
        input: 'textarea',
        inputPlaceholder: 'Enter reason for rejection...',
        inputValidator: (value) => {
            if (!value) {
                return 'Please provide a reason for rejection';
            }
        },
        showCancelButton: true,
        confirmButtonText: 'Reject & Escalate',
        confirmButtonColor: '#dc3545',
        cancelButtonText: 'Cancel'
    }).then(async (result) => {
        if (result.isConfirmed) {
            const response = await put(`${leave.id}/update/status`, {
                status: 'REJECTED_BY_SUPERVISOR',
                comment: result.value
            });
            
            if (response.status === 200) {
                Swal.fire('Rejected!', 'Leave has been rejected and escalated to admin.', 'info');
                leavesStore.getMyLeaves();
                leavesStore.getStats();
            }
        }
    });
}

function setOnlyMine() {
    leavesStore.filter.only_mine = true;
    leavesStore.current_page = 1;
    // leavesStore.getMyLeaves();
}

function setSupervised() {
    leavesStore.filter.only_mine = false;
    leavesStore.current_page = 1;
    // leavesStore.getMyLeaves();
}


function showForm(){
    leavesStore.showLeavesForm = true
}

onMounted(() => {
    leavesStore.getMyLeaves();
    leavesStore.getStats();
});
</script>