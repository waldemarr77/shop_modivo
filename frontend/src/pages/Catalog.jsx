import React from 'react';
import Header from '../components/Header';
import ProductCard from '../components/ProductCard';

const MOCK_PRODUCTS = [
  { id: 1, name: "Nike Air Max 270", category: "Кросівки", price: 5499, rating: 4.8, reviews: 342 },
  { id: 2, name: "Худі Essentials Fear of God", category: "Одяг", price: 3150, rating: 4.9, reviews: 128 },
  { id: 3, name: "Окуляри Ray-Ban Aviator", category: "Окуляри", price: 4290, rating: 4.5, reviews: 210 },
  { id: 4, name: "Кросівки New Balance 574", category: "Кросівки", price: 3899, rating: 4.7, reviews: 845 },
  { id: 5, name: "Сумка Jacquemus Le Chiquito", category: "Сумки", price: 15490, rating: 4.6, reviews: 312 },
  { id: 6, name: "Футболка Balenciaga Oversized", category: "Одяг", price: 11890, rating: 4.8, reviews: 156 },
];

export default function Catalog() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      
      <main className="mx-auto w-full max-w-7xl flex-1 px-6 py-12">
        <div className="mb-12 flex flex-col gap-2">
          <h1 className="font-display text-4xl font-bold tracking-tight text-white">
            Нове надходження
          </h1>
          <p className="text-slate-400 font-sans text-sm">
            Знайдіть найкращі девайси для свого преміум сетапу.
          </p>
        </div>

        <div className="flex gap-12">
          {/* Сайдбар з фільтрами */}
          <aside className="hidden w-56 md:block">
            <h2 className="mb-6 font-display text-sm font-semibold tracking-widest text-white uppercase">
              Фільтри
            </h2>
            
            <div className="mb-8">
              <h3 className="mb-4 text-xs font-semibold uppercase tracking-widest text-slate-500">Категорії</h3>
              <div className="flex flex-col gap-3.5">
                {['Кросівки', 'Одяг', 'Сумки', 'Окуляри', 'Аксесуари'].map(c => (
                  <label key={c} className="flex cursor-pointer items-center gap-3 group">
                    <div className="flex h-4 w-4 items-center justify-center rounded border border-white/20 bg-white/5 transition-colors group-hover:border-accent">
                      {/* Чекбокс UI */}
                      <div className="h-2 w-2 rounded-[2px] bg-transparent transition-colors"></div>
                    </div>
                    <span className="text-sm text-slate-400 group-hover:text-white transition-colors duration-300">
                      {c}
                    </span>
                  </label>
                ))}
              </div>
            </div>
            
            <div className="mb-8">
              <h3 className="mb-4 text-xs font-semibold uppercase tracking-widest text-slate-500">Ціна, ₴</h3>
              <div className="flex items-center gap-2">
                <input 
                  type="text" 
                  placeholder="Від" 
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-accent/50 transition-colors"
                />
                <span className="text-slate-600">-</span>
                <input 
                  type="text" 
                  placeholder="До" 
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-accent/50 transition-colors"
                />
              </div>
            </div>
          </aside>

          {/* Сітка товарів */}
          <div className="flex-1">
            <div className="mb-8 flex items-center justify-between">
              <span className="text-sm font-medium text-slate-500">Показано {MOCK_PRODUCTS.length} товарів</span>
              <select className="bg-surface border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-accent/50 cursor-pointer transition-colors duration-300 appearance-none pr-10 relative">
                <option>За популярністю</option>
                <option>Ціна: від дешевих</option>
                <option>Ціна: від дорогих</option>
              </select>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {MOCK_PRODUCTS.map(p => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
