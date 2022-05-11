import React from "react";
import { Select, DatePicker, Slider, Input } from "antd";

const { Option } = Select;
const { Search } = Input;

export function GameTypeSelector({ handleChange, notAll }) {
  return (
    <Select
      defaultValue={notAll ? "Bullet" : "All"}
      style={{ width: 120 }}
      onChange={handleChange}
    >
      {!notAll && <Option value="All">All</Option>}
      <Option value="UltraBullet">UltraBullet</Option>
      <Option value="Bullet">Bullet</Option>
      <Option value="Blitz">Blitz</Option>
      <Option value="Rapid">Rapid</Option>
      <Option value="Classical">Classical</Option>
      <Option value="Correspondence">Correspondence</Option>
    </Select>
  );
}

export function RatingTypeSelector({ handleChange }) {
  return (
    <Select
      defaultValue="Bullet"
      style={{ width: 120 }}
      onChange={handleChange}
    >
      <Option value="UltraBullet">UltraBullet</Option>
      <Option value="Bullet">Bullet</Option>
      <Option value="Blitz">Blitz</Option>
      <Option value="Rapid">Rapid</Option>
      <Option value="Classical">Classical</Option>
      <Option value="Correspondence">Correspondence</Option>
      <Option value="FIDE">FIDE</Option>
      <Option value="USCF">USCF</Option>
      <Option value="ECF">ECF</Option>
    </Select>
  );
}

export function DaySelector({ handleChange }) {
  return <DatePicker onChange={(_, e) => handleChange(e)} />;
}

export function TitleCountrySelector({ handleChange }) {
  return (
    <Select defaultValue="title" style={{ width: 120 }} onChange={handleChange}>
      <Option value="title">Title</Option>
      <Option value="country">Country</Option>
    </Select>
  );
}

export function SlicerSelector({ length, handleChange }) {
  return (
    <div style={{ display: "flex", width: "100%" }}>
      <div style={{ width: "20%" }}>Country Selector</div>
      <div style={{ width: "80%" }}>
        <Slider min={0} max={length - 10} onChange={handleChange} />
      </div>
    </div>
  );
}

export function RatingRangeSelector({ handleChange }) {
  return (
    <div style={{ display: "flex", width: "100%" }}>
      <div style={{ width: "20%" }}>Elo Range Selector</div>
      <div style={{ width: "80%" }}>
        <Slider
          min={0}
          max={3000}
          defaultValue={[0, 3000]}
          range
          onAfterChange={handleChange}
        />
      </div>
    </div>
  );
}

export function UsernameSelector({ onSearch, defaultValue }) {
  return (
    <Search
      placeholder="input username"
      allowClear
      enterButton="Search"
      size="large"
      onSearch={onSearch}
      defaultValue={defaultValue}
    />
  );
}
