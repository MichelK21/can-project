<template>
  <section class="vstack gap-3">
    <header>
      <h2 class="mb-1">Connexion</h2>
      <div class="small can-muted">Accès administrateur (prototype)</div>
    </header>

    <div class="can-card p-4" style="max-width: 460px">
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

  auth.login(email.value);

  router.push("/");
}
</script>
