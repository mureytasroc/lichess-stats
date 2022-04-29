import React, { useState, useEffect } from "react";
import "./App.css";
import Screen, { COLORS } from "./components/Screen";
import Menu from "./components/Menu";
import Splash from "./components/Splash";
import { TitleDistribution } from "./components/Charts";

function App() {
  const content = [
    TitleDistribution(),
    TitleDistribution(),
    TitleDistribution(),
    TitleDistribution(),
  ];
  console.log(content);
  return (
    <div className="App">
      <Menu content={content} />
      <Screen theme={COLORS.BLUE} id="Title Page" title="Chess Wins Net">
        <Splash />
      </Screen>
      {content.map((element, index) => (
        <Screen
          randomColor
          id={index}
          key={index}
          title={element.title}
          floating
        >
          {element.content}
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
