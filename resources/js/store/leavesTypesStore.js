import {reactive} from "vue";
import {get} from "../kit"

export const leavesTypesStores = reactive({
    list: {},
    async getLeavesTypes(){
        const response = await get('/leaves-types/all')
        this.list = response.data
    }
})