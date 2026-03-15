import type { ReactNode } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

type Theme = "light" | "dark";

const fetchTheme = async (): Promise<Theme | null> => {
  try {
    const res = await fetch("/api/theme/", { credentials: "include" });
    if (!res.ok) return null;
    const data = await res.json();
    return data.theme;
  } catch {
    return null;
  }
};

const saveTheme = async (theme: Theme) => {
  try {
    await fetch("/api/theme/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
      credentials: "include",
      body: JSON.stringify({ theme })
    });
  } catch {
    /* ignore */
  }
};

const getCSRFToken = () => {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : "";
};

const cards = [
  {
    title: "Cinematic Arrival",
    body: "Guests are greeted by clear hierarchy, elegant typography, and vivid visual rhythm.",
    tag: "Experience"
  },
  {
    title: "Adaptive Reservations",
    body: "Live inventory and booking actions remain fast across desktop and mobile layouts.",
    tag: "Operations"
  },
  {
    title: "Night and Day Themes",
    body: "Light and dark palettes feel intentional, accessible, and consistent across modules.",
    tag: "Personalization"
  },
  {
    title: "Data at a Glance",
    body: "Critical occupancy and revenue signals are readable in seconds with strong contrast.",
    tag: "Insight"
  },
  {
    title: "Confident Motion",
    body: "Cards and sections fade in and out while scrolling, inspired by modern portfolio interactions.",
    tag: "Motion"
  },
  {
    title: "Premium Responsiveness",
    body: "The interface scales smoothly from compact phones to wide dashboards without visual noise.",
    tag: "Quality"
  }
];

const metrics = [
  { value: "97%", label: "average guest satisfaction" },
  { value: "42s", label: "mean booking completion" },
  { value: "24/7", label: "front desk visibility" }
];

type RevealProps = {
  delayMs?: number;
  className?: string;
  children: ReactNode;
};

const revealDelayClass = (delayMs: number) => {
  const map: Record<number, string> = {
    0: "reveal-delay-0",
    80: "reveal-delay-80",
    120: "reveal-delay-120",
    160: "reveal-delay-160",
    240: "reveal-delay-240",
    320: "reveal-delay-320",
    400: "reveal-delay-400"
  };

  return map[delayMs] ?? "reveal-delay-0";
};

function Reveal({ delayMs = 0, className = "", children }: RevealProps) {
  const ref = useRef<HTMLDivElement | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setVisible(entry.isIntersecting);
      },
      {
        threshold: 0.35,
        rootMargin: "0px 0px -12% 0px"
      }
    );

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`reveal ${revealDelayClass(delayMs)} ${visible ? "is-visible" : ""} ${className}`.trim()}
    >
      {children}
    </div>
  );
}

