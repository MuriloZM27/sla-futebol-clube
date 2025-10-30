async function carregarEmprestimos() {
    const resp = await fetch("/api/loans");
    const loans = await resp.json();
  
    const tbody = document.querySelector("#loan-table tbody");
    if (!tbody) return;
  
    tbody.innerHTML = "";
    loans.forEach(l => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${l.id}</td>
        <td>${l.user}</td>
        <td>${l.book}</td>
        <td>${l.status}</td>
      `;
      tbody.appendChild(tr);
    });
  }
  
  document.addEventListener("DOMContentLoaded", carregarEmprestimos);
  