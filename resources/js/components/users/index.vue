<template>
  <div class="row">
    <div class="col-12">
      <div class="card mb-4">
        <div class="card-header pb-0">
          <div class="d-flex align-items-center">
            <h6 class="mb-0">Users List</h6>
          </div>
          <div class="text-end">
            <button @click="userStore.showUserForm = true" type="button" class="btn btn-outline-primary btn-sm mb-0">Add New User</button>
          </div>
        </div>
        <div class="card-body px-0 pt-0 pb-2">
          <div class="table-responsive p-0">
            <table class="table align-items-center mb-0">
              <thead>
                <tr>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Name</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Email</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Role</th>
                  <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Status</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, index) in users.list" :key="index">
                  <td>
                    <div class="d-flex px-2 py-1">
                      <div>
                        <img src="/static/img/bg1.jpg" class="avatar avatar-sm me-3" alt="user1">
                      </div>
                      <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">{{ user.first_name }} {{ user.last_name }}</h6>
                        <p class="text-xs text-secondary mb-0">{{ user.username }}</p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <p class="text-xs font-weight-bold mb-0">{{ user.email }}</p>
                  </td>
                  <td>
                    <p v-if="user.is_superuser" class="text-xs font-weight-bold mb-0">Admin</p>
                    <p v-else class="text-xs font-weight-bold mb-0">User</p>
                  </td>
                  <td class="align-middle text-center text-sm">
                    <div class="custom-control custom-switch">
                      <input @click="updateUserStatus(user)" type="checkbox" class="custom-control-input" :id="'customSwitch'+user.id" :checked="user.is_active">
                      <label class="custom-control-label" :for="'customSwitch'+user.id"></label>
                    </div>
<!--                    <span v-if="user.is_active" class="badge badge-sm bg-gradient-success">Active</span>-->
<!--                    <span v-else class="badge badge-sm bg-gradient-secondary">Suspended</span>-->
                  </td>
                  <td class="align-middle">
                    <a @click="edit(user)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-info btn-xs mx-2"
                      data-toggle="tooltip" data-original-title="Edit user">
                      <i class="fa fa-edit"></i>
                    </a>
                    <a @click="deleteUser(user)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-danger btn-xs"
                      data-toggle="tooltip" data-original-title="Edit user">
                      <i class="fa fa-trash"></i>
                    </a>
                    <a @click="updatePassword(user)" href="javascript:;" class="text-white font-weight-bold text-xs btn btn-success btn-xs mx-2"
                      data-toggle="tooltip" data-original-title="Edit user">
                      <i class="fa fa-eye-slash"></i>
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <pagination @updatePageNumber="updatePageNumber" :pagination="users.pagination"></pagination>
    </div>
    <delete-modal :data="user" @refresh-table="getUsers" v-show="deleteFormStore.showDeleteForm"></delete-modal>
    <add-new-user-modal :entity="entity" @refresh-table="getUsers" v-show="userStore.showUserForm"></add-new-user-modal>
    <edit-user-modal :data="entity"  @refresh-table="getUsers" v-show="userStore.showEditUserForm"></edit-user-modal>
    <snack-bar v-show="snackBarStore.snackbarMessage!==''"></snack-bar>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import addNewUserModal from './addNewUserModal.vue';
import editUserModal from './editUserModal.vue';
import deleteModal from '../shared/deleteModal.vue';
import snackBar from '../shared/snackBar.vue';
import pagination from '../pagination.vue';
import Swal from "sweetalert2";
import {post} from "../../kit";

import {userStore, snackBarStore, deleteFormStore, errorsStore} from '../../store.js';
const users = reactive({ list: {}, pagination:{}});
const user = ref({
  label: '',
  id: null,
  model: ''
})
const entity = ref({})
const editableUser = ref({})

async function updateUserStatus(user) {
    let response = await post(`update/${user.id}/status`)
}

function getUsers() {
  axios.get(`all?paginate=true&page=${users.pagination.page ? users.pagination.page : 1 }`).then(response => {
    users.list = response.data.data
    users.pagination = response.data.pagination
  })
}

async function updatePassword(user) {
  const {value: formValues} = await Swal.fire({
    title: `Update "${user.username}'s" password`,
    html: `
    <input id="new-password" class="form-control" placeholder="new password">
    <input id="confirm-password" class="form-control" placeholder="confirm new password">
  `,
    focusConfirm: false,
    confirmButtonText: 'Update Now',
    preConfirm: () => {
      return [
        document.getElementById("new-password").value,
        document.getElementById("confirm-password").value
      ];
    }
  })
  if (formValues) {
    let values = {new_password:formValues[0], confirm_password: formValues[1]}
    console.log(values)
    axios.put(`update/${user.id}/password`, values).then(response => {
      if (response.data.status === 'success') {
        Swal.fire({
          position: "top-end",
          icon: "success",
          title: response.data.message || "Password has been successfully updated",
          showConfirmButton: false,
          timer: 1500
        });
      } else {
        Swal.fire({
          position: "top-end",
          icon: "warning",
          title: response.data.message || "Something went wrong, please try again later",
          showConfirmButton: false,
          timer: 1500
        });
      }
    }).catch(error => {
            Swal.fire({
            position: "top-end",
            icon: "warning",
            title: error.response.data || "Something went wrong, please try again later",
            showConfirmButton: false,
            timer: 1500
          });
      })
  }
}

function updatePageNumber(page){
  users.pagination.page = page;
  getUsers();
}

function addSnackMessage(message){
  message = messsage
}

function deleteUser(user){
  deleteFormStore.showDeleteForm = true
  this.user.label = user.username
  this.user.id = user.id
  this.user.model = 'User'
}

function edit(user) {
  userStore.showEditUserForm = true
  this.entity = user
}


onMounted(() => {
  getUsers();
  // authenticate();
})

</script>
