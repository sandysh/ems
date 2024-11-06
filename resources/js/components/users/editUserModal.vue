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
                            <div v-if="errors.show" class="alert alert-danger mx-3" role="alert">
                                <li class="text-white" v-for="(error,index) in errors.list" :key="index">{{ error }}</li>
                            </div>
                            <div class="card-body">
                                <form action="" method="post" autocomplete="false">
                                    <div class="card-body px-0 pt-0 pb-2">
                                        <div class="form-group">
                                            <label for="first name" class="form-control-label">First Name</label>
                                            <input v-model="data.first_name" name="first_name" class="form-control" type="text" value=""
                                                id="first-name">
                                        </div>
                                        <div class="form-group">
                                            <label for="last name" class="form-control-label">last Name</label>
                                            <input v-model="data.last_name" name="last_name" class="form-control" type="text" value=""
                                                id="last-name">
                                        </div>
                                        <div class="form-group">
                                            <label for="example-email-input" class="form-control-label">Email</label>
                                            <input v-model="data.email" name="email" class="form-control" type="email" value=""
                                                id="example-email-input">
                                        </div>
                                        <div class="form-group">
                                            <label for="username" class="form-control-label">Username</label>
                                            <input v-model="data.username" name="username" class="form-control" type="text" value=""
                                                id="username">
                                        </div>
                                        <div class="form-check form-switch pb-2">
                                            <input v-model="data.is_superuser" name="is_admin" class="form-check-input" type="checkbox"
                                                id="flexSwitchCheckDefault">
                                            <label class="form-check-label" for="flexSwitchCheckDefault">Admin</label>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input v-model="data.is_active" name="is_active" class="form-check-input" type="checkbox"
                                                id="flexSwitchCheckDefault1" checked="">
                                            <label class="form-check-label" for="flexSwitchCheckDefault1">Active</label>
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
    import { userStore } from '../../store';
    const emit = defineEmits(['refresh-table'])
    const errors = reactive({list:{},show: false})
    const props = defineProps(['data'])
    function submit() {
        errors.list = {}
        errors.show = false
        axios.put(`update/${props.data.id}`,props.data).then(response => {
            userStore.showEditUserForm = false
            emit('refresh-table')
            // console.log('msg',response.data)
        }).catch(error => {
            console.log('errors',error.response.data)
            errors.list = error.response.data
            errors.show = true
        })
    }

    function cancel() {
        userStore.showEditUserForm = false;
    }

</script>
