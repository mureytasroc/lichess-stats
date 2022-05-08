import React, { useEffect, useState } from "react";
import { Menu } from "antd";
import Icon from "@ant-design/icons";

import { ChessIcon, ClockIcon, RatingIcon, WinnerIcon } from "./Icons";

export default function MenuBar({ content, scroll }) {
  const items = [
    {
      key: "-1",
      label: "Cover",
      icon: <Icon component={ChessIcon} />,
    },
    {
      key: "Rating",
      label: "Rating",
      children: [
        ...content
          .map(({ title, group }, index) => ({
            key: index,
            label: title,
            group,
          }))
          .filter((e) => e.group === "Rating"),
      ],
      icon: <Icon component={RatingIcon} />,
    },
    {
      key: "Profile",
      label: "Profile",
      children: [
        ...content
          .map(({ title, group }, index) => ({
            key: index,
            label: title,
            group,
          }))
          .filter((e) => e.group === "Profile"),
      ],
      icon: <Icon component={WinnerIcon} />,
    },
    {
      key: "Game",
      label: "Game",
      children: [
        ...content
          .map(({ title, group }, index) => ({
            key: index,
            label: title,
            group,
          }))
          .filter((e) => e.group === "Game"),
      ],
      icon: <Icon component={ClockIcon} />,
    },
  ];
  const [openKeys, setOpenKeys] = useState([]);
  useEffect(() => {
    if (content && content[scroll - 1]) {
      setOpenKeys([content[scroll - 1].group]);
    }
  }, [scroll]);
  return (
    content && (
      <Menu
        items={items}
        mode="inline"
        onSelect={(e) => {
          window.scrollTo(0, (parseInt(e.key, 10) + 1) * window.innerHeight);
        }}
        selectedKeys={[`${scroll - 1}`]}
        openKeys={openKeys}
        onOpenChange={(e) => setOpenKeys(e)}
      />
    )
  );
}
