# Asset Record

| ID | Purpose | Source/tool | License/status |
|---|---|---|---|
| dreamling-model | Original 3D star dreamling model | Blender 5.3 script in `blender/create_star_dreamling.py` | Original project asset |
| dreamling-preview | Godot title-screen visual | Blender render exported to PNG | Original project asset |
| traditional-font | Chinese UI glyphs | Windows `kaiu.ttf`, copied into project | System font asset, redistributed only inside this project build |

The OBJ/MTL model is stored under `blender/` and copied to `godot/assets/`; the Godot Web build uses the preview image for reliable HTML5 loading while preserving the model for future 3D scene expansion.
