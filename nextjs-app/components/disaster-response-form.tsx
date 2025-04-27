"use client";

import { useState } from "react";

export default function DisasterResponseForm() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<{
    isRelated: boolean;
    categories: Record<string, number>;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch("/api/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      if (!res.ok) {
        const textErr = await res.text();
        throw new Error(textErr || "Erro na API");
      }
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Erro inesperado");
      setResult(null);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="message" className="block text-sm font-medium text-gray-700">
          Mensagem
        </label>
        <textarea
          id="message"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Digite uma mensagem..."
          rows={4}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-indigo-200"
        />
      </div>

      <button
        type="submit"
        className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
      >
        Classificar
      </button>

      {error && (
        <p className="text-red-600 text-sm">Erro: {error}</p>
      )}

      {result && (
        <div className="mt-4">
          <p>
            <strong>Relacionado a desastre? </strong>
            {result.isRelated ? "Sim" : "Não"}
          </p>
          {result.isRelated && (
            <ul className="mt-2 list-disc list-inside">
              {Object.entries(result.categories).map(([cat, val]) => (
                <li key={cat} className="capitalize">
                  {cat.replace(/_/g, ' ')}: {val}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </form>
  );
}
