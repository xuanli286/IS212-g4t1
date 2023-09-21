const colors = require("tailwindcss/colors");

module.exports = {
  mode: "jit",
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx,vue}"],
  darkMode: false,
  theme: {
    colors: {
      grey: {
        DEFAULT: "#9F9F9F",
        50: "#EFEFEF",
      },
      black: "#323230",
      beige: "#F9F8F4",
      white: colors.white,
      green: {
        DEFAULT: "#307B74",
        50: "#D0FFE3",
      },
      yellow: {
        DEFAULT: "#FF9D01",
        50: "#FBB620",
      },
      red: {
        DEFAULT: "#FE4D35",
        50: "#FFD8D6",
      },
    },
    fontFamily: {
      serif: ["GFS Didot"],
      sans: ["Nunito Sans"],
    },

    fontWeight: {
      thin: "100",
      extralight: "200",
      light: "300",
      normal: "400",
      medium: "500",
      semibold: "600",
      bold: "700",
      extrabold: "800",
      black: "900",
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
