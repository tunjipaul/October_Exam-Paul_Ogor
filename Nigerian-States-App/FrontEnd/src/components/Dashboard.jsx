import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import StateCard from "./StateCard";

function Dashboard() {
  const [states, setStates] = useState([]);
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("user");
    navigate("/login");
  };

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (!user) {
      navigate("/login");
      return;
    }

    const loadStates = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/states");
        const data = await res.json();
        setStates(data.states || []);
      } catch (err) {
        console.error("Failed to load states:", err);
      }
    };
    loadStates();
  }, [navigate]);

  return (
    <div className="dashboard-container">
      <button className="logout-btn" onClick={logout}>
        Logout
      </button>
      <button onClick={() => window.scrollTo(0, document.body.scrollHeight)} className="buttonBottom">Scroll to Bottom</button>
      <div className="states-grid">
        {states.map((s) => (
          <StateCard key={s.id} state={s} />
        ))}
      </div>
      <button onClick={() => window.scrollTo(0, 0)} className="buttonTop">Scroll to top</button>
    </div>
  );
}

export default Dashboard;
