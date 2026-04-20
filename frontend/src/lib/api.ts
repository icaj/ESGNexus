const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api';

function getHeaders() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: getHeaders(),
    cache: 'no-store',
  });
  if (!response.ok) throw new Error(`Erro ao buscar ${path}`);
  return response.json();
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`Erro ao enviar ${path}`);
  return response.json();
}

export async function apiPut<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: 'PUT',
    headers: getHeaders(),
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) throw new Error(`Erro ao atualizar ${path}`);
  return response.json();
}
