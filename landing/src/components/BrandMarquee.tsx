import type { CSSProperties } from "react";

interface Brand {
  name: string;
  style: CSSProperties;
}

const BRANDS: Brand[] = [
  {
    name: "GoldAPI",
    style: {
      fontFamily: "Georgia, serif",
      fontWeight: 700,
      letterSpacing: "-0.02em",
      fontSize: "15px",
    },
  },
  {
    name: "SAR",
    style: {
      fontFamily: "Arial, sans-serif",
      fontWeight: 900,
      letterSpacing: "0.08em",
      fontSize: "13px",
      textTransform: "uppercase",
    },
  },
  {
    name: "DeFi",
    style: {
      fontFamily: "Trebuchet MS, sans-serif",
      fontWeight: 600,
      letterSpacing: "0.01em",
      fontSize: "15px",
      fontStyle: "italic",
    },
  },
  {
    name: "Bullion",
    style: {
      fontFamily: "Courier New, monospace",
      fontWeight: 700,
      letterSpacing: "0.12em",
      fontSize: "13px",
      textTransform: "uppercase",
    },
  },
  {
    name: "Portfolio",
    style: {
      fontFamily: "Palatino, 'Book Antiqua', serif",
      fontWeight: 400,
      letterSpacing: "-0.01em",
      fontSize: "16px",
    },
  },
  {
    name: "Analytics",
    style: {
      fontFamily: "Impact, 'Arial Narrow', sans-serif",
      fontWeight: 400,
      letterSpacing: "0.04em",
      fontSize: "14px",
    },
  },
  {
    name: "Forecast",
    style: {
      fontFamily: "Verdana, sans-serif",
      fontWeight: 700,
      letterSpacing: "-0.03em",
      fontSize: "13px",
    },
  },
];

function BrandList() {
  return (
    <>
      {BRANDS.map((brand) => (
        <span
          key={brand.name}
          className="mx-7 shrink-0 text-black/60 whitespace-nowrap"
          style={brand.style}
        >
          {brand.name}
        </span>
      ))}
    </>
  );
}

export default function BrandMarquee() {
  return (
    <div className="mt-24 w-full max-w-md overflow-hidden">
      <div className="marquee-track">
        <BrandList />
        <BrandList />
      </div>
    </div>
  );
}
