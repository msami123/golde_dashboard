import { ArrowRight } from "lucide-react";

const USE_CASE_VIDEO =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260423_183428_ab5e672a-f608-4dcb-b319-f3e040f02e2d.mp4";

export default function UseCasesSection() {
  return (
    <section id="analytics" className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
        <div className="md:pr-12 md:pt-2">
          <p className="text-black/60 text-sm mb-2">Smart Gold in Practice</p>
          <h2
            className="text-5xl md:text-6xl font-medium leading-none mb-6"
            style={{ letterSpacing: "-0.04em" }}
          >
            Use modes
          </h2>
          <p className="text-black/60 text-base leading-relaxed max-w-sm">
            Smart Gold powers portfolio overview, bar management, shared
            ownership, forecasting, and privacy mode — for individuals and
            families building wealth in physical gold.
          </p>
        </div>

        <div className="relative rounded-3xl overflow-hidden min-h-[720px]">
          <video
            autoPlay
            muted
            loop
            playsInline
            className="absolute inset-0 w-full h-full object-cover"
          >
            <source src={USE_CASE_VIDEO} type="video/mp4" />
          </video>

          <div className="relative z-10 p-10 md:p-12">
            <h3
              className="text-4xl md:text-5xl font-medium leading-tight mb-5"
              style={{ letterSpacing: "-0.03em" }}
            >
              Portfolio
            </h3>
            <p className="text-black/70 text-base max-w-md mb-8">
              Track every gold bar, see live profit and loss, export to CSV or
              Excel, and forecast returns at future price scenarios — all from
              one secure dashboard.
            </p>
            <a
              href="/login"
              className="inline-flex items-center gap-3 text-black font-medium group"
            >
              <span className="w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center group-hover:bg-white transition-colors duration-200">
                <ArrowRight className="w-4 h-4 text-black" />
              </span>
              Know more
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
