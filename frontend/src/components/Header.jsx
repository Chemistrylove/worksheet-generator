function Header() {
  return (
    <header className="site-header">
      <a href="/" className="wordmark" aria-label="Worksheet Generator home">
        <span className="wordmark-line">Worksheet</span>
        <span className="wordmark-line">Generator</span>
      </a>
      <nav className="site-nav" aria-label="Primary">
        <span className="site-nav-subject">Mathematics</span>
        <span className="site-nav-dot" aria-hidden="true" />
        <span className="site-nav-meta">Printable PDFs</span>
      </nav>
    </header>
  );
}

export default Header;
