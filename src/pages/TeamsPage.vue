<template>
  <section class="vstack gap-3">
    <header>
      <h2 class="mb-1">Équipes</h2>
      <div class="small can-muted">Participants CAN</div>
    </header>

    <div class="row g-3">
      <div v-for="t in teams" :key="t.id" class="col-12 col-md-6">
        <div class="p-3 can-card d-flex justify-content-between align-items-center">
          <div class="fw-semibold fs-6">{{ t.name }}</div>
          <div class="small can-muted">{{ t.code }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { teams } from "../data/mock";
</script>
