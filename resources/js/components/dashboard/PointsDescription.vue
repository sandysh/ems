<script setup>
import { defineProps, computed, isProxy, toRaw, defineEmits } from 'vue';
const emit = defineEmits(['close-modal'])
const props = defineProps(['data'])
const metric_scores = computed(() => {
    return props.data.user.metric_scores
})
const sum_total = computed(() => {
    return props.data.user.sum_total.score
})

const rated = computed(() => {
    return props.data.user.rated
})

const total_raters = computed(() => {
    return props.data.user.total_raters.total
})

function getScore(metric) {
    let index = _.findIndex(props.data.user.metric_scores,(met_score) => {
                    return met_score.metric__name == metric
                })
    if (index >= 0) {
        return props.data.user.metric_scores[index].score
    } else {
        return 0
    }           
}

function close(){
    emit('close-modal')
}
</script>

<template>
    <div class="modal fade show" id="modal-default" tabindex="-1" aria-labelledby="modal-default" style="display: block;" aria-modal="true" role="dialog">
      <div class="modal-dialog modal- modal-dialog-centered modal-" role="document">
         <div class="modal-content">
            <div class="modal-header">
               <h6 class="modal-title" id="modal-title-default">Votes Detail for {{ props.data.user.first_name }} {{ props.data.user.last_name }}</h6>
               <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
               <span aria-hidden="true">×</span>
               </button>
            </div>
            <div class="modal-body">
                <h4>Metrices</h4>
                <ul>
                    <li v-for="(metric,index) in props.data.metrices">{{ metric.name }} -  {{ getScore(metric.name) }}</li>
                </ul>
                
                <span>A total of {{ total_raters }} people voted for you.</span>
                <ul>
                    <li v-for="(rate,index) in rated">{{ rate.rater.first_name }} {{ rate.rater.last_name }} voted you on {{ rate.metric.name }} </li>
                </ul>
            </div>
            <div class="modal-footer">
               <button @click="close" type="button" class="btn btn-primary  ml-auto" data-bs-dismiss="modal">Close</button>
            </div>
         </div>
      </div>
   </div>
</template>