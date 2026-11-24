# Verification Record

## Automated checks

- Godot `4.7.2.stable` project scan: passed.
- Blender `5.3.0` availability check: passed.
- Blender OBJ asset import during Godot export: passed.
- Godot headless run with `--quit-after 3`: exit code 0.
- Godot Web release export: passed; generated `index.html`, `index.js`, `index.wasm`, `index.pck`, audio worklets, and `index.png`.
- Traditional Chinese UI: passed; a static Traditional Chinese font is embedded in the Godot project and the Web shell is marked `lang="zh-Hant"`.
- Local HTTP server: root `index.html` and `index.wasm` reachable.

## Manual acceptance checklist

- [x] Start screen and story screen exist.
- [x] Level 1 requires two choices and awards the first KEY only for breakfast + umbrella.
- [x] Level 2 uses a slider and awards the second KEY only for 10元 per week.
- [x] Each level updates score; result screen shows 200/200 and learning outcomes.
- [ ] Real student usability study remains deferred.

## Known environment note

The in-app browser may show a canvas capability fallback for the Godot runtime even though the generated Web export is valid and served with the required files. Verify the deployed page in a current Chrome, Edge, or Firefox browser as the release acceptance browser.
