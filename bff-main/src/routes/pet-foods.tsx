import { useState, useEffect } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { motion, AnimatePresence } from "framer-motion";
import { ProductCard } from "@/components/ProductCard";
import { PET_FOODS } from "@/lib/products";
import { FrostParticles } from "@/components/FrostParticles";
import { useTheme } from "@/lib/theme-context";
import PetFoodsLight from "@/components/light/PetFoods.jsx";
import { Wind } from "lucide-react";

export const Route = createFileRoute("/pet-foods")({
  head: () => ({
    meta: [
      { title: "Pet Foods — BFF Bharat Freeze Dry Foods" },
      {
        name: "description",
        content:
          "Explore premium freeze-dried pet foods with real chicken, liver, and salmon. Preserved for your best friend.",
      },
      { property: "og:title", content: "Pet Foods — BFF" },
      {
        property: "og:description",
        content: "Freeze-dried, zero fillers. Premium nutrition for your pets.",
      },
    ],
  }),
  component: PetFoodsPage,
});

function LoopingTypedText({
  text,
  className = "",
  startDelay = 0,
  speed = 100,
  pauseDelay = 2000,
}: {
  text: string;
  className?: string;
  startDelay?: number;
  speed?: number;
  pauseDelay?: number;
}) {
  const [displayed, setDisplayed] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout>;

    if (!isDeleting && displayed === text) {
      timeoutId = setTimeout(() => setIsDeleting(true), pauseDelay);
    } else if (isDeleting && displayed === "") {
      timeoutId = setTimeout(() => setIsDeleting(false), startDelay || 500);
    } else {
      const nextDelay = isDeleting ? speed / 2 : speed;
      timeoutId = setTimeout(() => {
        setDisplayed(current => {
          if (isDeleting) return current.slice(0, -1);
          return text.slice(0, current.length + 1);
        });
      }, nextDelay);
    }

    return () => clearTimeout(timeoutId);
  }, [displayed, isDeleting, text, speed, pauseDelay, startDelay]);

  return (
    <span className={className}>
      {displayed}
      <span
        className="ml-1 inline-block w-[3px] translate-y-[3px] bg-ice-blue animate-pulse"
        style={{ height: "0.85em" }}
        aria-hidden
      />
    </span>
  );
}

function PetFoodsPage() {
  const { theme } = useTheme();

  if (theme === "light") {
    return (
      <main>
        <section style={{ position: 'relative', padding: '140px 0 100px', display: 'flex', alignItems: 'center', overflow: 'hidden', background: 'linear-gradient(135deg, #081A0C 0%, #0D2314 50%, #0A1A0A 100%)' }}>
          <video autoPlay muted loop playsInline preload="metadata" style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: '85% center', opacity: 0.70 }}>
            <source src="/bff-pet.mp4" type="video/mp4" />
          </video>
          <div className="video-overlay" style={{ position: 'absolute', inset: 0, background: 'rgba(5,15,8,0.12)', zIndex: 1 }} />
          <div style={{ position: 'relative', zIndex: 10, paddingLeft: 'max(20px, 4vw)', maxWidth: '840px' }}>
            <div className="hero-label-anim" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '6px 16px', background: 'rgba(139,195,74,0.15)', border: '1px solid rgba(139,195,74,0.3)', borderRadius: '9999px', marginBottom: '36px' }}>
              <Wind size={13} color="#8BC34A" />
              <span style={{ fontFamily: 'var(--font-display)', fontSize: '11px', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#C5E1A5' }}>Premium Pet Nutrition</span>
            </div>
            <h1 className="hero-h1-anim" style={{ fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: 'clamp(44px, 7vw, 108px)', lineHeight: 1.02, letterSpacing: '-0.04em', color: 'white', marginBottom: '28px' }}>
              For Your{' '}<span style={{ background: 'linear-gradient(135deg, #8BC34A 0%, #C5E1A5 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>Best Friend.</span>
            </h1>
            <p className="hero-p-anim" style={{ fontFamily: 'var(--font-body)', fontSize: 'clamp(15px, 1.8vw, 21px)', fontWeight: 300, lineHeight: 1.72, color: 'rgba(255,255,255,0.70)', maxWidth: '600px' }}>
              Hover any pack to reveal the fresh ingredient inside. On mobile, tap the card.
            </p>
          </div>
        </section>
        <PetFoodsLight />
      </main>
    );
  }

  // Dark theme
  return (
    <div className="relative">
      {/* Header */}
      <section className="relative flex min-h-[60svh] w-full items-center justify-center overflow-hidden bg-deep-navy pt-24 pb-16">
        <video
          className="absolute inset-0 h-full w-full object-cover motion-reduce:hidden"
          src="/bff-pet.mp4"
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
        />
        <div className="absolute inset-0 bg-black/50" />
        <div className="absolute inset-0 bg-gradient-to-b from-deep-navy/60 via-deep-navy/30 to-background" />

        <FrostParticles count={25} />

        <div className="relative z-10 mx-auto max-w-7xl px-6 text-center">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-eyebrow mb-4"
          >
            Premium Pet Nutrition
          </motion.p>
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.15 }}
            className="text-display text-5xl text-frost-white sm:text-6xl md:text-7xl"
          >
            For your <br />
            <LoopingTypedText
              text="best friend."
              className="text-gradient-ice italic font-medium"
              startDelay={600}
              speed={150}
              pauseDelay={2500}
            />
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.35 }}
            className="mx-auto mt-6 max-w-2xl text-base text-steel-silver sm:text-lg text-shadow-sm"
          >
            Hover any pack to reveal the fresh ingredient inside. On mobile, tap the card.
          </motion.p>
        </div>
      </section>

      {/* Grid */}
      <section className="bg-background py-16 min-h-[50vh]">
        <div className="mx-auto max-w-7xl px-6">
          <AnimatePresence mode="popLayout">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
            >
              {PET_FOODS.map((p) => (
                <motion.div
                  key={p.id}
                  layout
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <ProductCard product={p} />
                </motion.div>
              ))}
            </motion.div>
          </AnimatePresence>
          {PET_FOODS.length === 0 && (
            <p className="py-16 text-center text-steel-silver">No pet foods available right now.</p>
          )}
        </div>
      </section>
    </div>
  );
}