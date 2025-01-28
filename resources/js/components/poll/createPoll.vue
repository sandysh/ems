<template>
    <div class="modal d-flex justify-content-center align-items-center">
        <div class="bg-white rounded shadow p-4" style="width: 100%; max-width: 400px;">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0">Create Poll</h5>
                <button class="btn-close" @click="closeCreateModal" aria-label="Close"></button>
            </div>
            <div>
                <input v-model="newPoll.name" class="form-control mb-3" placeholder="Poll Name" />
                <textarea v-model="newPoll.description" class="form-control mb-3"
                    placeholder="Poll Description"></textarea>
                <h6 class="mt-3">Options</h6>
                <div v-for="(option, index) in newPoll.options" :key="index" class="d-flex align-items-center mb-2">
                    <input v-model="newPoll.options[index]" class="form-control me-2" placeholder="Option Name" />
                    <button class="btn btn-danger btn-sm" @click="removeOption(index)">Remove</button>
                </div>
                <button class="btn btn-outline-primary btn-sm mt-2" @click="addOption">+ Add Option</button>
            </div>
            <div class="d-flex justify-content-between mt-4">
                <button class="btn btn-primary" :disabled="!isValidForm" @click="createPoll">Create</button>
                <button class="btn btn-primary" @click="closeCreateModal">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, computed, defineEmits } from "vue";

const newPoll = reactive({
    name: "",
    description: "",
    options: [],
});

const emit = defineEmits(["pollCreated", "close-create-poll"]);

function addOption() {
    newPoll.options.push("");
}

function removeOption(index) {
    newPoll.options.splice(index, 1);
}

const isValidForm = computed(() => {
    return (
        newPoll.name.trim() !== "" &&
        newPoll.description.trim() !== "" &&
        newPoll.options.filter((option) => option.trim() !== "").length >= 2
    );
});

async function createPoll() {
    try {
        const response = await axios.post("set_polls", newPoll);
        emit("pollCreated", response.data);
        resetForm();
        closeCreateModal();
    } catch (error) {
        console.error("Error creating poll:", error);
    }
}

function closeCreateModal() {
    resetForm();
    emit("close-create-poll");
}

function resetForm() {
    newPoll.name = "";
    newPoll.description = "";
    newPoll.options = [];
}
</script>
