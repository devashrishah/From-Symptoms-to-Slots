import csv
import random
import argparse
from typing import List, Dict

def clamp_int(x, lo, hi):
    return max(lo, min(hi, int(round(x))))

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic dermatology patient transcripts (short 2–3 sentences)."
    )
    parser.add_argument("--n", type=int, default=10000, help="Number of records to generate (default: 10000)")
    parser.add_argument("--out", type=str, default="short_derm_transcripts_10k.csv", help="Output CSV path")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducibility (default: 7)")
    parser.add_argument("--other-prob", type=float, default=0.12, help="Probability to generate a non-specific ('other') case")
    args = parser.parse_args()
    random.seed(args.seed)

    conditions: List[str] = [
        "acne", "atopic_dermatitis", "psoriasis", "rosacea", "tinea_corporis",
        "tinea_pedis", "onychomycosis", "impetigo", "folliculitis", "contact_dermatitis",
        "urticaria", "scabies", "shingles", "cellulitis", "molluscum", "warts",
        "vitiligo", "cold_sore", "actinic_keratosis", "basal_cell_carcinoma",
        "squamous_cell_carcinoma", "melanoma"
    ]
    cancer_like = {"basal_cell_carcinoma", "squamous_cell_carcinoma", "melanoma"}

    body_sites = [
        "face", "forehead", "cheeks", "nose", "chin", "neck", "scalp", "upper back", "lower back",
        "chest", "abdomen", "shoulders", "upper arm", "forearm", "wrist", "hand", "fingers",
        "thigh", "calf", "ankle", "foot", "toes", "groin", "buttock", "armpit", "near the eye"
    ]

    durations = [
        "today", "yesterday", "two days", "three days", "about a week", "ten days",
        "two weeks", "about a month", "six weeks", "two months", "three months",
        "about a year", "several years"
    ]

    itch_words = ["itchy", "super itchy", "maddening itch", "itch that comes and goes"]
    pain_words = ["tender", "sore", "stinging", "burning"]
    discharge_words = ["oozing", "weeping", "crusty", "bleeding"]
    color_words = ["red", "pink", "flesh-colored", "brown", "dark brown", "black", "pearly", "waxy", "purple", "white"]
    size_words = ["tiny", "small", "pea-sized", "quarter-sized", "bigger than a pencil eraser", "about 1 cm", "about 2 cm"]
    texture_words = ["rough", "scaly", "flaky", "raised", "flat", "bumpy", "nodular"]
    self_treatments = [
        "over-the-counter hydrocortisone", "antifungal cream", "benzoyl peroxide wash",
        "salicylic acid pads", "tea tree oil", "antihistamines", "ice", "aloe",
        "nothing yet", "antibiotic ointment"
    ]

    condition_cues: Dict[str, List[str]] = {
        "acne": ["whiteheads", "blackheads", "pimples", "cystic bumps"],
        "atopic_dermatitis": ["itchy patches", "behind knees", "elbow creases", "worse with soaps"],
        "psoriasis": ["thick scaly plaques", "elbows", "knees", "silvery scale"],
        "rosacea": ["facial flushing", "visible blood vessels", "triggers by heat or wine"],
        "tinea_corporis": ["ring-shaped", "central clearing", "itchy rash"],
        "tinea_pedis": ["athlete's foot", "between toes", "peeling"],
        "onychomycosis": ["yellow thick toenail", "crumbly nail"],
        "impetigo": ["honey-colored crust", "around nose and mouth"],
        "folliculitis": ["pimple-like bumps around hairs", "after shaving"],
        "contact_dermatitis": ["after new soap", "after nickel jewelry", "after poison ivy"],
        "urticaria": ["hives", "welts", "move around"],
        "scabies": ["worse at night", "burrows", "between fingers"],
        "shingles": ["band of blisters", "on one side", "burning pain"],
        "cellulitis": ["warm red area", "spreading", "fever"],
        "molluscum": ["small pearly bumps", "center dimple"],
        "warts": ["rough bumps", "on fingers or feet"],
        "vitiligo": ["white patches", "loss of pigment"],
        "cold_sore": ["tingling lip blister", "recurrent"],
        "actinic_keratosis": ["scaly rough spot", "sun exposed", "precancer"],
        "basal_cell_carcinoma": ["pearly bump", "bleeds easily", "non-healing"],
        "squamous_cell_carcinoma": ["scaly sore", "thick crust", "sun exposed"],
        "melanoma": ["asymmetry", "irregular border", "color variegation", "new dark mole"]
    }

    # ---------- Helpers for natural language variety ----------
    LESION_NOUNS = ["spot", "patch", "bump", "area", "rash", "sore", "lesion", "mark", "plaque", "mole"]
    OPENING_VERBS = ["noticed", "found", "developed", "got", "started having", "saw", "felt"]
    APPEAR_VERBS = ["appeared", "showed up", "popped up", "came up", "started", "started to form"]
    FEEL_VERBS = ["feels", "has been", "seems", "is"]
    INTENSIFIERS = ["kind of", "a bit", "pretty", "quite", "really"]

    def render_site(site: str) -> str:
        if site == "near the eye":
            return "near my eye"
        return f"on my {site}"

    def maybe_article(color: str, texture: str, size: str) -> str:
        parts = [size, color, texture]
        phrase = " ".join([p for p in parts if p])
        if phrase.startswith(("about", "bigger")):
            return phrase
        return f"a {phrase}"

    def choose_template(site_str: str, dur: str, size: str, color: str, texture: str) -> str:
        noun = random.choice(LESION_NOUNS)
        v_open = random.choice(OPENING_VERBS)
        v_appear = random.choice(APPEAR_VERBS)
        phrase = maybe_article(color, texture, size)
        templates = [
            f"I {v_open} {phrase} {noun} {site_str} {dur} ago.",
            f"I {v_open} {phrase} {noun} {site_str} around {dur} ago.",
            f"I {v_open} {phrase} {noun} {site_str} about {dur} ago.",
            f"{phrase.capitalize()} {noun} {site_str} {v_appear} {dur} ago.",
            f"{phrase.capitalize()} {noun} {v_appear} {site_str} {dur} ago.",
            f"{dur.capitalize()} ago, {phrase} {noun} {v_appear} {site_str}.",
            f"There’s {phrase} {noun} {site_str} that appeared {dur} ago.",
            f"There has been {phrase} {noun} {site_str} since {dur} ago.",
            f"My {noun} {v_appear} {site_str} about {dur} ago — {phrase}.",
            f"Could this {noun} {site_str} that {v_appear} {dur} ago be something to check?",
            f"{phrase.capitalize()} {noun} {site_str} showed up {dur} ago.",
        ]
        return random.choice(templates)

    def build_symptom_sentence(itch: str, pain: str, discharge: str) -> str:
        bits = []
        if random.random() < 0.8:
            feel = random.choice(FEEL_VERBS)
            maybe_intense = (random.random() < 0.35)
            prefix = (random.choice(INTENSIFIERS) + " ") if maybe_intense else ""
            bits.append(f"It {feel} {prefix}{itch}")
        if random.random() < 0.5:
            conj = "and" if bits else "It’s"
            bits.append(f"{conj} sometimes {pain}")
        if random.random() < 0.35:
            if bits:
                bits.append(f"with a bit of {discharge}")
            else:
                bits.append(f"It has a bit of {discharge}")
        if not bits:
            return "It hasn't really changed much."
        return ", ".join(bits) + "."

    def build_followup_specific(cond: str, self_tx: str, condition_cues: Dict[str, List[str]]) -> str:
        options = []
        if cond in condition_cues and random.random() < 0.7:
            options.append("I also noticed " + random.choice(condition_cues[cond]) + ".")
        if random.random() < 0.7:
            options.append(f"I tried {self_tx} with limited relief.")
        if not options:
            options = ["It hasn't really changed much."]
        return random.choice(options)

    def build_followup_other(self_tx: str) -> str:
        if random.random() < 0.7:
            return f"I tried {self_tx}, but I'm not sure what it is."
        return "I'm not sure what might have caused it."

    # ---------- Transcript builders (VARIED OPENINGS) ----------
    def make_short_transcript_specific(cond, site, dur, itch, pain, discharge, color, size, texture, self_tx):
        site_str = render_site(site)
        s1 = choose_template(site_str, dur, size, color, texture)
        s2 = build_symptom_sentence(itch, pain, discharge)
        s3 = build_followup_specific(cond, self_tx, condition_cues)
        if random.random() < 0.55:
            return f"{s1} {s2}"
        else:
            return f"{s1} {s2} {s3}"

    def make_short_transcript_other(site, dur, itch, pain, discharge, color, size, texture, self_tx):
        site_str = render_site(site)
        s1 = choose_template(site_str, dur, size, color, texture)
        s2 = build_symptom_sentence(itch, pain, discharge)
        s3 = build_followup_other(self_tx)
        if random.random() < 0.55:
            return f"{s1} {s2}"
        else:
            return f"{s1} {s2} {s3}"

    # ---------- Helpers for scoring/labels ----------
    def duration_to_days(dur: str) -> int:
        mapping = {
            "today": 0, "yesterday": 1, "two days": 2, "three days": 3,
            "about a week": 7, "ten days": 10, "two weeks": 14, "about a month": 30,
            "six weeks": 42, "two months": 60, "three months": 90,
            "about a year": 365, "several years": 365 * 3
        }
        return mapping.get(dur, 14)

    def compute_red_flags(cond: str, discharge: str) -> List[str]:
        flags = []
        if cond in cancer_like and random.random() < 0.7:
            flags.append("non_healing")
        if cond == "melanoma" and random.random() < 0.8:
            flags.extend(["asymmetry", "irregular_border", "color_variegation", "evolving"])
        if cond == "cellulitis" and random.random() < 0.6:
            flags.append("fever_reported")
        if discharge == "bleeding" and "bleeding" not in flags:
            flags.append("bleeding")
        return flags

    def triage_from_features(cond: str, sev: int, flags: List[str], site: str, dur: str) -> (int, str):
        """
        Produce a 0–10 triage_score + label:
          - urgent (>=8): same/next-day
          - priority_soon (5–7): within ~72h
          - routine (<=4): schedule when convenient
        """
        score = 0
        score += min(6, max(0, sev // 2))  # sev 0–10 -> 0–5-ish weight
        rf_weights = {
            "fever_reported": 3,
            "non_healing": 3,
            "asymmetry": 2,
            "irregular_border": 2,
            "color_variegation": 2,
            "evolving": 2,
            "bleeding": 2
        }
        for rf in flags:
            score += rf_weights.get(rf, 1)
        if cond in cancer_like:
            score += 2
        if site in {"face", "near the eye", "groin", "armpit", "scalp"}:
            score += 1
        days = duration_to_days(dur)
        if days <= 3 and sev >= 7:
            score += 1
        score = int(min(10, max(0, score)))
        if score >= 8:
            label = "urgent"
        elif score >= 5:
            label = "priority_soon"
        else:
            label = "routine"
        return score, label

    # ---------- CSV write ----------
    fieldnames = [
        "id",
        "transcript",
        "suspected_condition_label",
        "red_flags",
        "severity_0_10",
        "triage_score_0_10",
        "triage_label"
    ]

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, args.n + 1):
            is_other = (random.random() < args.other_prob)
            cond = "other" if is_other else random.choice(conditions)

            site = random.choice(body_sites)
            dur = random.choice(durations)
            sev = clamp_int(random.gauss(5, 2), 0, 10)
            itch = random.choice(itch_words)
            pain = random.choice(pain_words)
            discharge = random.choice(discharge_words)
            color = random.choice(color_words)
            size = random.choice(size_words)
            texture = random.choice(texture_words)
            self_tx = random.choice(self_treatments)

            if cond == "other":
                red_flags = []
                if discharge == "bleeding" and random.random() < 0.7:
                    red_flags = ["bleeding"]
                transcript = make_short_transcript_other(site, dur, itch, pain, discharge, color, size, texture, self_tx)
            else:
                red_flags = compute_red_flags(cond, discharge)
                transcript = make_short_transcript_specific(cond, site, dur, itch, pain, discharge, color, size, texture, self_tx)

            triage_score, triage_label = triage_from_features(cond, sev, red_flags, site, dur)

            writer.writerow({
                "id": i,
                "transcript": transcript,
                "suspected_condition_label": cond,
                "red_flags": ";".join(red_flags) if red_flags else "",
                "severity_0_10": sev,
                "triage_score_0_10": triage_score,
                "triage_label": triage_label
            })

    print(f"Wrote {args.n} records to {args.out}")

if __name__ == "__main__":
    main()
