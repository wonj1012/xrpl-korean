import React from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<"svg">>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: "XRP Ledger",
    Svg: require("@site/static/img/undraw_docusaurus_mountain.svg").default,
    description: <>XRP Ledger에 대한 소개글. 장점.</>,
  },
  {
    title: "개발자를 위한 안내서",
    Svg: require("@site/static/img/undraw_docusaurus_tree.svg").default,
    description: (
      <>
        API 문서, 튜토리얼, 예제 코드 등을 통해 XRP Ledger 개발을 손쉽게 시작할
        수 있습니다. <code>docs</code> 디렉터리를 확인해보세요.
      </>
    ),
  },
  {
    title: "XRP Ledger Korea 커뮤니티에 참가하세요!",
    Svg: require("@site/static/img/undraw_docusaurus_react.svg").default,
    description: (
      <>
        커뮤니티 포럼, 채팅방, 이벤트 등을 통해 다른 XRP Ledger 사용자와
        네트워킹을 즐길 수 있습니다. 지식을 공유하고, 문제를 해결하고, 새로운
        가능성을 함께 탐색하세요.
      </>
    ),
  },
];

function Feature({ title, Svg, description }: FeatureItem) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
