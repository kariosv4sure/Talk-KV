// Simple front-end chat logic
const chatForm = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = userInput.value.trim();
  if (!msg) return;

  // User bubble
  appendMsg('You', msg);
  userInput.value = '';

  // Call Flask backend
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await response.json();
    appendMsg('KV', data.reply || 'No response.');
  } catch (err) {
    appendMsg('KV', '⚠️ Error contacting server.');
    console.error(err);
  }
});

function appendMsg(sender, text) {
  const p = document.createElement('p');
  p.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(p);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// === Auto-typing rotating messages ===
const messages = [
  "❤️ Hearts and Talk to KV cares",
  "🌟 Your friendly AI diary",
  "💌 Share your thoughts with KV",
  "✨ Made by Karios Vantari",
  "🤗 KV is here for you anytime"
];

const autoTypeEl = document.getElementById('auto-type');
let msgIndex = 0;       // which message we’re on
let charIndex = 0;      // character position
let deleting = false;   // whether we’re deleting text

function typeLoop() {
  const currentMsg = messages[msgIndex];
  
  if (!deleting) {
    // typing forward
    autoTypeEl.textContent = currentMsg.substring(0, charIndex + 1);
    charIndex++;
    if (charIndex === currentMsg.length) {
      deleting = true;
      setTimeout(typeLoop, 2000); // hold full text before deleting
      return;
    }
  } else {
    // deleting backwards
    autoTypeEl.textContent = currentMsg.substring(0, charIndex - 1);
    charIndex--;
    if (charIndex === 0) {
      deleting = false;
      msgIndex = (msgIndex + 1) % messages.length; // next message
    }
  }
  setTimeout(typeLoop, deleting ? 60 : 100); // speed: delete faster
}

// kick it off
typeLoop();
