import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Round2() {
  const [number, setNumber] = useState(null);
  const [answer, setAnswer] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();
  const API = import.meta.env.VITE_API_URL;
  const session_code = localStorage.getItem("session_code");

  // Start Round 2
  const startRound = async () => {
    try {
      const res = await axios.post(`${API}/api/start-round2/`, {
        session_code: session_code,
      });

      setNumber(res.data.number);
    } catch (err) {
      setMessage("Error starting round");
    }
  };

  // Verify Answer
  const submitAnswer = async () => {
    try {
      const res = await axios.post(`${API}/api/verify-round2/`, {
        session_code: session_code,
        answer: answer,
      });

      if (res.data.completed) {
        setMessage("Round 2 Completed! word: how");

        setTimeout(() => {
          navigate("/dashboard");
        }, 2000);
      } else {
        setMessage("Wrong Answer!");
      }

    } catch (err) {
      setMessage("Error occurred");
    }
  };

  return (
    <div>
      <h2>Round 2</h2>

      {number === null ? (
        <button onClick={startRound}>Start Round 2</button>
      ) : (
        <>
          <p>Multiply this number by 2:</p>
          <h3>{number}</h3>

          <input
            type="number"
            placeholder="Enter answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <br /><br />

          <button onClick={submitAnswer}>Submit</button>
        </>
      )}

      <p>{message}</p>
    </div>
  );
}

export default Round2;
