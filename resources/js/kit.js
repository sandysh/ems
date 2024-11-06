import axios from "axios";
import { errorsStore } from "./store/errorStore";

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
            console.log('errors',error.response.data)
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

export async function notify() {
    let response = await fetch('https://api.onesignal.com/notifications',{
        method: "POST",
        headers: {
            "Authorization": 'Basic MDQ5M2E4MjktOGEwNC00Mzg0LTlkNjQtMDBiNzUwOTE5Zjdk',
            "accept": 'application/json',
            "content-type":'application/json'
        },
        body: {
            "app_id": "567b4ce3-247b-45cf-8999-a943c6a55897",
            "target_channel": "push",
            "contents": {"en": "English Message", "es": "Spanish Message"},
            "included_segments": ["All"]
        }
    })
    // axios.defaults.baseURL = 'https://api.onesignal.com/notifications';
    // axios.defaults.headers.common['Authorization'] = 'Basic MDQ5M2E4MjktOGEwNC00Mzg0LTlkNjQtMDBiNzUwOTE5Zjdk';
    // axios.defaults.headers.post['Content-Type'] = 'application/json';
    // axios.defaults.headers.post['Accept'] = 'application/json';
    // return axios.post('',{
    //   "app_id": "567b4ce3-247b-45cf-8999-a943c6a55897",
    //   "target_channel": "push",
    //   "contents": {"en": "English Message", "es": "Spanish Message"},
    // })
}