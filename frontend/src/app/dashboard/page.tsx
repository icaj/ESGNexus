'use client';

import { useEffect, useState } from 'react';
import { Layout } from '@/components/Layout';
import { Card } from '@/components/Card';
import { apiGet } from '@/lib/api';

type Dashboard = {
  indicadores: {
    totalFornecedores: number;
    totalAvaliacoes: number;
    totalCertificacoes: number;
    alertasAbertos: number;
    mediaScore: number;
  };
  topRanking: { fornecedorId: number; fornecedorNome: string; notaFinal: number }[];
};

export default function DashboardPage() {
  const [data, setData] = useState<Dashboard | null>(null);

  useEffect(() => {
    apiGet<Dashboard>('/dashboard').then(setData).catch(console.error);
  }, []);

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard ESG</h1>
          <p className="text-slate-500">Visão executiva dos indicadores da plataforma.</p>
        </div>

        <div className="grid md:grid-cols-5 gap-4">
          <Card><div className="text-sm text-slate-500">Fornecedores</div><div className="text-3xl font-bold">{data?.indicadores.totalFornecedores ?? '-'}</div></Card>
          <Card><div className="text-sm text-slate-500">Avaliações</div><div className="text-3xl font-bold">{data?.indicadores.totalAvaliacoes ?? '-'}</div></Card>
          <Card><div className="text-sm text-slate-500">Certificações</div><div className="text-3xl font-bold">{data?.indicadores.totalCertificacoes ?? '-'}</div></Card>
          <Card><div className="text-sm text-slate-500">Alertas abertos</div><div className="text-3xl font-bold">{data?.indicadores.alertasAbertos ?? '-'}</div></Card>
          <Card><div className="text-sm text-slate-500">Média ESG</div><div className="text-3xl font-bold">{data?.indicadores.mediaScore?.toFixed(2) ?? '-'}</div></Card>
        </div>

        <Card>
          <h2 className="text-xl font-semibold mb-4">Top ranking de fornecedores</h2>
          <table className="w-full text-left">
            <thead>
              <tr className="border-b">
                <th className="py-3">Posição</th>
                <th>Fornecedor</th>
                <th>Nota</th>
              </tr>
            </thead>
            <tbody>
              {data?.topRanking.map((item, index) => (
                <tr key={item.fornecedorId} className="border-b last:border-0">
                  <td className="py-3">#{index + 1}</td>
                  <td>{item.fornecedorNome}</td>
                  <td>{item.notaFinal.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>
    </Layout>
  );
}
