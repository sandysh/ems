import { reactive } from "vue";
import { store } from "../store";
import {get} from "../kit";

export const userStore = reactive({
    editableUser: {},
    allUsers : {list: {}},

    async FetchAllUser(){
        let response;
        response = await get('/users/all-users/')
        if (response){
            this.allUsers.list = response.data
        }
    }
})