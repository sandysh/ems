import { reactive, watch } from "vue";
import { post, put } from "./kit";
import Swal from 'sweetalert2';

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

export const leavesStore = reactive({
    showLeavesForm: false,
    list: {},
    stats: {},
    pagination: {},
    current_page: 1,
    form: {
        "leave_type": '',
        "leave_date_range": '',
        "reason": '',
    },
    filter: {
        range: '',
        status: 'all'
    },
    leave: {
        list:{},
        status: ''
    },
    async getMyLeaves() {
        let response = await post(`all?page=${this.current_page}`, this.filter)
        this.list = response.data.data
        this.pagination = response.data.pagination
    },
    async getStats(){
        let response = await post(`stats`, this.filter)
        console.log('stats', response.data)
        this.stats = response.data
    },
    async updateStatus(leave) {
        let response = await put(`${leave.id}/update/status`, {status:leave.status})
        if (response.data.status === 'success'){
            successMessage(response.data.message)
        }
    }
})

export const successMessage = function(msg){
    Swal.fire({
    position: "top-end",
    icon: "success",
    title: msg || "Success",
    showConfirmButton: false,
    timer: 1500
    });
}

export const failedMessage = function(msg){
    Swal.fire({
    position: "top-end",
    icon: "error",
    title: msg || "Something went wrong, please try again later",
    showConfirmButton: false,
    timer: 1500
    });
}
