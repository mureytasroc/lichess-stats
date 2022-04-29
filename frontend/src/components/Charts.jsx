import React, { useState, useEffect } from "react";
import { Bar } from "@ant-design/plots";
import { doApiRequest } from "../utils/fetch";

export function TitleDistribution() {
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest("/profile/title/distribution");
      setData(
        result.titles.filter((x) => x.title).sort((a, b) => b.count - a.count)
      );
    })();
  }, []);
  return {
    content: (
      <Bar
        data={data}
        xField={"count"}
        yField={"title"}
        seriesField={"title"}
        autoFit
      />
    ),
    title: "Title Distribution",
  };
}
