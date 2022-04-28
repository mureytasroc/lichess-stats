import React, { useState, useEffect } from "react";
import { Bar } from "@ant-design/plots";
import "./App.css";
import Screen, { COLORS } from "./components/Screen";
import { doApiRequest } from "./utils/fetch";

const OPTIONS = {
  axis: {
    line: {
      style: {
        color: "white",
      },
    },
  },
};

function App() {
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest("/profile/title/distribution");
      setData(
        result.titles.filter((x) => x.title).sort((a, b) => b.count - a.count)
      );
    })();
  }, []);
  return (
    <div className="App">
      <div style={{ position: "fixed" }}>
        <a href="#thrid">skip</a>
      </div>
      <Screen theme={COLORS.YELLOW} id="title" title="Chess Wins Net">
        Add some splash content
      </Screen>
      <Screen theme={COLORS.PINK} id="first" title="title distribution">
        <Bar
          data={data}
          xField={"count"}
          yField={"title"}
          seriesField={"title"}
          autoFit
          style={{
            backgroundColor: "#FFFFFF",
            padding: "25px",
            borderRadius: "5px",
            boxShadow: "1px 3px 1px black",
          }}
          {...OPTIONS}
        />
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
      </Screen>
    </div>
  );
}

export default App;
