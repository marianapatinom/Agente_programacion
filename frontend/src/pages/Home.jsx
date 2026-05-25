import ChatBox from "../components/ChatBox.jsx";
import Footer from "../components/Footer.jsx";
import Hero from "../components/Hero.jsx";
import Navbar from "../components/Navbar.jsx";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#080d18] text-white">
      <div className="fixed inset-0 -z-10 bg-[linear-gradient(180deg,rgba(15,23,42,0.2),rgba(8,13,24,1)),linear-gradient(90deg,rgba(34,211,238,0.06),transparent_38%,rgba(16,185,129,0.05))]" />
      <Navbar />
      <main>
        <Hero />
        <ChatBox />
      </main>
      <Footer />
    </div>
  );
}
