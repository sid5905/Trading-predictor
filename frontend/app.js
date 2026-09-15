const $ = (id) => document.getElementById(id);

async function analyze() {
  const symbol = $("symbol").value.trim();
  if (!symbol) return;
  $("error").classList.add("hidden");
  $("analyze").disabled = true;
  $("analyze").textContent = "Analyzing…";
  try {
    const res = await fetch("/api/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ symbol }) });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Analysis failed");
    $("dashboard").classList.remove("hidden");
    $("price").textContent = `₹${data.price.toFixed(2)}`;
    $("change").textContent = `${data.change_pct >= 0 ? "+" : ""}${data.change_pct.toFixed(2)}%`;
    $("signal").textContent = data.signal;
    $("trend").textContent = data.trend;
    $("momentum").textContent = data.momentum;
    $("volatility").textContent = data.volatility;
    $("confidence").textContent = `${data.confidence}%`;
    $("indicators").innerHTML = Object.entries(data.indicators).map(([k,v]) => `<div><span>${k}</span><b>${v == null ? "—" : Number(v).toFixed(2)}</b></div>`).join("");
    $("notes").innerHTML = data.notes.length ? data.notes.map(n => `<li>${n}</li>`).join("") : "<li>No additional notes.</li>";
  } catch (e) {
    $("error").textContent = e.message;
    $("error").classList.remove("hidden");
  } finally {
    $("analyze").disabled = false;
    $("analyze").textContent = "Analyze";
  }
}

$("analyze").addEventListener("click", analyze);
$("symbol").addEventListener("keydown", (e) => { if (e.key === "Enter") analyze(); });
analyze();
