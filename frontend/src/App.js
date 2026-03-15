import { useState } from "react";

function App(){

const [msg,setMsg]=useState("");
const [chat,setChat]=useState([]);

const speak = async (text) => {

  const res = await fetch("http://127.0.0.1:8000/text-to-speech", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: text })
  });

  const blob = await res.blob();

  const audioUrl = URL.createObjectURL(blob);

  const audio = new Audio(audioUrl);

  audio.play().catch(err => console.log("Audio play error:", err));
};
// send message to backend
const sendMessage = async () => {
  if (!msg.trim()) return;
  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });
    const data = await res.json();
    setChat([...chat, { user: msg, bot: data.reply }]);
    speak(data.reply);
    setMsg("");
  } catch (error) {
    alert("Error: " + error.message);
  }
};

// voice input
const startVoice = () => {

const recognition = new window.webkitSpeechRecognition();

recognition.lang = "en-IN";   // language (change later if needed)

recognition.onresult = (event) => {

const speechText = event.results[0][0].transcript;

setMsg(speechText);

};

recognition.start();

};

return(

<div style={{padding:"20px"}}>

<h2>University AI Helpdesk</h2>

<input
value={msg}
onChange={(e)=>setMsg(e.target.value)}
placeholder="Ask your question..."
/>

<button onClick={sendMessage}>Send</button>

<button onClick={startVoice}>🎤 Speak</button>

{chat.map((c,i)=>(
<div key={i}>
<p><b>Student:</b> {c.user}</p>
<p><b>Bot:</b> {c.bot}</p>
</div>
))}

</div>

)

}

export default App;