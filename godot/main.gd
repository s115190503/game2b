extends Control

const BG := Color("10152d")
const PANEL := Color("1a2444")
const PANEL_2 := Color("24315a")
const GOLD := Color("ffd166")
const MINT := Color("8ee6c5")
const TEXT := Color("f5f3ff")
const MUTED := Color("b7bfdc")

var screen := "title"
var score_one := 0
var score_two := 0
var selected: Array[int] = []
var status_label: Label
var content: VBoxContainer
var score_label: Label
var hero: TextureRect

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	apply_traditional_chinese_theme()
	build_shell()
	show_title()

func apply_traditional_chinese_theme() -> void:
	var chinese_theme := Theme.new()
	chinese_theme.default_font = load("res://assets/NotoSansTC-VF.ttf")
	chinese_theme.default_font_size = 20
	theme = chinese_theme

func build_shell() -> void:
	var bg := ColorRect.new()
	bg.color = BG
	bg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)
	var glow := ColorRect.new()
	glow.color = Color("18254a")
	glow.position = Vector2(0, 500)
	glow.size = Vector2(1280, 220)
	glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(glow)
	var root := VBoxContainer.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT, Control.PRESET_MODE_MINSIZE, 32)
	root.add_theme_constant_override("separation", 16)
	add_child(root)
	var top := HBoxContainer.new()
	top.custom_minimum_size.y = 58
	root.add_child(top)
	var brand := Label.new()
	brand.text = "✦ 小小夢魔｜理財星門"
	brand.add_theme_font_size_override("font_size", 24)
	brand.add_theme_color_override("font_color", GOLD)
	top.add_child(brand)
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top.add_child(spacer)
	score_label = Label.new()
	score_label.add_theme_font_size_override("font_size", 20)
	score_label.add_theme_color_override("font_color", TEXT)
	top.add_child(score_label)
	content = VBoxContainer.new()
	content.size_flags_vertical = Control.SIZE_EXPAND_FILL
	content.add_theme_constant_override("separation", 18)
	root.add_child(content)
	status_label = Label.new()
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_label.add_theme_color_override("font_color", MUTED)
	status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	root.add_child(status_label)

func clear_content() -> void:
	for child in content.get_children():
		child.queue_free()
	status_label.text = ""
	update_score()

func update_score() -> void:
	if score_label:
		score_label.text = "目前得分　%03d / 200" % (score_one + score_two)

func add_title(text: String, subtitle: String) -> void:
	var title := Label.new()
	title.text = text
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 48)
	title.add_theme_color_override("font_color", TEXT)
	content.add_child(title)
	var sub := Label.new()
	sub.text = subtitle
	sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub.add_theme_font_size_override("font_size", 22)
	sub.add_theme_color_override("font_color", MUTED)
	sub.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	content.add_child(sub)

