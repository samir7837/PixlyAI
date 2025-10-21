"""
Primary enhancer (fallback-only).
This module provides enhance_prompt(prompt) which returns an enriched prompt by
appending a randomized selection of descriptive snippets.
"""
import random

def enhance_prompt(prompt: str) -> str:
    if not prompt:
        return prompt

    
    descriptors = [
        "ultra-detailed",
        "photorealistic",
        "cinematic lighting",
        "8k",
        "highly detailed",
        "award-winning photography",
        "dramatic rim lighting",
        "golden hour",
        "moody film grain",
        "shallow depth of field",
        "bokeh background",
        "soft volumetric light",
        "vibrant color palette",
        "muted pastel tones",
        "hyperrealism",
        "studio portrait style",
        "wide-angle perspective",
        "telephoto compression",
        "high contrast shadows",
        "subtle lens flare",
        "matte finish",
        "editorial fashion style",
        "minimalist composition",
        "dynamic motion blur",
        "noir-inspired mood",
        "warm color temperature",
        "cool cinematic teal",
        "organic textures, fine detail",
        "reflective surfaces",
        "aerial viewpoint",
        "macro shallow focus",
        "soft natural rim light",
        "widescreen cinematic aspect ratio",
        "high dynamic range",
        "soft pastel haze",
        "cinematic color grading",
        "golden reflections",
        "ambient occlusion detail",
        "crisp micro-contrast",
        "textured film grain",
        "lens chromatic aberration",
        "studio strobe lighting",
        "environmental storytelling",
        "glass reflections, high polish",
        "moody backlight",
        "symmetrical composition",
        "rule-of-thirds composition",
        "hand-painted style",
        "digital matte painting vibe",
        # +40 additional descriptors for higher uniqueness
        "rich volumetric fog",
        "wet reflective pavement",
        "neon rim lights",
        "soft shadow gradients",
        "porcelain skin finish",
        "sun-dappled highlights",
        "intricate ornamental detail",
        "architectural macro detail",
        "art-house color palette",
        "painted brushstroke texture",
        "cross-processed film tone",
        "gold leaf accents",
        "ceramic glaze sheen",
        "low-key dramatic lighting",
        "high-key airy lighting",
        "softbox portrait lighting",
        "cinematic wide lens flare",
        "subsurface scattering",
        "deep focus clarity",
        "dust particles in air",
        "warm tungsten tones",
        "icy blue highlights",
        "rich chiaroscuro contrast",
        "urban decay textures",
        "rustic warm wood tones",
        "fine art print aesthetic",
        "exposed grain texture",
        "hand-tinted colorization",
        "oversaturated neon hues",
        "desaturated moody palette",
        "soft halation glow",
        "mirror-like reflections",
        "portrayal in golden light",
        "time-lapse motion streaks",
        "ornate baroque styling",
        "frosted glass blur",
        "ultra-crisp HDR detail",
        "long exposure light trails",
        "vintage kodak film look",
        "cinematic tilt-shift effect",
        "ultra-real skin pores",
        "intricate macro textures",
        "ethereal dreamlike haze",
        "architectural symmetry emphasis",
        "hand-crafted illustrative touch",
        "studio backdrops with gradients",
        "moody thunderstorm atmosphere",
        "sunset rim highlight",
    ]

    lower = (prompt or "").lower()
   
    candidates = [d for d in descriptors if d.lower() not in lower]
    if not candidates:
        
        return prompt.strip()

    
    n = min(len(candidates), random.randint(4, 7))
    chosen = random.sample(candidates, n)
    enhanced = f"{prompt.strip()}, " + ", ".join(chosen)
    return enhanced