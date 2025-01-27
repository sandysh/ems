<template>
  <div class="row">
    <div class="col-12">
      <div class="card mb-4">
        <div class="card-header pb-0">
          <div class="d-flex justify-content-between align-items-center">
            <h6 class="mb-0">Users List</h6>
            <button
              @click="userStore.showUserForm = true"
              type="button"
              class="btn btn-outline-primary btn-sm mb-0"
            >
              Add New User
            </button>
          </div>
        </div>

        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table align-items-center table-striped mb-0">
              <thead>
                <tr>
                  <th
                    class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
                  >
                    Name
                  </th>
                  <th
                    class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
                  >
                    Email
                  </th>
                  <th
                    class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"
                  >
                    Role
                  </th>
                  <th
                    class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
                  >
                    Status
                  </th>
                  <th
                    class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
                  >
                    Action
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(user, index) in users.list"
                  :key="index"
                  v-if="!user.is_superuser"
                >
                  <td>
                    <div class="d-flex px-2 py-1">
                      <img
                        src="/static/img/bg1.jpg"
                        class="avatar avatar-sm me-3"
                        alt="user1"
                      />
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">
                          {{ user.first_name }} {{ user.last_name }}
                        </h6>
                        <p class="text-xs text-secondary mb-0">
                          {{ user.username }}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <p class="text-xs font-weight-bold mb-0">
                      {{ user.email }}
                    </p>
                  </td>
                  <td>
                    <p
                      v-for="group in user.groups"
                      class="text-xs font-weight-bold mb-0"
                    >
                      {{ group.name }}
                    </p>
                  </td>
                  <td class="align-middle text-center text-sm">
                    <div class="custom-control custom-switch">
                      <input
                        @click="updateUserStatus(user)"
                        type="checkbox"
                        class="custom-control-input"
                        :id="'customSwitch' + user.id"
                        :checked="user.is_active"
                      />
                      <label
                        class="custom-control-label"
                        :for="'customSwitch' + user.id"
                      ></label>
                    </div>
                  </td>
                  <td class="align-middle">
                    <div class="d-flex justify-content-center">
                      <a
                        @click="edit(user)"
                        href="javascript:;"
                        class="text-white font-weight-bold text-xs btn btn-info btn-xs mx-2"
                        data-toggle="tooltip"
                        data-original-title="Edit user"
                      >
                        <i class="fa fa-edit"></i>
                      </a>
                      <a
                        @click="deleteUser(user)"
                        href="javascript:;"
                        class="text-white font-weight-bold text-xs btn btn-danger btn-xs mx-2"
                        data-toggle="tooltip"
                        data-original-title="Delete user"
                      >
                        <i class="fa fa-trash"></i>
                      </a>
                      <a
                        @click="updatePassword(user)"
                        href="javascript:;"
                        class="text-white font-weight-bold text-xs btn btn-success btn-xs mx-2"
                        data-toggle="tooltip"
                        data-original-title="Update password"
                      >
                        <i class="fa fa-eye-slash"></i>
                      </a>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <pagination
        @updatePageNumber="updatePageNumber"
        :pagination="workLogs.pagination"
      ></pagination>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import pagination from "../pagination.vue";

const workLogs = reactive({ list: {}, pagination: {} });

// function getWorkLogs() {
//   axios
//     .get(
//       `all?paginate=true&page=${
//         workLogs.pagination.page ? workLogs.pagination.page : 1
//       }`
//     )
//     .then((response) => {
//       workLogs.list = response.data.data;
//       console.log(workLogs.list);
//       workLogs.pagination = response.data.pagination;
//     });
// }

// function updatePageNumber(page) {
//   workLogs.pagination.page = page;
//   getWorkLogs();
// }

onMounted(() => {
  //getWorkLogs();
});
</script>
