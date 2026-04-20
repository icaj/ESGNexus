'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { PropsWithChildren } from 'react';

const items = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/fornecedores', label: 'Fornecedores' },
  { href: '/ranking-fornecedores', label: 'Ranking' },
  { href: '/alertas', label: 'Alertas' },
  { href: '/configuracoes', label: 'Configurações' },
];

export function Layout({ children }: PropsWithChildren) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen grid grid-cols-[250px_1fr]">
      <aside className="bg-slate-900 text-white p-6">
        <div className="text-2xl font-bold mb-8">ESG Nexus</div>
        <nav className="space-y-2">
          {items.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-xl px-4 py-3 transition ${pathname === item.href ? 'bg-green-700' : 'bg-slate-800 hover:bg-slate-700'}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="p-8">{children}</main>
    </div>
  );
}
