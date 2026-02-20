export const teams = [
  { id: 1, name: "Côte d’Ivoire", code: "CIV" },
  { id: 2, name: "Sénégal", code: "SEN" },
  { id: 3, name: "Maroc", code: "MAR" },
  { id: 4, name: "Nigeria", code: "NGA" },
];

export const matches = [
  {
    id: 1,
    group: "A",
    kickoffAt: "2025-01-15T20:00:00Z",
    homeTeamId: 1,
    awayTeamId: 2,
    homeScore: null,
    awayScore: null,
    status: "SCHEDULED",
  },
  {
    id: 2,
    group: "B",
    kickoffAt: "2025-01-16T17:00:00Z",
    homeTeamId: 3,
    awayTeamId: 4,
    homeScore: 1,
    awayScore: 1,
    status: "FT",
  },
];

export const groups = [
  { name: "A", teamIds: [1, 2] },
  { name: "B", teamIds: [3, 4] },
];
