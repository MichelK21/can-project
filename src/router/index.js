import { createRouter, createWebHistory } from "vue-router";
import MatchesPage from "../pages/MatchesPage.vue";
import StandingsPage from "../pages/StandingsPage.vue";
import TeamsPage from "../pages/TeamsPage.vue";
import LoginPage from "../pages/LoginPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: MatchesPage },
    { path: "/classement", component: StandingsPage },
    { path: "/equipes", component: TeamsPage },
    { path: "/login", component: LoginPage },
  ],
});

export default router;
