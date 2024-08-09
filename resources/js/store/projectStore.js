import {reactive, ref} from "vue";
import {get, post, put} from "../kit";
import {deleteFormStore} from "../store";
import {errorsStore} from "../store";

export const projectStore = reactive({
    showAddProjectForm: false,
    showAddStatusForm: false,
    showEditProjectForm: false,
    projects: {list: {}, pagination: {}},
    project: {
        label: '',
        id: null,
        model: ''
    },
    entity: {'status': {'id': 0}},
    filters: {
        searchText: ''
    },

    async getProjects() {
        let response;
        response = await get(`all?paginate=true&page=${projectStore.projects.pagination.page ? projectStore.projects.pagination.page : 1}&searchText=${projectStore.filters.searchText}`);
        if (response) {
            projectStore.projects.list = response.data.data;
            projectStore.projects.pagination = response.data.pagination;
        }
    },

    async showEditForm(project) {
        this.entity = project
        this.showEditProjectForm = true
    },

    async showStatusForm(project) {
        this.entity = project;
        this.showAddStatusForm = true;
    },
    async showDelForm(project) {
        deleteFormStore.showDeleteForm = true
        this.project.label = project.name
        this.project.id = project.id
        this.project.model = 'Project'
    },
    async cancel() {
        this.showEditProjectForm = false
        errorsStore.list = {}
        errorsStore.show = false
    },
    async submit() {
        errorsStore.list = {}
        errorsStore.show = false
        let response;
        response = await put(`update/${this.entity.id}/`, this.entity);
        if (response) {
            projectStore.showEditProjectForm = false
            await this.getProjects();
        }
    },
    data: {
        name: '',
    },
    async statusSubmit() {
        let response;
        response = await post(`add-status/${this.entity.id}/`, this.data);
        if (response) {
            projectStore.showAddStatusForm = false
        }
    },
    async statusCancel() {
        errorsStore.list = {}
        errorsStore.show = false
        projectStore.showAddStatusForm = false;
    },
    projectData: {
        name: '',
        description: '',
        status: ''
    },

    async submitNewProject() {
        let response;
        response = await post('create/', this.projectData);
        if (response) {
            projectStore.showAddProjectForm = false
            await this.getProjects()
        }
    },

    cancelNewProject() {
        projectStore.showAddProjectForm = false;
    },

    allProjects: { list: {}},
    async fetchAllProjects() {
        let response;
        response = await get('/project/all-projects/')
        if (response){
            this.allProjects.list = response.data
        }
    }
})
