"""Build team-specific CV variants from _data/cv.yml.

Each variant is the same CV with a different headline and a different order of
research interests, PhD highlights, papers under review and skills, so that the
most relevant work comes first. The output files are complete RenderCV inputs
(cv + design + locale + settings) that can be rendered with:

    rendercv render <output_dir>/cv_<variant>.yml --pdf-path <file.pdf>

Usage: python bin/make_cv_variants.py <output_dir>
"""

import copy
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

VARIANTS = {
    "spatial_audio": {
        "headline": "PhD Candidate in AI · Machine hearing and spatial audio",
        "Research Interests": ["Machine hearing", "Spatial audio", "Representation learning", "Speech"],
        "phd_highlights": ["Expected graduation", "AudioSphere", "Bearings", "SpeechJEPA", "Supervisors"],
        "Under Review": ["Bearings", "EquiSELD", "SpeechJEPA", "WavJEPA"],
        "Technical Skills": ["Audio & signal processing", "Deep learning", "Distributed training", "Languages & tools"],
    },
    "speech": {
        "headline": "PhD Candidate in AI · Self-supervised speech and audio representation learning",
        "Research Interests": ["Speech", "Representation learning", "Machine hearing", "Spatial audio"],
        "phd_highlights": ["Expected graduation", "SpeechJEPA", "AudioSphere", "Bearings", "Supervisors"],
        "Under Review": ["SpeechJEPA", "WavJEPA", "Bearings", "EquiSELD"],
        "Technical Skills": ["Deep learning", "Distributed training", "Languages & tools", "Audio & signal processing"],
    },
}


def reorder(items, priorities, text_of):
    """Stable reorder: items whose text starts with a priority keyword come first, in that order.

    Items that match no keyword keep their original order after the matched ones, so the
    script keeps working when entries are added or renamed in cv.yml.
    """

    def rank(item):
        text = text_of(item)
        for i, key in enumerate(priorities):
            if text.startswith(key):
                return i
        return len(priorities)

    return sorted(items, key=rank)


def build(variant, spec, cv_data, design, locale, bold_keywords):
    data = copy.deepcopy(cv_data)
    cv = data["cv"]
    cv["headline"] = spec["headline"]
    sections = cv["sections"]

    if "Research Interests" in sections:
        sections["Research Interests"] = reorder(
            sections["Research Interests"], spec["Research Interests"], lambda e: e.get("label", "")
        )
    if "Technical Skills" in sections:
        sections["Technical Skills"] = reorder(
            sections["Technical Skills"], spec["Technical Skills"], lambda e: e.get("label", "")
        )
    if "Under Review" in sections:
        sections["Under Review"] = reorder(sections["Under Review"], spec["Under Review"], lambda e: e.get("title", ""))
    for entry in sections.get("Education", []):
        if entry.get("degree") == "PhD" and entry.get("highlights"):
            entry["highlights"] = reorder(entry["highlights"], spec["phd_highlights"], str)

    data.update(design)
    data.update(locale)
    data["settings"] = {"bold_keywords": bold_keywords}
    return data


def main():
    out_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "cv_variants")
    out_dir.mkdir(parents=True, exist_ok=True)

    cv_data = yaml.safe_load((ROOT / "_data/cv.yml").read_text(encoding="utf-8"))
    design = yaml.safe_load((ROOT / "assets/rendercv/design.yaml").read_text(encoding="utf-8"))
    locale = yaml.safe_load((ROOT / "assets/rendercv/locale.yaml").read_text(encoding="utf-8"))
    settings = yaml.safe_load((ROOT / "assets/rendercv/settings.yaml").read_text(encoding="utf-8"))
    bold_keywords = settings.get("settings", {}).get("bold_keywords", [])

    for variant, spec in VARIANTS.items():
        data = build(variant, spec, cv_data, design, locale, bold_keywords)
        path = out_dir / f"cv_{variant}.yml"
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
