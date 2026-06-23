import { ArrowRight } from "lucide-react";
import type { ReactNode } from "react";

interface PillButtonProps {
  children: ReactNode;
  href?: string;
  className?: string;
}

export default function PillButton({
  children,
  href = "/login",
  className = "",
}: PillButtonProps) {
  return (
    <a
      href={href}
      className={`inline-flex items-center gap-3 bg-black text-white text-base md:text-lg font-medium pl-8 pr-2 py-2 rounded-full hover:bg-gray-800 transition-colors duration-200 ${className}`}
    >
      {children}
      <span className="bg-white rounded-full p-2 flex items-center justify-center">
        <ArrowRight className="w-5 h-5 text-black" />
      </span>
    </a>
  );
}
