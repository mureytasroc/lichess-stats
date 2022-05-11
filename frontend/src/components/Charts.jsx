import React, { useState, useEffect } from "react";
import { Statistic, Spin } from "antd";
import { Bar, Column, Heatmap } from "@ant-design/plots";
import doApiRequest from "../utils/fetch";
import {
  GameTypeSelector,
  DaySelector,
  TitleCountrySelector,
  SlicerSelector,
  UsernameSelector,
  RatingTypeSelector,
} from "../utils/selectors";

const NULL_NAME = "no title";

function TitleDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [slice, setSlice] = useState(0);
  const [data, setData] = useState([]);
  const [type, setType] = useState("title");
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/profile/${type}/distribution`);
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
        `/api/profile/${type}/completion-rate`,
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
      const result = await doApiRequest(`/api/profile/${type}/results`);
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
        .sort((a, b) => b.win_percentage - a.win_percentage)
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
  title: "Game Results %",
  content: <ResultPercentageDistributionChart />,
  group: "Profile",
};

function ResultCountDistributionChart() {
  const [unSlicedData, setUnSlicedData] = useState([]);
  const [slice, setSlice] = useState(0);
  const [data, setData] = useState([]);
  const [type, setType] = useState("title");

  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/profile/${type}/results/counts`);
      if (type === "title") {
        setUnSlicedData(result.titles);
      } else {
        setUnSlicedData(result.countries);
      }
    })();
  }, [type]);

  useEffect(() => {
    if (type === "title") {
      const transformedData = unSlicedData
        .filter(({ title }) => title)
        .flatMap(({ title, win_count, loss_count, draw_count }) => [
          {
            title: title || NULL_NAME,
            value: win_count,
            type: "win count",
          },
          {
            title: title || NULL_NAME,
            value: loss_count,
            type: "loss count",
          },
          {
            title: title || NULL_NAME,
            value: draw_count,
            type: "draw count",
          },
        ]);
      setData(transformedData.sort((a, b) => b.win_count - a.win_count));
    } else {
      const transformedData = unSlicedData
        .sort((a, b) => b.win_count - a.win_count)
        .slice(slice, slice + 10)
        .flatMap(({ country, win_count, loss_count, draw_count }) => [
          {
            country,
            value: win_count,
            type: "win count",
          },
          {
            country,
            value: loss_count,
            type: "loss count",
          },
          {
            country,
            value: draw_count,
            type: "draw count",
          },
        ]);
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
          xField="value"
          yField="title"
          seriesField="type"
        />
      ) : (
        <>
          <Bar
            data={data}
            isStack
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

export const ResultCountDistribution = {
  title: "Game Result Counts",
  content: <ResultCountDistributionChart />,
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
        `/api/profile/${type}/termination-type`,
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
      const result = await doApiRequest(`/api/profile/${type}/game-length`, params);
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

const loadingIndicator = (loading, elt) => loading ? <Spin /> : elt;

export const GameLengthDistribution = {
  title: "Game Lengths",
  content: <GameLengthDistributionChart />,
  group: "Profile",
};

function CastlingPercentageChart() {
  const [data, setData] = useState([{}]);
  const [username, setUsername] = useState("z1z0u");
  const [loading, setLoading] = useState(true);

  const [gameType, setGameType] = useState("All");
  const [startDay, setStartDay] = useState();
  const [endDay, setEndDay] = useState();
  useEffect(() => {
    (async () => {
      setLoading(true);
      const params = {};
      if (gameType !== "All") params.game_type = gameType;
      if (startDay && startDay.length > 0) params.start_date = startDay;
      if (endDay && endDay.length > 0) params.end_date = endDay;
      const result = await doApiRequest("/api/games/castling-percentage", {
        username,
        ...params,
      });
      setData(result.players);
      setLoading(false);
    })();
  }, [username, gameType, startDay, endDay]);

  return (
    <>
      <div style={{ display: "flex", marginBottom: 10 }}>
        <GameTypeSelector handleChange={setGameType} />
        <DaySelector handleChange={setStartDay} />
        <DaySelector handleChange={setEndDay} />
      </div>
      {loadingIndicator(loading, <Statistic
        title={`Castling Percentage by ${username}`}
        loading={loading}
        value={
          data[0] && data[0].castling_percentage
            ? `${data[0].castling_percentage}%`
            : "no data found"
        }
      />)}
      <UsernameSelector onSearch={setUsername} defaultValue="z1z0u" />
    </>
  );
}
export const CastlingPercentage = {
  title: "Castling Percentage",
  content: <CastlingPercentageChart />,
  group: "Game",
};

function CastlingTypePercentageChart() {
  const [data, setData] = useState([{}]);
  const [username, setUsername] = useState("z1z0u");
  const [loading, setLoading] = useState(true);

  const [gameType, setGameType] = useState("All");
  const [startDay, setStartDay] = useState();
  const [endDay, setEndDay] = useState();

  useEffect(() => {
    (async () => {
      setLoading(true);

      const params = {};
      if (gameType !== "All") params.game_type = gameType;
      if (startDay && startDay.length > 0) params.start_date = startDay;
      if (endDay && endDay.length > 0) params.end_date = endDay;

      const result = await doApiRequest("/api/games/castling-side-percentages", {
        username,
        ...params
      });
      setData(result.players.flatMap(
        ({ username: uname, kingside_percentage, queenside_percentage }) =>
          [
            { username: uname, value: kingside_percentage, castle_side: "Kingside" },
            { username: uname, value: queenside_percentage, castle_side: "Queenside" }
          ]
      ));
      setLoading(false);
    })();
  }, [username, gameType, startDay, endDay]);

  return (
    <>
      <div style={{ display: "flex", marginBottom: 10 }}>
        <GameTypeSelector handleChange={setGameType} />
        <DaySelector handleChange={setStartDay} />
        <DaySelector handleChange={setEndDay} />
      </div>
      {loadingIndicator(loading, (data.length > 0 ? (
          <Bar
            data={data}
            loading={loading}
            isStack
            isPercent
            xField="value"
            yField="username"
            seriesField="castle_side"
          />
      ) : <span style={{fontSize: 20, paddingBottom: 10}}>no data found</span>))}
      <UsernameSelector onSearch={setUsername} defaultValue="z1z0u" />
    </>
  );
}
export const CastlingTypePercentage = {
  title: "Ratio of King to Queen Castling",
  content: <CastlingTypePercentageChart />,
  group: "Game",
};

function TimeToWinChart() {
  const [data, setData] = useState([{}]);
  const [username, setUsername] = useState("z1z0u");
  const [loading, setLoading] = useState(true);

  const [gameType, setGameType] = useState("All");
  const [startDay, setStartDay] = useState();
  const [endDay, setEndDay] = useState();

  useEffect(() => {
    (async () => {
      setLoading(true);

      const params = {};
      if (gameType !== "All") params.game_type = gameType;
      if (startDay && startDay.length > 0) params.start_date = startDay;
      if (endDay && endDay.length > 0) params.end_date = endDay;

      const result = await doApiRequest("/api/games/avg-time-to-win", {
        username,
        ...params
      });
      setData(result.players);
      setLoading(false);
    })();
  }, [username, gameType, startDay, endDay]);

  return (
    <>
      <div style={{ display: "flex", marginBottom: 10 }}>
        <GameTypeSelector handleChange={setGameType} />
        <DaySelector handleChange={setStartDay} />
        <DaySelector handleChange={setEndDay} />
      </div>
      {loadingIndicator(loading, <Statistic
        title={`Average time to win by ${username}`}
        loading={loading}
        value={
          data[0] && data[0].avg_time_to_win
            ? `${data[0].avg_time_to_win} seconds`
            : "no data found"
        }
      />)}
      <UsernameSelector onSearch={setUsername} defaultValue="z1z0u" />
    </>
  );
}
export const TimeToWin = {
  title: "Average Time to Win",
  content: <TimeToWinChart />,
  group: "Game",
};

function RatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/rating/${ratingType}/distribution`, {
        bin_size: 100,
      });
      setData(result.bins);
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column data={data} xField="rating_max" yField="count" autoFit />
    </>
  );
}

export const RatingDistribution = {
  title: "Rating Distribution",
  content: <RatingDistributionChart />,
  group: "Rating",
};

function RatingCompareDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/rating/${ratingType}/compare`, {
        bin_size: 300,
      });
      setData(
        result.bins.flatMap(
          ({
            rating_max,
            ultrabullet_rating,
            bullet_rating,
            blitz_rating,
            rapid_rating,
            classical_rating,
            correspondence_rating,
            fide_rating,
            uscf_rating,
            ecf_rating,
          }) => [
            {
              name: "ultrabullet",
              value: ultrabullet_rating,
              rating: rating_max,
            },
            {
              name: "bullet",
              value: bullet_rating,
              rating: rating_max,
            },
            {
              name: "blitz",
              value: blitz_rating,
              rating: rating_max,
            },
            {
              name: "rapid",
              value: rapid_rating,
              rating: rating_max,
            },
            {
              name: "classical",
              value: classical_rating,
              rating: rating_max,
            },
            {
              name: "correspondence",
              value: correspondence_rating,
              rating: rating_max,
            },
            {
              name: "fide",
              value: fide_rating,
              rating: rating_max,
            },
            {
              name: "ecf",
              value: ecf_rating,
              rating: rating_max,
            },
            {
              name: "uscf",
              value: uscf_rating,
              rating: rating_max,
            },
          ]
        )
      );
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column
        data={data}
        isGroup
        xField="rating"
        yField="value"
        seriesField="name"
        autoFit
      />
    </>
  );
}

export const RatingCompareDistribution = {
  title: "Compare Rating",
  content: <RatingCompareDistributionChart />,
  group: "Rating",
};

function TitleByRatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/rating/${ratingType}/title`);
      setData(result.titles.sort((a, b) => b.avg_rating - a.avg_rating));
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column data={data} xField="title" yField="avg_rating" autoFit />
    </>
  );
}

export const TitleByRatingDistribution = {
  title: "Rating by Title",
  content: <TitleByRatingDistributionChart />,
  group: "Rating",
};

function RatingByCountryDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/rating/${ratingType}/country`);
      setData(result.countries.sort((a, b) => b.avg_rating - a.avg_rating));
    })();
  }, [ratingType]);
  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column
        data={data}
        xField="country"
        yField="avg_rating"
        autoFit
        scrollbar={{
          type: "horizontal",
        }}
      />
    </>
  );
}

