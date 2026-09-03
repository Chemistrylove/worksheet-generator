const DIFFICULTY_LABELS = {
  easy: "Easy",
  medium: "Medium",
  hard: "Hard",
};

function SettingsPanel({
  questionTypes,
  difficulties,
  questionType,
  difficulty,
  count,
  isLoading,
  errorMessage,
  onQuestionTypeChange,
  onDifficultyChange,
  onCountChange,
  onSubmit,
}) {
  function handleSubmit(event) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <section className="panel" aria-labelledby="settings-title">
      <div className="panel-header">
        <svg
          className="panel-icon"
          width="18"
          height="18"
          viewBox="0 0 18 18"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M1 6h16M1 12h16M6 1v16M12 1v16"
            stroke="currentColor"
            strokeWidth="1.25"
            strokeLinecap="round"
          />
        </svg>
        <h2 id="settings-title" className="panel-title">
          Worksheet settings
        </h2>
      </div>

      <form className="settings-form" onSubmit={handleSubmit} noValidate>
        <div className="field">
          <label className="field-label" htmlFor="question-type">
            Question type
          </label>
          <div className="select-wrap">
            <select
              id="question-type"
              className="control"
              value={questionType}
              onChange={(e) => onQuestionTypeChange(e.target.value)}
              disabled={isLoading}
            >
              {questionTypes.map((qt) => (
                <option key={qt.value} value={qt.value}>
                  {qt.label}
                </option>
              ))}
            </select>
            <svg
              className="select-chevron"
              width="14"
              height="14"
              viewBox="0 0 14 14"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M3 5.25 7 9.25l4-4"
                stroke="currentColor"
                strokeWidth="1.4"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>

        <fieldset className="field" disabled={isLoading}>
          <legend className="field-label">Difficulty</legend>
          <div className="segmented" role="radiogroup" aria-label="Difficulty">
            {difficulties.map((d) => {
              const checked = difficulty === d;
              return (
                <label
                  key={d}
                  className={`segment${checked ? " is-selected" : ""}`}
                >
                  <input
                    type="radio"
                    name="difficulty"
                    value={d}
                    checked={checked}
                    onChange={() => onDifficultyChange(d)}
                    className="sr-only"
                  />
                  <span>{DIFFICULTY_LABELS[d] ?? d}</span>
                </label>
              );
            })}
          </div>
        </fieldset>

        <div className="field">
          <label className="field-label" htmlFor="question-count">
            Number of questions
          </label>
          <input
            id="question-count"
            className="control"
            type="number"
            inputMode="numeric"
            min={1}
            max={50}
            step={1}
            value={count}
            onChange={(e) => onCountChange(Number(e.target.value))}
            disabled={isLoading}
            aria-describedby="question-count-hint"
          />
          <p id="question-count-hint" className="field-hint">
            Between 1 and 50 questions per worksheet.
          </p>
        </div>

        <button
          type="submit"
          className="button-primary"
          disabled={isLoading}
          aria-busy={isLoading}
        >
          {isLoading ? (
            <>
              <span className="spinner" aria-hidden="true" />
              Generating worksheet...
            </>
          ) : (
            <>
              Generate worksheet
              <span className="button-arrow" aria-hidden="true">
                →
              </span>
            </>
          )}
        </button>

        {errorMessage && (
          <p className="form-error" role="alert">
            {errorMessage}
          </p>
        )}
      </form>
    </section>
  );
}

export default SettingsPanel;
