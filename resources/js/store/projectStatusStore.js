import {reactive} from "vue";
import {get} from "../kit";

export const projectStatusStore = reactive({
    list: {},
    async statusData(id) {
      let response = await get(`/project/status/${id}/`);
      if (response) {
        this.list = JSON.parse(response.data);
      }
    }
})