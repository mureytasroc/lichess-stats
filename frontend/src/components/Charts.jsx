import React, { useState, useEffect } from "react";
import { Statistic } from "antd";
import { Bar, Line } from "@ant-design/plots";
import { doApiRequest } from "../utils/fetch";
import {
  GameTypeSelector,
  DaySelector,
  TitleCountrySelector,
  SlicerSelector,
  UsernameSelector,
} from "../utils/selectors";

const NULL_NAME = "no title";

function TitleDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [slice, setSlice] = useState(0);
  const [data, setData] = useState([]);
  const [type, setType] = useState("title");
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/profile/${type}/distribution`);
      if (type === "title") {
        setUnSlicedData(result.titles);
      } else {
        setUnSlicedData(result.countries);
      }
    })();
  }, [type]);

  useEffect(() => {
    if (type === "title") {
      setData(
        unSlicedData.filter((x) => x.title).sort((a, b) => b.count - a.count)
      );
    } else {
      const transformedResult = unSlicedData.map((entry) => ({
        ...entry,
        title: entry.title || NULL_NAME,
      }));
      setData(
        transformedResult
          .sort((a, b) => b.count - a.count)
          .slice(slice + 1, slice + 11)
      );
    }
  }, [unSlicedData, slice]);

  return (
    <>
      <TitleCountrySelector handleChange={setType} />
      {type === "title" ? (
        <Bar
          data={data}
          xField="count"
          yField="title"
          seriesField="title"
          autoFit
          yAxis={{ max: 30 }}
        />
      ) : (
        <>
          <Bar
            data={data}
            xField="count"
            yField="country"
            seriesField="country"
            autoFit
          />
          <SlicerSelector
            length={unSlicedData.length}
            handleChange={setSlice}
          />
        </>
      )}
    </>
  );
}

export const TitleDistribution = {
  title: "Title Distribution",
  content: <TitleDistributionChart />,
  group: "Profile",
};

function CompletionRateDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [slice, setSlice] = useState(0);

  const [data, setData] = useState([]);
  const [type, setType] = useState("title");

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
        `/profile/${type}/completion-rate`,
        params
      );
      if (type === "title") {
        setUnSlicedData(result.titles);
      } else {
        setUnSlicedData(result.countries);
      }
    })();
  }, [type, gameType, startDay, endDay]);

  useEffect(() => {
    if (type === "title") {
      const transformedResult = unSlicedData.map((entry) => ({
        ...entry,
        title: entry.title || NULL_NAME,
      }));
      setData(
        transformedResult.sort(
          (a, b) => b.avg_completion_rate - a.avg_completion_rate
        )
      );
    } else {
      setData(
        unSlicedData
          .sort((a, b) => b.avg_completion_rate - a.avg_completion_rate)
          .slice(slice, slice + 10)
      );
    }
  }, [unSlicedData, slice]);

  return (
    <>
      <div style={{ display: "flex" }}>
        <TitleCountrySelector handleChange={setType} />
        <GameTypeSelector handleChange={setGameType} />
        <DaySelector handleChange={setStartDay} />
        <DaySelector handleChange={setEndDay} />
      </div>
      {type === "title" ? (
        <Bar
          data={data}
          xField="avg_completion_rate"
          yField="title"
          seriesField="title"
          autoFit
        />
      ) : (
        <>
          <Bar
            data={data}
            xField="avg_completion_rate"
            yField="country"
            seriesField="country"
            autoFit
          />
          <SlicerSelector
            length={unSlicedData.length}
            handleChange={setSlice}
          />
        </>
      )}
    </>
  );
}

export const CompletionRateDistribution = {
  title: "Game Completion",
  content: <CompletionRateDistributionChart />,
  group: "Profile",
};

function ResultPercentageDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [slice, setSlice] = useState(0);
  const [data, setData] = useState([]);
  const [type, setType] = useState("title");

  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/profile/${type}/results`);
      if (type === "title") {
        setUnSlicedData(result.titles);
      } else {
        setUnSlicedData(result.countries);
      }
    })();
  }, [type]);

  useEffect(() => {
    if (type === "title") {
      const transformedData = unSlicedData.flatMap(
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
    } else {
      const transformedData = unSlicedData
        .sort((a, b) => b.win_percentage - a.winPercentage)
        .slice(slice, slice + 10)
        .flatMap(
          ({ country, win_percentage, loss_percentage, draw_percentage }) => [
            {
              country,
              value: win_percentage,
              type: "win percentage",
            },
            {
              country,
              value: loss_percentage,
              type: "loss percentage",
            },
            {
              country,
              value: draw_percentage,
              type: "draw percentage",
            },
          ]
        );
      setData(transformedData);
    }
  }, [unSlicedData, slice]);

  return (
    <>
      <TitleCountrySelector handleChange={setType} />
      {type === "title" ? (
        <Bar
          data={data}
          isStack
          isPercent
          xField="value"
          yField="title"
          seriesField="type"
        />
      ) : (
        <>
          <Bar
            data={data}
            isStack
            isPercent
            xField="value"
            yField="country"
            seriesField="type"
          />
          <SlicerSelector
            length={unSlicedData.length}
            handleChange={setSlice}
          />
        </>
      )}
    </>
  );
}

