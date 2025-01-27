<template>
  <div>
    <div class="mb-3">
      <label for="settingValue1" class="form-label">Start Time</label>
      <input type="time" class="form-control" id="settingValue1" v-model="start" placeholder="Enter new value"
        required />
    </div>
    <div class="mb-3">
      <label for="settingValue2" class="form-label">Finish Time</label>
      <input type="time" class="form-control" id="settingValue2" v-model="finish" placeholder="Enter new value"
        required />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { defineProps } from "vue";

const props = defineProps({
  editableSetting: {
    type: Object,
    required: true,
  },
});

const start = ref("");
const finish = ref("");

watch(
  () => props.editableSetting,
  (newSetting) => {
    const values = newSetting.values ? newSetting.values.split("-") : ["", ""];
    start.value = values[0].split(" ")[0];
    finish.value = values[1].split(" ")[0];
  },
  { immediate: true }
);

watch([start, finish], () => {

  props.editableSetting.values = `${start.value}-${finish.value}`;
});


</script>
