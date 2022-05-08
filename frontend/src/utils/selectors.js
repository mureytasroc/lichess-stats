import { Select, DatePicker } from "antd";

const { Option } = Select;

export function GameTypeSelector({ handleChange }) {
  return (
    <Select defaultValue="All" style={{ width: 120 }} onChange={handleChange}>
      <Option value="All">All</Option>
      <Option value="UltraBullet">UltraBullet</Option>
      <Option value="Bullet">Bullet</Option>
      <Option value="Blitz">Blitz</Option>
      <Option value="Rapid">Rapid</Option>
      <Option value="Classical">Classical</Option>
      <Option value="Correspondence">Correspondence</Option>
    </Select>
  );
}

export function MonthYearSelector({ handleChange }) {
  return <DatePicker onChange={(_, e) => handleChange(e)} picker="month" />;
}
