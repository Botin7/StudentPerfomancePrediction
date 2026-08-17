import { createRouter, createWebHistory } from "vue-router";

import Dashboard from "../Views/Dashboard.vue";
import Predict from "../Views/Predict.vue";
import Analytics from "../Views/Analytics.vue";
import About from "../Views/About.vue";


const routes = [
  { path: "/", component: Dashboard },
  { path: "/predict", component: Predict },
  { path: "/analytics", component: Analytics },
  { path: "/about", component: About },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;