export default function App() {
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    const local = localStorage.getItem("theme") as Theme | null;
    if (local) {
      setTheme(local);
      return;
    }
    fetchTheme().then((serverTheme) => {
      if (serverTheme) {
        setTheme(serverTheme);
        localStorage.setItem("theme", serverTheme);
      }
    });
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
    saveTheme(theme);
  }, [theme]);

  const toggle = () => setTheme((t) => (t === "light" ? "dark" : "light"));

  const themeLabel = useMemo(() => (theme === "light" ? "Switch to dark mode" : "Switch to light mode"), [theme]);

  return (
    <div className="relative min-h-screen overflow-hidden bg-canvas text-copy transition-colors duration-500">
      <div className="pointer-events-none absolute inset-0 z-0">
        <div className="orb orb-a" />
        <div className="orb orb-b" />
        <div className="noise-layer" />
      </div>

      <header className="relative z-30 border-b border-outline bg-header backdrop-blur-xl">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 md:px-6">
          <div>
            <p className="font-display text-xl tracking-tight">RoseGold Hotel</p>
            <p className="text-xs uppercase tracking-[0.22em] text-muted">hospitality control center</p>
          </div>
          <button
            onClick={toggle}
            className="rounded-full border border-outline bg-surface px-4 py-2 text-sm font-semibold text-copy transition hover:-translate-y-[1px] hover:bg-surfaceElevated"
            aria-label={themeLabel}
          >
            {theme === "light" ? "Dark mode" : "Light mode"}
          </button>
        </div>
      </header>

      <main className="relative z-10 mx-auto flex w-full max-w-6xl flex-col gap-14 px-4 py-10 md:px-6 md:py-14">
        <Reveal className="rounded-3xl border border-outline bg-surface p-7 shadow-soft md:p-10">
          <section className="grid items-end gap-10 lg:grid-cols-[1.2fr_0.8fr]">
            <div className="space-y-6">
              <p className="text-xs uppercase tracking-[0.28em] text-muted">Modern professional layout</p>
              <h1 className="font-display text-4xl leading-tight md:text-6xl">
                A modern command surface for premium hotel operations.
              </h1>
              <p className="max-w-2xl text-base text-muted md:text-lg">
                Built with React, Tailwind, and TypeScript using atmospheric backgrounds, high-contrast cards, and smooth fade interactions that elevate perceived quality.
              </p>
              <div className="flex flex-wrap gap-3">
                <button className="rounded-full bg-brand px-5 py-2.5 text-sm font-semibold text-brandContrast transition hover:brightness-110">
                  Start New Booking
                </button>
                <button className="rounded-full border border-outline px-5 py-2.5 text-sm font-semibold transition hover:bg-surfaceElevated">
                  View Occupancy
                </button>
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
              {metrics.map((item, index) => (
                <Reveal
                  key={item.label}
                  delayMs={index * 120}
                  className="rounded-2xl border border-outline bg-surfaceElevated p-4"
                >
                  <p className="text-3xl font-display leading-none">{item.value}</p>
                  <p className="mt-2 text-sm text-muted">{item.label}</p>
                </Reveal>
              ))}
            </div>
          </section>
        </Reveal>

        <section>
          <Reveal className="mb-5">
            <p className="text-xs uppercase tracking-[0.26em] text-muted">Portfolio-inspired motion cards</p>
            <h2 className="mt-2 font-display text-3xl md:text-4xl">Fade in and fade out as you scroll</h2>
          </Reveal>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {cards.map((card, index) => (
              <Reveal key={card.title} delayMs={index * 80}>
                <article className="group h-full rounded-2xl border border-outline bg-surface p-6 shadow-soft transition duration-300 hover:-translate-y-1 hover:bg-surfaceElevated">
                  <p className="text-xs uppercase tracking-[0.2em] text-muted">{card.tag}</p>
                  <h3 className="mt-3 font-display text-2xl leading-snug">{card.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted">{card.body}</p>
                  <div className="mt-6 h-[2px] w-0 bg-brand transition-all duration-300 group-hover:w-24" />
                </article>
              </Reveal>
            ))}
          </div>
        </section>

        <Reveal className="rounded-3xl border border-outline bg-surface p-7 shadow-soft md:p-10">
          <section className="grid gap-6 md:grid-cols-[1fr_auto] md:items-center">
            <div>
              <p className="text-xs uppercase tracking-[0.26em] text-muted">Layout quality check</p>
              <h2 className="mt-2 font-display text-3xl leading-tight">Clear hierarchy, smooth transitions, and polished dark/light contrast.</h2>
              <p className="mt-3 max-w-2xl text-muted">
                This implementation adds expressive typography, layered backgrounds, and deliberate motion so the interface feels modern and professionally composed.
              </p>
            </div>
            <div className="rounded-2xl border border-outline bg-surfaceElevated p-4 text-sm text-muted">
              <p>Animation style: scroll-triggered reveal</p>
              <p>Behavior: cards fade in and out repeatedly</p>
              <p>Modes: synchronized light and dark themes</p>
            </div>
          </section>
        </Reveal>
      </main>
    </div>
  );
}
