import React from "react";
import styles from "./Screen.module.css";

const COLORS = {
  YELLOW: "#FFBE0B",
  ORANGE: "#FB5607",
  PINK: "#FF006E",
  PURPLE: "#8338EC",
  BLUE: "#3A86FF",
  WHITE: "#dde1e7",
};

function Screen({ id, title, theme, randomColor, children, floating }) {
  let keys = Object.keys(COLORS);
  const color = COLORS[keys[(keys.length * Math.random()) << 0]];

  return (
    <div
      id={id}
      className={styles.Container}
      style={{ backgroundColor: randomColor ? color : theme }}
    >
      <div className={styles.InnerContainer}>
        <h1 className={styles.Title}>{title}</h1>
        <div className={floating ? styles.floating : ""}>{children}</div>
      </div>
    </div>
  );
}

export default Screen;
export { COLORS };
