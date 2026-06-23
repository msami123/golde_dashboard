import PillButton from "./PillButton";
import BrandMarquee from "./BrandMarquee";

const HERO_VIDEO =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_161253_c72b1869-400f-45ed-ac0c-52f68c2ed5bd.mp4";

export default function HeroSection() {
  return (
    <section className="flex-1 px-6 pt-20 pb-6 flex items-end">
      <div className="max-w-[88rem] mx-auto w-full">
        <div
          className="relative w-full rounded-2xl overflow-hidden"
          style={{ height: "calc(100vh - 96px)" }}
        >
          <video
            autoPlay
            muted
            loop
            playsInline
            className="absolute inset-0 w-full h-full object-cover"
          >
            <source src={HERO_VIDEO} type="video/mp4" />
          </video>

          <div className="relative z-10 flex flex-col items-start justify-start h-full p-12 pt-36">
            <h1
              className="text-black text-5xl md:text-6xl font-medium leading-tight max-w-xl mb-4"
              style={{ letterSpacing: "-0.04em" }}
            >
              Your Gold
              <br />
              Grows
            </h1>
            <p
              className="text-black/70 text-base md:text-lg max-w-md mb-8 leading-relaxed"
              style={{
                fontFamily: "'Inter', ui-sans-serif, system-ui, sans-serif",
              }}
            >
              A smart gold portfolio dashboard with live SAR prices, profit
              tracking, and effortless management of your bars and shared
              ownership.
            </p>
            <PillButton href="/login">Get started</PillButton>
            <BrandMarquee />
          </div>
        </div>
      </div>
    </section>
  );
}
