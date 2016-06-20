// This is the GLSL shader code used by the 'BrickBreaker' game's different filters.

precision highp float;
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_scale;
uniform vec2 u_sprite_size;
uniform float u_time;

uniform int u_style;

vec4 lcd_pixels() {
	vec2 uv = v_tex_coord;
	//Pixellate:
	float pixel_size = 3.0 / u_scale;
	float dx = pixel_size * (1.0/u_sprite_size.x*u_scale);
	float dy = pixel_size * (1.0/u_sprite_size.y*u_scale);
	vec2 tc = vec2(dx * floor(uv.x/dx), dy * floor(uv.y/dy));
	vec4 color = texture2D(u_texture, tc);
	//Increase contrast slightly:
	float contrast = 1.3;
	color = (color - 0.5) * contrast + 0.5;
	//Convert to grayscale:
	float gray = (color.r + color.g + color.b) / 3.0;
	//Reduce to 16 levels of gray:
	gray = floor(gray * 16.0) / 16.0;
	//Add a green-ish tint:
	vec4 gray_color = vec4(gray * 1.1, gray * 1.4, gray, color.a);
	return gray_color;
}

vec4 wavy() {
	vec2 uv = v_tex_coord;
	uv.y += sin(uv.x * 25.0 + u_time*3.0) * 0.003;
	uv.x += sin(uv.x * 15.0 + u_time*3.0) * 0.003;
	vec2 rgb_shift = vec2(sin(u_time*2.0) * 5.0, cos(u_time*1.5) * 5.0);
	vec2 uv_r = vec2(uv.x - (1.0/u_sprite_size.x) * rgb_shift.x, uv.y - (1.0/u_sprite_size.y) * rgb_shift.y);
	vec2 uv_b = vec2(uv.x + (1.0/u_sprite_size.x) * rgb_shift.x, uv.y - (1.0/u_sprite_size.y) * rgb_shift.y);
	float r = texture2D(u_texture, uv_r).r;
	float g = texture2D(u_texture, uv).g;
	float b = texture2D(u_texture, uv_b).b;
	vec4 color = vec4(r, g, b, 0.);
	return color;
}

vec4 grayscale() {
	vec4 color = texture2D(u_texture, v_tex_coord);
	float contrast = 1.7;
	color = (color - 0.5) * contrast + 0.5;
	float gray = (color.r + color.g + color.b) / 3.0;
	return vec4(gray, gray, gray, color.a);
}

vec4 blackwhite() {
	vec4 color = texture2D(u_texture, v_tex_coord);
	float gray = (color.r + color.g + color.b) / 3.0;
	gray = (gray > 0.5) ? 1.0 : 0.0;
	return vec4(gray, gray, gray, color.a);
}

void main() {
	if (u_style == 1) {
		gl_FragColor = grayscale();
	} else if (u_style == 2) {
		gl_FragColor = blackwhite();
	} else if (u_style == 3) {
		gl_FragColor = lcd_pixels();
	} else if (u_style == 4) {
		gl_FragColor = wavy();
	} else {
		gl_FragColor = texture2D(u_texture, v_tex_coord);
	}
}