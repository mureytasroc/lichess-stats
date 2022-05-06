import React, { useState, useEffect, useRef } from "react";
import { Layout } from "antd";
import "./App.css";
import "antd/dist/antd.css";

import Screen, { COLORS } from "./components/Screen";
import Menu from "./components/Menu";
import Splash from "./components/Splash";
import * as Charts from "./components/Charts";

const { Content, Sider } = Layout;

function App() {
  const content = [
    Charts.TitleDistribution,
    Charts.ResultPercentageDistribution,
  ];
  const [collapse, setCollapse] = useState(false);
  const [scrollPosition, setScrollPosition] = useState(0);
  const [menuScroll, setMenuScroll] = useState(0);

  const currScroll = useRef(0);
  const currMenuScroll = useRef(0);

  useEffect(() => {
    const onScroll = () => {
      const currScreen = Math.floor(window.scrollY / window.innerHeight);
      if (currScreen !== currMenuScroll.current) {
        setMenuScroll(currScreen);
        currMenuScroll.current = currScreen;
      }
      if (currScreen > currScroll.current) {
        setScrollPosition(currScreen);
        currScroll.current = Math.floor(currScreen);
      }
    };
    // clean up code
    window.removeEventListener("scroll", onScroll);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  return (
    <Layout
      className="App"
      style={{
        minHeight: "100vh",
      }}
    >
      <Sider
        collapsible
        collapsed={collapse}
        onCollapse={() => setCollapse(!collapse)}
        style={{
          position: "sticky",
          top: 0,
          height: "100vh",
          zIndex: 10000,
        }}
      >
        <div className="logo" />
        <Menu content={content} scroll={menuScroll} />
      </Sider>

      <Layout className="site-layout">
        <Content>
          <div style={{ height: 10, width: 300 }} />
          <Screen theme={COLORS.BLUE} id="Title" title="Chess Wins Net">
            <Splash />
          </Screen>
          {content.map((element, index) => (
            <Screen
              randomColor
              id={index}
              key={element.title}
              title={element.title}
              floating
            >
              {scrollPosition >= index ? element.content : null}
            </Screen>
          ))}
          <div style={{ height: 10, width: 300 }} />
        </Content>
      </Layout>
    </Layout>
  );
}

export default App;
