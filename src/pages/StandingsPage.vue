<template>
  <section class="vstack gap-4">
    <header>
      <h2 class="mb-1">Classement</h2>
      <div class="small can-muted">Groupes & statistiques</div>
    </header>

    <div v-for="g in groups" :key="g.name" class="can-card p-3">
      <h5 class="mb-3">Groupe {{ g.name }}</h5>

      <div class="table-responsive">
        <table class="table table-sm table-darkish mb-0">
          <thead>
            <tr>
              <th>#</th>
              <th>Équipe</th>
              <th>MJ</th>
              <th>V</th>
              <th>N</th>
              <th>D</th>
              <th>BP</th>
              <th>BC</th>
              <th>Diff</th>
              <th>PTS</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(s, i) in computeGroup(g)" :key="s.teamId">
              <td>{{ i + 1 }}</td>
              <td>{{ teamById.get(s.teamId)?.name }}</td>
              <td>{{ s.played }}</td>
              <td>{{ s.win }}</td>
              <td>{{ s.draw }}</td>
              <td>{{ s.loss }}</td>
              <td>{{ s.gf }}</td>
              <td>{{ s.ga }}</td>
              <td>{{ s.diff }}</td>
              <td class="fw-semibold">{{ s.pts }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { teams, matches, groups } from "../data/mock";

/* Map équipes */
const teamById = new Map(teams.map((t) => [t.id, t]));

/* Initialiser stats */
function initStats(teamIds) {
  const stats = {};

  for (const id of teamIds) {
    stats[id] = {
      teamId: id,
      played: 0,
      win: 0,
      draw: 0,
      loss: 0,
      gf: 0,
      ga: 0,
      diff: 0,
      pts: 0,
    };
  }

  return stats;
}

/* Calcul classement par groupe */
function computeGroup(group) {
  const stats = initStats(group.teamIds);

  for (const m of matches) {
    if (m.group !== group.name) continue;
    if (m.status !== "FT") continue;

    const home = stats[m.homeTeamId];
    const away = stats[m.awayTeamId];

    if (!home || !away) continue;

    home.played++;
    away.played++;

    home.gf += m.homeScore;
    home.ga += m.awayScore;

    away.gf += m.awayScore;
    away.ga += m.homeScore;

    if (m.homeScore > m.awayScore) {
      home.win++;
      away.loss++;
      home.pts += 3;
    } else if (m.homeScore < m.awayScore) {
      away.win++;
      home.loss++;
      away.pts += 3;
    } else {
      home.draw++;
      away.draw++;
      home.pts++;
      away.pts++;
    }
  }

  /* diff */
  for (const s of Object.values(stats)) {
    s.diff = s.gf - s.ga;
  }

  /* tri officiel */
  return Object.values(stats).sort((a, b) => {
    if (b.pts !== a.pts) return b.pts - a.pts;
    if (b.diff !== a.diff) return b.diff - a.diff;
    return b.gf - a.gf;
  });
}
</script>
