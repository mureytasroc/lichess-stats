import React from "react";

const COLORS = {
  YELLOW: "#FFBE0B",
  ORANGE: "#FB5607",
  PINK: "#FF006E",
  PURPLE: "#8338EC",
  BLUE: "#3A86FF",
};

function Screen({ id, title, theme, children }) {
  return (
    <div
      id={id}
      style={{
        scrollSnapAlign: "start",
        width: "100vw",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: theme,
      }}
    >
      <div
        style={{
          width: "80%",
        }}
      >
        <h1 style={{ color: "#FFFFFF", textShadow: "1px 2px 0px black" }}>
          {title}
        </h1>
        {children}
      </div>
    </div>
  );
}

export default Screen;
export { COLORS };