export const RatingByCountryDistribution = {
  title: "Rating by Country",
  content: <RatingByCountryDistributionChart />,
  group: "Rating",
};

function PlayTimeByRatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/rating/${ratingType}/play-time`, {
        bin_size: 100,
      });
      setData(result.bins);
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column data={data} xField="rating_max" yField="avg_play_time" autoFit />
    </>
  );
}

export const PlayTimeByRatingDistribution = {
  title: "Play Times",
  content: <PlayTimeByRatingDistributionChart />,
  group: "Rating",
};

function PatronsByRatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(
        `/api/rating/${ratingType}/percent-patron`,
        {
          bin_size: 100,
        }
      );
      setData(result.bins);
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column data={data} xField="rating_max" yField="percent_patron" autoFit />
    </>
  );
}

export const PatronsByRatingDistribution = {
  title: "Lichess Patrons",
  content: <PatronsByRatingDistributionChart />,
  group: "Rating",
};

function TOSViolatorsByRatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(
        `/api/rating/${ratingType}/percent-tos-violators`,
        {
          bin_size: 100,
        }
      );
      setData(result.bins);
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column
        data={data}
        xField="rating_max"
        yField="percent_tos_violators"
        autoFit
      />
    </>
  );
}

export const TOSViolatorsByRatingDistribution = {
  title: "TOS Violators",
  content: <TOSViolatorsByRatingDistributionChart />,
  group: "Rating",
};

function CumulativeResultByRatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(
        `/api/rating/${ratingType}/cumulative-result-percentages`,
        {
          bin_size: 100,
        }
      );
      setData(
        result.bins.flatMap(
          ({
            rating_max,
            win_percentage,
            loss_percentage,
            draw_percentage,
          }) => [
            {
              name: rating_max,
              value: loss_percentage,
              type: "win",
            },
            {
              name: rating_max,
              value: loss_percentage,
              type: "loss",
            },
            {
              name: rating_max,
              value: draw_percentage,
              type: "draw",
            },
            {
              name: rating_max,
              value: win_percentage,
              type: "win",
            },
          ]
        )
      );
    })();
  }, [ratingType]);

  return (
    <>
      <RatingTypeSelector handleChange={setRatingType} />
      <Column
        data={data}
        isPercent
        isStack
        xField="name"
        yField="value"
        seriesField="type"
        autoFit
      />
    </>
  );
}

export const CumulativeResultByRatingDistribution = {
  title: "Cumulative Results",
  content: <CumulativeResultByRatingDistributionChart />,
  group: "Rating",
};

function ResultPercentageTwoDimDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(
        `/api/rating/${ratingType}/result-percentages-2d`,
        {
          bin_size: 100,
        }
      );
      setData(
        result.bins.map(
          ({ white_rating_max, black_rating_max, white_win_percentage }) => ({
            white: white_rating_max.toString(),
            black: black_rating_max.toString(),
            white_win_percentage,
          })
        )
      );
    })();
  }, [ratingType]);
  const config = {
    data,
    xField: "white",
    yField: "black",
    colorField: "white_win_percentage",
  };
  return (
    <>
      <GameTypeSelector handleChange={setRatingType} notAll />
      <Heatmap {...config} />
    </>
  );
}

export const ResultPercentageTwoDimDistribution = {
  title: "Result Heat Map",
  content: <ResultPercentageTwoDimDistributionChart />,
  group: "Rating",
};

function NumOpeningByRatingDistributionChart() {
  const [ratingType, setRatingType] = useState("Bullet");
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest(`/api/rating/${ratingType}/num-openings`, {
        bin_size: 100,
      });
      setData(result.bins);
    })();
  }, [ratingType]);

  return (
    <>
      <GameTypeSelector handleChange={setRatingType} notAll />
      <Column data={data} xField="rating_max" yField="num_openings" autoFit />
    </>
  );
}

export const NumOpeningByRatingDistribution = {
  title: "Opening Count",
  content: <NumOpeningByRatingDistributionChart />,
  group: "Rating",
};
