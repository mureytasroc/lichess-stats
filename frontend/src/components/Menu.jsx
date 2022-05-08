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
      key: "Profile",
      label: "Profile",
      children: [
        ...content
          .filter((e) => e.group === "Profile")
          .map(({ title }, index) => ({
            key: index,
            label: title,
          })),
      ],
      icon: <Icon component={WinnerIcon} />,
    },
    {
      key: "Game",
      label: "Game",
      children: [
        ...content
          .filter((e) => e.group === "Game")
          .map(({ title }, index) => ({
            key: index,
            label: title,
          })),
      ],
      icon: <Icon component={ClockIcon} />,
    },
    {
      key: "Rating",
      label: "Rating",
      children: [
        ...content
          .filter((e) => e.group === "Rating")
          .map(({ title }, index) => ({
            key: index,
            label: title,
          })),
      ],
      icon: <Icon component={RatingIcon} />,
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
          window.scrollTo(0, (parseInt(e.key) + 1) * window.innerHeight);
        }}
        selectedKeys={[`${scroll - 1}`]}
        openKeys={openKeys}
        onOpenChange={(e) => setOpenKeys(e)}
      />
    )
  );
}
