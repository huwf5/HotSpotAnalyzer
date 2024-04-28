# Geeker-Admin

### 介绍 📖

web界面基于 [Geeker-Admin](https://github.com/HalseySpicy/Geeker-Admin) 构建

- **Install：**

```text
pnpm install
```

- **Run：**

```text
pnpm dev
pnpm serve
```

- **Build：**

```text
# 开发环境
pnpm build:dev

# 测试环境
pnpm build:test

# 生产环境
pnpm build:pro
```

- **Lint：**

```text
# eslint 检测代码
pnpm lint:eslint

# prettier 格式化代码
pnpm lint:prettier

# stylelint 格式化样式
pnpm lint:stylelint
```

### 文件资源目录 📚

```text
web
├─ .husky                  # husky 配置文件
├─ .vscode                 # VSCode 推荐配置
├─ build                   # Vite 配置项
├─ public                  # 静态资源文件（该文件夹不会被打包）
├─ src
│  ├─ api                  # API 接口管理
│  ├─ assets               # 静态资源文件
│  ├─ components           # 全局组件
│  ├─ config               # 全局配置项
│  ├─ directives           # 全局指令文件
│  ├─ enums                # 项目常用枚举
│  ├─ hooks                # 常用 Hooks 封装
│  ├─ languages            # 语言国际化 i18n
│  ├─ layouts              # 框架布局模块
│  ├─ routers              # 路由管理
│  ├─ stores               # pinia store
│  ├─ styles               # 全局样式文件
│  ├─ typings              # 全局 ts 声明
│  ├─ utils                # 常用工具库
│  ├─ views                # 项目所有页面
│  ├─ App.vue              # 项目主组件
│  ├─ main.ts              # 项目入口文件
│  └─ vite-env.d.ts        # 指定 ts 识别 vue
├─ .editorconfig           # 统一不同编辑器的编码风格
├─ .env                    # vite 常用配置
├─ .env.development        # 开发环境配置
├─ .env.production         # 生产环境配置
├─ .env.test               # 测试环境配置
├─ .eslintignore           # 忽略 Eslint 校验
├─ .eslintrc.cjs           # Eslint 校验配置文件
├─ .gitignore              # 忽略 git 提交
├─ .prettierignore         # 忽略 Prettier 格式化
├─ .prettierrc.cjs         # Prettier 格式化配置
├─ .stylelintignore        # 忽略 stylelint 格式化
├─ .stylelintrc.cjs        # stylelint 样式格式化配置
├─ commitlint.config.cjs   # git 提交规范配置
├─ index.html              # 入口 html
├─ LICENSE                 # 开源协议文件
├─ lint-staged.config.cjs  # lint-staged 配置文件
├─ pnpm-lock.yaml          # pnpm 依赖包包版本锁定
├─ package.json            # 依赖包管理
├─ postcss.config.cjs      # postcss 配置
├─ README.md               # README 介绍
├─ tsconfig.json           # typescript 全局配置
└─ vite.config.ts          # vite 全局配置文件
```

## 前端开发者设置

- src/api/modules/login.ts 的 getAuthMenuListApi 中注释上面的代码，可以实现无需开启后端得到路由权限
  ![code1](https://github.com/ao-space/gt/assets/134463404/56eec78a-1e6e-4018-9231-2c3b0529c777)

- src/routers/index.ts 的 router.beforeEach 函数中可以注释这行代码来实现绕过用户登录，来进行其他界面的跳转以及测试
  ![code2](https://github.com/ao-space/gt/assets/134463404/8f74e1a3-5893-4601-afdc-9603b6521308)

  进行上述操作后，即可实现在前端界面开发时，无需开启后端。

- 启动前端服务
  - a. 更改 proxy 设置（先检查下述文件，更改**PROXY**设置为对应的 web 后端 url）
    ```ts
    //.env.development
    VITE_PROXY = [["/api", "http://localhost:8000"]];
    ```
  - b. 启动 web 服务
    ```shell
    pnpm run dev
    ```
