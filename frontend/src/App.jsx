import { useState } from "react";
import "./App.css";

const QUESTION_TYPES = [
  { value: "linear_equation", label: "Linear equations" },
  { value: "quadratic_equation", label: "Quadratic equations" },
  { value: "system_of_linear_equations", label: "Systems of linear equations" },
];

const DIFFICULTIES = ["easy", "medium", "hard"];

function App() {
  const [questionType, setQuestionType] = useState("linear_equation");
  const [difficulty, setDifficulty] = useState("easy");
  const [count, setCount] = useState(5);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  async function handleGenerate() {
    setIsLoading(true);
    setErrorMessage(null);

    const url = `http://127.0.0.1:8000/worksheet?question_type=${questionType}&difficulty=${difficulty}&count=${count}`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        const errorBody = await response.json();
        throw new Error(errorBody.detail || "Something went wrong.");
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "worksheet_package.zip";
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="title-block">
        <h1>Worksheet Generator</h1>
        <p className="tagline">Math worksheets and answer keys, ready to print.</p>
        <hr className="rule" />
      </div>

      <div className="form-panel">
        <label className="field">
          Question type
          <select
            value={questionType}
            onChange={(e) => setQuestionType(e.target.value)}
          >
            {QUESTION_TYPES.map((qt) => (
              <option key={qt.value} value={qt.value}>
                {qt.label}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          Difficulty
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            {DIFFICULTIES.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          Number of questions
          <input
            type="number"
            min={1}
            max={50}
            value={count}
            onChange={(e) => setCount(Number(e.target.value))}
          />
        </label>

        <button
          className="generate-button"
          onClick={handleGenerate}
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate worksheet"}
        </button>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </div>
    </div>
  );
}

export default App;