import { Calculator, Activity, History, Sparkles } from "lucide-react";

const ITEMS = [
  { icon: Calculator, title: "Automatic calculations", desc: "Cost per gram, returns, and portfolio totals computed in real time." },
  { icon: Activity, title: "Live tracking", desc: "Gold prices update on demand with full API usage transparency." },
  { icon: History, title: "Historical performance", desc: "Portfolio growth charts show invested capital vs current value." },
  { icon: Sparkles, title: "Future forecasting", desc: "Test scenarios from 400 to 700 SAR per gram and beyond." },
];

export default function AnalyticsSection() {
  return (
    <section id="analytics" className="bg-white px-6 py-24 border-y border-gray-100">
      <div className="max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
        <div>
          <p className="text-black/60 text-sm mb-2">Analytics</p>
          <h2 className="text-4xl md:text-5xl font-medium leading-tight mb-6" style={{ letterSpacing: "-0.03em" }}>
            Professional-grade insights
          </h2>
          <p className="text-black/60 text-base leading-relaxed max-w-md">
            Every calculation runs automatically. You focus on your gold — we handle the math.
          </p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {ITEMS.map((item) => (
            <div key={item.title} className="bg-[#F5F5F5] rounded-2xl p-6">
              <item.icon className="w-5 h-5 text-black mb-3" strokeWidth={1.5} />
              <h3 className="font-medium text-black mb-1">{item.title}</h3>
              <p className="text-sm text-black/60">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
