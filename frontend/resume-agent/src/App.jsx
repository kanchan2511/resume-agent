
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resumeText) return alert("Please paste a resume first!");
    
    setLoading(true);
    setResult(null); // Clear old results

    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze-resume", {
        text: resumeText,
      });
      
      console.log("Data received from backend:", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("Connection Error:", err);
      alert("Backend is not responding. Check your terminal!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🚀 AI Resume Feedback Agent</h1>
        <p>Get real-time market insights and skill gap analysis.</p>
      </header>

      <main className="container">
        <textarea 
          className="resume-input"
          placeholder="Paste your resume content here..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
        />
        
        <button 
          className={`analyze-btn ${loading ? 'loading' : ''}`}
          onClick={analyzeResume} 
          disabled={loading}
        >
          {loading ? "Thinking..." : "Analyze Resume"}
        </button>

        {loading && <div className="spinner"></div>}

        {result && (
          <div className="results-grid">
            <ResultCard title="✅ Strengths" data={result.strengths} color="green" />
            <ResultCard title="⚠️ Weaknesses" data={result.weaknesses} color="orange" />
            <ResultCard title="🔍 Missing Skills" data={result.missing_skills} color="red" />
            <ResultCard title="💡 Suggestions" data={result.suggestions} color="blue" />
          </div>
        )}
      </main>
    </div>
  );
}

// Sub-component for individual cards
function ResultCard({ title, data, color }) {
  return (
    <div className={`card ${color}`}>
      <h3>{title}</h3>
      <ul>
        {data && data.length > 0 ? (
          data.map((item, index) => <li key={index}>{item}</li>)
        ) : (
          <li>No data found.</li>
        )}
      </ul>
    </div>
  );
}

export default App;