func make_button(text: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.custom_minimum_size = Vector2(0, 58)
	button.add_theme_font_size_override("font_size", 22)
	button.add_theme_color_override("font_color", BG)
	button.add_theme_color_override("font_hover_color", BG)
	var normal := StyleBoxFlat.new()
	normal.bg_color = GOLD
	normal.corner_radius_top_left = 16
	normal.corner_radius_top_right = 16
	normal.corner_radius_bottom_left = 16
	normal.corner_radius_bottom_right = 16
	button.add_theme_stylebox_override("normal", normal)
	var hover := normal.duplicate()
	hover.bg_color = Color("ffe29a")
	button.add_theme_stylebox_override("hover", hover)
	button.pressed.connect(action)
	return button

func show_title() -> void:
	screen = "title"
	clear_content()
	add_title("夢境裡的第一桶金", "跟著星星小夢魔學會分辨需要、想要，還有穩定儲蓄。")
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	content.add_child(row)
	var image := TextureRect.new()
	image.texture = load("res://assets/star_dreamling_preview.png")
	image.custom_minimum_size = Vector2(300, 230)
	image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	row.add_child(image)
	var card := VBoxContainer.new()
	card.custom_minimum_size = Vector2(430, 0)
	card.add_theme_constant_override("separation", 12)
	row.add_child(card)
	var intro := Label.new()
	intro.text = "兩個互動單元，答對才能拿到 KEY。\n完成後會看到你的理財進步成果。"
	intro.add_theme_font_size_override("font_size", 22)
	intro.add_theme_color_override("font_color", TEXT)
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	card.add_child(intro)
	card.add_child(make_button("開始冒險　→", show_story))
	var note := Label.new()
	note.text = "提示：你可以用滑鼠、觸控或鍵盤操作。"
	note.add_theme_color_override("font_color", MUTED)
	card.add_child(note)

func show_story() -> void:
	screen = "story"
	clear_content()
	add_title("星門需要兩把 KEY", "小夢魔的錢包被夜霧吹散了，我們要一起把理財知識找回來！")
	var panel := Label.new()
	panel.text = "第一關：把有限的錢先用在真正需要的地方。\n第二關：把每週的小額零用錢，固定放進儲蓄罐。\n\n每關 100 分，答對就能開啟下一道星門。"
	panel.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	panel.add_theme_font_size_override("font_size", 24)
	panel.add_theme_color_override("font_color", TEXT)
	panel.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	content.add_child(panel)
	content.add_child(make_button("進入第一關　✦", show_level_one))

func show_level_one() -> void:
	screen = "level_one"
	selected.clear()
	clear_content()
	add_title("第一關｜需要，還是想要？", "你有 100 元，只能選兩樣。請優先選擇生活中真正需要的物品。")
	var hint := Label.new()
	hint.text = "請選兩項：早餐（需要）、限量玩具（想要）、雨傘（需要）、糖果（想要）"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.add_theme_color_override("font_color", MUTED)
	content.add_child(hint)
	var grid := GridContainer.new()
	grid.columns = 2
	grid.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	grid.add_theme_constant_override("h_separation", 16)
	grid.add_theme_constant_override("v_separation", 16)
	content.add_child(grid)
	var options := ["🍞 早餐　｜需要", "🧸 限量玩具　｜想要", "☂ 雨傘　｜需要", "🍬 糖果　｜想要"]
	for i in options.size():
		var b := Button.new()
		b.text = options[i]
		b.custom_minimum_size = Vector2(330, 62)
		b.add_theme_font_size_override("font_size", 20)
		b.toggle_mode = true
		b.toggled.connect(func(on: bool): toggle_choice(i, on, b))
		grid.add_child(b)
	content.add_child(make_button("確認選擇並取得 KEY", check_level_one))

func toggle_choice(index: int, on: bool, button: Button) -> void:
	if on:
		if selected.size() >= 2:
			button.button_pressed = false
			return
		selected.append(index)
	else:
		selected.erase(index)
	button.modulate = Color("a6f0d2") if on else Color.WHITE

func check_level_one() -> void:
	if selected.size() != 2:
		status_label.text = "請先選兩樣物品。"
		return
	if selected.has(0) and selected.has(2):
		score_one = 100
		status_label.add_theme_color_override("font_color", MINT)
		status_label.text = "答對！你拿到第一把 KEY：需要優先於想要。"
		update_score()
		await get_tree().create_timer(0.8).timeout
		show_level_two()
	else:
		status_label.text = "再想想：先滿足生活需要，再考慮想要的物品。"

func show_level_two() -> void:
	screen = "level_two"
	clear_content()
	add_title("第二關｜儲蓄小魔法", "小夢魔有 60 元，連續 3 週每週存多少，才能存到 90 元？")
	var equation := Label.new()
	equation.text = "60 ＋（每週儲蓄 × 3）＝ 90"
	equation.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	equation.add_theme_font_size_override("font_size", 34)
	equation.add_theme_color_override("font_color", GOLD)
	content.add_child(equation)
	var slider := HSlider.new()
	slider.min_value = 0
	slider.max_value = 20
	slider.step = 5
	slider.value = 10
	slider.custom_minimum_size = Vector2(560, 48)
	slider.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	content.add_child(slider)
	var value := Label.new()
	value.text = "每週儲蓄：10 元"
	value.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	value.add_theme_font_size_override("font_size", 25)
	value.add_theme_color_override("font_color", TEXT)
	content.add_child(value)
	slider.value_changed.connect(func(v: float): value.text = "每週儲蓄：%d 元" % int(v))
	content.add_child(make_button("確認計畫並取得 KEY", func(): check_level_two(slider.value)))

func check_level_two(value: float) -> void:
	if int(value) == 10:
		score_two = 100
		status_label.add_theme_color_override("font_color", MINT)
		status_label.text = "答對！第二把 KEY 到手：固定儲蓄，目標就會慢慢靠近。"
		update_score()
		await get_tree().create_timer(0.8).timeout
		show_result()
	else:
		status_label.text = "提示：90 - 60 = 30，再把 30 平均分成 3 週。"

func show_result() -> void:
	screen = "result"
	clear_content()
	add_title("兩把 KEY 都收集完成！", "你的理財星門進步成果")
	var result := Label.new()
	result.text = "第一關：%d / 100　　第二關：%d / 100\n\n總分：%d / 200\n\n學會了：\n✓ 先分辨需要與想要\n✓ 設定目標並固定儲蓄\n✓ 用計算檢查自己的理財計畫" % [score_one, score_two, score_one + score_two]
	result.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	result.add_theme_font_size_override("font_size", 25)
	result.add_theme_color_override("font_color", TEXT)
	result.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	content.add_child(result)
	var badge := Label.new()
	badge.text = "✦ 進步成果：你已經能做出負責任的小小金錢決定 ✦"
	badge.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	badge.add_theme_font_size_override("font_size", 24)
	badge.add_theme_color_override("font_color", GOLD)
	content.add_child(badge)
	content.add_child(make_button("重新挑戰", reset_game))

func reset_game() -> void:
	score_one = 0
	score_two = 0
	show_title()
