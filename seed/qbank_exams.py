"""Authored bank for the exam and subject tracks: STEM science, English, SAT
Reading & Writing, ACT, MATHCOUNTS, and AMC 8/10/12.

Everything here is written for Veelearn. None of it is copied from MAA (AMC),
College Board (SAT), ACT, or MATHCOUNTS material — those items are copyrighted
and the contest ones are actively used for scoring. Each question is modelled on
the *style* of the exam and carries the same anatomy as the rest of the bank:
four options, a specific `why` on every distractor, a two-step hint ladder and
short solution steps.

Diagrams are authored SVGs (`visual = {"svg": ..., "alt": ...}`), which the
session card renders as a figure and the outline creator shows as a thumbnail.
`build_session_seed.py` checks them for safety before they reach the database.
"""

from __future__ import annotations


AUTHORED = ("authored", "Veelearn original \u2014 written for Veelearn")

# Openly licensed sets. The licence and the work it came from travel with every
# row, so provenance is in the data rather than in a comment somewhere.
OBQA = ("openbookqa", "OpenBookQA (Mihaylov et al. 2018), Allen Institute for AI \u2014 Apache-2.0")
GSM8K = ("gsm8k", "GSM8K (Cobbe et al. 2021), OpenAI \u2014 MIT")


def Q(skill, tier, stem, options, hints, steps, visual=None, source=None, attribution=None):
    """Same shape as seed/qbank.py: options are (text, is_correct, why).

    `source` / `attribution` travel into `qbank_items.source` and
    `qbank_items.attribution`, so every row says where it came from. Anything
    not authored by Veelearn must name its licence and the work it came from.
    """
    src = source or AUTHORED
    source_id, credit = src if isinstance(src, tuple) else (src, attribution or "")
    return {
        "skill": skill,
        "tier": tier,
        "stem": stem,
        "options": options,
        "hints": hints,
        "steps": steps,
        "visual": visual,
        "source": source_id,
        "attribution": credit,
    }


def svg(body, alt):
    return {
        "svg": (
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 200' role='img' "
            "aria-label='" + alt + "' font-family='Nunito, Arial, sans-serif'>" + body + "</svg>"
        ),
        "alt": alt,
    }


INK = "#334155"

# --------------------------------------------------------------------------- #
# Diagrams
# --------------------------------------------------------------------------- #

RIGHT_6_8 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<path d='M60 160 L60 76 L220 160 Z'/>"
    "<path d='M60 148 L72 148 L72 160' stroke-width='1.5'/></g>"
    "<g fill='" + INK + "' font-size='14'>"
    "<text x='34' y='122'>6</text><text x='132' y='182'>8</text><text x='150' y='104'>?</text></g>",
    "Right triangle with legs 6 and 8 and an unknown hypotenuse",
)

RECT_12_5 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<path d='M40 154 H244 V74 H40 Z'/>"
    "<path d='M40 154 L244 74' stroke-dasharray='6 5'/></g>"
    "<g fill='" + INK + "' font-size='14'>"
    "<text x='132' y='176'>12</text><text x='252' y='120'>5</text><text x='128' y='104'>?</text></g>",
    "Rectangle 12 wide and 5 tall with a dashed diagonal",
)

TRI_10_7 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<path d='M50 160 H250 L120 62 Z'/>"
    "<path d='M120 62 V160' stroke-dasharray='6 5' stroke-width='1.5'/></g>"
    "<g fill='" + INK + "' font-size='14'>"
    "<text x='144' y='182'>10</text><text x='128' y='118'>7</text></g>",
    "Triangle with base 10 and a dashed height of 7",
)

CHORD_8_R5 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<circle cx='160' cy='104' r='66'/>"
    "<path d='M114 60 H206'/>"
    "<path d='M160 104 L114 60' stroke-dasharray='6 5' stroke-width='1.5'/>"
    "<path d='M160 104 V82' stroke-dasharray='4 4' stroke-width='1.5'/>"
    "<path d='M152 82 H160 V90' stroke-width='1.2'/></g>"
    "<g fill='" + INK + "' font-size='13'>"
    "<text x='152' y='52'>8</text><text x='168' y='94'>5</text><text x='166' y='120'>?</text></g>",
    "Circle of radius 5 with a chord of length 8 and an unknown distance from the centre",
)

TRI_5_13 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<path d='M64 158 L64 66 L222 158 Z'/>"
    "<path d='M64 146 L76 146 L76 158' stroke-width='1.5'/></g>"
    "<g fill='" + INK + "' font-size='14'>"
    "<text x='40' y='116'>5</text><text x='196' y='140'>13</text><text x='128' y='182'>?</text></g>",
    "Right triangle with one leg 5 and hypotenuse 13",
)

GRID_4 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='1.5'>"
    "<path d='M50 160 H250 M50 130 H250 M50 100 H250 M50 70 H250 M50 40 H250'/>"
    "<path d='M50 40 V160 M100 40 V160 M150 40 V160 M200 40 V160 M250 40 V160'/></g>"
    "<g fill='" + INK + "' font-size='13'>"
    "<circle cx='50' cy='160' r='4'/><circle cx='250' cy='40' r='4'/>"
    "<text x='24' y='182'>start</text><text x='238' y='32'>end</text></g>",
    "A four by four grid with the start at the lower left and the end at the upper right",
)

GRID_3 = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='1.5'>"
    "<path d='M60 160 H220 M60 120 H220 M60 80 H220 M60 40 H220'/>"
    "<path d='M60 40 V160 M100 40 V160 M140 40 V160 M180 40 V160 M220 40 V160'/></g>"
    "<g fill='" + INK + "' font-size='13'><text x='90' y='184'>3 × 3 grid of unit squares</text></g>",
    "A three by three grid of unit squares",
)

CELL_DIAGRAM = svg(
    "<rect x='24' y='18' width='272' height='164' rx='18' fill='#f8fafc' stroke='" + INK + "' stroke-width='2'/>"
    "<circle cx='96' cy='100' r='38' fill='#e0e7ff' stroke='" + INK + "' stroke-width='2'/>"
    "<circle cx='96' cy='100' r='14' fill='#818cf8'/>"
    "<g fill='#fde68a' stroke='" + INK + "' stroke-width='2'>"
    "<ellipse cx='212' cy='72' rx='34' ry='17'/>"
    "<ellipse cx='212' cy='132' rx='34' ry='17'/></g>"
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<path d='M196 66 q10 8 0 16 q10 8 0 16' /><path d='M196 126 q10 8 0 16'/></g>"
    "<g fill='#1e293b' font-size='11'>"
    "<text x='146' y='52'>mitochondria</text>"
    "<text x='62' y='52'>nucleus</text>"
    "<text x='40' y='176'>cell membrane</text></g>"
    "<path d='M96 62 L96 42' stroke='" + INK + "' stroke-width='1'/>"
    "<path d='M212 55 L212 46' stroke='" + INK + "' stroke-width='1'/>",
    "Diagram of a cell with the nucleus, cell membrane and two mitochondria labelled",
)

TRIAL_TABLE = svg(
    "<g stroke='" + INK + "' stroke-width='1.5' fill='none'>"
    "<rect x='40' y='40' width='240' height='120'/>"
    "<path d='M40 70 H280 M40 100 H280 M40 130 H280'/>"
    "<path d='M140 40 V160 M200 40 V160'/></g>"
    "<g fill='#1e293b' font-size='12'>"
    "<text x='52' y='62'>Trial</text><text x='148' y='62'>Volume (mL)</text><text x='206' y='62'>Time (s)</text>"
    "<text x='58' y='92'>1</text><text x='164' y='92'>10</text><text x='222' y='92'>20</text>"
    "<text x='58' y='122'>2</text><text x='164' y='122'>20</text><text x='222' y='122'>40</text>"
    "<text x='58' y='152'>3</text><text x='164' y='152'>30</text><text x='222' y='152'>60</text></g>",
    "Table of three trials listing volume in millilitres against time in seconds",
)

