import { Shield, Zap, Lock, BarChart2, Gem } from "lucide-react";

const REASONS = [
  { icon: Zap, title: "Simplicity", desc: "Add a bar in seconds. No spreadsheets, no manual math." },
  { icon: Gem, title: "Automation", desc: "Prices, profits, and forecasts update without your input." },
  { icon: Lock, title: "Security", desc: "Encrypted sessions, bcrypt passwords, and privacy mode." },
  { icon: BarChart2, title: "Professional analytics", desc: "Charts and metrics worthy of a fintech product." },
  { icon: Shield, title: "Premium experience", desc: "Designed like Stripe or Mercury — not a hobby tracker." },
];

export default function WhyChooseUs() {
  return (
    <section className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-[88rem] mx-auto">
        <h2 className="text-4xl md:text-5xl font-medium text-center mb-14" style={{ letterSpacing: "-0.03em" }}>
          Why Smart Gold?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {REASONS.map((r) => (
            <div key={r.title} className="text-center">
              <div className="w-12 h-12 bg-white border border-gray-200 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm">
                <r.icon className="w-5 h-5 text-black" strokeWidth={1.5} />
              </div>
              <h3 className="font-medium text-black mb-2">{r.title}</h3>
              <p className="text-sm text-black/60 leading-relaxed">{r.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
