<template>
  <div class="col-md-12">
    <div
      class="modal fade show"
      style="display: block"
      id="modal-form"
      tabindex="-1"
      aria-modal="true"
      role="dialog"
      aria-labelledby="modal-form-title"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title" id="modal-form-title">New User Form</h3>
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click.prevent="cancel"
            ></button>
          </div>
          <div class="modal-body">
            <div v-if="errors.show" class="alert alert-danger">
              <ul>
                <li v-for="(error, index) in errors.list" :key="index">
                  {{ error }}
                </li>
              </ul>
            </div>

            <form @submit.prevent="submit">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="first-name" class="form-label">First Name</label>
                  <input
                    v-model="data.first_name"
                    name="first_name"
                    id="first-name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="last-name" class="form-label">Last Name</label>
                  <input
                    v-model="data.last_name"
                    name="last_name"
                    id="last-name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    v-model="data.email"
                    name="email"
                    id="email"
                    class="form-control"
                    type="email"
                    required
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input
                    v-model="data.username"
                    name="username"
                    id="username"
                    class="form-control"
                    type="text"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="groups" class="form-label">Role</label>
                  <select
                    v-model="data.groups"
                    name="groups"
                    id="groups"
                    class="form-select"
                  >
                    <option
                      v-for="role in roles"
                      :key="role.id"
                      :value="role.id"
                    >
                      {{ role.name }}
                    </option>
                  </select>
                </div>

                <div class="col-md-12 mb-3">
                  <div class="form-check">
                    <input
                      v-model="data.is_superuser"
                      name="is_admin"
                      id="is-admin"
                      class="form-check-input"
                      type="checkbox"
                    />
                    <label class="form-check-label" for="is-admin">
                      Admin
                    </label>
                  </div>
                  <div class="form-check">
                    <input
                      v-model="data.is_active"
                      name="is_active"
                      id="is-active"
                      class="form-check-input"
                      type="checkbox"
                    />
                    <label class="form-check-label" for="is-active">
                      Active
                    </label>
                  </div>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-3">
                <button type="submit" class="btn btn-primary">Create</button>
                <button
                  type="button"
                  class="btn btn-secondary"
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
import { reactive, defineProps, defineEmits, onMounted } from "vue";
import { userStore } from "../../store";

const props = defineProps(["data", "roles"]);
const emit = defineEmits(["refresh-table"]);

const errors = reactive({
  list: {},
  show: false,
});

function submit() {
  errors.list = {};
  errors.show = false;
  console.log("fsdfksdjes", props.data);
  axios
    .put(`update/${props.data.id}`, props.data)
    .then(() => {
      userStore.showEditUserForm = false;
      emit("refresh-table");
    })
    .catch((error) => {
      console.log(error);
      errors.list = error.response.data;
      errors.show = true;
    });
}

onMounted(() => {
  console.log("edit user", props.data);
});

function cancel() {
  userStore.showEditUserForm = false;
}
</script>

<style scoped>
.modal-content {
  border-radius: 8px;
}
.modal-header {
  border-bottom: 1px solid #dee2e6;
}
.modal-title {
  font-weight: 600;
}
.btn {
  min-width: 100px;
}
</style>
