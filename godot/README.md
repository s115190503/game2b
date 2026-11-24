# Godot Web 版

使用 Godot 4.7.2 建立，主場景為 `main.tscn`，輸出預設為 Web 平台。

## 本機執行

```powershell
C:\Godot\Godot_v4.7.2-stable_win64.exe --editor --path godot
```

## 匯出 HTML5

```powershell
C:\Godot\Godot_v4.7.2-stable_win64_console.exe --headless --path godot --export-release Web ../index.html
```

匯出後將 `index.html`、`index.js`、`index.wasm`、`index.pck` 一起部署到 GitHub Pages 或 Netlify。

