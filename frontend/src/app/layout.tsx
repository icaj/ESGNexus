import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  titulo: 'ESG Nexus',
  descricao: 'Análise e monitoramento ESG de fornecedores',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
