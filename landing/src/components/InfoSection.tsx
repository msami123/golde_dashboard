import PillButton from "./PillButton";

const INFO_IMAGE =
  "https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260423_164207_f243351d-ed59-48ec-83a0-a5e996bdbe3c.png&w=1280&q=85";

export default function InfoSection() {
  return (
    <section id="portfolio" className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-[88rem] mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-16 items-start">
          <div>
            <h2
              className="text-black text-4xl md:text-5xl font-medium leading-tight mb-8"
              style={{ letterSpacing: "-0.03em" }}
            >
              Meet Smart Gold.
            </h2>
            <PillButton href="/login" className="text-base">
              Open dashboard
            </PillButton>
          </div>
          <p className="text-black/70 text-2xl md:text-3xl leading-relaxed">
            A personal gold portfolio that tracks every bar, live SAR prices, and
            your profit — all in one place.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div
            className="lg:col-span-2 rounded-2xl overflow-hidden min-h-80 flex flex-col justify-between p-7"
            style={{
              backgroundImage: `url(${INFO_IMAGE})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          >
            <h3
              className="text-black text-2xl font-medium leading-snug"
              style={{ letterSpacing: "-0.02em" }}
            >
              Savings that bloom
            </h3>
            <p className="text-black/70 text-base max-w-xs">
              Watch your portfolio value grow as live gold prices update and
              every bar&apos;s profit is calculated automatically.
            </p>
          </div>

          <div className="bg-[#2B2644] rounded-2xl p-7 min-h-80 flex flex-col justify-between">
            <h3 className="text-white text-2xl font-medium leading-snug whitespace-pre-line">
              Always live,{"\n"}always SAR.
            </h3>
            <p className="text-white/60 text-base">
              Real-time gold prices in Saudi Riyals with manual refresh to
              conserve your API quota — no guesswork.
            </p>
          </div>

          <div className="bg-[#2B2644] rounded-2xl p-7 min-h-80 flex flex-col justify-between">
            <h3 className="text-white text-2xl font-medium leading-snug whitespace-pre-line">
              Fully{"\n"}automated
            </h3>
            <p className="text-white/60 text-base">
              Skip spreadsheets and manual math. Smart Gold tracks cost per gram,
              returns, and forecasts in the background.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
