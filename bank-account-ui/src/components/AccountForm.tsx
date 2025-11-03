import { useState } from "react";

interface Props {
  onCreate: (type: string, overdraft?: number, cap?: number) => Promise<void>;
}

export default function AccountForm({ onCreate }: Props) {
  const [type, setType] = useState("CURRENT");
  const [overdraft, setOverdraft] = useState(0);
  const [cap, setCap] = useState(22950);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await onCreate(type, overdraft, cap);
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow p-4 rounded mb-6">
      <h2 className="font-bold mb-2">Créer un compte</h2>
      <div className="flex items-center gap-4">
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}     className="border p-2 rounded"
        >
          <option value="CURRENT">Compte courant</option>
          <option value="SAVINGS">Livret d'épargne</option>
        </select>

        {type === "CURRENT" && (
          <input
            type="number"
            placeholder="Découvert autorisé (€)"
            value={overdraft}
            onChange={(e) => setOverdraft(parseFloat(e.target.value))}
            className="border p-2 rounded w-48"
          />
        )}

        {type === "SAVINGS" && (
          <input
            type="number"
            placeholder="Plafond (€)"
            value={cap}
            onChange={(e) => setCap(parseFloat(e.target.value))}
            className="border p-2 rounded w-48"
          />
        )}

        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          ➕ Créer
        </button>
      </div>
    </form>
  );
}
