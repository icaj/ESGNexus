import { PropsWithChildren } from 'react';

export function Card({ children }: PropsWithChildren) {
  return <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">{children}</div>;
}
