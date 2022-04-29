import React from "react";

export default function Menu({ content }) {
  return (
    <div style={{ position: "fixed" }}>
      {content.map((element, index) => (
        <div>
          <a key={index} href={`#${index}`}>
            {element.title}
          </a>
        </div>
      ))}
    </div>
  );
}
