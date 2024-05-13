<template>
    <div>
        <div v-show="alertData.type==='primary'" class="alert alert-primary" role="alert">
            A simple primary alert—check it out!
        </div>

        <div v-show="alertData.type==='success'" class="alert alert-success" role="alert">
            A simple success alert—check it out!
        </div>

        <div v-show="alertData.type==='danger'" class="alert alert-danger" role="alert">
            <ul>
                <li v-if="alertData.errors" v-for="(error,index) in alertData.errors">
                    {{ error[0] }}
                </li>
                <li v-else>
                    {{ alertData.error }}
                </li>
            </ul>
        </div>

        <div v-show="alertData.type==='warning'" class="alert alert-warning" role="alert">
            A simple warning alert—check it out!
        </div>

        <div v-show="alertData.type==='info'" class="alert alert-info" role="alert">
            A simple info alert—check it out!
        </div>
    </div>
</template>

<script setup>
    const props = defineProps(['alertData'])
</script>

<style scoped>

</style>
