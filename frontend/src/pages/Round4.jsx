import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Round4() {
  const [answer, setAnswer] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();
  const API = import.meta.env.VITE_API_URL;
  const session_code = localStorage.getItem("session_code");

  const submitAnswer = async () => {
    try {
      const res = await axios.post(`${API}/api/verify-round4/`, {
        session_code,
        answer,
      });

      if (res.data.completed) {
        setTimeout(() => {
          navigate("/winner");
        }, 1500);
      } else {
        setMessage("Wrong!");
      }

    } catch {
      setMessage("Error");
    }
  };

  return (
    <div>
      <h2>Final Round</h2>

      <h3>heyyyy</h3>

      {/* hidden typing */}
      <input
        type="password"
        placeholder="Type here"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <br /><br />

      <button onClick={submitAnswer}>
        Submit
      </button>

      <p>{message}</p>
    </div>
  );
}

export default Round4;
