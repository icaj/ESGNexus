'use client';

import { useEffect, useState } from 'react';
import { Layout } from '@/components/Layout';
import { Card } from '@/components/Card';
import { apiGet, apiPut } from '@/lib/api';

type Alerta = {
  id: number;
  fornecedorNome: string;
  tipoAlerta: string;
  severidade: string;
  titulo: string;
  descricao: string;
  status: string;
  dataCriacao: string;
};

export default function AlertasPage() {
  const [alertas, setAlertas] = useState<Alerta[]>([]);

  async function carregar() {
    const data = await apiGet<Alerta[]>('/alertas');
    setAlertas(data);
  }

  useEffect(() => { carregar().catch(console.error); }, []);

  async function resolver(id: number) {
    await apiPut(`/alertas/${id}/resolver`);
    await carregar();
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Alertas</h1>
          <p className="text-slate-500">Ocorrências críticas e acompanhamento de resolução.</p>
        </div>

        <div className="space-y-4">
          {alertas.map((alerta) => (
            <Card key={alerta.id}>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="text-lg font-semibold">{alerta.titulo}</div>
                  <div className="text-sm text-slate-500">Fornecedor: {alerta.fornecedorNome}</div>
                  <div className="text-sm text-slate-500">Tipo: {alerta.tipoAlerta} | Severidade: {alerta.severidade}</div>
                  <p className="mt-3 text-slate-700">{alerta.descricao}</p>
                </div>
                <div className="text-right space-y-2">
                  <div className="font-medium">{alerta.status}</div>
                  {alerta.status !== 'RESOLVIDO' && (
                    <button className="bg-green-700 text-white rounded-xl px-4 py-2" onClick={() => resolver(alerta.id)}>
                      Resolver
                    </button>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </Layout>
  );
}
