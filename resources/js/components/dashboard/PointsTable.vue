<template>
  <div class="row mt-4">
    <!-- Points Activities Section -->
    <div class="col-lg-7 mb-lg-0 mb-4">
      <div class="card">
        <div class="card-header pb-0 p-3">
          <div class="d-flex justify-content-between align-items-center">
            <h6 class="mb-0">Points Activities ({{ selectedPeriod1 }})</h6>
            <div class="dropdown">
              <button 
                class="btn btn-outline-primary btn-sm dropdown-toggle" 
                type="button" 
                @click="toggleDropdown1"
                :aria-expanded="dropdown1Open"
              >
                {{ selectedPeriod1 }}
              </button>
              <ul class="dropdown-menu" :class="{'show': dropdown1Open}">
                <li><a class="dropdown-item" @click.prevent="changePeriod1('Weekly')" href="#">Weekly</a></li>
                <li><a class="dropdown-item" @click.prevent="changePeriod1('Monthly')" href="#">Monthly</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table align-items-center mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Rater</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Action</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Rated</th>
                  <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Metric</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(rating, index) in points.data.ratings" :key="`rating-${index}`">
                  <td class="px-3 py-2">
                    <div class="d-flex align-items-center">
                      <div class="avatar avatar-sm me-3">
                        <div class="avatar-name">{{ getInitials(rating.rater.first_name, rating.rater.last_name) }}</div>
                      </div>
                      <div>
                        <h6 class="text-sm mb-0">{{ rating.rater.first_name }} {{ rating.rater.last_name }}</h6>
                      </div>
                    </div>
                  </td>
                  <td class="px-3 py-2">
                    <span class="text-secondary text-xs">voted</span>
                  </td>
                  <td class="px-3 py-2">
                    <span class="text-sm font-weight-bold">{{ rating.rated.first_name }} {{ rating.rated.last_name }}</span>
                  </td>
                  <td class="px-3 py-2">
                    <span class="badge badge-sm bg-gradient-success">{{ rating.metric.name }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Points Table Section -->
    <div class="col-lg-5">
      <div class="card">
        <div class="card-header pb-0 p-3">
          <div class="d-flex justify-content-between align-items-center">
            <h6 class="mb-0">Points Table ({{ selectedPeriod2 }})</h6>
            <div class="dropdown">
              <button 
                class="btn btn-outline-primary btn-sm dropdown-toggle" 
                type="button" 
                @click="toggleDropdown2"
                :aria-expanded="dropdown2Open"
              >
                {{ selectedPeriod2 }}
              </button>
              <ul class="dropdown-menu" :class="{'show': dropdown2Open}">
                <li><a class="dropdown-item" @click.prevent="changePeriod2('Weekly')" href="#">Weekly</a></li>
                <li><a class="dropdown-item" @click.prevent="changePeriod2('Monthly')" href="#">Monthly</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="card-body p-3">
          <div class="list-group list-group-flush">
            <div 
              v-for="(user, index) in points.data.users" 
              :key="`user-${index}`"
              class="list-group-item border-0 d-flex justify-content-between align-items-center ps-0 mb-2 border-radius-lg"
            >
              <div class="d-flex align-items-center flex-grow-1">
                <div class="position-relative me-3">
                  <div class="avatar avatar-sm bg-gradient-dark">
                    <span class="text-white text-xs">{{ getInitials(user.first_name, user.last_name) }}</span>
                  </div>
                  <div class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-success">
                    {{ index + 1 }}
                  </div>
                </div>
                <div class="flex-grow-1">
                  <h6 class="mb-1 text-dark text-sm">
                    {{ user.first_name }} {{ user.last_name }}
                    <span class="badge bg-gradient-primary ms-2">{{ user.sum_total.score }} pts</span>
                  </h6>
                  <span class="text-xs text-secondary">
                    <i class="fas fa-users me-1"></i>
                    {{ user.total_raters.total }} {{ user.total_raters.total === 1 ? 'voter' : 'voters' }}
                  </span>
                </div>
              </div>
              <div class="d-flex align-items-center">
                <button 
                  @click="showModal(user)" 
                  class="btn btn-link btn-icon-only btn-rounded btn-sm text-dark my-auto"
                  :title="`View details for ${user.first_name} ${user.last_name}`"
                >
                  <i class="ni ni-bold-right" aria-hidden="true"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Component -->
    <Teleport to="body">
      <points-description 
        @close-modal="closeModal" 
        v-if="modal.show" 
        :data="modalData"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from 'vue';
import PointsDescription from './PointsDescription.vue';

// Reactive state
const points = reactive({ data: { ratings: [], users: [], metrices: [] } });
const modalData = reactive({ user: {}, metrices: [] });
const modal = reactive({ show: false });
const selectedPeriod1 = ref('Weekly');
const selectedPeriod2 = ref('Weekly');
const dropdown1Open = ref(false);
const dropdown2Open = ref(false);
const isLoading = ref(false);

// Computed properties
const hasRatings = computed(() => points.data.ratings?.length > 0);
const hasUsers = computed(() => points.data.users?.length > 0);

// Helper functions
function getInitials(firstName, lastName) {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
}

// API functions
async function getPoints() {
  try {
    isLoading.value = true;
    const response = await fetch(`points?period1=${selectedPeriod1.value.toLowerCase()}&period2=${selectedPeriod2.value.toLowerCase()}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch points data');
    }
    
    const data = await response.json();
    points.data = data.data || { ratings: [], users: [], metrices: [] };
  } catch (error) {
    console.error('Error fetching points:', error);
    // Handle error appropriately
  } finally {
    isLoading.value = false;
  }
}

// Event handlers
function changePeriod1(period) {
  selectedPeriod1.value = period;
  dropdown1Open.value = false;
  getPoints();
}

function changePeriod2(period) {
  selectedPeriod2.value = period;
  dropdown2Open.value = false;
  getPoints();
}

function toggleDropdown1() {
  dropdown1Open.value = !dropdown1Open.value;
  dropdown2Open.value = false;
}

function toggleDropdown2() {
  dropdown2Open.value = !dropdown2Open.value;
  dropdown1Open.value = false;
}

function showModal(user) {
  modal.show = true;
  modalData.user = user;
  modalData.metrices = points.data.metrices;
}

function closeModal() {
  modal.show = false;
}

// Lifecycle
onMounted(async () => {
  await getPoints();
});
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
  color: black;
}

.avatar-name {
  font-size: 0.75rem;
}

.dropdown-menu {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.list-group-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
  transition: background-color 0.2s ease;
}

.badge {
  font-size: 0.75rem;
}

.table th {
  border-bottom: 1px solid #dee2e6;
  padding: 0.75rem;
  
}

.table td {
  border-bottom: 1px solid #f8f9fa;
  vertical-align: middle;
}
</style>