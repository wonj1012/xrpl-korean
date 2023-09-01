import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/en/blog',
    component: ComponentCreator('/en/blog', '774'),
    exact: true
  },
  {
    path: '/en/blog/archive',
    component: ComponentCreator('/en/blog/archive', 'fd5'),
    exact: true
  },
  {
    path: '/en/blog/first-blog-post',
    component: ComponentCreator('/en/blog/first-blog-post', 'd61'),
    exact: true
  },
  {
    path: '/en/blog/long-blog-post',
    component: ComponentCreator('/en/blog/long-blog-post', '0aa'),
    exact: true
  },
  {
    path: '/en/blog/mdx-blog-post',
    component: ComponentCreator('/en/blog/mdx-blog-post', 'c9d'),
    exact: true
  },
  {
    path: '/en/blog/tags',
    component: ComponentCreator('/en/blog/tags', 'dc1'),
    exact: true
  },
  {
    path: '/en/blog/tags/docusaurus',
    component: ComponentCreator('/en/blog/tags/docusaurus', '818'),
    exact: true
  },
  {
    path: '/en/blog/tags/facebook',
    component: ComponentCreator('/en/blog/tags/facebook', '356'),
    exact: true
  },
  {
    path: '/en/blog/tags/hello',
    component: ComponentCreator('/en/blog/tags/hello', '8cb'),
    exact: true
  },
  {
    path: '/en/blog/tags/hola',
    component: ComponentCreator('/en/blog/tags/hola', '572'),
    exact: true
  },
  {
    path: '/en/blog/welcome',
    component: ComponentCreator('/en/blog/welcome', '768'),
    exact: true
  },
  {
    path: '/en/markdown-page',
    component: ComponentCreator('/en/markdown-page', 'd45'),
    exact: true
  },
  {
    path: '/en/docs',
    component: ComponentCreator('/en/docs', 'ed8'),
    routes: [
      {
        path: '/en/docs/account_and_transaction/account',
        component: ComponentCreator('/en/docs/account_and_transaction/account', '026'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/account_and_transaction/environment',
        component: ComponentCreator('/en/docs/account_and_transaction/environment', 'b50'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/account_and_transaction/token',
        component: ComponentCreator('/en/docs/account_and_transaction/token', '072'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/account_and_transaction/transaction',
        component: ComponentCreator('/en/docs/account_and_transaction/transaction', '2fd'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/category/nft',
        component: ComponentCreator('/en/docs/category/nft', '703'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/category/xrpl-hooks',
        component: ComponentCreator('/en/docs/category/xrpl-hooks', '826'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/category/계정과-트랜잭션',
        component: ComponentCreator('/en/docs/category/계정과-트랜잭션', 'aeb'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/category/고급-결제-타입',
        component: ComponentCreator('/en/docs/category/고급-결제-타입', 'dfb'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/category/탈중앙화-거래소-dex',
        component: ComponentCreator('/en/docs/category/탈중앙화-거래소-dex', '48c'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/decentralized_exchange/amm',
        component: ComponentCreator('/en/docs/decentralized_exchange/amm', '509'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/decentralized_exchange/dex_scenario',
        component: ComponentCreator('/en/docs/decentralized_exchange/dex_scenario', '50b'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/decentralized_exchange/introduction',
        component: ComponentCreator('/en/docs/decentralized_exchange/introduction', 'a38'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/decentralized_exchange/xrpl_dex',
        component: ComponentCreator('/en/docs/decentralized_exchange/xrpl_dex', 'b90'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/hooks/hooks_advanced',
        component: ComponentCreator('/en/docs/hooks/hooks_advanced', 'bbb'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/hooks/hooks_development',
        component: ComponentCreator('/en/docs/hooks/hooks_development', '9b3'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/hooks/introduction',
        component: ComponentCreator('/en/docs/hooks/introduction', '2b6'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/intro',
        component: ComponentCreator('/en/docs/intro', 'fb4'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/nft/introduction',
        component: ComponentCreator('/en/docs/nft/introduction', '5c6'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/nft/xls-20',
        component: ComponentCreator('/en/docs/nft/xls-20', '2f7'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/specialized_payment_types/checks',
        component: ComponentCreator('/en/docs/specialized_payment_types/checks', '2e9'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/specialized_payment_types/cross_currency_payments',
        component: ComponentCreator('/en/docs/specialized_payment_types/cross_currency_payments', '309'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/specialized_payment_types/escrow',
        component: ComponentCreator('/en/docs/specialized_payment_types/escrow', '334'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/en/docs/specialized_payment_types/payment_channels',
        component: ComponentCreator('/en/docs/specialized_payment_types/payment_channels', '68e'),
        exact: true,
        sidebar: "tutorialSidebar"
      }
    ]
  },
  {
    path: '/en/',
    component: ComponentCreator('/en/', 'ae4'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
