import LogoIcon from "./LogoIcon";

export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 px-6 py-16">
      <div className="max-w-[88rem] mx-auto grid grid-cols-1 md:grid-cols-4 gap-10">
        <div className="md:col-span-2">
          <div className="flex items-center gap-2 mb-4">
            <LogoIcon className="w-6 h-6 text-black" />
            <span className="text-lg font-medium">Smart Gold</span>
          </div>
          <p className="text-black/60 text-sm max-w-xs leading-relaxed">
            Premium gold portfolio management for savers, families, and treasuries.
          </p>
        </div>
        <div>
          <h4 className="font-medium text-sm mb-4">Product</h4>
          <ul className="space-y-2 text-sm text-black/60">
            <li><a href="#features" className="hover:text-black transition-colors">Features</a></li>
            <li><a href="#preview" className="hover:text-black transition-colors">Dashboard</a></li>
            <li><a href="#pricing" className="hover:text-black transition-colors">Pricing</a></li>
            <li><a href="/login" className="hover:text-black transition-colors">Open Wallet</a></li>
          </ul>
        </div>
        <div>
          <h4 className="font-medium text-sm mb-4">Legal</h4>
          <ul className="space-y-2 text-sm text-black/60">
            <li><a href="#" className="hover:text-black transition-colors">Privacy</a></li>
            <li><a href="#" className="hover:text-black transition-colors">Terms</a></li>
            <li><a href="#faq" className="hover:text-black transition-colors">FAQ</a></li>
          </ul>
        </div>
      </div>
      <div className="max-w-[88rem] mx-auto mt-12 pt-8 border-t border-gray-100 text-center text-sm text-black/40">
        © {new Date().getFullYear()} Smart Gold. All rights reserved.
      </div>
    </footer>
  );
}
