'use client';

import { useEffect, useState } from 'react';
import { Layout } from '@/components/Layout';
import { Card } from '@/components/Card';
import { apiGet, apiPost } from '@/lib/api';

type Fornecedor = {
  id: number;
  razaoSocial: string;
  nomeFantasia: string;
  cnpj: string;
  segmento: string;
  categoria: string;
  status: string;
  nivelRisco: string;
};

const formularioInicial = {
  razaoSocial: '', nomeFantasia: '', cnpj: '', email: '', telefone: '', nomeContato: '', segmento: '', categoria: '', cidade: '', estado: '', pais: 'Brasil', nivelRisco: '', status: 'ATIVO'
};

export default function FornecedoresPage() {
  const [fornecedores, setFornecedores] = useState<Fornecedor[]>([]);
  const [formulario, setFormulario] = useState(formularioInicial);

  async function carregar() {
    const data = await apiGet<Fornecedor[]>('/fornecedores');
    setFornecedores(data);
  }

  useEffect(() => { carregar().catch(console.error); }, []);

  async function handleCreate() {
    await apiPost('/fornecedores', formulario);
    setFormulario(formularioInicial);
    await carregar();
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Fornecedores</h1>
          <p className="text-slate-500">Cadastro manual e gestão da base de fornecedores.</p>
        </div>

        <div className="grid lg:grid-cols-[1fr_420px] gap-6">
          <Card>
            <table className="w-full text-left">
              <thead>
                <tr className="border-b">
                  <th className="py-3">Razão social</th>
                  <th>CNPJ</th>
                  <th>Segmento</th>
                  <th>Risco</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {fornecedores.map((fornecedor) => (
                  <tr key={fornecedor.id} className="border-b last:border-0">
                    <td className="py-3">{fornecedor.razaoSocial}</td>
                    <td>{fornecedor.cnpj}</td>
                    <td>{fornecedor.segmento}</td>
                    <td>{fornecedor.nivelRisco}</td>
                    <td>{fornecedor.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>

          <Card>
            <h2 className="text-xl font-semibold mb-4">Novo fornecedor</h2>
            <div className="space-y-3">
              {Object.entries(formulario).map(([chave, valor]) => (
                <input
                  key={chave}
                  className="w-full border rounded-xl px-4 py-3"
                  placeholder={chave}
                  value={valor}
                  onChange={(e) => setFormulario({ ...formulario, [chave]: e.target.value })}
                />
              ))}
              <button onClick={handleCreate} className="w-full bg-green-700 text-white rounded-xl py-3 font-semibold">
                Salvar fornecedor
              </button>
            </div>
          </Card>
        </div>
      </div>
    </Layout>
  );
}
