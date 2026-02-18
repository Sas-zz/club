import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

function Round1() {
  const [currentSet, setCurrentSet] = useState(1);
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const session_code = localStorage.getItem("session_code");

  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        `${API}/api/verify-round1/`,
        {
          session_code: session_code,
          code: code,
        }
      );

      if (res.data.completed) {
        setMessage("Round Completed! Word: " + res.data.word);

        // go back to dashboard after 2 sec
        setTimeout(() => {
          navigate("/dashboard");
        }, 2000);

        return;
      }

      if (res.data.success) {
        setCurrentSet(res.data.next_set);
        setCode("");
        setMessage("Correct! Next Set.");
      } else {
        setMessage("Wrong Code!");
      }

    } catch (err) {
      setMessage("Error occurred");
    }
  };

  return (
    <div>
      <h2>Round 1 - Set {currentSet}</h2>

      <p>Go to: Location {currentSet}</p>

      <input
        type="text"
        placeholder="Enter 10 digit code"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSubmit}>Submit</button>

      <p>{message}</p>
    </div>
  );
}

export default Round1;
