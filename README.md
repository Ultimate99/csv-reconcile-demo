# Local CSV reconciliation sample

Compare two UTF-8 CSV exports by a unique ID. Reports missing records and field changes as JSON. Runs locally with Python 3.10+ and no packages, network calls or credentials. All included records are synthetic.

Run: `python reconcile.py before.csv after.csv --key id --output report.json`

Check: `python -m unittest -v`

The output must be a new filename. Input files remain unchanged. Rejects missing/duplicate IDs, malformed row widths and mismatched column sets. Column order can differ. Preserves leading zeros, Unicode and quoted multiline values. Compares exact text: `10` and `10.00` are different. Inputs must fit in memory. This sample is not an accounting certification or a live SharePoint connector. Reports contain input values; keep them private when using real data.

## Proposed introductory service

**US$25 fixed price, subject to agreeing scope before work:** adapt this tool to one buyer's two CSV export formats, one unique match key and one agreed comparison rule; deliver source code, sample report, tests and run instructions. One correction round for the agreed specification. Larger integrations are quoted separately. Payment timing and PayPal availability must be agreed before starting client work.

This is a new AI-assisted demonstration, not a past client project. No sales, client references or earnings are claimed. The price is an offer, not confirmed demand or an agreed contract.

Interested in the scoped customization? Open a repository issue describing only your column names, matching rule and expected result, using synthetic examples. Do not post real exports, credentials, financial records or payment details publicly. Availability, final scope and payment terms require confirmation before work starts.
