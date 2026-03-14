// const API_BASE = import.meta.env.DEV ? '' : 'http://localhost:8000';
const API_BASE = 'http://localhost:8000';

export const apiCall = async (endpoint: string, body: any, apiKey: string) => {
  const res = await fetch(`${API_BASE}/api${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
};