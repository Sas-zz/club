import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const [roundsCompleted, setRoundsCompleted] = useState(0);
  const navigate = useNavigate();

  const API = import.meta.env.VITE_API_URL;
  const session_code = localStorage.getItem("session_code");

  const fetchProgress = async () => {
    try {
      const res = await axios.post(`${API}/api/progress/`, {
        session_code,
      });

      setRoundsCompleted(res.data.rounds_completed);
    } catch {
      console.log("Failed to fetch progress");
    }
  };

  useEffect(() => {
    fetchProgress();
  }, []);

  return (
    <div>
      <h2>Game Dashboard</h2>

      <p>Rounds Completed: {roundsCompleted} / 4</p>

      <br />

      {/* ROUND 1 */}
      <button
        onClick={() => navigate("/round1")}
        disabled={roundsCompleted >= 1}
      >
        Round 1
      </button>

      <br /><br />

      {/* ROUND 2 */}
      <button
        onClick={() => navigate("/round2")}
        disabled={roundsCompleted < 1 || roundsCompleted >= 2}
      >
        Round 2
      </button>

      <br /><br />

      {/* ROUND 3 */}
      <button
        onClick={() => navigate("/round3")}
        disabled={roundsCompleted < 2 || roundsCompleted >= 3}
      >
        Round 3
      </button>

      <br /><br />

      {/* ROUND 4 */}
      <button
        onClick={() => navigate("/round4")}
        disabled={roundsCompleted < 3 || roundsCompleted >= 4}
      >
        Final Round
      </button>

      <br /><br />

      {/* GAME COMPLETED */}
      {roundsCompleted === 4 && (
        <>
          <h3>🎉 Game Completed!</h3>
          <button onClick={() => navigate("/winner")}>
            View Winner Page
          </button>
        </>
      )}
    </div>
  );
}

export default Dashboard;
