import React from 'react';
import { ShoppingCart, Star, Shirt, Footprints, Watch, Glasses, ShoppingBag, Package } from 'lucide-react';

const CATEGORY_ICONS = {
  'Кросівки': Footprints,
  'Одяг': Shirt,
  'Аксесуари': Watch,
  'Окуляри': Glasses,
  'Сумки': ShoppingBag,
  'Інше': Package
};

export default function ProductCard({ product }) {
  const Icon = CATEGORY_ICONS[product.category] || Package;

  return (
    <div className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-white/5 bg-surface p-5 transition-all duration-500 hover:border-accent/30 hover:bg-white/[0.02]">
      {/* Glow effect on hover */}
      <div className="absolute -inset-px bg-gradient-to-b from-accent/20 to-transparent opacity-0 transition-opacity duration-500 group-hover:opacity-100 blur-xl"></div>
      
      <div className="relative z-10">
        <div className="mb-6 flex h-40 items-center justify-center rounded-xl bg-background/50 border border-white/5 transition-transform duration-700 group-hover:scale-[1.02]">
          <Icon size={48} className="text-slate-700 transition-colors duration-700 group-hover:text-accent" strokeWidth={1.5} />
        </div>

        <div className="mb-2 flex items-center gap-2 text-[10px] font-semibold tracking-widest text-slate-500 uppercase">
          {product.category}
        </div>
        
        <h3 className="mb-3 font-display text-lg font-semibold text-slate-200 transition-colors duration-300 group-hover:text-white leading-tight">
          {product.name}
        </h3>

        <div className="flex items-center gap-1.5 mb-6">
          <Star size={13} className="fill-accent text-accent" />
          <span className="text-sm font-medium text-slate-300">{product.rating}</span>
          <span className="text-xs text-slate-600">({product.reviews} відгуків)</span>
        </div>
      </div>

      <div className="relative z-10 flex items-center justify-between border-t border-white/5 pt-4">
        <span className="font-display text-xl font-bold text-white">
          ₴{product.price.toLocaleString('uk-UA')}
        </span>
        
        <button className="flex h-10 w-10 items-center justify-center rounded-full bg-white/5 text-slate-300 transition-all duration-300 hover:bg-accent hover:text-black hover:scale-110 active:scale-95 shadow-lg">
          <ShoppingCart size={16} />
        </button>
      </div>
    </div>
  );
}
