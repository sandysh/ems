import { reactive } from "vue";

export const userStore = reactive({
    showUserForm: false,
    showEditUserForm: false,
})
export const metricStore = reactive({
    showAddMetricForm: false,
    showEditMetricForm: false,
})

export const snackBarStore = reactive({
    snackbarMessage: '',
})

export const deleteFormStore = reactive({
    showDeleteForm: false,
})

export const errorsStore = reactive({
    list:{},show: false
})

