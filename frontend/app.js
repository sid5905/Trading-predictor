const $ = (id) => document.getElementById(id);
let lastData = null;

function drawChart(points) {
  const canvas = $("price-chart");
  const wrap = $("chart-wrap");
  const dpr = window.devicePixelRatio || 1;
  const w = wrap.clientWidth, h = Math.max(300, wrap.clientHeight);
  canvas.width = w * dpr; canvas.height = h * dpr; canvas.style.width = `${w}px`; canvas.style.height = `${h}px`;
  const ctx = canvas.getContext("2d"); ctx.scale(dpr, dpr); ctx.clearRect(0, 0, w, h);
  const values = points.map(p => p.close); const min = Math.min(...values), max = Math.max(...values), pad = 30;
  const x = i => pad + i * (w - pad * 2) / Math.max(1, points.length - 1);
  const y = v => h - pad - (v - min) / Math.max(0.0001, max - min) * (h - pad * 2);
  ctx.strokeStyle = "#28313a"; ctx.lineWidth = 1;
  for (let i=0;i<5;i++){const yy=pad+i*(h-pad*2)/4;ctx.beginPath();ctx.moveTo(pad,yy);ctx.lineTo(w-pad,yy);ctx.stroke();}
  ctx.strokeStyle = "#dfe6ed"; ctx.lineWidth = 2; ctx.beginPath(); values.forEach((v,i)=>{i?ctx.lineTo(x(i),y(v)):ctx.moveTo(x(i),y(v))}); ctx.stroke();
  const sma = []; for(let i=0;i<values.length;i++){const a=values.slice(Math.max(0,i-19),i+1);sma.push(a.reduce((s,v)=>s+v,0)/a.length)}
  ctx.strokeStyle = "#7f8b98"; ctx.lineWidth = 1.5; ctx.setLineDash([5,4]); ctx.beginPath(); sma.forEach((v,i)=>{i?ctx.lineTo(x(i),y(v)):ctx.moveTo(x(i),y(v))}); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = "#8d98a5"; ctx.font = "11px system-ui"; for(let i=0;i<5;i++){const v=max-i*(max-min)/4;ctx.fillText(`₹${v.toFixed(0)}`,4,pad+i*(h-pad*2)/4+4)}
}

function render(data) {
  lastData = data;
  $("dashboard-content").classList.remove("hidden"); $("empty").classList.add("hidden");
  $("stock-symbol").textContent = data.symbol; $("price").textContent = `₹${data.price.toFixed(2)}`;
  $("change").textContent = `${data.change_pct >= 0 ? "+" : ""}${data.change_pct.toFixed(2)}% session move`;
  $("signal").textContent = data.signal; $("signal-copy").textContent = data.notes.length ? data.notes.join(" ") : "The current setup is mixed; wait for stronger confirmation.";
  $("trend").textContent = data.trend; $("momentum").textContent = data.momentum; $("volatility").textContent = data.volatility; $("confidence").textContent = `${data.confidence}%`; $("confidence-bar").style.width = `${data.confidence}%`; $("signal-meter").style.width = `${data.confidence}%`;
  const names = {sma20:"20D SMA",sma50:"50D SMA",ema20:"20D EMA",ema50:"50D EMA",rsi14:"RSI (14)",macd:"MACD",macd_signal:"MACD Signal",atr14:"ATR (14)",bb_upper:"Bollinger Upper",bb_lower:"Bollinger Lower"};
  $("indicator-list").innerHTML = Object.entries(data.indicators).map(([k,v])=>`<div><span>${names[k]||k}</span><b>${v==null?"—":Number(v).toFixed(2)}</b></div>`).join("");
  $("notes").innerHTML = data.notes.length ? data.notes.map(n=>`<li>${n}</li>`).join("") : "<li>No additional observations.</li>";
  drawChart(data.chart || []);
}

async function analyze() {
  const symbol = $("symbol").value.trim(); if (!symbol) return;
  $("error").classList.add("hidden"); $("analyze").disabled=true; $("analyze").innerHTML="Analyzing…";
  try { const res=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({symbol})}); const data=await res.json(); if(!res.ok) throw new Error(data.detail||"Analysis failed"); render(data); }
  catch(e){$("error").textContent=e.message;$("error").classList.remove("hidden");}
  finally{$("analyze").disabled=false;$("analyze").innerHTML='Analyze stock <span>→</span>';}
}
$("analyze").addEventListener("click",analyze); $("symbol").addEventListener("keydown",e=>{if(e.key==="Enter")analyze()}); window.addEventListener("resize",()=>{if(lastData)drawChart(lastData.chart||[])});
analyze();
