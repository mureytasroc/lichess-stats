import React, { useEffect, useState } from "react";
import { Menu } from "antd";

export default function MenuBar({ content, scroll }) {
  const items = [
    {
      key: "-1",
      label: "Cover",
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
    },
    {
      key: "Player",
      label: "Player",
      children: [
        ...content
          .filter((e) => e.group === "Player")
          .map(({ title }, index) => ({
            key: index,
            label: title,
          })),
      ],
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
        onSelect={(e) => window.scrollTo(0, (e.key + 1) * window.innerHeight)}
        selectedKeys={[`${scroll - 1}`]}
        openKeys={openKeys}
        onOpenChange={(e) => setOpenKeys(e)}
      />
    )
  );
}
