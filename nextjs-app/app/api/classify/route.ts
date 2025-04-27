import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  // 1) lê o JSON enviado pelo form
  const { message } = await request.json();

  // 2) repassa para o Flask
  const flaskRes = await fetch("http://localhost:5000/api/classify", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ message }),
  });

  // 3) trata erro do Flask
  if (!flaskRes.ok) {
    const errText = await flaskRes.text();
    console.error("ML API error:", errText);
    return NextResponse.json(
      { error: "Falha na ML API" },
      { status: 500 }
    );
  }

  // 4) extrai e repassa o JSON ao cliente
  const { isRelated, categories } = await flaskRes.json();
  return NextResponse.json({ isRelated, categories });
}
