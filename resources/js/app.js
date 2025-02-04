/**
 * First we will load all of this project's JavaScript dependencies which
 * includes Vue and other libraries. It is a great starting point when
 * building robust, powerful web applications using Vue and Laravel.
 */

require("./bootstrap");

window.Vue = require("vue").default;

/**
 * The following block of code may be used to automatically register your
 * Vue components. It will recursively scan this directory for the Vue
 * components and automatically register them with their "basename".
 *
 * Eg. ./components/ExampleComponent.vue -> <example-component></example-component>
 */

// const files = require.context('./', true, /\.vue$/i)
// files.keys().map(key => Vue.component(key.split('/').pop().split('.')[0], files(key).default))

// Vue.component('example-component', require('./components/ExampleComponent.vue').default);

/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

import { createApp } from "vue";
import ExampleComponent from "./components/ExampleComponent";
import UserIndex from "./components/users/index.vue";
import MetricesIndex from "./components/metrices/index.vue";
import RateIndex from "./components/rate/index.vue";
import UserSummary from "./components/attendance/UserSummary.vue";
import LeavesIndex from "./components/leaves/LeavesIndex.vue";
import AdminLeavesIndex from "./components/leaves/AdminLeavesIndex.vue";
import DashStats from "./components/dashboard/DashStats.vue";
import DashPoints from "./components/dashboard/PointsTable.vue";
import ProjectIndex from "./components/project/index.vue";
import TaskIndex from "./components/task/index.vue";
import SettingsIndex from "./components/settings/index.vue";
import PollIndex from "./components/poll/index.vue";
const app = createApp({
  components: {
    ExampleComponent,
    UserIndex,
    MetricesIndex,
    RateIndex,
    UserSummary,
    LeavesIndex,
    AdminLeavesIndex,
    DashStats,
    DashPoints,
    ProjectIndex,
    TaskIndex,
    SettingsIndex,
    PollIndex,
  },
  data() {
    return {};
  },
}).mount("#app");
