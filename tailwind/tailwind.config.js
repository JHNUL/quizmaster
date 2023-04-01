const path = require("path");
const colors = require("tailwindcss/colors");
const templates = path.join(__dirname, "..", "src", "templates/**/*.html");
const javascript = path.join(__dirname, "..", "src", "static/**/*.js");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [templates, javascript],
  theme: {
    extend: {
      colors: {
        primary: colors.cyan
      }
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
