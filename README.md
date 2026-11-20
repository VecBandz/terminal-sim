# Terminal SIM: Linux CLI

A safe Linux command-line simulator. Learn the terminal right on your phone: nothing you type touches your real device.

**▶ Open it:** https://vecbandz.github.io/terminal-sim/
**⬇ Offline file (always the latest):** https://github.com/VecBandz/terminal-sim/raw/main/Terminal-SIM.html

- 12 guided modules: setup, packages, files, Git, Python, SSH and networking, monitoring, security basics and more
- 62 tasks that tick off by themselves when you run the right command
- Searchable command reference (tap to copy)
- 20-question quiz with explanations
- Works offline. No account, no ads, no tracking

## Install it like an app
Open the link above on your phone, then use your browser's **Add to Home Screen** (or **Install app**).
It works offline and updates itself: when a new version is out, you'll see "New version of Terminal SIM ready. Tap to update."

## Follow the video series
Every module has a narrated episode on the VecBandz and David Haddix Facebook pages.
Get it free on Gumroad: https://vecbandz.gumroad.com/l/termuxtrainer

## For the maintainer: releasing an update
1. Replace `index.html` and `Terminal-SIM.html` with the new build (keep the install/update block at the end of `index.html`).
2. Bump `VERSION` in `sw.js` and the version in `version.json`.
3. Commit and push to `main`. GitHub Pages republishes in about a minute, and the offline-file link serves the new `Terminal-SIM.html` right away.
4. Optional: tag the commit (for example `v1.0.1`) to keep a record of each version.

---
Terminal SIM is an independent learning simulator. It is not affiliated with or endorsed by the Termux project.
