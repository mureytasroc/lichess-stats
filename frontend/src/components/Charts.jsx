import React, { useState, useEffect } from "react";
import { Bar } from "@ant-design/plots";
import { doApiRequest } from "../utils/fetch";
import { GameTypeSelector, MonthYearSelector } from "../utils/selectors";

const NULL_NAME = "no title";

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

  return <Bar data={data} xField="count" yField="title" seriesField="title" />;
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
            title: title || NULL_NAME,
            value: win_percentage,
            type: "win percentage",
          },
          {
            title: title || NULL_NAME,
            value: loss_percentage,
            type: "loss percentage",
          },
          {
            title: title || NULL_NAME,
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

function GameTerminationDistributionChart() {
  const [data, setData] = useState([]);
  const [gameType, setGameType] = useState("All");
  const [startDay, setStartDay] = useState();
  const [endDay, setEndDay] = useState();

  useEffect(() => {
    (async () => {
      const params = {};
      if (gameType !== "All") params.game_type = gameType;
      if (startDay && startDay.length > 0) params.start_date = startDay;
      if (endDay && endDay.length > 0) params.end_date = endDay;

      const result = await doApiRequest(
        "/profile/title/termination-type",
        params
      );
      const transformedData = result.titles.flatMap(
        ({ title, termination_types }) =>
          termination_types.map((entry) => ({
            title: title || NULL_NAME,
            ...entry,
          }))
      );
      setData(transformedData);
    })();
  }, [gameType, startDay]);

  return (
    <>
      <div style={{ display: "flex" }}>
        <GameTypeSelector handleChange={setGameType} />
        {/* <MonthYearSelector handleChange={setStartDay} />
        <MonthYearSelector handleChange={setEndDay} /> */}
      </div>
      <br />
      <Bar
        data={data}
        isStack
        isPercent
        xField="percentage"
        yField="title"
        seriesField="termination_type"
      />
    </>
  );
}

export const GameTerminationDistribution = {
  title: "Game Terminations",
  content: <GameTerminationDistributionChart />,
  group: "Profile",
};
