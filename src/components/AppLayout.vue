<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

function handleAuth() {
  if (auth.isLogged) {
    auth.logout();
    router.push("/");
  } else {
    router.push("/login");
  }
}
</script>

<template>
  <div class="min-vh-100">
    <header class="can-header">
      <div class="container py-3 d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-baseline gap-3">
          <div class="fw-semibold fs-5 can-brand">CAN</div>
          <div class="small can-muted">Vue 3 • Bootstrap</div>
        </div>

        <div class="d-flex align-items-center gap-3">
          <nav class="d-flex gap-3 small">
            <RouterLink to="/" class="nav-link-lite" active-class="active">Matchs</RouterLink>
            <RouterLink to="/classement" class="nav-link-lite" active-class="active"
              >Classement</RouterLink
            >
            <RouterLink to="/equipes" class="nav-link-lite" active-class="active"
              >Équipes</RouterLink
            >
          </nav>

          <button class="can-btn can-btn-primary small" @click="handleAuth">
            {{ auth.isLogged ? "Logout" : "Login" }}
          </button>
        </div>
      </div>
    </header>

    <main class="container py-4">
      <slot />
    </main>
  </div>
</template>
