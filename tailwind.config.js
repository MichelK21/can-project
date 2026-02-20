/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: {
    extend: {
      colors: {
        sahara: "#C98C3A",
        ebony: "#0B1F1A",
        kente: "#1F7A4D",
        night: "#0B1020",
      },
    },
  },
  plugins: [],
};
