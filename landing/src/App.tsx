import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import InfoSection from "./components/InfoSection";
import FeaturesSection from "./components/FeaturesSection";
import DashboardPreview from "./components/DashboardPreview";
import AnalyticsSection from "./components/AnalyticsSection";
import BackedBySection from "./components/BackedBySection";
import WhyChooseUs from "./components/WhyChooseUs";
import UseCasesSection from "./components/UseCasesSection";
import PricingSection from "./components/PricingSection";
import FAQSection from "./components/FAQSection";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="flex flex-col bg-[#F5F5F5]">
      <div className="h-screen flex flex-col overflow-hidden">
        <Navbar />
        <HeroSection />
      </div>
      <InfoSection />
      <FeaturesSection />
      <DashboardPreview />
      <AnalyticsSection />
      <BackedBySection />
      <WhyChooseUs />
      <UseCasesSection />
      <PricingSection />
      <FAQSection />
      <Footer />
    </div>
  );
}
