async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;
  const res = await fetch('/api/prompt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ prompt })
  });
  const data = await res.json();
  document.getElementById('log').textContent = JSON.stringify(data, null, 2);
} 