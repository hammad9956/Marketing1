"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

export type ThemeMode = "light" | "dark";

type Ctx = {
  theme: ThemeMode;
  setTheme: (t: ThemeMode) => void;
  toggle: () => void;
  mounted: boolean;
};

const ThemeContext = createContext<Ctx | null>(null);

function applyClass(mode: ThemeMode) {
  document.documentElement.classList.toggle("dark", mode === "dark");
}

function persistTheme(t: ThemeMode) {
  try {
    localStorage.setItem("helix-theme", t);
  } catch {
    /* private mode */
  }
  applyClass(t);
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<ThemeMode>("dark");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    try {
      const stored = localStorage.getItem("helix-theme") as ThemeMode | null;
      if (stored === "dark" || stored === "light") {
        setThemeState(stored);
        applyClass(stored);
      } else {
        setThemeState("dark");
        applyClass("dark");
      }
    } catch {
      setThemeState("dark");
      applyClass("dark");
    }
  }, []);

  const setTheme = useCallback((t: ThemeMode) => {
    setThemeState(t);
    persistTheme(t);
  }, []);

  const toggle = useCallback(() => {
    setThemeState((c) => {
      const next = c === "dark" ? "light" : "dark";
      persistTheme(next);
      return next;
    });
  }, []);

  const value = useMemo(
    () => ({ theme, setTheme, toggle, mounted }),
    [theme, setTheme, toggle, mounted]
  );

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme must be used within ThemeProvider");
  }
  return ctx;
}
