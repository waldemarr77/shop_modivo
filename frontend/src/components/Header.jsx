import React from 'react';
import { Diamond, Search, ShoppingCart, User } from 'lucide-react';

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/5 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <div className="flex items-center gap-2 text-accent">
          <Diamond size={24} className="text-accent" />
          <span className="font-display text-xl font-bold tracking-widest text-white uppercase">
            MODIVO
          </span>
        </div>

        <div className="relative hidden w-full max-w-md items-center md:flex group">
          <Search size={18} className="absolute left-4 text-slate-500 transition-colors group-focus-within:text-accent" />
          <input
            type="text"
            placeholder="Шукати преміум товари..."
            className="w-full rounded-full border border-white/10 bg-white/5 py-2.5 pl-11 pr-4 text-sm text-white placeholder:text-slate-500 focus:border-accent/50 focus:bg-white/10 focus:outline-none transition-all duration-300"
          />
        </div>

        <div className="flex items-center gap-6">
          <button className="text-slate-400 hover:text-white transition-colors duration-300">
            <User size={20} />
          </button>
          <button className="relative text-slate-400 hover:text-accent transition-colors duration-300">
            <ShoppingCart size={20} />
            <span className="absolute -right-2 -top-2 flex h-4 w-4 items-center justify-center rounded-full bg-accent text-[10px] font-bold text-black shadow-[0_0_10px_rgba(204,255,0,0.5)]">
              3
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
