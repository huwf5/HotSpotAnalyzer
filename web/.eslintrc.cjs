module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es6: true
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@typescript-eslint/parser",
    ecmaVersion: 2020,
    sourceType: "module",
    jsxPragma: "React",
    ecmaFeatures: {
      jsx: true
    }
  },
  extends: [
    "plugin:vue/vue3-recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:prettier/recommended" // 确保 Prettier 插件被引入
  ],
  // 添加 Prettier 插件
  plugins: ["prettier"],
  rules: {
    // Prettier 规则
    "prettier/prettier": [
      "error",
      {
        endOfLine: "auto"
      },
      {
        usePrettierrc: true // 使用 .prettierrc 文件中的配置
      }
    ],

    // ESLint 规则
    "no-var": "error",
    "no-multiple-empty-lines": ["error", { max: 1 }],
    "prefer-const": "off",
    "no-use-before-define": "off",

    // TypeScript 规则
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-empty-function": "error",
    "@typescript-eslint/prefer-ts-expect-error": "error",
    "@typescript-eslint/ban-ts-comment": "error",
    "@typescript-eslint/no-inferrable-types": "off",
    "@typescript-eslint/no-namespace": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/ban-types": "off",
    "@typescript-eslint/no-var-requires": "off",
    "@typescript-eslint/no-non-null-assertion": "off",

    // Vue 规则
    "vue/script-setup-uses-vars": "error",
    "vue/v-slot-style": "error",
    "vue/no-mutating-props": "error",
    "vue/custom-event-name-casing": "error",
    "vue/html-closing-bracket-newline": "error",
    "vue/attribute-hyphenation": "error",
    "vue/attributes-order": "off",
    "vue/no-v-html": "off",
    "vue/require-default-prop": "off",
    "vue/multi-word-component-names": "off",
    "vue/no-setup-props-destructure": "off"
  }
};
