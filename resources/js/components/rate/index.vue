<template>
    <div class="row">
        <!-- Leaderboard Section -->
        <div class="col-12 mb-4">
            <div class="card">
                <div class="card-header pb-0 p-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">
                            <i class="fas fa-trophy text-warning me-2"></i>
                            Leaderboard
                        </h6>
                        <button 
                            @click="getLeaderboard" 
                            class="btn btn-outline-primary btn-sm"
                            :disabled="isLoading"
                        >
                            <i class="fas fa-sync-alt me-2" :class="{'fa-spin': isLoading}"></i>
                            Refresh
                        </button>
                    </div>
                </div>
                <div class="card-body p-3">
                    <div class="table-responsive">
                        <table class="table align-items-center mb-0">
                            <thead class="bg-light">
                                <tr>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Rank</th>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">User</th>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Metric</th>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Department</th>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Average Score</th>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Total Votes</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="leaderboard.list.length === 0">
                                    <td colspan="5" class="text-center py-4">
                                        <div class="text-muted">
                                            <i class="fas fa-chart-line fa-2x mb-2"></i>
                                            <p class="mb-0">No ratings yet. Be the first to rate someone!</p>
                                        </div>
                                    </td>
                                </tr>
                                <tr v-for="(entry, index) in leaderboard.list" :key="`leaderboard-${index}`">
                                    <td class="px-3 py-2">
                                        <div class="d-flex align-items-center">
                                            <span 
                                                class="badge badge-sm"
                                                :class="getRankBadgeClass(index)"
                                            >
                                                {{ index + 1 }}
                                            </span>
                                        </div>
                                    </td>
                                    <td class="px-3 py-2">
                                        <div class="d-flex align-items-center">
                                            <div class="avatar avatar-sm me-3">
                                                <div class="avatar-name">
                                                    {{ getInitials(entry.rated__first_name, entry.rated__last_name) }}
                                                </div>
                                            </div>
                                            <div>
                                                <h6 class="mb-0 text-sm">{{ entry.rated__first_name }} {{ entry.rated__last_name }}</h6>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-3 py-2">
                                        <span class="badge badge-sm bg-gradient-info">{{ entry.metric__name }}</span>
                                    </td>


                                    <td class="px-3 py-2">
                                        <span class="font-semibold text-sm text-gray-800">
                                            {{ entry.department }}
                                        </span>
                                    </td>





                                    <td class="px-3 py-2">
                                        <div class="d-flex align-items-center">
                                            <span class="text-sm font-weight-bold">{{ formatScore(entry.avg_score) }}</span>
                                            <div class="progress ms-2" style="width: 60px; height: 6px;">
                                                <div 
                                                    class="progress-bar bg-gradient-success" 
                                                    :style="`width: ${(entry.avg_score / 10) * 100}%`"
                                                ></div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-3 py-2">
                                        <span class="text-sm font-weight-bold">{{ entry.total_votes }}</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Rating Section -->
        <div class="col-12">
            <div class="card">
                <div class="card-header pb-0 p-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">
                            <i class="fas fa-star text-warning me-2"></i>
                            Rate Your Colleagues
                        </h6>
                        <div class="text-sm text-muted">
                            Click "Vote" to rate a user on each metric
                        </div>
                    </div>
                </div>
                <div class="card-body p-3">
                    <div class="table-responsive">
                        <table class="table align-items-center mb-0">
                            <thead class="bg-light">
                                <tr>
                                    <th class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7">Users</th>
                                    <th 
                                        class="text-uppercase text-secondary text-xs font-weight-bolder opacity-7 text-center" 
                                        v-for="metric in metrices.list" 
                                        :key="`metric-header-${metric.id}`"
                                    >
                                        {{ metric.name }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="users.list.length === 0">
                                    <td :colspan="metrices.list.length + 1" class="text-center py-4">
                                        <div class="text-muted">
                                            <i class="fas fa-users fa-2x mb-2"></i>
                                            <p class="mb-0">No users available to rate</p>
                                        </div>
                                    </td>
                                </tr>
                                <tr v-for="user in users.list" :key="`user-${user.id}`">
                                    <td class="px-3 py-3">
                                        <div class="d-flex align-items-center">
                                            <div class="avatar avatar-sm me-3">
                                                <div class="avatar-name">
                                                    {{ getInitials(user.first_name, user.last_name) }}
                                                </div>
                                            </div>
                                            <div>
                                                <h6 class="mb-0 text-sm">{{ user.first_name }} {{ user.last_name }}</h6>
                                                <p class="text-xs text-muted mb-0">{{ user.email }}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td 
                                        v-for="metric in metrices.list" 
                                        :key="`user-${user.id}-metric-${metric.id}`"
                                        class="px-3 py-3 text-center"
                                    >
                                        <button 
                                            @click="rate(user, metric)" 
                                            class="btn btn-primary btn-sm"
                                            :disabled="isRating"
                                        >
                                            <i class="fas fa-star me-1"></i>
                                            Vote
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>  

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { get, post } from '../../kit';
import Swal from 'sweetalert2';

// Reactive state
const users = reactive({ list: [] });
const metrices = reactive({ list: [] });
const leaderboard = reactive({ list: [] });
const isLoading = ref(false);
const isRating = ref(false);

// Helper functions
function getInitials(firstName, lastName) {
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
}

function formatScore(score) {
    return score ? score.toFixed(2) : '0.00';
}

function getRankBadgeClass(index) {
    if (index === 0) return 'bg-gradient-warning'; // Gold
    if (index === 1) return 'bg-gradient-secondary'; // Silver
    if (index === 2) return 'bg-gradient-info'; // Bronze
    return 'bg-gradient-success'; // Default
}

// API functions
async function getUsers() {
    try {
        isLoading.value = true;
        const response = await get('/users/all');
        users.list = response.data || [];
    } catch (error) {
        console.error('Error fetching users:', error);
        Swal.fire({
            title: 'Error',
            text: 'Failed to load users',
            icon: 'error'
        });
    } finally {
        isLoading.value = false;
    }
}

async function getMetrices() {
    try {
        isLoading.value = true;
        const response = await get('/metrices/all');
        metrices.list = response.data || [];
    } catch (error) {
        console.error('Error fetching metrics:', error);
        Swal.fire({
            title: 'Error',
            text: 'Failed to load metrics',
            icon: 'error'
        });
    } finally {
        isLoading.value = false;
    }
}

async function getLeaderboard() {
    try {
        isLoading.value = true;
        const response = await get('/rate/leaderboard');
        leaderboard.list = response.data || [];
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        Swal.fire({
            title: 'Error',
            text: 'Failed to load leaderboard',
            icon: 'error'
        });
    } finally {
        isLoading.value = false;
    }
}

async function rate(user, metric) {
    try {
        const { value: score } = await Swal.fire({
            title: `Rate ${user.first_name} ${user.last_name}`,
            text: `How would you rate them on ${metric.name}?`,
            input: 'range',
            inputLabel: 'Score (1-10)',
            inputAttributes: {
                min: 1,
                max: 10,
                step: 1
            },
            inputValue: 5,
            showCancelButton: true,
            confirmButtonText: 'Submit Rating',
            cancelButtonText: 'Cancel',
            showLoaderOnConfirm: true,
            preConfirm: (value) => {
                return new Promise((resolve) => {
                    setTimeout(() => {
                        resolve(value);
                    }, 200);
                });
            },
            didOpen: () => {
                const input = Swal.getInput();
                const output = document.createElement('div');
                output.innerHTML = `<span class="text-primary font-weight-bold">${input.value}</span>/10`;
                output.style.textAlign = 'center';
                output.style.marginTop = '10px';
                input.parentNode.appendChild(output);
                
                input.addEventListener('input', () => {
                    output.innerHTML = `<span class="text-primary font-weight-bold">${input.value}</span>/10`;
                });
            }
        });

        if (score) {
            isRating.value = true;
            const response = await post('store', {
                user: user,
                metric: { ...metric, score: parseInt(score) }
            });

            if (response.data === 'success') {
                await Swal.fire({
                    title: "Awesome!",
                    text: `You rated ${user.first_name} ${user.last_name} on ${metric.name} with score ${score}`,
                    icon: "success",
                    timer: 3000,
                    showConfirmButton: false
                });
                // Refresh leaderboard after rating
                await getLeaderboard();
            }else if (response.data === 'fail') {
                await Swal.fire({
                    title: "Already Rated!",
                    text: `You already rated ${user.first_name} ${user.last_name} on ${metric.name} for this month`,
                    icon: "error",
                    timer: 3000,
                    showConfirmButton: false
                });
            } else {
                throw new Error('Failed to save rating');
            }
        }
    } catch (error) {
        console.error('Error rating user:', error);
        Swal.fire({
            title: 'Error',
            text: 'Failed to submit rating. Please try again.',
            icon: 'error'
        });
    } finally {
        isRating.value = false;
    }
}

// Lifecycle
onMounted(async () => {
    await Promise.all([
        getUsers(),
        getMetrices(),
        getLeaderboard()
    ]);
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.avatar-name {
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

.progress {
    border-radius: 3px;
    background-color: #e9ecef;
}

.progress-bar {
    border-radius: 3px;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.card {
    border: none;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.badge {
    font-size: 0.75rem;
}

.fa-spin {
    animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>