<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>scan.py · animated readme</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      background: #0d1117;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 1.5rem;
    }

    /* GitHub-style card */
    .readme-container {
      max-width: 860px;
      width: 100%;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      transition: border-color 0.3s ease;
    }

    .readme-container:hover {
      border-color: #58a6ff;
    }

    /* header bar like GitHub file view */
    .file-header {
      background: #21262d;
      padding: 0.75rem 1.2rem;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid #30363d;
    }

    .file-icon {
      color: #8b949e;
      font-size: 1.1rem;
    }

    .file-name {
      color: #e6edf3;
      font-size: 0.9rem;
      font-weight: 500;
    }

    .file-name span {
      color: #58a6ff;
    }

    .badge {
      margin-left: auto;
      background: #238636;
      color: #ffffff;
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 20px;
      letter-spacing: 0.3px;
      animation: badgePulse 2s infinite;
    }

    @keyframes badgePulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }

    /* terminal body */
    .terminal-body {
      padding: 1.5rem 1.5rem 1.8rem;
      background: #0d1117;
    }

    /* command line */
    .terminal-line {
      display: flex;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 6px;
      font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
      font-size: 1.1rem;
      background: #161b22;
      padding: 1.1rem 1.3rem;
      border-radius: 8px;
      border: 1px solid #30363d;
      position: relative;
      overflow: hidden;
      margin-bottom: 1.5rem;
    }

    .terminal-line::after {
      content: "";
      position: absolute;
      top: 0;
      left: -100%;
      width: 50%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(88, 166, 255, 0.08), transparent);
      animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
      0% { left: -100%; }
      100% { left: 150%; }
    }

    .prompt {
      color: #3fb950;
      font-weight: 700;
      font-size: 1.2rem;
      margin-right: 4px;
    }

    .cmd-python {
      color: #79c0ff;
      font-weight: 600;
    }

    .cmd-script {
      color: #d2a8ff;
    }

    .cmd-file {
      color: #7ee787;
    }

    .cmd-flag {
      color: #ffa657;
    }

    .cmd-output {
      color: #ff7b72;
    }

    .cursor {
      display: inline-block;
      width: 9px;
      height: 1.3rem;
      background: #e6edf3;
      margin-left: 6px;
      animation: blink 1.1s step-end infinite;
      vertical-align: middle;
      border-radius: 1px;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }

    /* scan results grid */
    .scan-results {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 1.5rem;
    }

    @media (max-width: 500px) {
      .scan-results {
        grid-template-columns: 1fr;
      }
    }

    .result-item {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 0.85rem 1rem;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: border-color 0.2s ease, background 0.2s ease;
    }

    .result-item:hover {
      border-color: #58a6ff;
      background: #1c2128;
    }

    .result-icon {
      font-size: 1.3rem;
      line-height: 1;
      filter: drop-shadow(0 0 6px currentColor);
    }

    .result-text {
      display: flex;
      flex-direction: column;
      gap: 2px;
      overflow: hidden;
    }

    .result-label {
      font-size: 0.7rem;
      color: #8b949e;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      font-weight: 500;
    }

    .result-value {
      font-family: 'SFMono-Regular', Consolas, monospace;
      font-size: 0.9rem;
      color: #e6edf3;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .value-green {
      color: #7ee787;
    }

    .value-blue {
      color: #79c0ff;
    }

    .value-yellow {
      color: #ffa657;
    }

    /* progress bar */
    .progress-container {
      margin-bottom: 1.8rem;
    }

    .progress-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 6px;
      font-size: 0.75rem;
      color: #8b949e;
      font-family: 'SFMono-Regular', Consolas, monospace;
    }

    .progress-track {
      height: 10px;
      background: #21262d;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid #30363d;
    }

    .progress-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #238636, #3fb950, #7ee787, #3fb950, #238636);
      background-size: 300% 100%;
      border-radius: 6px;
      animation: progressFill 2.5s infinite alternate, gradientShift 2s infinite;
      box-shadow: 0 0 12px rgba(63, 185, 80, 0.5);
    }

    @keyframes progressFill {
      0% { width: 15%; }
      50% { width: 82%; }
      100% { width: 68%; }
    }

    @keyframes gradientShift {
      0% { background-position: 0% 0%; }
      100% { background-position: 100% 0%; }
    }

    /* footer */
    .readme-footer {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      padding-top: 1.2rem;
      border-top: 1px solid #30363d;
      color: #8b949e;
      font-size: 0.8rem;
    }

    .footer-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      background: #3fb950;
      border-radius: 50%;
      animation: pulse 1.5s infinite;
      box-shadow: 0 0 8px #3fb950;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }

    .footer-right {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: 'SFMono-Regular', Consolas, monospace;
      font-size: 0.75rem;
    }

    .footer-right span {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .shield-icon {
      color: #d2a8ff;
      animation: gentleWiggle 3s infinite;
    }

    @keyframes gentleWiggle {
      0%, 100% { transform: rotate(0deg); }
      25% { transform: rotate(8deg); }
      75% { transform: rotate(-8deg); }
    }

    /* subtle noise texture overlay */
    .terminal-body::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.02'/%3E%3C/svg%3E");
      pointer-events: none;
      opacity: 0.3;
      z-index: 0;
    }

    .terminal-body {
      position: relative;
    }

    .terminal-body > * {
      position: relative;
      z-index: 1;
    }
  </style>
</head>
<body>
  <div class="readme-container">
    <!-- GitHub file header -->
    <div class="file-header">
      <span class="file-icon">📄</span>
      <span class="file-name"><span>scan.py</span> · README</span>
      <span class="badge">● active</span>
    </div>

    <!-- terminal preview -->
    <div class="terminal-body">
      <!-- animated command -->
      <div class="terminal-line">
        <span class="prompt">$</span>
        <span class="cmd-python">python3</span>
        <span class="cmd-script">scan.py</span>
        <span class="cmd-file">file.txt</span>
        <span class="cmd-flag">-o</span>
        <span class="cmd-output">results</span>
        <span class="cursor"></span>
      </div>

      <!-- scan result cards -->
      <div class="scan-results">
        <div class="result-item">
          <span class="result-icon" style="color: #58a6ff;">🔍</span>
          <div class="result-text">
            <span class="result-label">scan target</span>
            <span class="result-value">file.txt · 12.4 MB</span>
          </div>
        </div>
        <div class="result-item">
          <span class="result-icon" style="color: #d2a8ff;">⚡</span>
          <div class="result-text">
            <span class="result-label">patterns found</span>
            <span class="result-value value-blue">42 signatures</span>
          </div>
        </div>
        <div class="result-item">
          <span class="result-icon" style="color: #ffa657;">📦</span>
          <div class="result-text">
            <span class="result-label">output directory</span>
            <span class="result-value value-yellow">results/</span>
          </div>
        </div>
        <div class="result-item">
          <span class="result-icon" style="color: #3fb950;">✅</span>
          <div class="result-text">
            <span class="result-label">status</span>
            <span class="result-value value-green">complete · 0.34s</span>
          </div>
        </div>
      </div>

      <!-- progress -->
      <div class="progress-container">
        <div class="progress-header">
          <span>⏳ scan progress</span>
          <span>79%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill"></div>
        </div>
      </div>

      <!-- footer -->
      <div class="readme-footer">
        <div class="footer-left">
          <span class="pulse-dot"></span>
          <span>ready to scan</span>
        </div>
        <div class="footer-right">
          <span><span class="shield-icon">🛡️</span> safe</span>
          <span>⚡ fast</span>
          <span>📄 file.txt</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
