import React, { useState } from "react";
import "./App.css";

function App() {
  const [topic, setTopic] = useState("");
  const [model1, setModel1] = useState("openai");
  const [model2, setModel2] = useState("claude");
  const [position1, setPosition1] = useState("support");
  const [rounds, setRounds] = useState(3);
  const [debateHistory, setDebateHistory] = useState([]);
  const [isDebating, setIsDebating] = useState(false);

  const models = [
    { value: "openai", label: "OpenAI" },
    { value: "claude", label: "Claude" },
    { value: "deepseek", label: "Deepseek" },
  ];

  const handleStartDebate = async () => {
    if (!topic) return;

    setIsDebating(true);
    setDebateHistory([]);

    // TODO: Implement API call to backend
    // This is a placeholder for the actual implementation
    const mockResponse = {
      round: 1,
      model1: {
        name: model1,
        position: position1,
        argument: `This is a sample argument from ${model1} supporting the topic: ${topic}`,
      },
      model2: {
        name: model2,
        position: position1 === "support" ? "oppose" : "support",
        argument: `This is a sample counter-argument from ${model2}`,
      },
    };

    setDebateHistory([mockResponse]);
    setIsDebating(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Debate Platform</h1>
      </header>

      <main className="debate-container">
        <div className="input-section">
          <div className="form-group">
            <label htmlFor="topic">Debate Topic:</label>
            <input
              type="text"
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter debate topic"
            />
          </div>

          <div className="form-group">
            <label>AI Model 1:</label>
            <select value={model1} onChange={(e) => setModel1(e.target.value)}>
              {models.map((model) => (
                <option key={model.value} value={model.value}>
                  {model.label}
                </option>
              ))}
            </select>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  value="support"
                  checked={position1 === "support"}
                  onChange={() => setPosition1("support")}
                />
                Support
              </label>
              <label>
                <input
                  type="radio"
                  value="oppose"
                  checked={position1 === "oppose"}
                  onChange={() => setPosition1("oppose")}
                />
                Oppose
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>AI Model 2:</label>
            <select value={model2} onChange={(e) => setModel2(e.target.value)}>
              {models.map((model) => (
                <option key={model.value} value={model.value}>
                  {model.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="rounds">Number of Rounds:</label>
            <input
              type="number"
              id="rounds"
              value={rounds}
              onChange={(e) => setRounds(parseInt(e.target.value))}
              min="1"
              max="10"
            />
          </div>

          <button onClick={handleStartDebate} disabled={isDebating || !topic}>
            Start Debate
          </button>
        </div>

        <div className="debate-history">
          {debateHistory.map((round, index) => (
            <div key={index} className="debate-round">
              <h3>Round {round.round}</h3>
              <div className="argument">
                <h4>
                  {round.model1.name} ({round.model1.position}):
                </h4>
                <p>{round.model1.argument}</p>
              </div>
              <div className="argument">
                <h4>
                  {round.model2.name} ({round.model2.position}):
                </h4>
                <p>{round.model2.argument}</p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
