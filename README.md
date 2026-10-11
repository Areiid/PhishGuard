# PhishGuard

A small, beginner-friendly Python tool that helps people spot **phishing links and scam messages** — fake websites, emails, and texts that try to steal logins, money, or personal information.

PhishGuard does **not** visit websites or send your text anywhere. It only reads what you paste on your computer, then explains the result in everyday language.

## What it is good for

Online scams hurt people who are busy, new to the internet, or trying to help family members. A fake “PayPal security” page can look almost real. PhishGuard is a free practice and warning tool for:

- students learning digital safety
- families checking a suspicious text or email link
- libraries, classrooms, and community classes
- anyone who wants a second opinion **before** they click

It is **education**, not a magic shield. If something still feels wrong, do not click. Open a new tab and type the company name yourself, or use the official app.

## What it can catch

### Links (Phase 1)

| Warning sign | Example of the idea |
| --- | --- |
| Look-alike names | `paypa1` instead of `paypal` |
| Extra fake words in the address | `paypal.com.evil-site.net` |
| The `@` trick | `https://paypal.com@bad-site.example` |
| No `https` | `http://...` login pages |
| Number instead of a name | `http://192.168.1.50/paypal/login` |
| Hidden / unusual prefixes | `javascript:` or `xn--` look-alike letters |

### Messages (Phase 2)

| Warning sign | Example of the idea |
| --- | --- |
| Urgent pressure | “Act now or your account closes in 24 hours” |
| Threats | “You will be arrested” / “account locked” |
| Password or SSN requests | “Confirm your password” |
| Gift cards, wires, crypto | “Buy Apple gift cards and send the codes” |
| Fake invoices | “Wire payment to our new bank details” |
| “Don’t tell anyone” | Family emergency scams |
| Remote-access apps | “Install AnyDesk so we can help” |

If a message also contains a link, PhishGuard checks the **words and the address**.

## Who this is for

You only need:

- Python 3.10 or newer
- a terminal (Terminal on Mac, Command Prompt or PowerShell on Windows)

No account, no API key, no extra packages.

## File map (start here)

```
PhishGuard/
├── README.md                 ← you are here
├── main.py                   ← run this file
├── requirements.txt          ← empty on purpose (standard library only)
├── checker/
│   ├── url_checks.py         ← rules for links
│   ├── text_checks.py        ← rules for email/SMS wording
│   └── report.py             ← turns rules into a readable answer
├── data/
│   ├── known_brands.json     ← brands scammers often copy
│   └── suspicious_keywords.json
└── examples/
    ├── sample_urls.txt       ← practice links (do not visit them)
    └── sample_messages.txt   ← practice emails/texts (do not follow them)
```

## Setup

1. Install [Python 3](https://www.python.org/downloads/) if you do not have it.
2. Open a terminal in this folder.

```bash
cd PhishGuard
python3 --version
```

You should see Python 3.10 or higher. Nothing else to install.

## How to run it

In Cursor: open a terminal in this folder (**Terminal → New Terminal**) and type **`python3`**, not `python`.

Easiest — then paste a link when asked:

```bash
python3 main.py
```

Check one link (quotes keep the whole address together):

```bash
python3 main.py "https://paypa1-secure-login.com"
```

Run the practice list:

```bash
python3 main.py --examples
```

### If it does not start

| What you see | What to do |
| --- | --- |
| `python: command not found` | Use `python3` instead of `python`. |
| `can't open file 'main.py'` | You are in the wrong folder. Run `cd /Users/anthonyr./PhishGuard` first. |
| `No module named 'checker'` | Same fix: run `main.py` from the PhishGuard folder, or use `python3 /Users/anthonyr./PhishGuard/main.py`. |
| Play button in Cursor does nothing useful | Use the terminal commands above so you can paste a link. |

### Sample output

```
PhishGuard — URL check (Phase 1)
========================================
Checked: https://paypa1-secure-login.com
Risk:    High

Why:
  1. [HIGH] Look-alike of PayPal
     'paypa1-secure-login.com' is close to the real PayPal domain...
```

## How to read the risk level

- **High** — common scam pattern. Do not click.
- **Medium** — something is off. Slow down and verify another way.
- **Looks OK (so far)** — Phase 1 did not see its warning signs. The page could still be fake.

## Privacy

Your URL stays on your machine. There is no server, no tracking, and no log file.

## What this will never do

- It will not open or “test-click” the link for you (that would be unsafe).
- It will not tell you that a site is 100% safe.
- It does not replace your bank’s official app or a phone number you already trust.

## Next phases (not built yet)

- Phase 2: check the wording of emails and texts (urgency, threats, fake invoices)
- Phase 3: more practice examples and a clearer report
- Phase 4: automated tests so the rules stay reliable

## License

Use and share freely for education and personal protection.
