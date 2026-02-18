import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Round3() {
  const [asciiValue, setAsciiValue] = useState(null);
  const [answer, setAnswer] = useState("");
  const [message, setMessage] = useState("");
  const [finalPhase, setFinalPhase] = useState(false);

  const navigate = useNavigate();
  const API = import.meta.env.VITE_API_URL;
  const session_code = localStorage.getItem("session_code");

  const startRound = async () => {
    const res = await axios.post(`${API}/api/start-round3/`, {
      session_code,
    });

    setAsciiValue(res.data.ascii); // now backend should send ascii
  };

  const submitAnswer = async () => {
    const res = await axios.post(`${API}/api/verify-round3/`, {
      session_code,
      answer,
    });

    if (res.data.completed) {
      setMessage("Round 3 Completed!");
      setTimeout(() => navigate("/dashboard"), 2000);
      return;
    }

    if (res.data.final_phase) {
      setFinalPhase(true);
      setAsciiValue(null);
      setAnswer("");
      setMessage("Enter only CAPITAL letters.");
      return;
    }

    if (res.data.success) {
      setAsciiValue(res.data.next_ascii);
      setAnswer("");
      setMessage("Correct!");
    } else {
      setMessage("Wrong Answer!");
    }
  };

  return (
    <div>
      <h2>Round 3 - ASCII Quiz</h2>

      {!finalPhase && asciiValue === null && (
        <button onClick={startRound}>Start Round 3</button>
      )}

      {!finalPhase && asciiValue !== null && (
        <>
          <h3>ASCII Code: {asciiValue}</h3>

          <input
            type="text"
            maxLength="1"
            placeholder="Enter character"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <br /><br />
          <button onClick={submitAnswer}>Submit</button>
        </>
      )}

      {finalPhase && (
        <>
          <h3>Enter CAPITAL letters only</h3>

          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <br /><br />
          <button onClick={submitAnswer}>Submit Final</button>
        </>
      )}

      <p>{message}</p>
    </div>
  );
}

export default Round3;
