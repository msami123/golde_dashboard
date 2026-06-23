import {
  TrendingUp,
  BarChart3,
  Users,
  LineChart,
  FileText,
  Bell,
  Cloud,
} from "lucide-react";

const FEATURES = [
  { icon: TrendingUp, title: "Live Gold Prices", desc: "Real-time SAR gold prices with smart caching and manual refresh." },
  { icon: BarChart3, title: "Portfolio Tracking", desc: "Track every bar, cost per gram, and total portfolio value automatically." },
  { icon: LineChart, title: "Profit & Loss", desc: "Instant P/L calculations with return percentages for each holding." },
  { icon: Users, title: "Shared Ownership", desc: "Manage jointly owned bars with participant breakdowns." },
  { icon: TrendingUp, title: "Forecast Scenarios", desc: "Simulate future gold prices and projected portfolio returns." },
  { icon: FileText, title: "Reports", desc: "Export your full portfolio to CSV or Excel in one click." },
  { icon: Bell, title: "Alerts", desc: "Price and portfolio alerts — coming soon." },
  { icon: Cloud, title: "Secure Cloud", desc: "Your data stored securely with encrypted authentication." },
];

export default function FeaturesSection() {
  return (
    <section id="features" className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-[88rem] mx-auto">
        <h2 className="text-black text-4xl md:text-5xl font-medium leading-tight mb-4" style={{ letterSpacing: "-0.03em" }}>
          Everything you need
        </h2>
        <p className="text-black/60 text-lg max-w-lg mb-14">A complete gold portfolio platform — not just a price tracker.</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {FEATURES.map((f) => (
            <div key={f.title} className="bg-white border border-gray-200 rounded-2xl p-7 hover:shadow-md transition-shadow duration-200">
              <f.icon className="w-6 h-6 text-black mb-4" strokeWidth={1.5} />
              <h3 className="text-black text-lg font-medium mb-2" style={{ letterSpacing: "-0.02em" }}>{f.title}</h3>
              <p className="text-black/60 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
