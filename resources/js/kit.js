import axios from "axios";
import { errorsStore } from "./store";

export function get(url) {
    return axios.get(url).then(response => {
        return response;
    }).catch(error => {
       if (error.response.status === 405) {
            errorsStore.list[0] = error.response.statusText
            errorsStore.show = true
        } else {
            errorsStore.list = error.response.data
            errorsStore.show = true
        }
    })
}

export function post(url, payload) {
    return axios.post(url, payload).then(response => {
       return response;
    }).catch(error => {
        if (error.response.status === 405) {
            errorsStore.list[0] = error.response.statusText
            errorsStore.show = true
        } else {
            errorsStore.list = error.response.data
            errorsStore.show = true
        }
    })

}

export function put(url, payload) {
    return axios.put(url, payload).then(response => {
       return response;
    }).catch(error => {
        if (error.response.statusText === 405) {
            errorsStore.list[0] = error.response.statusText
            errorsStore.show = true
        } else {
            errorsStore.list = error.response.data
            errorsStore.show = true
        }
    })

}

export function destroy(url) {
    return axios.delete(url, payload).then(response => {
       return response;
    }).catch(error => {
        if (error.response.statusText === 405) {
            errorsStore.list[0] = error.response.statusText
            errorsStore.show = true
        } else {
            errorsStore.list = error.response.data
            errorsStore.show = true
        }
    })

}