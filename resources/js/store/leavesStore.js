import {reactive} from "vue";
import {post, put} from "../kit";
import {successMessage, failedMessage} from "../store";
import {errorsStore} from "./errorStore";
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
