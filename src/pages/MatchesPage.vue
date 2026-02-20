<template>
  <section class="vstack gap-3">
    <header>
      <h2 class="mb-1">Matchs</h2>
      <div class="can-muted small">Calendrier et résultats</div>
    </header>

    <div class="vstack gap-3">
      <div v-for="m in matches" :key="m.id" class="p-3 can-card">
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
          <div class="fw-semibold">
            {{ teamName(m.homeTeamId) }}
            <span class="can-muted fw-normal mx-2">vs</span>
            {{ teamName(m.awayTeamId) }}
          </div>

          <div class="d-flex align-items-center gap-2">
            <span class="badge text-bg-secondary">Groupe {{ m.group }}</span>
            <span class="badge" :class="m.status === 'FT' ? 'text-bg-warning' : 'text-bg-info'">
              {{ m.status }}
            </span>
          </div>
        </div>

        <div class="d-flex justify-content-between align-items-center mt-3">
          <div class="small can-muted">{{ new Date(m.kickoffAt).toLocaleString() }}</div>
          <div class="fw-bold fs-5">{{ m.homeScore ?? "—" }} : {{ m.awayScore ?? "—" }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { teams, matches } from "../data/mock";
const teamById = new Map(teams.map((t) => [t.id, t]));
const teamName = (id) => teamById.get(id)?.name ?? "—";
</script>
