'use client';

import { useEffect, useState } from 'react';
import { Layout } from '@/components/Layout';
import { Card } from '@/components/Card';
import { apiGet, apiPost } from '@/lib/api';

type Configuracao = {
  id: number;
  chave: string;
  valor: string;
};

export default function ConfiguracoesPage() {
  const [configuracoes, setConfiguracoes] = useState<Configuracao[]>([]);
  const [chave, setChave] = useState('esg.peso.ambiental');
  const [valor, setValor] = useState('35');

  async function carregar() {
    const data = await apiGet<Configuracao[]>('/configuracoes');
    setConfiguracoes(data);
  }

  useEffect(() => { carregar().catch(console.error); }, []);

  async function salvar() {
    await apiPost('/configuracoes', { chave, valor });
    setValor('');
    await carregar();
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Configurações</h1>
          <p className="text-slate-500">Parâmetros da plataforma, incluindo pesos ESG.</p>
        </div>

        <div className="grid lg:grid-cols-[1fr_380px] gap-6">
          <Card>
            <table className="w-full text-left">
              <thead>
                <tr className="border-b">
                  <th className="py-3">Chave</th>
                  <th>Valor</th>
                </tr>
              </thead>
              <tbody>
                {configuracoes.map((configuracao) => (
                  <tr key={configuracao.id} className="border-b last:border-0">
                    <td className="py-3">{configuracao.chave}</td>
                    <td>{configuracao.valor}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>

          <Card>
            <h2 className="text-xl font-semibold mb-4">Atualizar parâmetro</h2>
            <div className="space-y-3">
              <input className="w-full border rounded-xl px-4 py-3" value={chave} onChange={(e) => setChave(e.target.value)} placeholder="chave" />
              <input className="w-full border rounded-xl px-4 py-3" value={valor} onChange={(e) => setValor(e.target.value)} placeholder="valor" />
              <button onClick={salvar} className="w-full bg-green-700 text-white rounded-xl py-3 font-semibold">Salvar</button>
            </div>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