NUMBER_LINE_ABS = svg(
    "<g fill='none' stroke='" + INK + "' stroke-width='2'>"
    "<path d='M30 110 H290'/><path d='M284 104 L296 110 L284 116'/></g>"
    "<g fill='" + INK + "' font-size='13'>"
    "<path d='M160 100 V120' stroke-width='2'/><text x='154' y='138'>0</text>"
    "<circle cx='230' cy='110' r='4'/><text x='222' y='94'>7</text>"
    "<circle cx='90' cy='110' r='4'/><text x='82' y='94'>−7</text></g>",
    "Number line showing the points 7 and −7 around 0",
)


# Diagrams for the openly licensed items. The text of those questions comes from
# the datasets; these figures are Veelearn's own, which is why they can be
# redrawn freely (see THIRD_PARTY_NOTICES.txt).

STAR_DIAGRAM = svg(
    "<text x='16' y='24' font-size='13' fill='" + INK + "'>A star is a huge ball of hot gas</text>"
    "<circle cx='160' cy='118' r='70' fill='#fde68a' stroke='#f59e0b' stroke-width='2'/>"
    "<circle cx='160' cy='118' r='48' fill='#fbbf24' stroke='#f59e0b' stroke-width='1.5'/>"
    "<circle cx='160' cy='118' r='26' fill='#fb923c'/>"
    "<g font-size='11' fill='" + INK + "'>"
    "<text x='214' y='116'>photosphere (surface)</text>"
    "<text x='214' y='136'>outer gas layers</text>"
    "<text x='222' y='160'>core: millions of K</text></g>"
    "<g stroke='" + INK + "' stroke-width='1' fill='none'>"
    "<path d='M160 118 L210 112'/><path d='M160 118 L210 132'/><path d='M160 118 L218 156'/></g>",
    "A star drawn as a hot gas sphere: a very hot core inside outer gas layers",
)

CLIP_BARS = svg(
    "<text x='16' y='24' font-size='13' fill='" + INK + "'>Clips sold</text>"
    "<g stroke='" + INK + "' stroke-width='2'>"
    "<rect x='40' y='52' width='220' height='30' fill='#bfdbfe'/>"
    "<rect x='40' y='94' width='110' height='30' fill='#a7f3d0'/></g>"
    "<g font-size='12' fill='" + INK + "'>"
    "<text x='48' y='72'>April: 48 clips</text>"
    "<text x='48' y='114'>May: half of 48 = 24</text>"
    "<text x='40' y='152' font-size='13'>Total = 48 + 24 = ?</text>"
    "<path d='M262 52 v72' stroke='" + INK + "' stroke-width='1.5'/></g>",
    "Two bars: April 48 clips and May half of that, with the total left to work out",
)

RATE_BARS = svg(
    "<text x='16' y='24' font-size='13' fill='" + INK + "'>Pay is proportional to time</text>"
    "<g stroke='" + INK + "' stroke-width='2'>"
    "<rect x='40' y='50' width='240' height='26' fill='#bfdbfe'/>"
    "<rect x='40' y='96' width='200' height='26' fill='#fde68a'/></g>"
    "<g font-size='12' fill='" + INK + "'>"
    "<text x='46' y='68'>60 min ................ $12</text>"
    "<text x='46' y='114'>50 min ................ ?</text>"
    "<text x='40' y='152'>50/60 of the hour is worked</text></g>",
    "Bar model comparing 60 minutes paid at 12 dollars with 50 minutes of unknown pay",
)


