import { reactive, watch } from "vue";
import { post, put } from "./kit";
import Swal from "sweetalert2";

export const userStore = reactive({
  showUserForm: false,
  showEditUserForm: false,
});
export const settingsUpdate = reactive({
  showSettingForm: false,
  showEditSettingForm: false,
});
export const metricStore = reactive({
  showAddMetricForm: false,
  showEditMetricForm: false,
});

export const projectStore = reactive({
  showProjectForm: false,
  showEditProjectForm: false,
  showAddStatusForm: false,
});

export const snackBarStore = reactive({
  snackbarMessage: "",
});

export const deleteFormStore = reactive({
  showDeleteForm: false,
});

export const errorsStore = reactive({
  list: {},
  show: false,
});

export const successMessage = function (msg) {
  Swal.fire({
    position: "top-end",
    icon: "success",
    title: msg || "Success",
    showConfirmButton: false,
    timer: 1500,
  });
};

export const failedMessage = function (msg) {
  Swal.fire({
    position: "top-end",
    icon: "error",
    title: msg || "Something went wrong, please try again later",
    showConfirmButton: false,
    timer: 1500,
  });
};

export const stausStore = reactive({ list: {} });
