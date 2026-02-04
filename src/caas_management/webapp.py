from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict
from urllib.parse import parse_qs

from caas_management.compliance_agent import ComplianceAgent
from caas_management.kyu_agent import KYUAgent
from caas_management.models import RequestContext
from caas_management.orchestrator import ComplianceOrchestrator, OrchestrationInputs
from caas_management.perception import CompliancePipeline


HTML_PAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Agentic Consent Manager Demo</title>
    <style>
      body {
        font-family: "Segoe UI", Roboto, sans-serif;
        background: #f6f7fb;
        margin: 0;
        padding: 32px;
        color: #1f2933;
      }
      .container {
        max-width: 960px;
        margin: 0 auto;
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 12px 30px rgba(30, 41, 59, 0.08);
      }
      h1 {
        margin-top: 0;
        font-size: 28px;
      }
      form {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
      }
      label {
        display: block;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #52606d;
        margin-bottom: 6px;
      }
      input, textarea {
        width: 100%;
        padding: 10px 12px;
        border-radius: 8px;
        border: 1px solid #d9e2ec;
        font-size: 14px;
      }
      textarea {
        min-height: 90px;
      }
      .full {
        grid-column: 1 / -1;
      }
      button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
      }
      .results {
        margin-top: 24px;
        padding: 16px;
        border-radius: 12px;
        background: #f0f4ff;
      }
      .results pre {
        white-space: pre-wrap;
        margin: 0;
        font-family: "SFMono-Regular", ui-monospace, monospace;
        font-size: 13px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Agentic Consent Manager Demo</h1>
      <p>Enter a request to see how the perception, reasoning, and orchestration layers respond.</p>
      <form method="post" action="/submit">
        <div>
          <label for="data_principal_id">Data principal ID</label>
          <input id="data_principal_id" name="data_principal_id" value="dp-001" required />
        </div>
        <div>
          <label for="requester_email">Requester email</label>
          <input id="requester_email" name="requester_email" value="analyst@bank.example" required />
        </div>
        <div>
          <label for="purpose">Purpose</label>
          <input id="purpose" name="purpose" value="Loan underwriting" required />
        </div>
        <div>
          <label for="domain">Domain</label>
          <input id="domain" name="domain" value="finance" required />
        </div>
        <div>
          <label for="attributes">Attributes (comma-separated)</label>
          <input id="attributes" name="attributes" value="income,employment" required />
        </div>
        <div>
          <label for="receiving_entity">Receiving entity</label>
          <input id="receiving_entity" name="receiving_entity" value="Acme Bank" required />
        </div>
        <div class="full">
          <label for="source_ip">Source IP</label>
          <input id="source_ip" name="source_ip" value="203.0.113.42" required />
        </div>
        <div class="full">
          <button type="submit">Run Agentic Decision</button>
        </div>
      </form>
      {results_block}
    </div>
  </body>
</html>
"""


class ConsentDemoHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self._send_html("", status=200)

    def do_POST(self) -> None:
        if self.path != "/submit":
            self._send_html("Unknown route", status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        payload = {key: values[0] for key, values in parse_qs(body).items()}
        results = self._run_pipeline(payload)
        results_html = f"<div class=\"results\"><pre>{html.escape(results)}</pre></div>"
        self._send_html(results_html, status=200)

    def _run_pipeline(self, payload: Dict[str, str]) -> str:
        pipeline = CompliancePipeline()
        request = pipeline.normalize_request(payload)
        kyu_result = KYUAgent().calculate_trust_score(
            request.requester_email, request.purpose
        )
        compliance_result = ComplianceAgent().classify(request.domain, request.attributes)
        decision = ComplianceOrchestrator().decide(
            OrchestrationInputs(
                trust_score=kyu_result.trust_score, sensitivity=compliance_result.sensitivity
            )
        )
        return (
            f"Request: {request}\n"
            f"KYU: {kyu_result}\n"
            f"Compliance: {compliance_result}\n"
            f"Decision: {decision}\n"
        )

    def _send_html(self, results_block: str, status: int) -> None:
        content = HTML_PAGE.format(results_block=results_block).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), ConsentDemoHandler)
    print(f"Serving demo at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
