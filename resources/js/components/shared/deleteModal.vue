<template>
    <div class="modal fade show" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
        style="display: block;" aria-modal="true" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Delete {{ props.data.model }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p>Are you sure, you want to delete <span class="text-danger text-bold">{{ props.data.label }}</span> ?</p>
                </div>
                <div class="modal-footer">
                    <button @click="deleteFormStore.showDeleteForm=false" type="button" class="btn bg-gradient-secondary" data-bs-dismiss="modal">Close</button>
                    <button @click="destroy" type="button" class="btn bg-gradient-danger">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import {deleteFormStore, snackBarStore} from '../../store';
    const props = defineProps(['data']);
    const emit = defineEmits(['refresh-table'])
    function destroy() {
        axios.delete(`${props.data.id}/delete`).then(response => {
            deleteFormStore.showDeleteForm = false;
            emit('refresh-table')
            snackBarStore.snackbarMessage = `${props.data.model} deleted successfully`
        })
    }
</script>