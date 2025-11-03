export const API_URL = "http://127.0.0.1:8000";

export async function fetchAccounts() {
  const res = await fetch(`${API_URL}/accounts`);
  if (!res.ok) throw new Error("Erreur de chargement des comptes");
  return res.json();
}

export async function createAccount(data: { type: string; overdraft_limit?: number; deposit_cap?: number }) {
  const res = await fetch(`${API_URL}/accounts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Erreur de création du compte");
  return res.json();
}

export async function deposit(accountId: string, amount: number) {
  const res = await fetch(`${API_URL}/accounts/${accountId}/deposit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount }),
  });
  if (!res.ok) throw new Error("Erreur de dépôt");
  return res.json();
}

export async function withdraw(accountId: string, amount: number) {
  const res = await fetch(`${API_URL}/accounts/${accountId}/withdraw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount }),
  });
  if (!res.ok) throw new Error("Erreur de retrait");
  return res.json();
}

export async function getStatement(accountId: string) {
  const res = await fetch(`${API_URL}/accounts/${accountId}/statement`);
  if (!res.ok) throw new Error("Erreur de relevé");
  return res.json();
}
