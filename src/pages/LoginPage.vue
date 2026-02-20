<template>
  <section class="vstack gap-3">
    <!-- Header -->
    <header>
      <h2 class="mb-1">Connexion</h2>
      <div class="small can-muted">Accès administrateur (prototype)</div>
    </header>

    <!-- Card -->
    <div class="can-card p-4" style="max-width: 460px">
      <!-- Email -->
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          placeholder="admin@can.app"
          autocomplete="username"
        />
      </div>

      <!-- Password -->
      <div class="mb-3">
        <label class="form-label">Mot de passe</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          placeholder="••••••••"
          autocomplete="current-password"
        />
      </div>

      <!-- Button -->
      <button class="can-btn can-btn-primary w-100" @click="submit">Se connecter</button>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");

const auth = useAuthStore();
const router = useRouter();

function submit() {
  if (!email.value.trim()) {
    alert("Veuillez entrer un email");
    return;
  }

  // Fake login (temporaire)
  auth.login(email.value);

  // Redirection après login
  router.push("/");
}
</script>
