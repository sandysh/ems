<template>
    <div class="container mt-4 text-end">
        <button class="btn btn-primary" @click="showCreatePoll = true">Create Poll</button>
    </div>
    <div>
        <div class="container self-style mt-5">
            <div class="grid-container">
                <div :key="index" class="grid-item" v-for="(poll, index) in polls.list">
                    <div class="card mb-3">
                        <div class="card-header">
                            <div class="card-title">
                                <p class="fs-3 text-uppercase font-weight-bold mb-1">{{ poll.name }}</p>
                                <p class="text-ss text-uppercase font-weight-bold mb-1">{{ poll.created_by.first_name +
                                    " "
                                    + poll.created_by.last_name }}</p>
                                <p class="fs-5 text-uppercase font-weight-bold mb-1">{{ poll.timestamp }}</p>

                            </div>
                            <hr>
                        </div>
                        <div class="card-body">
                            <div class="progress" style="height: 25px;">
                                <div id="progress-bar" class="progress-bar" role="progressbar" style="width: 0%;"
                                    aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                                    0%
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div v-if="showCreatePoll" class="modal-backdrop" @click.self="closeCreateModal">
        <createPoll @close-create-poll="closeCreateModal" @pollCreated="addPoll"></createPoll>
    </div>

    <snack-bar v-show="snackBarStore.snackbarMessage !== ''"></snack-bar>
</template>

<style scoped>
.card {
    box-sizing: border-box;
    border-radius: 12px;
    width: 280px;
    height: 200px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.card-header {
    display: flex;
    justify-content: space-between;
    padding: 12px;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
</style>

<script setup>
import { ref, reactive, onMounted } from "vue";
import snackBar from "../shared/snackBar.vue";
import { snackBarStore } from "../../store.js";
import createPoll from "./createPoll.vue";

const polls = reactive({ list: [] });
const showCreatePoll = ref(false);

async function getPolls() {
    try {
        const response = await axios.get("get_polls");
        polls.list = response.data;

    } catch (error) {
        console.error("Error fetching polls:", error);
        snackBarStore.showSnackbar("Failed to load polls.", "error");
    }
}

function closeCreateModal() {
    showCreatePoll.value = false;
}

function addPoll(newPoll) {
    polls.list.unshift(newPoll);
}

onMounted(() => {
    getPolls();
});
</script>
