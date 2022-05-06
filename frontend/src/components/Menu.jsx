import React from "react";

export default function Menu({ content }) {
  return (
    <div style={{ position: "fixed", left: 5, top: 5 }}>
      <div key={"MenuItemTitle"}>
        <a href={`#Title`}>{"Title"}</a>
      </div>
      {content.map((element, index) => (
        <div key={`MenuItem${index}`}>
          <a href={`#${index}`}>{element.title}</a>
        </div>
      ))}
    </div>
  );
}
