<template>
    <div>
        <button @click="increment" style="border:2px solid; padding: 2px">{{ state.count }}</button>
    <ul>
        <li v-for="(user,index) in data.users" :key="index">{{ user.name}} </li>
    </ul>
    </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';

const state = reactive({count: 0, msg: 'test'})
const data = reactive({users: []});
function increment() {
    state.count++;
}

function getUsers()
{
    axios.get('/users')
        .then(response => {
            this.data.users = response.data.users
        })
}

onMounted(()=>{
    getUsers()
    console.log('working');
});

</script>

<style scoped>

</style>
