interface Props {
  statement: any;
  onClose: () => void;
}

export default function StatementModal({ statement, onClose }: Props) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded w-96 shadow-lg">
        <h2 className="text-xl font-bold mb-4">
          📄 Relevé du compte {statement.type}
        </h2>
        <p className="text-sm text-gray-500 mb-3">
          Période : {statement.period}
        </p>
        <p className="mb-3 font-semibold">
          Solde actuel : {statement.balance.toFixed(2)} €
        </p>

        <ul className="border-t max-h-48 overflow-y-auto text-sm">
          {statement.operations.map((op: any, i: number) => (
            <li key={i} className="py-1 border-b flex justify-between">
              <span>{op.type}</span>
              <span className={op.amount < 0 ? "text-red-600" : "text-green-600"}>
                {op.amount} €
              </span>
            </li>
          ))}
        </ul>

        <button
          onClick={onClose}
          className="mt-4 bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
        >
          Fermer
        </button>
      </div>
    </div>
  );
}
