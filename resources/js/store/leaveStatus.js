import {reactive} from "vue";

export const leaveStatus = reactive({
    options: [
      { text: 'APPROVED', value: 'APPROVED' },
      { text: 'PENDING', value: 'PENDING' },
      { text: 'REJECTED', value: 'REJECTED' },
      { text: 'CANCELLED', value: 'CANCELLED' },
    ]
})