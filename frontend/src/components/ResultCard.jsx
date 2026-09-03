const DIFFICULTY_LABELS = {
  easy: "Easy",
  medium: "Medium",
  hard: "Hard",
};

function ResultCard({ result, onDownload, onReset }) {
  const { questionTypeLabel, difficulty, count, fileName } = result;

  return (
    <section className="result" aria-labelledby="result-title" aria-live="polite">
      <div className="result-status">
        <span className="result-check" aria-hidden="true">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path
              d="M2.5 6.5 5 9l4.5-6"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
        Generated
      </div>

      <h2 id="result-title" className="result-title">
        Your worksheet is ready.
      </h2>
      <p className="result-lede">
        Your download should have started automatically. If it did not, use
        the button below.
      </p>

      <div className="document">
        <div className="document-sheet" aria-hidden="true">
          <div className="document-rule document-rule--title" />
          <div className="document-rule" />
          <div className="document-rule document-rule--short" />
          <div className="document-rule" />
          <div className="document-rule document-rule--short" />
        </div>
        <dl className="document-meta">
          <div className="document-meta-row">
            <dt>Topic</dt>
            <dd>{questionTypeLabel}</dd>
          </div>
          <div className="document-meta-row">
            <dt>Difficulty</dt>
            <dd>{DIFFICULTY_LABELS[difficulty] ?? difficulty}</dd>
          </div>
          <div className="document-meta-row">
            <dt>Questions</dt>
            <dd>{count}</dd>
          </div>
          <div className="document-meta-row">
            <dt>Contents</dt>
            <dd>worksheet.pdf, answer_key.pdf</dd>
          </div>
        </dl>
      </div>

      <div className="result-actions">
        <button type="button" className="button-primary" onClick={onDownload}>
          Download worksheet &amp; answer key
          <span className="button-file" aria-hidden="true">
            {fileName}
          </span>
        </button>
        <button type="button" className="button-secondary" onClick={onReset}>
          Create another
        </button>
      </div>
    </section>
  );
}

export default ResultCard;
