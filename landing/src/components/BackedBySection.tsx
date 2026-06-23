import type { CSSProperties } from "react";

interface Backer {
  name: string;
  style: CSSProperties;
}

const BACKERS: Backer[] = [
  {
    name: "Gold Markets",
    style: {
      fontFamily: "Times New Roman, serif",
      fontWeight: 400,
      letterSpacing: "0.02em",
      fontSize: "14px",
    },
  },
  {
    name: "Saudi Gold",
    style: {
      fontFamily: "Arial Black, sans-serif",
      fontWeight: 900,
      letterSpacing: "0.08em",
      fontSize: "16px",
    },
  },
  {
    name: "Bullion",
    style: {
      fontFamily: "Impact, sans-serif",
      fontWeight: 700,
      letterSpacing: "0.05em",
      fontSize: "18px",
    },
  },
  {
    name: "Portfolio",
    style: {
      fontFamily: "Georgia, serif",
      fontWeight: 600,
      letterSpacing: "-0.02em",
      fontSize: "17px",
    },
  },
  {
    name: "Analytics",
    style: {
      fontFamily: "Helvetica, sans-serif",
      fontWeight: 700,
      letterSpacing: "-0.01em",
      fontSize: "15px",
    },
  },
  {
    name: "Forecast",
    style: {
      fontFamily: "Verdana, sans-serif",
      fontWeight: 700,
      letterSpacing: "0.06em",
      fontSize: "14px",
      textTransform: "uppercase",
    },
  },
  {
    name: "DeFi",
    style: {
      fontFamily: "Courier New, monospace",
      fontWeight: 700,
      letterSpacing: "0.18em",
      fontSize: "14px",
    },
  },
  {
    name: "Treasury",
    style: {
      fontFamily: "Palatino, serif",
      fontWeight: 500,
      letterSpacing: "0.03em",
      fontSize: "15px",
    },
  },
];

function BackerList() {
  return (
    <>
      {BACKERS.map((backer) => (
        <span
          key={backer.name}
          className="mx-10 shrink-0 text-black/50 whitespace-nowrap"
          style={backer.style}
        >
          {backer.name}
        </span>
      ))}
    </>
  );
}

export default function BackedBySection() {
  return (
    <section className="bg-[#F5F5F5] px-6 py-16">
      <div className="max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 items-center">
        <p className="text-black/70 text-base leading-relaxed whitespace-pre-line">
          Built for gold savers,{"\n"}treasuries, and families.
        </p>
        <div className="md:col-span-3 overflow-hidden">
          <div className="backers-track">
            <BackerList />
            <BackerList />
          </div>
        </div>
      </div>
    </section>
  );
}
