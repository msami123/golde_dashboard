const PLANS = [
  {
    name: "Free",
    price: "0",
    desc: "Perfect for getting started with gold tracking.",
    features: ["Up to 10 gold bars", "Live gold prices", "Portfolio overview", "CSV export"],
    featured: false,
  },
  {
    name: "Pro",
    price: "29",
    desc: "For serious gold savers and families.",
    features: ["Unlimited bars", "Forecast scenarios", "Shared ownership", "Excel export", "Analytics"],
    featured: true,
  },
  {
    name: "Premium",
    price: "79",
    desc: "For treasuries and power users.",
    features: ["Everything in Pro", "Price alerts", "Monthly reports", "Priority support", "API access"],
    featured: false,
  },
];

export default function PricingSection() {
  return (
    <section id="pricing" className="bg-white px-6 py-24 border-t border-gray-100">
      <div className="max-w-[88rem] mx-auto">
        <h2 className="text-4xl md:text-5xl font-medium text-center mb-4" style={{ letterSpacing: "-0.03em" }}>Pricing</h2>
        <p className="text-black/60 text-center mb-14">Design preview — payments not yet implemented.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {PLANS.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-2xl p-8 border ${plan.featured ? "border-black shadow-lg bg-white" : "border-gray-200 bg-[#F5F5F5]"}`}
            >
              <h3 className="text-lg font-medium mb-1">{plan.name}</h3>
              <p className="text-3xl font-medium mb-1" style={{ letterSpacing: "-0.03em" }}>
                {plan.price === "0" ? "Free" : `$${plan.price}`}
                {plan.price !== "0" && <span className="text-sm text-black/50 font-normal">/mo</span>}
              </p>
              <p className="text-sm text-black/60 mb-6">{plan.desc}</p>
              <ul className="space-y-2 mb-8">
                {plan.features.map((f) => (
                  <li key={f} className="text-sm text-black/70 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-black/30" />{f}
                  </li>
                ))}
              </ul>
              <a
                href="/login"
                className={`block text-center py-2.5 rounded-full text-sm font-medium transition-colors duration-200 ${
                  plan.featured ? "bg-black text-white hover:bg-gray-800" : "bg-white border border-gray-200 text-black hover:bg-gray-50"
                }`}
              >
                Get started
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
