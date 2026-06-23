import { useState } from "react";
import { ChevronDown } from "lucide-react";

const FAQS = [
  { q: "What is Smart Gold?", a: "Smart Gold is a premium gold portfolio management platform. Track bars, live SAR prices, profit/loss, shared ownership, and forecasts — all in one place." },
  { q: "How are gold prices fetched?", a: "Prices come from GoldAPI in Saudi Riyals. We cache prices smartly and only refresh when you click — saving your monthly API quota." },
  { q: "Can I share ownership of a bar?", a: "Yes. Add participants with ownership percentages. Smart Gold calculates each person's grams, cost, and profit automatically." },
  { q: "Is my data secure?", a: "Yes. Passwords are bcrypt-hashed, sessions are encrypted, and privacy mode hides sensitive amounts when sharing your screen." },
  { q: "Can I export my portfolio?", a: "Export to CSV or Excel anytime from the Reports page. All your bar data, costs, and returns are included." },
];

export default function FAQSection() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section id="faq" className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-4xl font-medium text-center mb-12" style={{ letterSpacing: "-0.03em" }}>FAQ</h2>
        {FAQS.map((faq, i) => (
          <div key={i} className="border-b border-gray-200">
            <button
              type="button"
              className="w-full flex items-center justify-between py-5 text-left font-medium text-black"
              onClick={() => setOpen(open === i ? null : i)}
            >
              {faq.q}
              <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform duration-200 ${open === i ? "rotate-180" : ""}`} />
            </button>
            {open === i && (
              <p className="pb-5 text-black/60 text-sm leading-relaxed">{faq.a}</p>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
