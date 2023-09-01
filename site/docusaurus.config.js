// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "XRPL Korea 🇰🇷",
  tagline: "XRP Ledger 공식 한국어 사이트에 오신 것을 환영합니다!",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://your-docusaurus-test-site.com",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "Catalyze-Research", // Usually your GitHub org/user name.
  projectName: "xrpl-korean", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "ko",
    locales: ["en", "ko"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl: "https://github.com/Catalyze-Research/xrpl-korean/site/",
        },
        blog: {
          showReadingTime: true,
          editUrl: "https://github.com/Catalyze-Research/xrpl-korean/site/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: "img/docusaurus-social-card.jpg",
      navbar: {
        title: "XRPL Korea",
        logo: {
          alt: "XRPL Logo",
          src: "img/logo_light.svg",
          srcDark: "img/logo_dark.svg",
        },
        items: [
          {
            type: "docSidebar",
            sidebarId: "tutorialSidebar",
            position: "left",
            label: "튜토리얼",
          },
          { to: "/blog", label: "블로그", position: "left" },
          {
            href: "https://github.com/Catalyze-Research/xrpl-korean",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Docs",
            items: [
              {
                label: "Tutorial",
                to: "/docs/intro",
              },
            ],
          },
          {
            title: "Community",
            items: [
              {
                label: "Twitter",
                href: "https://twitter.com/xrplkorea",
              },
              {
                label: "Discord",
                href: "https://twitter.com/docusaurus",
              },
              {
                label: "Telegram",
                href: "https://t.me/xrplkoreanchat",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "Blog",
                to: "/blog",
              },
              {
                label: "GitHub",
                href: "https://github.com/Catalyze-Research/xrpl-korean",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Catalyze-Research`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
