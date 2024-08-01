<template>
    <div class="col-md-4">
            <div class="modal fade show" id="modal-form" tabindex="-1" role="dialog" aria-labelledby="modal-form" aria-hidden="true" style="display: block; padding-left: 0px;">
            <div class="modal-dialog modal-dialog-centered modal-md" role="document">
                <div class="modal-content">
                <div class="modal-body p-0">
                    <div class="card card-plain">
                    <div class="card-header pb-0 text-left">
                        <h3 class="font-weight-bolder text-info text-gradient">Apply for leave</h3>
                    </div>
                    <div v-if="errorsStore.show" class="alert alert-danger mx-3" role="alert">
                        <li class="text-white" v-for="(error,index) in errorsStore.list" :key="index">{{ error }}</li>
                    </div>
                    <div class="card-body">
                        <form role="form text-left">
                        <label>Type</label>
                        <div class="input-group mb-3">
                            <select v-model="leavesStore.form.leave_type" class="form-control" name="leave_type" id="" required>
                                <option value="CASUAL">Casual</option>
                                <option value="SICK">Sick</option>
                            </select>
                        </div>
                        <label>Date</label>
                        <div class="input-group mb-3">
                            <input required v-model="leavesStore.form.leave_date" class="form-control datepicker" placeholder="Please select date" type="text" onfocus="focused(this)" onfocusout="defocused(this)">
                        </div>
                        <label for="reason">Reason</label>
                        <div class="input-group">
                            <textarea v-model="leavesStore.form.reason" class="form-control" name="" id="" required></textarea>
                        </div>
                        <div class="text-center">
                            <button @click="leavesStore.form.id ? update() : submit()" type="button" class="btn btn-success m-4">Apply</button>
                            <button @click="cancel" type="button" class="btn btn-danger m-4">Cancel</button>
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
import {onMounted, reactive} from 'vue';
import { get, post, put } from '../../kit.js';
import { leavesStore, snackBarStore, successMessage, errorsStore } from '../../store.js';

async function submit() {
    let response = await post('store',leavesStore.form)
    if (response.data == 'success') {
        successMessage('Leave applied successfully')
        leavesStore.showLeavesForm = false
        leavesStore.form = {
            "leave_type": '',
            "leave_date_range": '',
            "reason": '',
        }
        leavesStore.getMyLeaves()
    }
}

async function update() {
    let response = await put(leavesStore.form.id+'/update', leavesStore.form)
    if(response.status === 200){
        successMessage('Leave updated')
        leavesStore.showLeavesForm = false
        leavesStore.form = {
            "leave_type": '',
            "leave_date_range": '',
            "reason": '',
        }
        leavesStore.getMyLeaves()
    }
}

function cancel() {
    leavesStore.showLeavesForm = false
    leavesStore.form = {
        "leave_type": '',
        "leave_date_range": '',
        "reason": '',
    }
    errorsStore.list = {}
    errorsStore.show = false
}

onMounted(() => {
    flatpickr('.datepicker', {
          mode: "range"
        }); 

})

</script>