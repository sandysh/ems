<template>
  <div class="modal fade show d-block" tabindex="-1" aria-labelledby="modal-title" aria-modal="true" role="dialog">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header border-bottom-0 pb-0">
          <div class="d-flex align-items-center">
            <div class="avatar avatar-lg bg-gradient-primary me-3">
              <span class="text-white text-lg font-weight-bold">
                {{ getInitials(props.data.user.first_name, props.data.user.last_name) }}
              </span>
            </div>
            <div>
              <h5 class="modal-title mb-0" id="modal-title">
                {{ props.data.user.first_name }} {{ props.data.user.last_name }}
              </h5>
              <p class="text-sm text-secondary mb-0">Vote Details</p>
            </div>
          </div>
          <button 
            type="button" 
            class="btn-close" 
            @click="close"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        
        <div class="modal-body py-4">
          <!-- Total Score Section -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="card bg-gradient-success">
                <div class="card-body p-3 text-center">
                  <h2 class="text-white mb-1">{{ sum_total }} pts</h2>
                  <p class="text-white text-sm mb-0 opacity-8">Total Score</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Metrics Section -->
          <div class="mb-4">
            <div class="d-flex align-items-center mb-3">
              <i class="fas fa-chart-bar text-primary me-2"></i>
              <h6 class="mb-0">Metrics Breakdown</h6>
            </div>
            
            <div class="row">
              <div 
                v-for="(metric, index) in props.data.metrices" 
                :key="`metric-${index}`"
                class="col-md-6 mb-3"
              >
                <div class="card border">
                  <div class="card-body p-3">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="text-sm mb-1">{{ metric.name }}</h6>
                        <span class="text-xs text-secondary">Metric</span>
                      </div>
                      <div class="text-end">
                        <span class="badge bg-gradient-primary">
                          {{ getScore(metric.name) }} pts
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Voters Section -->
          <div class="mb-3">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div class="d-flex align-items-center">
                <i class="fas fa-users text-info me-2"></i>
                <h6 class="mb-0">Voters</h6>
              </div>
              <span class="badge bg-gradient-info">
                {{ total_raters }} {{ total_raters === 1 ? 'voter' : 'voters' }}
              </span>
            </div>
            
            <div class="list-group list-group-flush">
              <div 
                v-for="(rate, index) in rated" 
                :key="`rate-${index}`"
                class="list-group-item border-0 px-0 py-2"
              >
                <div class="d-flex align-items-center">
                  <div class="avatar avatar-sm bg-gradient-dark me-3">
                    <span class="text-white text-xs">
                      {{ getInitials(rate.rater.first_name, rate.rater.last_name) }}
                    </span>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="text-sm mb-0">
                      {{ rate.rater.first_name }} {{ rate.rater.last_name }}
                    </h6>
                    <p class="text-xs text-secondary mb-0">
                      Voted on <span class="badge badge-sm bg-gradient-success">{{ rate.metric.name }}</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer border-top-0 pt-0">
          <button 
            @click="close" 
            type="button" 
            class="btn btn-primary"
          >
            <i class="fas fa-times me-2"></i>
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Modal Backdrop -->
  <div class="modal-backdrop fade show" @click="close"></div>
</template>

<script setup>
import { defineProps, computed, defineEmits } from 'vue';

const emit = defineEmits(['close-modal']);
const props = defineProps(['data']);

// Computed properties
const metric_scores = computed(() => props.data.user.metric_scores);
const sum_total = computed(() => props.data.user.sum_total.score);
const rated = computed(() => props.data.user.rated);
const total_raters = computed(() => props.data.user.total_raters.total);

// Helper functions
function getInitials(firstName, lastName) {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
}

function getScore(metric) {
  const index = props.data.user.metric_scores?.findIndex(
    (met_score) => met_score.metric__name === metric
  );
  return index >= 0 ? props.data.user.metric_scores[index].score : 0;
}

function close() {
  emit('close-modal');
}
</script>

<style scoped>
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.avatar-lg {
  width: 60px;
  height: 60px;
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  border: none;
}

.modal-header {
  padding: 1.5rem;
}

.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}

.card {
  border-radius: 10px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.list-group-item {
  background-color: transparent;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.list-group-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.badge {
  font-size: 0.75rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  opacity: 0.7;
}

.btn-close:hover {
  opacity: 1;
}
</style>