<template>
  <section class="vstack gap-3">
    <header class="d-flex justify-content-between align-items-end">
      <div>
        <h2 class="mb-1">Matchs</h2>
        <div class="small can-muted">Depuis l’API FastAPI</div>
      </div>

      <div class="d-flex gap-2">
        <button class="can-btn small" @click="load" :disabled="loading">Refresh</button>
        <button class="can-btn can-btn-primary small" @click="handleSeed" :disabled="loading">
          Seed
        </button>
      </div>
    </header>

    <div v-if="error" class="alert alert-danger mb-0">{{ error }}</div>
    <div v-if="loading" class="can-muted">Chargement…</div>

    <div v-else class="vstack gap-3">
      <div v-for="m in matches" :key="m.id" class="can-card p-3">
        <div class="d-flex justify-content-between">
          <div class="fw-semibold">Groupe {{ m.group }}</div>
          <div class="badge text-bg-dark">{{ m.status }}</div>
        </div>

        <div class="mt-2 fw-bold fs-5">{{ m.homeScore ?? "—" }} : {{ m.awayScore ?? "—" }}</div>

        <div class="small can-muted mt-1">
          {{ new Date(m.kickoffAt).toLocaleString() }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getMatches, seed } from "../api/canApi";

const loading = ref(false);
const error = ref("");
const matches = ref([]);

async function load() {
  loading.value = true;
  error.value = "";
  try {
    matches.value = await getMatches();
  } catch (e) {
    error.value = e?.message ?? "Erreur";
  } finally {
    loading.value = false;
  }
}

async function handleSeed() {
  loading.value = true;
  error.value = "";
  try {
    await seed();
    await load();
  } catch (e) {
    error.value = e?.message ?? "Seed échoué";
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>
