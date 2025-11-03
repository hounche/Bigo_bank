import { useEffect, useState } from "react";
import {
  fetchAccounts,
  createAccount,
  deposit,
  withdraw,
  getStatement,
} from "./api";
import "./App.css";

function App() {
  const [accounts, setAccounts] = useState([]);
  const [amount, setAmount] = useState("");
  const [statement, setStatement] = useState(null);
  const [type, setType] = useState("CURRENT");
  const [overdraft, setOverdraft] = useState("");
  const [cap, setCap] = useState("");

  async function loadAccounts() {
    const data = await fetchAccounts();
    setAccounts(data);
  }

  useEffect(() => {
    loadAccounts();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();

    await createAccount({
      type,
      overdraft_limit: overdraft ? parseFloat(overdraft) : 0,
      deposit_cap: cap ? parseFloat(cap) : null, 
    });

    await loadAccounts();
  }

  async function handleDeposit(id) {
    if (!amount || parseFloat(amount) <= 0) return alert("Montant invalide");
    await deposit(id, parseFloat(amount));
    await loadAccounts();
  }

  async function handleWithdraw(id) {
    if (!amount || parseFloat(amount) <= 0) return alert("Montant invalide");
    await withdraw(id, parseFloat(amount));
    await loadAccounts();
  }

  async function handleStatement(id) {
    const data = await getStatement(id);
    setStatement(data);
  }

  async function handleInterest(id) {
    await fetch(`http://127.0.0.1:8000/accounts/${id}/interest`, {
      method: "POST",
    });
    await loadAccounts();
  }

  const totalBalance = accounts
    .reduce((sum, acc) => sum + acc.balance, 0)
    .toFixed(2);

  return (
    <div className="app">
      <header>
        <h1>🏦 BIGO BANK</h1>
        <p>Votre espace client</p>
      </header>

      <div className="welcome-banner">
        <div>
          <h2>👋 Bonjour Maël de Exalt_IT</h2>
          <p>Ravi de vous revoir sur votre tableau de bord 💸</p>
        </div>
        <div className="total-balance">
          <span>Total de vos comptes</span>
          <strong>{totalBalance} €</strong>
        </div>
      </div>

      <main>
        <section className="create-account">
          <h2>Créer un compte</h2>
          <form onSubmit={handleCreate}>
            <select value={type} onChange={(e) => setType(e.target.value)}>
              <option value="CURRENT">Compte courant</option>
              <option value="SAVINGS">Livret A</option>
              <option value="LIVRET_B">Livret B</option> {/* ajouté */}
            </select>

            {type === "CURRENT" && (
              <input
                type="number"
                placeholder="Découvert autorisé (€)"
                value={overdraft}
                onChange={(e) => setOverdraft(e.target.value)}
              />
            )}

            {(type === "SAVINGS" || type === "LIVRET_B") && (
              <input
                type="number"
                placeholder="Plafond (€)"
                value={cap}
                onChange={(e) => setCap(e.target.value)}
              />
            )}

            <button type="submit">➕ Créer</button>
          </form>
        </section>

        <section className="accounts">
          <h2>Mes comptes</h2>
          <div className="cards">
            {accounts.map((a) => {
              let backgroundColor = "#fff";
              let textColor = "#000";
              let label = "";

              if (a.type === "SAVINGS") {
                label = "A";
                backgroundColor = "#ec8d43";
                textColor = "#fff";
              } else if (a.type === "LIVRET_B") {
                label = "B";
                backgroundColor = "#877b7aff";
                textColor = "#fff";
              }

              return (
                <div
                  key={a.id}
                  className="card"
                  style={{
                    backgroundColor,
                    color: textColor,
                    transition: "0.3s ease",
                  }}
                >
                  <h3 className="account-title">
                    {a.type === "CURRENT" ? (
                      "💳 Courant"
                    ) : (
                      <>
                        💰 Livret
                        <span
                          className="badge"
                          style={{
                            backgroundColor:
                              label === "A" ? "#ec8d43" : "#877b7aff",
                          }}
                        >
                          {label}
                        </span>
                      </>
                    )}
                  </h3>

                  <p className="balance">{a.balance.toFixed(2)} €</p>

                  <div className="actions">
                    <input
                      type="number"
                      placeholder="Montant"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                    />
                    <button
                      onClick={() => handleDeposit(a.id)}
                      className="btn-green"
                    >
                      Dépôt
                    </button>
                    <button
                      onClick={() => handleWithdraw(a.id)}
                      className="btn-red"
                    >
                      Retrait
                    </button>

                    {a.type === "LIVRET_B" && (
                      <button
                        onClick={() => handleInterest(a.id)}
                        className="btn-yellow"
                      >
                        💹 Intérêts
                      </button>
                    )}
                  </div>

                  <button
                    onClick={() => handleStatement(a.id)}
                    className="btn-blue full"
                  >
                    📄 Relevé
                  </button>
                </div>
              );
            })}
          </div>
        </section>

        {statement && (
          <div className="modal">
            <div className="modal-content statement-card">
              <div className="statement-header">
                <h2>📄 Relevé du compte</h2>
                <button
                  onClick={() => setStatement(null)}
                  className="close-btn"
                >
                  ✖
                </button>
              </div>

              <div className="statement-info">
                <p>
                  <strong>Type :</strong>{" "}
                  {statement.type === "CURRENT"
                    ? "Compte courant"
                    : statement.type === "LIVRET_B"
                    ? "Livret B"
                    : "Livret A"}
                </p>
                <p>
                  <strong>Solde actuel :</strong>{" "}
                  {statement.balance.toFixed(2)} €
                </p>
              </div>

              <table className="operations-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Montant</th>
                  </tr>
                </thead>
                <tbody>
                  {statement.operations.length === 0 ? (
                    <tr>
                      <td colSpan="3" className="empty">
                        Aucune opération enregistrée
                      </td>
                    </tr>
                  ) : (
                    statement.operations.map((op, i) => (
                      <tr
                        key={i}
                        className={
                          op.type === "DEPOSIT"
                            ? "deposit"
                            : op.type === "INTEREST"
                            ? "interest"
                            : "withdraw"
                        }
                      >
                        <td>{op.date}</td>
                        <td>
                          {op.type === "DEPOSIT"
                            ? "Dépôt"
                            : op.type === "INTEREST"
                            ? "Intérêts"
                            : "Retrait"}
                        </td>
                        <td>{op.amount} €</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
