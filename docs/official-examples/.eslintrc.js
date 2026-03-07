module.exports = {
  root: true,
  plugins: ["@typescript-eslint", "unused-imports"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  parserOptions: {
      "project": "./tsconfig.json",
      "tsconfigRootDir": __dirname,
      "sourceType": "module"
  },
  rules: {
    "@typescript-eslint/member-ordering": "off",
    "lines-between-class-members": "off",
    "padding-line-between-statements": "off",
    "no-unused-vars": "off",
    "max-len": "off",
    "max-depth": ["error", 3],
    "max-lines-per-function": "off",
    "max-params": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-unused-vars": "off",
    "unused-imports/no-unused-imports": "off",
    "unused-imports/no-unused-vars": 0,
  },
};
  