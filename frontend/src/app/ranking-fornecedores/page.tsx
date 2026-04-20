'use client';

import { useEffect, useState } from 'react';
import { Layout } from '@/components/Layout';
import { Card } from '@/components/Card';
import { apiGet } from '@/lib/api';

type Avaliacao = {
  id: number;
  fornecedorNome: string;
  notaAmbiental: number;
  notaSocial: number;
  notaGovernanca: number;
  notaFinal: number;
};

export default function RankingFornecedoresPage() {
  const [itens, setItens] = useState<Avaliacao[]>([]);

  useEffect(() => {
    apiGet<Avaliacao[]>('/avaliacoes').then(setItens).catch(console.error);
  }, []);

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Ranking ESG</h1>
          <p className="text-slate-500">Classificação dos fornecedores com base na nota final.</p>
        </div>

        <Card>
          <table className="w-full text-left">
            <thead>
              <tr className="border-b">
                <th className="py-3">Posição</th>
                <th>Fornecedor</th>
                <th>Ambiental</th>
                <th>Social</th>
                <th>Governança</th>
                <th>Nota final</th>
              </tr>
            </thead>
            <tbody>
              {itens.map((item, index) => (
                <tr key={item.id} className="border-b last:border-0">
                  <td className="py-3">#{index + 1}</td>
                  <td>{item.fornecedorNome}</td>
                  <td>{item.notaAmbiental}</td>
                  <td>{item.notaSocial}</td>
                  <td>{item.notaGovernanca}</td>
                  <td className="font-bold">{item.notaFinal.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>
    </Layout>
  );
}