export const ResultPercentageDistribution = {
  title: "Game Results",
  content: <ResultPercentageDistributionChart />,
  group: "Profile",
};

function GameTerminationDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [data, setData] = useState([]);
  const [type, setType] = useState("title");

  const [gameType, setGameType] = useState("All");
  const [startDay, setStartDay] = useState();
  const [endDay, setEndDay] = useState();

  const [slice, setSlice] = useState(0);

  useEffect(() => {
    (async () => {
      const params = {};
      if (gameType !== "All") params.game_type = gameType;
      if (startDay && startDay.length > 0) params.start_date = startDay;
      if (endDay && endDay.length > 0) params.end_date = endDay;

      const result = await doApiRequest(
        `/profile/${type}/termination-type`,
        params
      );
      if (type === "title") {
        setUnSlicedData(result.titles);
      } else {
        setUnSlicedData(result.countries);
      }
    })();
  }, [type, gameType, startDay, endDay]);

  useEffect(() => {
    if (type === "title") {
      const transformedData = unSlicedData
        .slice(slice, slice + 10)
        .flatMap(({ title, termination_types }) =>
          termination_types.map((entry) => ({
            title: title || NULL_NAME,
            ...entry,
          }))
        );
      setData(transformedData);
    } else {
      const transformedData = unSlicedData
        .slice(slice, slice + 10)
        .flatMap(({ country, termination_types }) =>
          termination_types.map((entry) => ({
            country,
            ...entry,
          }))
        );
      setData(transformedData);
    }
  }, [unSlicedData, slice]);
  return (
    <>
      <div style={{ display: "flex" }}>
        <TitleCountrySelector handleChange={setType} />
        <GameTypeSelector handleChange={setGameType} />
        <DaySelector handleChange={setStartDay} />
        <DaySelector handleChange={setEndDay} />
      </div>
      {type === "title" ? (
        <Bar
          data={data}
          isStack
          isPercent
          xField="percentage"
          yField="title"
          seriesField="termination_type"
        />
      ) : (
        <>
          <Bar
            data={data}
            isStack
            isPercent
            xField="percentage"
            yField="country"
            seriesField="termination_type"
          />
          <SlicerSelector
            length={unSlicedData.length}
            handleChange={setSlice}
          />
        </>
      )}
    </>
  );
}

export const GameTerminationDistribution = {
  title: "Game Terminations",
  content: <GameTerminationDistributionChart />,
  group: "Profile",
};

function GameLengthDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [slice, setSlice] = useState(0);
  const [type, setType] = useState("title");

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
      const result = await doApiRequest(`/profile/${type}/game-length`, params);
      if (type === "title") {
        setUnSlicedData(
          result.titles.sort((a, b) => b.avg_game_length - a.avg_game_length)
        );
      } else {
        setUnSlicedData(
          result.countries.sort((a, b) => b.avg_game_length - a.avg_game_length)
        );
      }
    })();
  }, [type, gameType, startDay, endDay]);

  useEffect(() => {
    if (type === "title") {
      const transformedResult = unSlicedData.map((entry) => ({
        ...entry,
        title: entry.title || NULL_NAME,
      }));
      setData(transformedResult);
    } else {
      setData(unSlicedData.slice(slice, slice + 10));
    }
  }, [unSlicedData, slice]);

  return (
    <>
      <div style={{ display: "flex" }}>
        <TitleCountrySelector handleChange={setType} />
        <GameTypeSelector handleChange={setGameType} />
        <DaySelector handleChange={setStartDay} />
        <DaySelector handleChange={setEndDay} />
      </div>
      {type === "title" ? (
        <Bar
          data={data}
          xField="avg_game_length"
          yField="title"
          seriesField="title"
          autoFit
        />
      ) : (
        <>
          <Bar
            data={data}
            xField="avg_game_length"
            yField="country"
            seriesField="country"
          />
          <SlicerSelector
            length={unSlicedData.length}
            handleChange={setSlice}
          />
        </>
      )}
    </>
  );
}

export const GameLengthDistribution = {
  title: "Game Lengths",
  content: <GameLengthDistributionChart />,
  group: "Profile",
};

function GameTimeDistributionChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    (async () => {
      const result = await doApiRequest("/games/date-distribution");
      console.log(result.dates);
      setData(result.dates);
    })();
  }, []);

  return (
    <>
      <Line data={data} xField="start_date" yField="count" autoFit />
    </>
  );
}
export const GameTimeDistribution = {
  title: "Game Times",
  content: <GameTimeDistributionChart />,
  group: "Game",
};

function CastlingPercentageChart() {
  const [data, setData] = useState([{}]);
  const [username, setUsername] = useState("ChaShu");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    (async () => {
      setLoading(true);
      const result = await doApiRequest("/games/CastlingPercentage", {
        username,
      });

      setData(result.players);
      setLoading(false);
    })();
  }, [username]);

  return (
    <>
      <Statistic
        title={`Castling Percentage by ${username}`}
        loading={loading}
        value={
          data[0] && data[0].CastlingPercentage
            ? data[0].CastlingPercentage + "%"
            : "user not found"
        }
      />
      <UsernameSelector onSearch={setUsername} />
    </>
  );
}
export const CastlingPercentage = {
  title: "Castling Percentage",
  content: <CastlingPercentageChart />,
  group: "Game",
};
