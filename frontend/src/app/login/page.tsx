'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('admin@esgnexus.com');
  const [senha, setSenha] = useState('admin123');
  const [erro, setErro] = useState('');

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setErro('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api'}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha }),
      });

      if (!response.ok) {
        throw new Error('Credenciais inválidas');
      }

      const data = await response.json();
      localStorage.setItem('token', data.token);
      localStorage.setItem('userName', data.nome);
      router.push('/dashboard');
    } catch (err) {
      setErro(err instanceof Error ? err.message : 'Erro ao fazer login');
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">
      <div className="bg-white w-full max-w-md rounded-3xl shadow-xl p-8 border border-slate-200">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">ESG Nexus</h1>
        <p className="text-slate-500 mb-6">Plataforma de análise e ranking ESG de fornecedores</p>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-1">E-mail</label>
            <input className="w-full border rounded-xl px-4 py-3" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Senha</label>
            <input type="password" className="w-full border rounded-xl px-4 py-3" value={senha} onChange={(e) => setSenha(e.target.value)} />
          </div>
          {erro && <div className="text-red-600 text-sm">{erro}</div>}
          <button className="w-full bg-green-700 hover:bg-green-800 text-white rounded-xl py-3 font-semibold">
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
}
