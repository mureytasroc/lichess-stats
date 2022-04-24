import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import "./App.css";
import { doApiRequest } from "./utils/fetch";

function App() {
  const [data, setData] = useState([]);
  useEffect(() => {
    (async () => {
      const result = await doApiRequest("/profile/title/distribution");
      setData(result.titles);
    })();
  }, []);
  return (
    <div className="App">
      <h1>Chess Wins</h1>
      <ResponsiveContainer width="80%" height={600}>
        <BarChart
          width={500}
          height={300}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="title" />
          <YAxis scale="log" domain={[0.8, "auto"]} />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;
