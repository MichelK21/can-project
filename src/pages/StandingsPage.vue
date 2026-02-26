<template>
  <section class="vstack gap-3">
    <header class="d-flex justify-content-between align-items-end">
      <div>
        <h2 class="mb-1">Classement</h2>
        <div class="small can-muted">Calculé depuis les matchs FT</div>
      </div>

      <button class="can-btn small" @click="load" :disabled="loading">Refresh</button>
    </header>

    <div v-if="error" class="alert alert-danger mb-0">{{ error }}</div>
    <div v-if="loading" class="can-muted">Chargement…</div>

    <div v-else class="vstack gap-4">
      <div v-for="(rows, group) in groups" :key="group" class="can-card p-3">
        <div class="fw-semibold mb-2">Groupe {{ group }}</div>

        <div class="table-responsive">
          <table class="table table-dark table-sm align-middle mb-0">
            <thead>
              <tr>
                <th>#</th>
                <th>Équipe</th>
                <th class="text-end">MJ</th>
                <th class="text-end">G</th>
                <th class="text-end">N</th>
                <th class="text-end">P</th>
                <th class="text-end">BP</th>
                <th class="text-end">BC</th>
                <th class="text-end">Diff</th>
                <th class="text-end">Pts</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in rows" :key="r.teamId">
                <td>{{ i + 1 }}</td>
                <td>{{ r.team }}</td>
                <td class="text-end">{{ r.played }}</td>
                <td class="text-end">{{ r.wins }}</td>
                <td class="text-end">{{ r.draws }}</td>
                <td class="text-end">{{ r.losses }}</td>
                <td class="text-end">{{ r.gf }}</td>
                <td class="text-end">{{ r.ga }}</td>
                <td class="text-end">{{ r.gd }}</td>
                <td class="text-end fw-semibold">{{ r.points }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="Object.keys(groups).length === 0" class="can-muted">
        Aucun match terminé (FT) pour calculer le classement.
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

const loading = ref(false);
const error = ref("");
const groups = ref({});

async function load() {
  loading.value = true;
  error.value = "";
  try {
    const res = await fetch("http://localhost:8000/standings");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    groups.value = await res.json();
  } catch (e) {
    error.value = e?.message ?? "Erreur";
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>
