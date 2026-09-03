import { useEffect, useRef, useState } from "react";
import Header from "./components/Header.jsx";
import SettingsPanel from "./components/SettingsPanel.jsx";
import ResultCard from "./components/ResultCard.jsx";
import "./App.css";

const QUESTION_TYPES = [
  { value: "linear_equation", label: "Linear equations" },
  { value: "quadratic_equation", label: "Quadratic equations" },
  { value: "system_of_linear_equations", label: "Systems of linear equations" },
];

const DIFFICULTIES = ["easy", "medium", "hard"];

const DOWNLOAD_FILE_NAME = "worksheet_package.zip";

function triggerDownload(url, fileName) {
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  link.click();
}

function App() {
  const [questionType, setQuestionType] = useState("linear_equation");
  const [difficulty, setDifficulty] = useState("easy");
  const [count, setCount] = useState(5);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [result, setResult] = useState(null);

  const resultRef = useRef(null);

  // Release the object URL when it is replaced or the app unmounts.
  useEffect(() => {
    if (!result) return;
    return () => window.URL.revokeObjectURL(result.downloadUrl);
  }, [result]);

  async function handleGenerate() {
    setIsLoading(true);
    setErrorMessage(null);
    setResult(null);

    const url = `http://127.0.0.1:8000/worksheet?question_type=${questionType}&difficulty=${difficulty}&count=${count}`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        const errorBody = await response.json();
        throw new Error(errorBody.detail || "Something went wrong.");
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      triggerDownload(downloadUrl, DOWNLOAD_FILE_NAME);

      const selectedType = QUESTION_TYPES.find((qt) => qt.value === questionType);
      setResult({
        downloadUrl,
        fileName: DOWNLOAD_FILE_NAME,
        questionTypeLabel: selectedType ? selectedType.label : questionType,
        difficulty,
        count,
      });
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  function handleDownloadAgain() {
    if (!result) return;
    triggerDownload(result.downloadUrl, result.fileName);
  }

  function handleReset() {
    setResult(null);
    setErrorMessage(null);
  }

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }, [result]);

  return (
    <div className="page">
      <Header />

      <main className="main">
        <section className="intro">
          <p className="eyebrow">Mathematics · Worksheets &amp; answer keys</p>
          <h1 className="headline">Create a worksheet.</h1>
          <p className="lede">Choose what you want your students to practice.</p>
          <p className="lede lede--secondary">
            Generate printable mathematics worksheets and answer keys in seconds.
          </p>
        </section>

        <div className="workspace">
          <SettingsPanel
            questionTypes={QUESTION_TYPES}
            difficulties={DIFFICULTIES}
            questionType={questionType}
            difficulty={difficulty}
            count={count}
            isLoading={isLoading}
            errorMessage={errorMessage}
            onQuestionTypeChange={setQuestionType}
            onDifficultyChange={setDifficulty}
            onCountChange={setCount}
            onSubmit={handleGenerate}
          />

          <div className="workspace-side" ref={resultRef}>
            {result ? (
              <ResultCard
                result={result}
                onDownload={handleDownloadAgain}
                onReset={handleReset}
              />
            ) : (
              <aside className="steps" aria-label="How it works">
                <h2 className="steps-title">How it works</h2>
                <ol className="steps-list">
                  <li className={isLoading ? "" : "is-current"}>
                    <span className="steps-label">Configure</span>
                    <span className="steps-text">
                      Pick a topic, difficulty, and length.
                    </span>
                  </li>
                  <li className={isLoading ? "is-current" : ""}>
                    <span className="steps-label">Generate</span>
                    <span className="steps-text">
                      Problems are generated and verified programmatically.
                    </span>
                  </li>
                  <li>
                    <span className="steps-label">Download</span>
                    <span className="steps-text">
                      Receive a worksheet PDF and a separate answer key.
                    </span>
                  </li>
                </ol>
              </aside>
            )}
          </div>
        </div>
      </main>

      <footer className="site-footer">
        <p>Every problem and answer is generated and checked by code, not guessed.</p>
      </footer>
    </div>
  );
}

export default App;
