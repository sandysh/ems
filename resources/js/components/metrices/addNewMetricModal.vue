<template>
    <div class="col-md-4">
        <div class="modal fade show" style="display: block;" id="modal-form" tabindex="-1" aria-modal="true" role="dialog" aria-labelledby="modal-form"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-body p-0">
                        <div class="card card-plain">
                            <div class="card-header pb-0 text-left">
                                <h3 class="">New User Form</h3>
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
                                            <input v-model="data.name" name="first_name" class="form-control" type="text" value=""
                                                id="first-name">
                                        </div>
                                        <div class="form-group">
                                            <label for="score" class="form-control-label">Score</label>
                                            <input v-model="data.score" name="score" class="form-control" type="number" value=""
                                                id="score">
                                        </div>
                                        <div class="form-check form-switch">
                                            <input v-model="data.is_active" name="is_active" class="form-check-input" type="checkbox"
                                                id="flexSwitchCheckDefault" checked="">
                                            <label class="form-check-label" for="flexSwitchCheckDefault">Active</label>
                                        </div>

                                        <div class="d-flex justify-content-end">
                                            <button @click.prevent="submit" type="button"
                                                class="btn btn-round bg-gradient-info w-20 mt-4 mb-0">Create</button>
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
    import { onMounted, reactive, ref } from 'vue';
    import { metricStore, errorsStore } from '../../store';
    const emit = defineEmits(['refresh-table'])
    import { post } from "../../kit";

    const data = reactive({
        name: '',
        score: '',
        is_active: true
    })

    async function submit() {
        errorsStore.list = {}
        errorsStore.show = false
        let response;
        response = await post('store',data);
        if (response.status === 200) {
            metricStore.showAddMetricForm = false
            emit('refresh-table')
        } else {
            errorsStore.list = response.data
            errorsStore.show = true
        }
    }

    function cancel() {
      errorsStore.list = {}
      errorsStore.show = false
      metricStore.showAddMetricForm = false;
    }

</script>
