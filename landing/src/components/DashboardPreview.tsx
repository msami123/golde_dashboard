export default function DashboardPreview() {
  return (
    <section id="preview" className="bg-[#F5F5F5] px-6 py-24">
      <div className="max-w-[88rem] mx-auto">
        <h2 className="text-black text-4xl md:text-5xl font-medium leading-tight mb-4 text-center" style={{ letterSpacing: "-0.03em" }}>
          Your portfolio, at a glance
        </h2>
        <p className="text-black/60 text-center mb-12 max-w-md mx-auto">A real dashboard preview — not a mockup placeholder.</p>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-lg overflow-hidden max-w-5xl mx-auto">
          <div className="flex items-center gap-2 px-5 py-3 border-b border-gray-100 bg-gray-50">
            <div className="w-3 h-3 rounded-full bg-gray-300" />
            <div className="w-3 h-3 rounded-full bg-gray-300" />
            <div className="w-3 h-3 rounded-full bg-gray-300" />
            <span className="ml-3 text-xs text-gray-400 font-medium">Smart Gold Dashboard</span>
          </div>
          <div className="p-8">
            <p className="text-sm text-gray-500 mb-1">Portfolio Value</p>
            <p className="text-4xl font-medium text-black mb-6" style={{ letterSpacing: "-0.04em" }}>22,909.3 SAR</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              {[
                { label: "Total Gold", value: "45 g" },
                { label: "Today's P/L", value: "-2,985.7 SAR", neg: true },
                { label: "Gold Price", value: "509.1 SAR/g" },
                { label: "Return", value: "-11.5%", neg: true },
              ].map((s) => (
                <div key={s.label} className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                  <p className="text-xs text-gray-500 mb-1">{s.label}</p>
                  <p className={`text-lg font-medium ${s.neg ? "text-red-500" : "text-black"}`}>{s.value}</p>
                </div>
              ))}
            </div>
            <div className="h-32 bg-gradient-to-r from-gray-100 to-gray-50 rounded-xl border border-gray-100 flex items-end px-4 pb-4 gap-1">
              {[40, 55, 45, 70, 60, 80, 75, 90, 85, 95].map((h, i) => (
                <div key={i} className="flex-1 bg-black/10 rounded-t" style={{ height: `${h}%` }} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
