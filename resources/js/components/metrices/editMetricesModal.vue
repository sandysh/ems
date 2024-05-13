<template>
    <div class="col-md-4">
        <div class="modal fade show" style="display: block;" id="modal-form" tabindex="-1" aria-modal="true" role="dialog" aria-labelledby="modal-form"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-body p-0">
                        <div class="card card-plain">
                            <div class="card-header pb-0 text-left">
                                <h3 class="">Edit Metric Form</h3>
                                <hr class="border border-default border-1">
                            </div>
                            <div v-if="errorsStore.show" class="alert alert-danger mx-3" role="alert">
                                <li class="text-white" v-for="(error,index) in errorsStore.list" :key="index">{{ error }}</li>
                            </div>
                            <div class="card-body">
                                <form action="" method="post" autocomplete="false">
                                    <div class="card-body px-0 pt-0 pb-2">
                                        <div class="form-group">
                                            <label for="first name" class="form-control-label">Name</label>
                                            <input v-model="props.data.name" name="first_name" class="form-control" type="text" value=""
                                                id="first-name">
                                        </div>
                                        <div class="form-group">
                                            <label for="score" class="form-control-label">Score</label>
                                            <input v-model="props.data.score" name="score" class="form-control" type="number" value=""
                                                id="score">
                                        </div>
                                        <div class="form-check form-switch">
                                            <input v-model="props.data.is_active" name="is_active" class="form-check-input" type="checkbox"
                                                id="flexSwitchCheckDefault" checked="">
                                            <label class="form-check-label" for="flexSwitchCheckDefault">Active</label>
                                        </div>

                                        <div class="d-flex justify-content-end">
                                            <button @click.prevent="submit" type="button"
                                                class="btn btn-round bg-gradient-info w-20 mt-4 mb-0">Update</button>
                                            <button @click.prevent="cancel" type="button"
                                                class="btn btn-round bg-gradient-danger w-20 mt-4 mb-0">Cancel</button>
                                        </div>
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
    import { reactive } from 'vue';
    import { metricStore, errorsStore } from '../../store';
    const emit = defineEmits(['refresh-users'])
    import { put } from "../../kit";
    const props = defineProps(['data'])

    async function submit() {
        errorsStore.list = {}
        errorsStore.show = false
        let response;
        response = await put(`${props.data.id}/update`,props.data);
        if (response.status === 200) {
            metricStore.showEditMetricForm = false
            emit('refresh-table')
        }
    }

    function cancel() {
        metricStore.showEditMetricForm = false;
        errorsStore.list = {}
        errorsStore.show = false
    }

</script>
