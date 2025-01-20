<template>
  <div class="col-md-12 col-lg-6">
    <div
      class="modal fade show"
      style="display: block"
      id="modal-form"
      tabindex="-1"
      aria-modal="true"
      role="dialog"
      aria-labelledby="modal-form"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title" id="modal-form">New User Form</h3>
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click.prevent="cancel"
            ></button>
          </div>
          <div class="modal-body">
            <div v-if="errorsStore.show" class="alert alert-danger">
              <ul>
                <li v-for="(error, index) in errorsStore.list" :key="index">
                  {{ error }}
                </li>
              </ul>
            </div>
            <form @submit.prevent="submit">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="first-name" class="form-label">First Name</label>
                  <input
                    v-model="data.list.first_name"
                    id="first-name"
                    name="first_name"
                    type="text"
                    class="form-control"
                    placeholder="Enter first name"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="last-name" class="form-label">Last Name</label>
                  <input
                    v-model="data.list.last_name"
                    id="last-name"
                    name="last_name"
                    type="text"
                    class="form-control"
                    placeholder="Enter last name"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    v-model="data.list.email"
                    id="email"
                    name="email"
                    type="email"
                    class="form-control"
                    placeholder="Enter email"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input
                    v-model="data.list.username"
                    id="username"
                    name="username"
                    type="text"
                    class="form-control"
                    placeholder="Enter username"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input
                    v-model="data.list.password"
                    id="password"
                    name="password"
                    type="password"
                    class="form-control"
                    placeholder="Enter password"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="role" class="form-label">Role</label>
                  <select
                    v-model="data.list.group"
                    id="role"
                    name="role"
                    class="form-select"
                  >
                    <option disabled value="">Select role</option>
                    <option
                      v-for="role in roles"
                      :key="role.id"
                      :value="role.id"
                      selected
                    >
                      {{ role.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6 mb-3 form-check form-switch">
                  <input
                    v-model="data.list.is_superuser"
                    id="is_superuser"
                    name="is_superuser"
                    class="form-check-input"
                    type="checkbox"
                  />
                  <label class="form-check-label" for="is_superuser"
                    >Admin</label
                  >
                </div>
                <div class="col-md-6 mb-3 form-check form-switch">
                  <input
                    v-model="data.list.is_active"
                    id="is_active"
                    name="is_active"
                    class="form-check-input"
                    type="checkbox"
                  />
                  <label class="form-check-label" for="is_active">Active</label>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button type="submit" class="btn btn-success w-25 mt-4">
                  Create
                </button>
                <button
                  type="button"
                  class="btn btn-secondary w-25 mt-4"
                  @click.prevent="cancel"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { userStore, errorsStore } from "../../store";

const emit = defineEmits(["refresh-table"]);
const { props } = defineProps(["roles"]);

const data = reactive({
  list: {
    first_name: "",
    last_name: "",
    email: "",
    username: "",
    password: "",
    group: "",
    is_superuser: false,
    is_active: true,
  },
});

function submit() {
  errorsStore.list = {};
  errorsStore.show = false;

  axios
    .post("store", data.list)
    .then(() => {
      data.list = {
        first_name: "",
        last_name: "",
        email: "",
        username: "",
        password: "",
        group: "",
        is_superuser: false,
        is_active: true,
      };
      userStore.showUserForm = false;
      emit("refresh-table");
    })
    .catch((error) => {
      errorsStore.list = error.response?.data || [];
      errorsStore.show = true;
    });
}

function cancel() {
  data.list = {
    first_name: "",
    last_name: "",
    email: "",
    username: "",
    password: "",
    group: "",
    is_superuser: false,
    is_active: true,
  };
  userStore.showUserForm = false;
}
</script>

<style scoped>
.modal-content {
  border-radius: 8px;
}
.modal-header {
  border-bottom: 1px solid #dee2e6;
  background-color: #f7f7f7;
}
.modal-title {
  font-weight: 600;
  color: #333;
}
.card-body {
  padding: 20px;
}
.form-label {
  font-weight: bold;
}
.form-check-input {
  margin-top: 0.3rem;
}
.d-flex .btn {
  min-width: 120px;
}
</style>
