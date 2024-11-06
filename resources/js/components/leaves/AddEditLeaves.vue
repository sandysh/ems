<template>
    <div class="col-md-4">
            <div class="modal fade show" id="modal-form" tabindex="-1" role="dialog" aria-labelledby="modal-form" style="display: block; padding-left: 0px;">
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
                            <select v-model="leavesStore.form.leave_type" class="form-select" name="leave_type" id="" required>
                                <option v-for="(type,t) in leavesTypesStores.list" :value="type.id" :key="t">{{ type.name }}</option>
                            </select>
                        </div>
                        <label>Date</label>
                        <div class="input-group mb-3">
                            <input required v-model="leavesStore.form.leave_date_range" class="form-control datepicker" placeholder="Please select date" type="text" onfocus="focused(this)" onfocusout="defocused(this)">
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
import {onMounted,watch} from 'vue';
import { get, post, put, notify } from '../../kit.js';
import { leavesStore} from '../../store/leavesStore';
import { leavesTypesStores } from "../../store/leavesTypesStore";
import {errorsStore} from "../../store/errorStore";
import { successMessage } from "../../store/messageStore";
import moment from "moment";

watch(leavesStore.form, async() => {
    let date_range = leavesStore.form.leave_date_range.split('to')
    let date1 = moment(date_range[0])
    let date2 = moment(date_range[1])
    let diffDays = date2.diff(date1, 'days');
    console.log(diffDays)
})

async function submit() {
    let response = await post('store',leavesStore.form)
    if (response && response.data == 'success') {
        successMessage('Leave applied successfully')
        leavesStore.showLeavesForm = false
        leavesStore.form = {
            "leave_type": '',
            "leave_date_range": '',
            "reason": '',
        }
        notify()
        leavesStore.getMyLeaves()
        leavesStore.getStats()
    }
}

async function update() {
    let response = await put(leavesStore.form.id+'/update', leavesStore.form)
    if(response.status === 200 && response.data.status ==="success"){
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
  leavesTypesStores.getLeavesTypes()
    flatpickr('.datepicker', {
          mode: "range"
        }); 

})

</script>