QUESTIONS = [
    # ======================================================== STEM: cell biology
    Q("sci.bio.cell", 1,
      "Which organelle is the main site of ATP production in a eukaryotic cell?",
      [("Mitochondrion", 1, ""),
       ("Ribosome", 0, "Ribosomes build proteins; they do not generate the cell's ATP supply."),
       ("Golgi apparatus", 0, "The Golgi packages and ships proteins — it consumes ATP rather than making it."),
       ("Lysosome", 0, "Lysosomes digest material; they are not the cell's power plant.")],
      ["Which organelle has folded inner membranes called cristae?",
       "The same one uses the electron transport chain."],
      ["Mitochondria run oxidative phosphorylation on their inner membrane.",
       "That is where most ATP is made."],
      CELL_DIAGRAM),

    Q("sci.bio.cell", 2,
      "A cell that secretes large amounts of protein hormones would contain an unusually large amount of which structure?",
      [("Rough endoplasmic reticulum", 1, ""),
       ("Smooth endoplasmic reticulum", 0, "Smooth ER makes lipids and detoxifies; secreted proteins are built on the rough ER."),
       ("Lysosome", 0, "Lysosomes break material down; they do not build proteins for export."),
       ("Peroxisome", 0, "Peroxisomes handle fatty acids and peroxide, not protein synthesis for secretion.")],
      ["Secreted proteins are translated by ribosomes bound to a membrane.",
       "Which ER has ribosomes attached?"],
      ["Ribosomes on the rough ER translate the protein into the ER lumen.",
       "The Golgi then packages it for secretion."]),

    Q("sci.bio.cell", 3,
      "A plant cell and an animal cell are both placed in distilled water. Which statement best explains why only the animal cell bursts?",
      [("The plant cell wall resists expansion, so the cell becomes turgid instead of bursting.", 1, ""),
       ("The plant cell has no membrane, so water cannot enter it.", 0, "Every cell has a plasma membrane; the wall is additional."),
       ("The plant cell actively pumps all water back out.", 0, "Water still enters by osmosis; the wall is what prevents bursting."),
       ("The plant cell contains no solutes, so osmosis stops.", 0, "Plant cells contain many solutes, which is why water enters at all.")],
      ["Water moves toward the side with more solute.",
       "What extra layer does a plant cell have outside its membrane?"],
      ["Osmosis pulls water into both cells.",
       "The rigid wall pushes back, so pressure rises without rupture."]),

    Q("sci.bio.cell", 4,
      "A drug blocks the function of the Golgi apparatus. Which process is most directly affected?",
      [("Modifying and packaging proteins for transport out of the cell", 1, ""),
       ("Transcribing DNA into mRNA in the nucleus", 0, "Transcription happens in the nucleus and does not require the Golgi."),
       ("Generating a proton gradient across the inner mitochondrial membrane", 0, "That is the mitochondrion's job."),
       ("Replicating chromosomes before mitosis", 0, "Replication occurs in the nucleus during S phase.")],
      ["Think about what happens to a protein after the rough ER.",
       "The Golgi is the cell's sorting and shipping centre."],
      ["Proteins leave the ER and enter the Golgi.",
       "Without the Golgi they are not modified, sorted or shipped."]),

    # ====================================================== STEM: bonding & moles
    Q("sci.chem.moles", 1,
      "How many moles are in 18 g of water? (Molar mass of H₂O = 18 g/mol)",
      [("1 mol", 1, ""),
       ("18 mol", 0, "That would be 18 g/mol × 18, treating grams as moles."),
       ("0.5 mol", 0, "You divided 18 by 36; the molar mass is 18 g/mol."),
       ("324 mol", 0, "You multiplied grams by the molar mass instead of dividing.")],
      ["Moles = mass ÷ molar mass.",
       "18 ÷ 18."],
      ["n = m / M = 18 / 18.",
       "n = 1 mol."]),

    Q("sci.chem.moles", 2,
      "Which bond forms when one atom transfers electrons to another?",
      [("Ionic bond", 1, ""),
       ("Covalent bond", 0, "Covalent bonds share electrons; transfer is ionic."),
       ("Hydrogen bond", 0, "Hydrogen bonds are attractions between molecules, not electron transfer."),
       ("Metallic bond", 0, "Metallic bonding pools electrons across a lattice rather than transferring them to one atom.")],
      ["Transfer means one atom gains electrons and the other loses them.",
       "Which bond is between a metal and a nonmetal?"],
      ["A metal loses electrons and becomes a cation.",
       "A nonmetal gains them and becomes an anion — an ionic bond."]),

    Q("sci.chem.moles", 3,
      "How many formula units are in 0.50 mol of NaCl? (Use 6.0 × 10²³ per mole.)",
      [("3.0 × 10²³", 1, ""),
       ("6.0 × 10²³", 0, "That is one full mole; you have half a mole."),
       ("1.2 × 10²⁴", 0, "You multiplied by 2 instead of by 0.5."),
       ("3.0 × 10²²", 0, "The exponent is off by ten — check 0.5 × 6.0.")],
      ["Multiply moles by Avogadro's number.",
       "0.5 × 6.0 = 3.0, so the exponent stays 10²³."],
      ["N = n × N_A.",
       "N = 0.50 × 6.0 × 10²³ = 3.0 × 10²³."]),

    Q("sci.chem.moles", 4,
      "Which 1-mole sample contains the greatest number of atoms?",
      [("CH₄", 1, ""),
       ("H₂O", 0, "One mole of water has 3 mol of atoms (2 H + 1 O)."),
       ("CO₂", 0, "One mole of CO₂ has 3 mol of atoms, fewer than CH₄'s 5."),
       ("O₂", 0, "One mole of O₂ has only 2 mol of atoms.")],
      ["Count the atoms in one formula unit.",
       "CH₄ has one carbon and four hydrogens."],
      ["CH₄: 5 atoms per formula unit.",
       "So 1 mol CH₄ holds 5 mol of atoms, the largest of the four."]),

    # ==================================================== English: boundaries
    Q("eng.grammar.boundaries", 1,
      "Which sentence is punctuated correctly?",
      [("The experiment failed; however, the data were still useful.", 1, ""),
       ("The experiment failed, however, the data were still useful.",
        0, "Two complete sentences joined by a comma is a comma splice. Use a semicolon or a period."),
       ("The experiment failed however the data were still useful.",
        0, "A conjunctive adverb between two complete sentences needs punctuation before it."),
       ("The experiment failed, however; the data were still useful.",
        0, "The semicolon belongs before 'however', not after it.")],
      ["'The experiment failed' and 'the data were still useful' are both complete sentences.",
       "A conjunctive adverb like 'however' needs a semicolon before it."],
      ["Two independent clauses need a semicolon, period or comma + conjunction.",
       "Semicolon before 'however', comma after it."]),

    Q("eng.grammar.boundaries", 2,
      "Which choice fixes the comma splice: 'The samples were stored at −20 °C, they remained stable for a year.'",
      [("The samples were stored at −20 °C; they remained stable for a year.", 1, ""),
       ("The samples were stored at −20 °C, they remained stable for a year, too.",
        0, "Adding a word does not remove the splice — two complete sentences still meet at a comma."),
       ("The samples were stored at −20 °C they remained stable for a year.",
        0, "Removing the comma leaves a run-on with no boundary at all."),
       ("The samples were stored, at −20 °C, they remained stable for a year.",
        0, "A comma after 'stored' splits a verb from its object and keeps the splice.")],
      ["Count the subjects and verbs on each side.",
       "Both halves could stand alone as sentences."],
      ["Two independent clauses cannot be joined by a comma alone.",
       "Replace the comma with a semicolon."]),

    Q("eng.grammar.boundaries", 3,
      "Which sentence needs a comma after its opening phrase?",
      [("After the centrifuge stopped the technician removed the tubes.", 1, ""),
       ("The technician removed the tubes after the centrifuge stopped.", 0, "Nothing opens the sentence here, so no comma is needed."),
       ("The tubes that were removed had already been labelled.", 0, "This begins with the subject, not an introductory phrase."),
       ("Removing the tubes took longer than expected.", 0, "A gerund phrase acting as the subject takes no comma.")],
      ["Look for a phrase before the main subject.",
       "In the first option, where does the introductory phrase end?"],
      ["'After the centrifuge stopped' is an introductory clause.",
       "It takes a comma before 'the technician'."]),

    Q("eng.grammar.boundaries", 4,
      "Which sentence uses the semicolon correctly?",
      [("Three trials were run; each used a fresh sample.", 1, ""),
       ("Three trials were run; and each used a fresh sample.",
        0, "Do not put a semicolon before a coordinating conjunction joining two clauses."),
       ("Three trials were run; using a fresh sample each time.",
        0, "A semicolon must join two independent clauses; the second part is a fragment."),
       ("Three trials; were run using a fresh sample each time.",
        0, "The semicolon splits the subject from its verb.")],
      ["A semicolon joins two complete sentences.",
       "Check whether both sides could stand alone."],
      ["'Three trials were run' and 'each used a fresh sample' are both complete.",
       "So the semicolon is correct."]),

    # ==================================================== English: inference
    Q("eng.read.inference", 1,
      "Passage: 'The lab's oldest freezer was finally retired. Its replacement arrived on Tuesday, and by Thursday every sample had been transferred.' What can be inferred?",
      [("The samples needed to stay frozen during the move.", 1, ""),
       ("The old freezer was repaired instead of replaced.", 0, "The passage says it was retired and a replacement arrived."),
       ("The samples were destroyed in the transfer.", 0, "Nothing suggests loss; the transfer was completed."),
       ("The new freezer arrived after Thursday.", 0, "It arrived on Tuesday, before the transfer.")],
      ["Why move samples quickly from one freezer to another?",
       "What happens to samples if they warm up?"],
      ["Samples in a freezer are temperature-sensitive.",
       "A fast transfer keeps them frozen."]),

    Q("eng.read.inference", 2,
      "Passage: 'Although the second draft was shorter, reviewers requested even more cuts before publication.' What does this suggest about the reviewers?",
      [("They thought the piece still contained unnecessary material.", 1, ""),
       ("They wanted the author to add supporting detail.", 0, "They asked for cuts, which removes material."),
       ("They had not read the second draft.", 0, "They comment on the second draft specifically."),
       ("They preferred the first draft.", 0, "The passage never compares drafts by preference, only by length.")],
      ["What does asking for 'more cuts' mean?",
       "How does that relate to the draft already being shorter?"],
      ["Shortening a draft removes material.",
       "Asking for more cuts implies material still to remove."]),

    Q("eng.read.inference", 3,
      "Passage: 'The museum extended its hours for the exhibition's final week. Attendance that week was triple the monthly average.' What is the most reasonable conclusion?",
      [("Longer hours contributed to the higher attendance.", 1, ""),
       ("The exhibition was unpopular for most of the month.", 0, "We only know the final week's spike, not overall popularity."),
       ("The museum lost money that week.", 0, "Higher attendance says nothing about costs or revenue."),
       ("Attendance is always triple in the last week of a show.", 0, "The passage gives no such general pattern — this one moved its hours.")],
      ["What changed that week?",
       "Which explanation links the change to the attendance?"],
      ["The only change mentioned is the extended hours.",
       "So the increase is best explained by the hours."]),

    Q("eng.read.inference", 4,
      "Passage: 'The recipe calls for room-temperature eggs, but the note in the margin warns that cold eggs will curdle the batter.' What does the margin note do?",
      [("It explains why the temperature instruction matters.", 1, ""),
       ("It contradicts the main instruction.", 0, "It supports the instruction by giving a reason."),
       ("It suggests replacing eggs with another ingredient.", 0, "No substitute is mentioned."),
       ("It describes how to warm the eggs.", 0, "No warming method is given.")],
      ["What is the note attached to?",
       "Does it agree with the instruction or explain it?"],
      ["The instruction says use room-temperature eggs.",
       "The note supplies the consequence of ignoring it."]),

    # ================================================== SAT R&W: words in context
    Q("sat.rw.words", 1,
      "The researcher's conclusion was ______: two independent teams reached it without sharing data.",
      [("robust", 1, ""),
       ("tentative", 0, "'Tentative' means uncertain, but independent agreement strengthens a conclusion."),
       ("redundant", 0, "Redundant means unnecessary repetition, not independent confirmation."),
       ("hasty", 0, "Haste is about speed, and the sentence is about agreement.")],
      ["Two teams agreed independently.",
       "Does that make the finding stronger or weaker?"],
      ["Independent confirmation makes a result more reliable.",
       "'Robust' fits."]),

    Q("sat.rw.words", 2,
      "Although the editor praised the essay's argument, she found its prose ______ and asked for a rewrite.",
      [("convoluted", 1, ""),
       ("concise", 0, "Concise prose is compact; a rewrite request after praise suggests a problem, not brevity."),
       ("polished", 0, "Polished prose would not prompt a rewrite."),
       ("candid", 0, "Candour means honesty, which is not a fault to fix.")],
      ["The 'although' signals a contrast with praise.",
       "The rewrite request suggests the writing is hard to follow."],
      ["Contrast: good argument, problem with prose.",
       "'Convoluted' means tangled and hard to follow."]),

    Q("sat.rw.words", 3,
      "The city's new bus lanes had a ______ effect: average commute times fell by eleven minutes within a month.",
      [("pronounced", 1, ""),
       ("negligible", 0, "An eleven-minute drop is not negligible."),
       ("speculative", 0, "Speculative describes something unproven, but the effect was measured."),
       ("unintended", 0, "The passage gives no evidence the result was a surprise.")],
      ["The colon introduces the measurement.",
       "Is an eleven-minute drop large or small?"],
      ["An eleven-minute improvement is substantial.",
       "'Pronounced' means clearly noticeable."]),

    Q("sat.rw.words", 4,
      "Rather than ______ the criticism, the author revised the chapter and thanked the reviewer in the next edition.",
      [("dismiss", 1, ""),
       ("solicit", 0, "Soliciting criticism means asking for it, which does not fit 'rather than'."),
       ("anticipate", 0, "The author responded after the criticism, not in advance."),
       ("endorse", 0, "Endorsing criticism does not contrast with revising.")],
      ["'Rather than' sets up a contrast with revising.",
       "Which verb names the opposite response to criticism?"],
      ["The contrast is refusing the criticism versus acting on it.",
       "'Dismiss' is the refusal."]),

    # ================================================= SAT R&W: boundaries
    Q("sat.rw.boundaries", 1,
      "Which choice completes the text so that it conforms to the conventions of Standard English? 'The survey was sent to 400 households ______ only 120 were returned.'",
      [(";", 1, ""),
       (",", 0, "A comma alone between two complete sentences is a comma splice."),
       (":", 0, "A colon must follow an independent clause and introduce what follows; here it separates two full sentences."),
       ("", 0, "Without punctuation the two sentences run together.")],
      ["Are both halves complete sentences?",
       "Two complete sentences need a semicolon, period or comma + conjunction."],
      ["'The survey was sent to 400 households' is complete.",
       "'Only 120 were returned' is complete too — use a semicolon."]),

    Q("sat.rw.boundaries", 2,
      "Which choice completes the text so that it conforms to the conventions of Standard English? 'Marie Tharp, ______ mapped the ocean floor, changed how geologists understood plate tectonics.'",
      [("a cartographer who", 1, ""),
       ("a cartographer, who", 0, "This closes the non-essential phrase early and leaves 'mapped the ocean floor' dangling."),
       ("who a cartographer", 0, "The words are out of order."),
       ("a cartographer whom", 0, "'Whom' would be the object, but this person is the subject of 'mapped'.")],
      ["The phrase between the commas describes Tharp.",
       "Inside the phrase, who performs 'mapped'?"],
      ["The appositive is 'a cartographer who mapped the ocean floor'.",
       "Only the first choice keeps it intact."]),

    Q("sat.rw.boundaries", 3,
      "Which choice completes the text so that it conforms to the conventions of Standard English? 'The museum's collection includes works by Rivera, Kahlo, and Siqueiros ______ none of the three is on display this month.'",
      [(".", 1, ""),
       (",", 0, "A comma would splice two complete sentences."),
       ("; and", 0, "A semicolon plus a conjunction is not a standard boundary."),
       (":", 0, "A colon after a list does not introduce a contrasting full sentence well here; the second sentence stands on its own.")],
      ["Both sides of the gap are complete sentences.",
       "Which mark ends a sentence?"],
      ["The first sentence lists artists; the second is a new statement.",
       "A period separates them."]),

    Q("sat.rw.boundaries", 4,
      "Which choice completes the text so that it conforms to the conventions of Standard English? 'Because the samples were kept in the dark ______ the algae lost their colour.'",
      [(",", 1, ""),
       (";", 0, "A semicolon cannot follow a dependent clause introduced by 'because'."),
       (":", 0, "A colon needs a complete clause before it; 'Because the samples were kept in the dark' is not one."),
       ("", 0, "The dependent clause needs a comma before the main clause.")],
      ["'Because …' opens a dependent clause.",
       "What punctuation closes an introductory dependent clause?"],
      ["Introductory dependent clause + comma + main clause.",
       "The comma is required."]),

    # ===================================================== ACT: rates & percents
    Q("act.math.rates", 1,
      "A printer produces 45 pages in 3 minutes. At the same rate, how many pages does it produce in 8 minutes?",
      [("120", 1, ""),
       ("90", 0, "That is 45 × 2 minutes, but you need 8 minutes."),
       ("135", 0, "That would be 9 minutes of printing."),
       ("15", 0, "That is the pages-per-minute rate, not an 8-minute total.")],
      ["Find the rate per minute first.",
       "45 ÷ 3 = 15 pages per minute."],
      ["Rate = 15 pages/min.",
       "15 × 8 = 120."]),

    Q("act.math.rates", 2,
      "A jacket originally priced at $80 is discounted 25%, then an additional 10% is taken off the sale price. What is the final price?",
      [("$54", 1, ""),
       ("$52", 0, "That subtracts 35% at once; successive discounts multiply, they do not add."),
       ("$56", 0, "That applies only the 25% and then subtracts $4."),
       ("$60", 0, "That applies only the first discount.")],
      ["Apply the discounts one after the other.",
       "80 × 0.75 = 60, then 60 × 0.90."],
      ["After 25% off: $60.",
       "After a further 10%: $54."]),

    Q("act.math.rates", 3,
      "A car travels 150 miles in 2.5 hours. What is its average speed in miles per hour?",
      [("60", 1, ""),
       ("75", 0, "That is 150 ÷ 2, ignoring the extra half hour."),
       ("375", 0, "You multiplied distance by time."),
       ("55", 0, "Check the division: 150 ÷ 2.5.")],
      ["Speed = distance ÷ time.",
       "150 ÷ 2.5 = 1500 ÷ 25."],
      ["150 ÷ 2.5 = 60.",
       "Average speed is 60 mph."]),

    Q("act.math.rates", 4,
      "A solution is 15% acid. How many litres of pure acid are in 240 litres of the solution?",
      [("36", 1, ""),
       ("15", 0, "That is the percentage, not the amount."),
       ("24", 0, "That is 10% of 240."),
       ("3.6", 0, "Decimal point slipped: 0.15 × 240 = 36.")],
      ["Convert the percent to a decimal.",
       "0.15 × 240."],
      ["0.15 × 240 = 36.",
       "36 litres of acid."]),

    # ================================================ ACT: reading data
    Q("act.science.data", 1,
      "The table records three trials of a filter. What is the flow rate, in mL per second?",
      [("0.5 mL/s", 1, ""),
       ("2 mL/s", 0, "That inverts the ratio: you divided seconds by millilitres."),
       ("1 mL/s", 0, "That is the change between trials, not the rate within a trial."),
       ("20 mL/s", 0, "That is the time, not the rate.")],
      ["Rate is volume ÷ time.",
       "Use any row: 10 mL in 20 s."],
      ["10 ÷ 20 = 0.5.",
       "Every row gives the same rate."],
      TRIAL_TABLE),

    Q("act.science.data", 2,
      "Using the table, which statement is best supported?",
      [("The volume collected is proportional to the time.", 1, ""),
       ("The flow rate slows down in each later trial.", 0, "The rate is 0.5 mL/s in all three trials, so it is constant."),
       ("Time increases faster than volume.", 0, "Both double and triple together, so they grow at the same rate."),
       ("Trial 3 is an outlier.", 0, "Trial 3 fits the same 0.5 mL/s pattern as the others.")],
      ["Compare volume to time in each row.",
       "20/10, 40/20 and 60/30 all give the same ratio."],
      ["Each pair has the same ratio of 2 s per mL.",
       "So the volume is proportional to the time."],
      TRIAL_TABLE),

    Q("act.science.data", 3,
      "A graph of plant height against light intensity rises and then flattens out. What does the flat section most likely show?",
      [("Some other factor, such as carbon dioxide or water, has become limiting.", 1, ""),
       ("The plant has stopped absorbing light entirely.", 0, "The plateau shows growth is limited, not that light is ignored."),
       ("The measurements must be wrong.", 0, "A plateau is a normal saturation pattern, not evidence of error."),
       ("Height decreases as light increases.", 0, "The graph flattens; it does not fall.")],
      ["What happens to growth when one input keeps increasing but growth stops?",
       "Something else must be in short supply."],
      ["Growth saturates when another input runs short.",
       "That is the limiting-factor pattern."]),

    Q("act.science.data", 4,
      "Two species are plotted against temperature: species A peaks at 20 °C and species B peaks at 30 °C. Which conclusion is best supported?",
      [("Species B is better adapted to warmer conditions than species A.", 1, ""),
       ("Species A cannot survive at 30 °C.", 0, "The data shows a peak, not a survival limit."),
       ("Species B has a larger population at every temperature.", 0, "Nothing in the description says B is larger everywhere."),
       ("Temperature has no effect on either species.", 0, "Each species has a clear peak, so temperature matters.")],
      ["Compare where each curve reaches its highest point.",
       "The peak is the temperature the species does best at."],
      ["B peaks at the higher temperature.",
       "So B is adapted to warmer conditions."]),

    # ================================================= ACT: usage & punctuation
    Q("act.english.usage", 1,
      "Choose the best version of the underlined portion: 'Each of the students (have) submitted a lab report.'",
      [("has", 1, ""),
       ("have", 0, "The subject is 'Each', which is singular, so the verb must be 'has'."),
       ("were", 0, "That changes the tense and still disagrees with 'Each'."),
       ("having", 0, "That is not a finite verb, so the sentence loses its main verb.")],
      ["Find the subject — it is 'Each', not 'students'.",
       "'Each' is singular."],
      ["Singular subject takes a singular verb.",
       "'Each … has submitted'."]),

    Q("act.english.usage", 2,
      "Which version is clearest and most conventional?",
      [("The team finished the trial and published its results.", 1, ""),
       ("The team finished the trial and published their results.", 0, "'Team' is singular here, so 'its' matches; 'their' shifts number."),
       ("The team finished the trial, and published its results.", 0, "No comma is needed before 'and' when joining two verbs with one subject."),
       ("The team finished the trial and published there results.", 0, "'There' is a place; 'their' is the possessive.")],
      ["Is 'team' singular or plural in this sentence?",
       "Does the comma before 'and' separate complete clauses?"],
      ["One subject with two verbs takes no comma.",
       "'Team' is singular, so 'its'."]),

    Q("act.english.usage", 3,
      "Which sentence uses the apostrophe correctly?",
      [("The students' data were stored in the lab's freezer.", 1, ""),
       ("The student's data were stored in the labs' freezer.", 0, "'Student's' and 'labs'' put the possessives on the wrong nouns."),
       ("The students data were stored in the lab's freezer.", 0, "The plural possessive needs an apostrophe after 'students'."),
       ("The students' data were stored in the labs freezer.", 0, "'Labs freezer' is missing its possessive apostrophe.")],
      ["Decide whether each noun is plural before adding the apostrophe.",
       "Plural nouns ending in -s take the apostrophe after the s."],
      ["Many students → students'.",
       "One lab → lab's."]),

    Q("act.english.usage", 4,
      "Which choice best joins the ideas without a run-on? 'The reagent was expensive. It was the only one that worked.'",
      [("The reagent was expensive, but it was the only one that worked.", 1, ""),
       ("The reagent was expensive, it was the only one that worked.", 0, "That is a comma splice."),
       ("The reagent was expensive it was the only one that worked.", 0, "That is a run-on."),
       ("The reagent was expensive; but it was the only one that worked.", 0, "Do not use a semicolon before 'but'.")],
      ["The two clauses contrast.",
       "Use a comma plus a coordinating conjunction."],
      ["Contrast calls for 'but'.",
       "Comma + but is the conventional join."]),

    # ===================================================== MATHCOUNTS: counting
    Q("mc.counting", 1,
      "How many different 3-digit numbers can be formed using only the digits 1, 2 and 3 if repetition is allowed?",
      [("27", 1, ""),
       ("9", 0, "That is 3 choices for two positions; there are three positions."),
       ("6", 0, "That is the number of orderings without repetition (3!)."),
       ("12", 0, "That is 3 + 3 + 3 + 3, not a product of choices.")],
      ["Each of the three positions has 3 choices.",
       "Multiply the choices: 3 × 3 × 3."],
      ["3 choices per digit, 3 digits.",
       "3³ = 27."]),

    Q("mc.counting", 2,
      "How many ways can the letters of LEVEL be arranged?",
      [("30", 1, ""),
       ("120", 0, "That is 5! and ignores the repeated letters."),
       ("60", 0, "That divides by only one of the two repeated pairs."),
       ("20", 0, "That treats the two L's and two E's as three repeats in total.")],
      ["There are 5 letters, with L twice and E twice.",
       "Divide 5! by 2! for the L's and 2! for the E's."],
      ["5! = 120.",
       "120 ÷ (2 × 2) = 30."]),

    Q("mc.counting", 3,
      "A bug walks from the lower-left corner of a 4 × 4 grid to the upper-right corner, moving only right or up. How many shortest paths are there?",
      [("70", 1, ""),
       ("16", 0, "That counts the moves, not the orders in which they can be made."),
       ("256", 0, "That is 2⁸, treating each step as independent of the count of rights."),
       ("35", 0, "That is C(7,3), which is the answer for a 3 × 4 grid.")],
      ["Every shortest path is 4 rights and 4 ups.",
       "Choose which 4 of the 8 moves are the rights."],
      ["Paths = C(8, 4).",
       "C(8, 4) = 70."],
      GRID_4),

    Q("mc.counting", 4,
      "How many of the integers from 1 to 60 are divisible by 2 or by 3?",
      [("40", 1, ""),
       ("50", 0, "That adds 30 and 20 without removing the double-counted multiples of 6."),
       ("30", 0, "That counts only the multiples of 2."),
       ("10", 0, "That is the number of multiples of 6.")],
      ["Count multiples of 2, multiples of 3, then fix the overlap.",
       "Multiples of 6 were counted twice."],
      ["30 + 20 − 10 = 40.",
       "So 40 integers qualify."]),

    # ================================================ MATHCOUNTS: number theory
    Q("mc.numbertheory", 1,
      "What is the smallest prime factor of 91?",
      [("7", 1, ""),
       ("13", 0, "13 is a factor (91 = 7 × 13) but not the smallest one."),
       ("3", 0, "9 + 1 = 10, which is not divisible by 3."),
       ("11", 0, "11 × 8 = 88 and 11 × 9 = 99, so 11 does not divide 91.")],
      ["Test primes in order: 2, 3, 5, 7.",
       "91 ÷ 7 = 13."],
      ["91 is odd, digits sum to 10, does not end in 5.",
       "91 = 7 × 13, so 7 is smallest."]),

    Q("mc.numbertheory", 2,
      "How many positive divisors does 360 have?",
      [("24", 1, ""),
       ("12", 0, "That counts only some of the exponent combinations."),
       ("18", 0, "Check the exponents: 360 = 2³ · 3² · 5."),
       ("30", 0, "That is the number of divisors of 720, not 360.")],
      ["Prime factorise 360.",
       "Add one to each exponent and multiply."],
      ["360 = 2³ · 3² · 5¹.",
       "(3+1)(2+1)(1+1) = 24."]),

    Q("mc.numbertheory", 3,
      "What is the remainder when 3¹⁰⁰ is divided by 5?",
      [("1", 1, ""),
       ("3", 0, "That is 3¹, i.e. an exponent of 1 mod 4."),
       ("4", 0, "Powers of 3 mod 5 cycle 3, 4, 2, 1 — 4 appears at exponent 2."),
       ("0", 0, "3¹⁰⁰ is not a multiple of 5.")],
      ["Powers of 3 mod 5 repeat every 4 steps.",
       "100 is a multiple of 4."],
      ["3¹ ≡ 3, 3² ≡ 4, 3³ ≡ 2, 3⁴ ≡ 1 (mod 5).",
       "3¹⁰⁰ = (3⁴)²⁵ ≡ 1."]),

    Q("mc.numbertheory", 4,
      "What is the largest power of 3 that divides 50!?",
      [("3²²", 1, ""),
       ("3¹⁶", 0, "That counts only multiples of 3 and misses 9, 27."),
       ("3²⁷", 0, "That counts 50 ÷ 3 by rounding up rather than using Legendre's formula."),
       ("3²⁰", 0, "Close; recheck the 27 contribution.")],
      ["Count multiples of 3, then 9, then 27.",
       "16 + 5 + 1."],
      ["floor(50/3) = 16, floor(50/9) = 5, floor(50/27) = 1.",
       "16 + 5 + 1 = 22, so 3²²."]),

    # ============================================================ AMC 8: geometry
    Q("amc8.geometry", 1,
      "A right triangle has legs of length 6 and 8. What is the length of its hypotenuse?",
      [("10", 1, ""),
       ("14", 0, "That adds the legs; the hypotenuse is shorter than the sum."),
       ("√28", 0, "That is √(6² − 8²)-style arithmetic; add the squares, not subtract."),
       ("48", 0, "That is the area, not a length.")],
      ["Use the Pythagorean theorem.",
       "6² + 8² = 36 + 64."],
      ["36 + 64 = 100.",
       "√100 = 10."],
      RIGHT_6_8),

    Q("amc8.geometry", 2,
      "A rectangle is 12 cm wide and 5 cm tall. How long is its diagonal?",
      [("13 cm", 1, ""),
       ("17 cm", 0, "That adds the sides rather than using the diagonal."),
       ("60 cm", 0, "That is the area."),
       ("√119 cm", 0, "You subtracted the squares instead of adding them.")],
      ["The diagonal is the hypotenuse of a right triangle.",
       "12² + 5² = 144 + 25."],
      ["144 + 25 = 169.",
       "√169 = 13."],
      RECT_12_5),

    Q("amc8.geometry", 3,
      "A triangle has base 10 cm and height 7 cm. What is its area?",
      [("35 cm²", 1, ""),
       ("70 cm²", 0, "That is base × height; a triangle is half of that."),
       ("17 cm²", 0, "That adds the base and height."),
       ("140 cm²", 0, "That doubles base × height instead of halving it.")],
      ["Area of a triangle = ½ × base × height.",
       "½ × 10 × 7."],
      ["½ × 70 = 35.",
       "Area = 35 cm²."],
      TRI_10_7),

    Q("amc8.geometry", 4,
      "A circle has radius 3. What is its circumference, in terms of π?",
      [("6π", 1, ""),
       ("3π", 0, "That uses the radius in place of the diameter."),
       ("9π", 0, "That is the area, not the circumference."),
       ("12π", 0, "That multiplies by 4r.")],
      ["Circumference = 2πr.",
       "r = 3."],
      ["C = 2π(3).",
       "C = 6π."]),

    # =========================================================== AMC 8: counting
    Q("amc8.counting", 1,
      "How many integers from 1 to 100 are divisible by 3 or by 5?",
      [("47", 1, ""),
       ("53", 0, "That adds 33 and 20 without removing the multiples of 15."),
       ("33", 0, "That counts only multiples of 3."),
       ("60", 0, "That over-counts the overlap twice.")],
      ["Count by 3, count by 5, then subtract the double-counted numbers.",
       "Multiples of 15 are counted in both lists."],
      ["33 + 20 − 6 = 47.",
       "So 47 integers."]),

    Q("amc8.counting", 2,
      "How many squares of all sizes are in a 3 × 3 grid of unit squares?",
      [("14", 1, ""),
       ("9", 0, "That counts only the unit squares."),
       ("13", 0, "That misses the large 3 × 3 square."),
       ("36", 0, "That counts rectangles instead of squares.")],
      ["Count 1 × 1, then 2 × 2, then 3 × 3.",
       "How many 2 × 2 squares fit?"],
      ["1 × 1: 9, 2 × 2: 4, 3 × 3: 1.",
       "9 + 4 + 1 = 14."],
      GRID_3),

    Q("amc8.counting", 3,
      "In how many ways can 10 identical stickers be split between two children so that each child gets at least one?",
      [("9", 1, ""),
       ("10", 0, "That includes giving all ten to one child."),
       ("11", 0, "That counts the split 0-and-10 as well as 10-and-0."),
       ("45", 0, "That is the number of ways to choose 2 of 10, not a two-way split.")],
      ["Let the first child get k stickers.",
       "k can be 1 through 9."],
      ["k = 1, 2, …, 9, with the second child getting the rest.",
       "That is 9 splits."]),

    Q("amc8.counting", 4,
      "In how many ways can 3 students be seated in 5 chairs arranged in a row?",
      [("60", 1, ""),
       ("10", 0, "That is the number of ways to choose 3 chairs, ignoring who sits where."),
       ("125", 0, "That is 5³, which allows two students in the same chair."),
       ("15", 0, "That is 5 × 3, which is not a permutation.")],
      ["First choose who sits in the first chair, then the second, then the third.",
       "5 × 4 × 3."],
      ["5 × 4 × 3 = 60.",
       "That is P(5, 3)."]),

    # ========================================================== AMC 10: algebra
    Q("amc10.algebra", 1,
      "If x + 1/x = 3, what is x² + 1/x²?",
      [("7", 1, ""),
       ("9", 0, "That is (x + 1/x)² without subtracting the cross term."),
       ("6", 0, "That is 2 × 3, which ignores the squaring."),
       ("11", 0, "That adds 2 instead of subtracting 2.")],
      ["Square both sides.",
       "(x + 1/x)² = x² + 2 + 1/x²."],
      ["9 = x² + 2 + 1/x².",
       "So x² + 1/x² = 7."]),

    Q("amc10.algebra", 2,
      "The equation |2x − 3| = 7 has two solutions. What is their product?",
      [("−10", 1, ""),
       ("10", 0, "The solutions are 5 and −2, whose product is negative."),
       ("−5", 0, "That is the sum of the solutions, not the product."),
       ("0", 0, "Neither solution is 0.")],
      ["Split into 2x − 3 = 7 and 2x − 3 = −7.",
       "Solve each for x."],
      ["x = 5 or x = −2.",
       "5 × (−2) = −10."],
      NUMBER_LINE_ABS),

    Q("amc10.algebra", 3,
      "What is the sum of the roots of 2x² − 8x + 6 = 0?",
      [("4", 1, ""),
       ("3", 0, "That is the product of the roots (c/a)."),
       ("8", 0, "That is −b, not −b/a."),
       ("−4", 0, "Check the sign rule: sum = −b/a with b = −8.")],
      ["Sum of roots = −b/a.",
       "Here a = 2 and b = −8."],
      ["−(−8)/2 = 4.",
       "The roots are 1 and 3, which sum to 4."]),

    Q("amc10.algebra", 4,
      "If a + b = 5 and ab = 6, what is a² + b²?",
      [("13", 1, ""),
       ("25", 0, "That is (a + b)², which includes the cross term."),
       ("11", 0, "That subtracts 2ab incorrectly as 14."),
       ("19", 0, "That adds ab instead of subtracting 2ab.")],
      ["Use a² + b² = (a + b)² − 2ab.",
       "25 − 12."],
      ["25 − 2(6) = 13.",
       "(Indeed a = 2, b = 3.)"]),

    # ========================================================= AMC 10: geometry
    Q("amc10.geometry", 1,
      "A chord of length 8 lies in a circle of radius 5. How far is the chord from the centre?",
      [("3", 1, ""),
       ("4", 0, "That is half the chord, not the distance to the centre."),
       ("√41", 0, "You subtracted the wrong way: 25 − 16 = 9."),
       ("9", 0, "That is the square of the distance.")],
      ["The perpendicular from the centre bisects the chord.",
       "You get a right triangle with hypotenuse 5 and one leg 4."],
      ["Leg² = 25 − 16 = 9.",
       "Distance = 3."],
      CHORD_8_R5),

    Q("amc10.geometry", 2,
      "What is the area of an equilateral triangle with side length 6?",
      [("9√3", 1, ""),
       ("18", 0, "That is ½ × 6 × 6, using the side as the height."),
       ("36√3", 0, "That uses the wrong factor in the formula."),
       ("3√3", 0, "That is the area for side length 2√3.")],
      ["Area = (√3/4)s².",
       "s = 6, so s² = 36."],
      ["(√3/4)(36) = 9√3.",
       "Area = 9√3."]),

    Q("amc10.geometry", 3,
      "What is the area of a regular hexagon with side length 2?",
      [("6√3", 1, ""),
       ("12", 0, "That is the perimeter times the apothem incorrectly; recheck the apothem."),
       ("24", 0, "That is 6 × 2 × 2, which is not the hexagon's area."),
       ("3√3", 0, "That is the area of three equilateral triangles, not six.")],
      ["Split the hexagon into 6 equilateral triangles.",
       "Each triangle has side 2, area (√3/4)(4) = √3."],
      ["6 × √3 = 6√3.",
       "Area = 6√3."]),

    Q("amc10.geometry", 4,
      "A right triangle has hypotenuse 13 and one leg 5. What is its area?",
      [("30", 1, ""),
       ("32.5", 0, "That is ½ × 13 × 5, treating the hypotenuse as a leg."),
       ("60", 0, "That is leg × leg without halving."),
       ("65", 0, "That is hypotenuse × leg.")],
      ["Find the other leg first.",
       "13² − 5² = 144, so the leg is 12."],
      ["Area = ½ × 5 × 12.",
       "Area = 30."],
      TRI_5_13),

    # ====================================================== AMC 12: functions
    Q("amc12.functions", 1,
      "If f(x) = 2x + 3, what is f⁻¹(7)?",
      [("2", 1, ""),
       ("17", 0, "That is f(7), not the inverse."),
       ("4", 0, "That solves 2x + 3 = 11 rather than 7."),
       ("5", 0, "That is (7 + 3)/2, adding instead of subtracting.")],
      ["Solve 2x + 3 = 7 for x.",
       "2x = 4."],
      ["2x + 3 = 7 → 2x = 4.",
       "x = 2."]),

    Q("amc12.functions", 2,
      "What is the period of f(x) = sin(3x)?",
      [("2π/3", 1, ""),
       ("2π", 0, "That is the period of sin(x), before the horizontal compression."),
       ("3π", 0, "That multiplies by 3 instead of dividing."),
       ("π/3", 0, "That is the period of sin(6x).")],
      ["sin(kx) has period 2π/k.",
       "k = 3."],
      ["Period = 2π/3.",
       "The graph completes one cycle in that interval."]),

    Q("amc12.functions", 3,
      "What is the minimum value of f(x) = x² − 4x + 7?",
      [("3", 1, ""),
       ("7", 0, "That is f(0), not the minimum."),
       ("4", 0, "That is the x-coordinate of the vertex."),
       ("−3", 0, "You subtracted the vertex value instead of adding it.")],
      ["Complete the square or use x = −b/(2a).",
       "The vertex is at x = 2."],
      ["f(2) = 4 − 8 + 7.",
       "Minimum value is 3."]),

    Q("amc12.functions", 4,
      "Solve 2^(x+1) = 8^(x−1).",
      [("x = 2", 1, ""),
       ("x = 1", 0, "Check: 2² = 4 and 8⁰ = 1, which are not equal."),
       ("x = 4", 0, "That gives 2⁵ = 32 and 8³ = 512."),
       ("x = 1/2", 0, "That gives 2^1.5 ≈ 2.83 and 8^(−0.5) ≈ 0.35.")],
      ["Write 8 as 2³.",
       "Then x + 1 = 3(x − 1)."],
      ["x + 1 = 3x − 3.",
       "4 = 2x, so x = 2."]),

    # ================================================== AMC 12: combinatorics
    Q("amc12.combinatorics", 1,
      "How many 4-letter strings can be made from the letters A, B, C that contain at least one A?",
      [("65", 1, ""),
       ("81", 0, "That counts all 3⁴ strings, including those with no A."),
       ("32", 0, "That is 2⁵, which is for 5-letter strings."),
       ("16", 0, "That is 2⁴, the strings with no A.")],
      ["Count all strings, then subtract those with no A.",
       "3⁴ − 2⁴."],
      ["81 − 16 = 65.",
       "So 65 strings contain at least one A."]),

    Q("amc12.combinatorics", 2,
      "How many ways can a committee of 3 be chosen from 8 people?",
      [("56", 1, ""),
       ("336", 0, "That is P(8, 3), which counts order."),
       ("24", 0, "That is 4!, unrelated to this choice."),
       ("112", 0, "That doubles C(8, 3).")],
      ["Order does not matter, so use combinations.",
       "C(8, 3) = 8!/(3!5!)."],
      ["(8 × 7 × 6)/(3 × 2 × 1).",
       "= 56."]),

    Q("amc12.combinatorics", 3,
      "How many shortest lattice paths go from (0, 0) to (4, 4) moving only right or up?",
      [("70", 1, ""),
       ("16", 0, "That counts moves, not orderings."),
       ("256", 0, "That treats each step independently of the number of rights."),
       ("35", 0, "That is C(7, 3), for a 3 × 4 grid.")],
      ["Any shortest path is 4 R's and 4 U's.",
       "Choose 4 of the 8 positions for the R's."],
      ["C(8, 4) = 70.",
       "So 70 paths."],
      GRID_4),

    Q("amc12.combinatorics", 4,
      "At a meeting, each of 10 people shakes hands with every other person exactly once. How many handshakes occur?",
      [("45", 1, ""),
       ("90", 0, "That counts each handshake twice, once from each person."),
       ("100", 0, "That is 10², which includes people shaking their own hand."),
       ("55", 0, "That is C(11, 2), for 11 people.")],
      ["Each handshake is a pair of people.",
       "Count pairs, not directed greetings."],
      ["C(10, 2) = (10 × 9)/2.",
       "= 45."]),

    # ==================================== OpenBookQA items (Apache-2.0)
    # Open-book science questions from Allen Institute for AI's OpenBookQA
    # (Mihaylov et al., 2018), Apache License 2.0. Stems and choices follow the
    # source; hints, solution steps and option rationales are written by us.
    Q("sci.elem.concepts", 1,
      "Stars are",
      [("great balls of gas burning billions of miles away", 1, ""),
       ("warm lights that float", 0, "Stars are not floating lamps; they are enormous bodies of hot gas."),
       ("made out of nitrate", 0, "Nitrate is a chemical group found on Earth, not what stars are made of."),
       ("lights in the sky", 0, "That describes how they look from here, not what they are.")],
      ["What is the Sun, the nearest star, made of?",
       "It is mostly hydrogen and helium, and it is extremely hot."],
      ["Stars are huge, hot spheres of gas.",
       "The best choice says exactly that."],
      visual=STAR_DIAGRAM,
      source=OBQA),

    Q("sci.elem.concepts", 1,
      "What happens when mercury is placed in water?",
      [("It sinks", 1, ""),
       ("It dissolves", 0, "Liquid mercury does not dissolve in water; the two do not mix."),
       ("It floats", 0, "Mercury is much denser than water, so it does not float."),
       ("It hardens", 0, "Mercury stays liquid at room temperature and does not harden in water.")],
      ["Which is denser: mercury or water?",
       "A coin-sized amount of mercury is heavier than the same volume of water."],
      ["Mercury is about 13 times denser than water.",
       "So it sinks to the bottom."],
      source=OBQA),

    Q("sci.elem.concepts", 2,
      "A magnet will stick to",
      [("a belt buckle", 1, ""),
       ("a wooden table", 0, "Wood is not magnetic; magnets ignore it."),
       ("a plastic cup", 0, "Plastic is not magnetic."),
       ("a paper plate", 0, "Paper is not magnetic.")],
      ["Which of these objects is made of metal?",
       "Magnets attract iron and steel."],
      ["A belt buckle is typically steel or another iron alloy.",
       "The other three are wood, plastic and paper."],
      source=OBQA),

    Q("sci.elem.concepts", 2,
      "Which of these things will supplement a squirrel's caloric needs?",
      [("Nuts", 1, ""),
       ("Fish", 0, "Squirrels are not fishers; nuts and seeds are their staple food."),
       ("Tree bark", 0, "Bark is eaten in hard times but is a poor calorie source compared with nuts."),
       ("Leaves", 0, "Leaves provide little energy for a squirrel.")],
      ["What do squirrels spend the autumn collecting?",
       "Think of the food they bury for winter."],
      ["Nuts are dense in fat and energy.",
       "That is exactly what a squirrel caches."],
      source=OBQA),

    Q("sci.elem.concepts", 2,
      "A student can scratch a mineral sample with a fingernail. How is that mineral best described?",
      [("A soft mineral", 1, ""),
       ("A hard mineral", 0, "If a fingernail scratches it, the mineral is softer than a fingernail, not harder."),
       ("A liquid mineral", 0, "Scratching is a test of hardness; nothing here suggests a liquid."),
       ("A mineral melt", 0, "A melt would be molten rock, which a solid sample is not.")],
      ["A fingernail has a low Mohs hardness (about 2.5).",
       "What does it mean if a mineral can be scratched by something that soft?"],
      ["Being scratched by a fingernail puts the mineral below about 2.5 on the Mohs scale.",
       "That makes it soft."],
      source=OBQA),

    Q("sci.elem.concepts", 3,
      "One example of a chemical change is acid breaking down a substance. Which of these is another example of a chemical change?",
      [("Lemon juice added to milk", 1, ""),
       ("Flour added to salt", 0, "Mixing two powders is a physical change; nothing new is formed."),
       ("Milk added to water", 0, "Diluting milk in water leaves both substances unchanged."),
       ("Corn added to soup", 0, "Stirring corn into soup is mixing, not a reaction.")],
      ["A chemical change makes a new substance.",
       "Which pair reacts to form something different (here, curds)?"],
      ["Acid curdles the protein in milk, forming new material.",
       "That is a chemical change; mixing powders is not."],
      source=OBQA),

    Q("sci.elem.concepts", 3,
      "Matter in the gas phase has",
      [("a volume that changes with its container", 1, ""),
       ("a fixed volume but no fixed shape", 0, "That describes a liquid, not a gas."),
       ("a fixed volume and a fixed shape", 0, "That describes a solid."),
       ("no particles at all", 0, "Gases are made of particles; they are simply far apart and moving fast.")],
      ["How does the volume of a gas respond to the container it is in?",
       "Think of helium filling a whole balloon."],
      ["Gas particles spread out to fill their container.",
       "So both shape and volume follow the container."],
      source=OBQA),

    Q("sci.elem.concepts", 4,
      "What is most likely to be an effect of acid rain on an aquatic environment?",
      [("A decrease in plant life", 1, ""),
       ("An increase in fish population", 0, "Acidified water stresses fish; populations fall rather than rise."),
       ("An increase in plant growth", 0, "Acid rain damages aquatic plants rather than fertilising them."),
       ("Cleaner, clearer water", 0, "Acid rain can leach metals into water, which is worse, not cleaner.")],
      ["Acid rain lowers the pH of lakes and streams.",
       "How do plants and fish cope with acidic water?"],
      ["Lower pH harms aquatic plants and animals.",
       "The best-supported effect is a decline in plant life."],
      source=OBQA),

    # ========================================== GSM8K items (MIT licence)
    # Word problems from OpenAI's GSM8K (Cobbe et al., 2021), MIT licence. Stems
    # follow the source; the multiple-choice options, hints and steps are ours.
    Q("mc.wordproblems", 1,
      "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
      [("72", 1, ""),
       ("96", 0, "That doubles 48 instead of adding half of it."),
       ("24", 0, "That is May's sales alone."),
       ("60", 0, "That adds a quarter of 48 rather than half.")],
      ["How many did she sell in May?",
       "Half of 48 is 24, and the question asks for both months."],
      ["May: 48 ÷ 2 = 24 clips.",
       "Total: 48 + 24 = 72."],
      visual=CLIP_BARS,
      source=GSM8K),

    Q("mc.wordproblems", 1,
      "Weng earns $12 an hour for babysitting. Yesterday, she did 50 minutes of babysitting. How much did she earn?",
      [("$10", 1, ""),
       ("$12", 0, "That is a full hour's pay; she worked less than an hour."),
       ("$6", 0, "That treats 50 minutes as half an hour."),
       ("$600", 0, "You multiplied 12 by 50 without converting minutes to hours.")],
      ["Convert 50 minutes to a fraction of an hour.",
       "50 minutes is 50/60 = 5/6 of an hour."],
      ["Pay = 12 × 5/6.",
       "12 × 5/6 = $10."],
      visual=RATE_BARS,
      source=GSM8K),

    Q("mc.wordproblems", 2,
      "Julie is reading a 120-page book. Yesterday she read 12 pages and today she read twice as many pages as yesterday. If she wants to read half of the remaining pages tomorrow, how many pages should she read?",
      [("42", 1, ""),
       ("84", 0, "That is all the remaining pages, not half of them."),
       ("48", 0, "That is half of 96, which miscounts today's pages."),
       ("108", 0, "That is the remaining pages after reading only 12.")],
      ["How many pages did she read today?",
       "Then subtract both days from 120."],
      ["Today: 2 × 12 = 24 pages. Read so far: 36.",
       "Remaining 84; half is 42."],
      source=GSM8K),

    Q("mc.wordproblems", 3,
      "Albert buys 2 large pizzas and 2 small pizzas. A large pizza has 16 slices and a small pizza has 8 slices. If he eats it all, how many slices does he eat that day?",
      [("48", 1, ""),
       ("24", 0, "That counts only the large pizzas."),
       ("40", 0, "That uses one large and three small pizzas."),
       ("64", 0, "That doubles the total instead of adding the two sizes.")],
      ["Find the slices from the large pizzas, then from the small ones.",
       "2 × 16 = 32 and 2 × 8 = 16."],
      ["32 + 16 = 48.",
       "So he eats 48 slices."],
      source=GSM8K),
]
