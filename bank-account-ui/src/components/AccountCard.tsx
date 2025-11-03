import { useState } from "react";
import { Account } from "../App";

interface Props {
  account: Account;
  onDeposit: (id: string, amount: number) => Promise<void>;
  onWithdraw: (id: string, amount: number) => Promise<void>;
  onStatement: (id: string) => Promise<void>;
}

export default function AccountCard({ account, onDeposit, onWithdraw, onStatement }: Props) {
  const [amount, setAmount] = useState(0);

  return (
    <div className="bg-white p-4 shadow rounded">
      <h3 className="text-xl font-semibold">
        {account.type === "CURRENT" ? "💳 Compte courant" : "💰 Livret d’épargne"}
      </h3>
      <p className="text-gray-700 mb-2">Solde : <strong>{account.balance.toFixed(2)} €</strong></p>

      <input
        type="number"
        placeholder="Montant"
        className="border p-1 rounded w-32 mr-2"
        value={amount}
        onChange={(e) => setAmount(parseFloat(e.target.value))}
      />

      <button
        onClick={() => onDeposit(account.id, amount)}
        className="bg-green-600 text-white px-3 py-1 rounded mr-2"
      >
        ➕ Dépôt
      </button>

      <button
        onClick={() => onWithdraw(account.id, amount)}
        className="bg-red-600 text-white px-3 py-1 rounded mr-2"
      >
        ➖ Retrait
      </button>

      <button
        onClick={() => onStatement(account.id)}
        className="bg-gray-700 text-white px-3 py-1 rounded"
      >
        📄 Relevé
      </button>
    </div>
  );
}
