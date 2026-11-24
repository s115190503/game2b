# 小小夢魔：星光理財所

一款給小學生的原創生活理財投資網頁遊戲。視覺參考《Little Nightmares》的低光、異想探索氛圍，但角色、故事、美術與互動內容皆為本專案原創，並移除恐怖與暴力元素。

## 遊戲內容

- 第一關「月光雜貨間」：分辨生活中的「需要」與「想要」，答對取得第一把 KEY。
- 第二關「星光溫室」：用簡單算式規劃每週儲蓄，達成 3 週目標後取得第二把 KEY。
- 每關 100 分，結尾顯示兩關分數、總分與「星光理財小達人」進步成果。
- 支援手機版、鍵盤焦點、`prefers-reduced-motion`，無後端、無帳號、無外部 API。

## 本機預覽

直接用瀏覽器開啟 `index.html` 即可遊玩。若要用本機伺服器：

```bash
python -m http.server 8000
```

然後開啟 `http://localhost:8000`。

## GitHub Pages / Netlify

此專案是靜態網站，將整個資料夾推送到 GitHub 後，在 Settings → Pages 選擇分支與 `/ (root)`；Netlify 則直接將此資料夾拖入部署區，或連接 GitHub repository 即可。

## Blender 延伸資產

`blender/create_star_dreamling.py` 是可在 Blender 5.x 執行的原創低多邊形角色產生腳本，會建立小夢魔與星光燈場景並輸出 `.blend`、`.obj` 與預覽圖。網頁版目前採用零依賴 CSS 插畫以確保部署輕量；模型可作為下一版 Three.js 或 Godot HTML5 版本的資產來源。
