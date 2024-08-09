import {reactive, ref} from "vue";
import {get, post, put} from "../kit";
import {deleteFormStore} from "../store";
import {errorsStore} from "../store";

export const taskStore = reactive({
    showAddTaskForm: false,
    showEditTaskForm: false,
    showViewTask: false,
    tasks: {list: {}, pagination: {}},
    task: {
        label: '',
        id: null,
        model: ''
    },
    entity: {'status': {'id': 0}},
    filters: {
        searchText: ''
    },

    async gettasks() {
        let response;
        response = await get(`all?paginate=true&page=${taskStore.tasks.pagination.page ? taskStore.tasks.pagination.page : 1}&searchText=${taskStore.filters.searchText}`);
        if (response) {
            taskStore.tasks.list = response.data.data;
            taskStore.tasks.pagination = response.data.pagination;
        }
    },

    async showEditForm(task) {
        this.entity = task
        this.showEditTaskForm = true
    },

    taskData: {
        title: '',
        description: '',
        project: '',
        status: '',
        assign_to: '',
        start_time: '',
        end_time: '',
        attachments: {list: {}}
    },

    cancelNewTask() {
        this.showAddTaskForm = false;
    },
    cancelTaskDetails(){
        this.showViewTask = false;
    },
    cancelEditTask(){
        this.showEditTaskForm = false;
    },
    async viewClick(task){
        this.entity = task;
        this.showViewTask = true;
    },

    async deleteTask(task){
        deleteFormStore.showDeleteForm = true;
        this.task.label = task.title
        this.task.id = task.id
        this.task.model = 'Task'
    }
})