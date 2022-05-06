import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import Screen, { COLORS } from "./components/Screen";
import Menu from "./components/Menu";
import Splash from "./components/Splash";
import { TitleDistributionTitle, TitleDistribution } from "./components/Charts";

function App() {
  const content = [
    { title: TitleDistributionTitle, content: <TitleDistribution /> },
    // { title: TitleDistributionTitle, content: <TitleDistribution /> },
    // { title: TitleDistributionTitle, content: <TitleDistribution /> },
    // { title: TitleDistributionTitle, content: <TitleDistribution /> },
  ];
  const [scrollPosition, setScrollPosition] = useState(0);
  const currScroll = useRef(0);

  useEffect(() => {
    const onScroll = () => {
      const currScreen = Math.floor(window.scrollY / window.innerHeight);
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
    <div className="App">
      <Menu content={content} />
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

      {/* <Screen theme={COLORS.BLUE} id="title" title="Chess Wins Net">
        <Splash />
      </Screen>
      <Screen
        theme={COLORS.WHITE}
        id="first"
        title="title distribution"
        floating
      >
        <TitleDistribution />
      </Screen>
      <Screen theme={COLORS.YELLOW} id="second" title="second">
        Second Page
      </Screen>
      <Screen theme={COLORS.ORANGE} id="thrid" title="third">
        {" "}
        Third Page
      </Screen>
      <Screen theme={COLORS.BLUE} id="forth">
        {" "}
        Forth Page
      </Screen>
      <Screen theme={COLORS.YELLOW} id="fifth">
        {" "}
        five Page
      </Screen>
      <Screen theme={COLORS.ORANGE} id="sixth">
        {" "}
        six Page
      </Screen>
      <Screen theme={COLORS.BLUE} id="sevent">
        {" "}
        seven Page
      </Screen> */}
    </div>
  );
}

export default App;
