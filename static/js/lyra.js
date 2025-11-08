// === LYRA ELEMENTS ===
const lyraBubble = document.getElementById('lyra-container');
const lyraBox = document.getElementById('lyra-chatbox');
const lyraSend = document.getElementById('lyra-send');
const lyraInput = document.getElementById('lyra-input-text');
const lyraMessages = document.getElementById('lyra-messages');

// ✅ TOGGLE CHATBOX VISIBILITY
lyraBubble.addEventListener('click', (event) => {
  event.stopPropagation(); // prevent instant close
  lyraBox.classList.toggle('active'); // show/hide using .active (matches CSS)
});

// ✅ CLOSE WHEN CLICKING OUTSIDE
document.addEventListener('click', (event) => {
  if (!lyraBox.contains(event.target) && !lyraBubble.contains(event.target)) {
    lyraBox.classList.remove('active');
  }
});

// ✅ SEND MESSAGE ON CLICK OR ENTER
lyraSend.addEventListener('click', sendLyraMessage);
lyraInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendLyraMessage();
});

// === MAIN SEND FUNCTION ===
function sendLyraMessage() {
  const text = lyraInput.value.trim();
  if (!text) return;

  appendMessage('You', text);
  lyraInput.value = '';

  const typing = document.createElement('div');
  typing.classList.add('lyra-typing');
  typing.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
  lyraMessages.appendChild(typing);

  fetch('/lyra', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  })
  .then(res => res.json())
  .then(data => {
    setTimeout(() => {
      typing.remove();

      // Standard reply
      if (data.type === "text" || !data.type) {
        appendMessage("Lyra", data.message || data.reply || "Hmm...");
        speak(data.message || data.reply || "");
      }
      // Option buttons
      else if (data.type === "options") {
        appendMessage("Lyra", data.message);
        showLyraOptions(data.buttons);
      }
    }, 1200);
  });
}

// === SHOW OPTIONS (GENRE / ARTIST / FACIAL) ===
function showLyraOptions(buttons) {
  const container = document.createElement('div');
  container.classList.add('lyra-options');

  buttons.forEach(btn => {
    const bubble = document.createElement('button');
    bubble.classList.add('lyra-option-bubble');
    bubble.innerText = btn.label;
    bubble.onclick = () => window.location.href = btn.link;
    container.appendChild(bubble);
  });

  lyraMessages.appendChild(container);
  lyraMessages.scrollTop = lyraMessages.scrollHeight;
}

// === DISPLAY MESSAGES ===
function appendMessage(sender, text) {
  const msg = document.createElement('div');
  msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
  lyraMessages.appendChild(msg);
  lyraMessages.scrollTop = lyraMessages.scrollHeight;
}

// === TEXT TO SPEECH ===
function speak(text) {
  if (!text) return;
  const u = new SpeechSynthesisUtterance(text);
  u.pitch = 1;
  u.rate = 1;
  speechSynthesis.speak(u);
}
