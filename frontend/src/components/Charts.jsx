import React, { useState, useEffect } from "react";
import { Bar } from "@ant-design/plots";
import { doApiRequest } from "../utils/fetch";

function TitleDistributionChart() {
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
    <Bar
      data={data}
      xField="count"
      yField="title"
      seriesField="title"
      autoFit
    />
  );
}

export const TitleDistribution = {
  title: "Title Distribution",
  content: <TitleDistributionChart />,
  group: "Profile",
};

function CompletionRateDistributionChart() {
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest("/profile/title/completion-rate");
      console.log(result);
      setData(
        result.titles
          .filter((x) => x.title)
          .sort((a, b) => b.avg_completion_rate - a.avg_completion_rate)
      );
    })();
  }, []);

  return (
    <Bar
      data={data}
      xField="count"
      yField="avg_completion_rate"
      seriesField="completion rate"
      autoFit
    />
  );
}

export const CompletionRateDistribution = {
  title: "Completion Distribution",
  content: <CompletionRateDistributionChart />,
  group: "Profile",
};

function ResultPercentageDistributionChart() {
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest("/profile/title/results");
      const transformedData = result.titles.flatMap(
        ({ title, win_percentage, loss_percentage, draw_percentage }) => [
          {
            title: title || "no title",
            value: win_percentage,
            type: "win percentage",
          },
          {
            title: title || "no title",
            value: loss_percentage,
            type: "loss percentage",
          },
          {
            title: title || "no title",
            value: draw_percentage,
            type: "draw percentage",
          },
        ]
      );
      setData(
        transformedData.sort((a, b) => b.win_percentage - a.win_percentage)
      );
    })();
  }, []);

  return (
    <Bar
      data={data}
      isStack
      isPercent
      xField="value"
      yField="title"
      seriesField="type"
    />
  );
}

export const ResultPercentageDistribution = {
  title: "Result Distribution",
  content: <ResultPercentageDistributionChart />,
  group: "Profile",
};
