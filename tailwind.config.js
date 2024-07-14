module.exports = {
  mode: "jit",
  content: [
    "core/**/*.{html,js,py}",
    "app/**/*.{html,js,py}",
    "notifier/**/*.{html,js,py}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/forms")],
};
