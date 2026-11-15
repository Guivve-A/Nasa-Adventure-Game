shader_type canvas_item;

// Desenfoque optico didactico sobre la imagen completa, incluido el limbo.
uniform float desenfoque = 0.0;

void fragment() {
	vec2 d = TEXTURE_PIXEL_SIZE * desenfoque;
	vec4 c = texture(TEXTURE, UV) * 0.2;
	c += texture(TEXTURE, UV + vec2(d.x, 0.0)) * 0.1;
	c += texture(TEXTURE, UV - vec2(d.x, 0.0)) * 0.1;
	c += texture(TEXTURE, UV + vec2(0.0, d.y)) * 0.1;
	c += texture(TEXTURE, UV - vec2(0.0, d.y)) * 0.1;
	c += texture(TEXTURE, UV + d * 0.7071) * 0.1;
	c += texture(TEXTURE, UV - d * 0.7071) * 0.1;
	c += texture(TEXTURE, UV + vec2(d.x, -d.y) * 0.7071) * 0.1;
	c += texture(TEXTURE, UV + vec2(-d.x, d.y) * 0.7071) * 0.1;
	COLOR = c;
}
