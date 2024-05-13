import { reactive } from "vue";

export const metricStore = reactive({
    showAddMetricForm: false,
    showDeleteForm: false,
    snackbarMessage: '',
    showEditMetricForm: false,
})
