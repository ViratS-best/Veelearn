"""AP Biology units 5–8: Heredity through Ecology."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    page_break,
    mq,
    xy_graph,
    sample_curve,
    punnett_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _pedigree_svg(w=300, h=160):
    """Three-generation pedigree: shaded recessive child of heterozygous parents."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="90" cy="30" r="14" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        f'<rect x="176" y="16" width="28" height="28" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="104" y1="30" x2="176" y2="30" stroke="#0f172a"/>'
        f'<line x1="140" y1="30" x2="140" y2="80" stroke="#0f172a"/>'
        f'<line x1="70" y1="80" x2="210" y2="80" stroke="#0f172a"/>'
        f'<circle cx="70" cy="110" r="14" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        f'<rect x="126" y="96" width="28" height="28" fill="#1e3a8a"/>'
        f'<circle cx="210" cy="110" r="14" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="150" y="150" text-anchor="middle" font-size="11">shaded = affected (often recessive if parents are clear)</text>'
        f"</svg>"
    )


def _transcription_pair_svg(w=340, h=170):
    """DNA template pairing to RNA, including A·U (not a DNA A–T ladder)."""
    xs = (70, 130, 190, 250)
    rna = ("A", "U", "G", "C")
    dna = ("T", "A", "C", "G")
    rungs = "".join(
        f'<line x1="{x}" y1="52" x2="{x}" y2="98" stroke="#64748b" stroke-width="2.2" stroke-dasharray="4 3"/>'
        for x in xs
    )
    rna_txt = "".join(
        f'<text x="{x}" y="44" text-anchor="middle" font-size="14" fill="#047857">{b}</text>'
        for x, b in zip(xs, rna)
    )
    dna_txt = "".join(
        f'<text x="{x}" y="118" text-anchor="middle" font-size="14" fill="#1d4ed8">{b}</text>'
        for x, b in zip(xs, dna)
    )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="40" y1="48" x2="280" y2="48" stroke="#059669" stroke-width="6"/>'
        f'<line x1="40" y1="102" x2="280" y2="102" stroke="#1d4ed8" stroke-width="6"/>'
        f"{rungs}{rna_txt}{dna_txt}"
        f'<rect x="108" y="28" width="44" height="96" fill="none" stroke="#d97706" stroke-dasharray="4 3"/>'
        f'<text x="130" y="22" text-anchor="middle" font-size="11" fill="#b45309">A templates U</text>'
        f'<text x="20" y="52" font-size="11" fill="#047857">5′</text>'
        f'<text x="288" y="52" font-size="11" fill="#047857">3′ RNA</text>'
        f'<text x="20" y="106" font-size="11" fill="#1d4ed8">3′</text>'
        f'<text x="288" y="106" font-size="11" fill="#1d4ed8">5′ DNA template</text>'
        f'<text x="170" y="155" text-anchor="middle" font-size="12">T on DNA still pairs A on RNA</text>'
        f"</svg>"
    )


def _fork_svg(w=320, h=150):
    """Replication fork: leading strand vs lagging Okazaki fragments."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="20" y1="40" x2="160" y2="40" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="20" y1="110" x2="160" y2="110" stroke="#b91c1c" stroke-width="4"/>'
        f'<line x1="160" y1="40" x2="280" y2="20" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="160" y1="110" x2="280" y2="130" stroke="#b91c1c" stroke-width="4"/>'
        f'<line x1="180" y1="44" x2="250" y2="28" stroke="#059669" stroke-width="3"/>'
        f'<line x1="175" y1="100" x2="200" y2="108" stroke="#d97706" stroke-width="3"/>'
        f'<line x1="210" y1="108" x2="235" y2="116" stroke="#d97706" stroke-width="3"/>'
        f'<text x="210" y="22" font-size="11" fill="#059669">leading 5′→3′</text>'
        f'<text x="150" y="145" font-size="11" fill="#d97706">Okazaki fragments</text>'
        f"</svg>"
    )


def _operon_svg(w=340, h=130):
    """Lac operon: promoter, operator, genes."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="10" y="40" width="50" height="36" fill="#fde68a" stroke="#92400e"/>'
        f'<text x="35" y="62" text-anchor="middle" font-size="11">P</text>'
        f'<rect x="70" y="40" width="50" height="36" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="95" y="62" text-anchor="middle" font-size="11">O</text>'
        f'<rect x="130" y="40" width="60" height="36" fill="#bbf7d0" stroke="#166534"/>'
        f'<text x="160" y="62" text-anchor="middle" font-size="11">Z</text>'
        f'<rect x="200" y="40" width="60" height="36" fill="#bbf7d0" stroke="#166534"/>'
        f'<text x="230" y="62" text-anchor="middle" font-size="11">Y</text>'
        f'<rect x="270" y="40" width="60" height="36" fill="#bbf7d0" stroke="#166534"/>'
        f'<text x="300" y="62" text-anchor="middle" font-size="11">A</text>'
        f'<text x="170" y="110" text-anchor="middle" font-size="12">repressor binds O unless lactose is present</text>'
        f"</svg>"
    )


def _cladogram_svg(w=300, h=170):
    """Simple cladogram with a shared derived trait mark."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="30" y1="150" x2="30" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="30" y1="40" x2="90" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="30" y1="90" x2="160" y2="90" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="160" y1="90" x2="160" y2="50" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="160" y1="90" x2="160" y2="130" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="160" y1="50" x2="250" y2="50" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="160" y1="130" x2="250" y2="130" stroke="#0f172a" stroke-width="2"/>'
        f'<circle cx="90" cy="40" r="5" fill="#b91c1c"/>'
        f'<text x="100" y="36" font-size="11">outgroup</text>'
        f'<text x="258" y="54" font-size="11">A</text>'
        f'<text x="258" y="134" font-size="11">B</text>'
        f'<text x="120" y="84" font-size="11" fill="#1d4ed8">shared derived trait</text>'
        f"</svg>"
    )


def _pyramid_svg(w=260, h=170):
    """Energy pyramid: producer → consumer → top."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="40,150 220,150 180,110 80,110" fill="#86efac" stroke="#166534"/>'
        f'<polygon points="80,110 180,110 155,70 105,70" fill="#fde68a" stroke="#92400e"/>'
        f'<polygon points="105,70 155,70 140,36 120,36" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="130" y="138" text-anchor="middle" font-size="11">producers 1000</text>'
        f'<text x="130" y="96" text-anchor="middle" font-size="11">herbivores 100</text>'
        f'<text x="130" y="58" text-anchor="middle" font-size="11">carnivores 10</text>'
        f"</svg>"
    )


def _qs(pairs):
    qs, idx = [], 1
    for text, ans, expl, dist in pairs:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return qs


# ===========================================================================
# UNIT 5: Heredity
# ===========================================================================

def _u5_questions():
    return _qs([
        ("Mendel’s law of segregation says that the two alleles of a gene:",
         "separate into different gametes so each gamete carries one",
         "In meiosis I, homologs (which carry the two alleles) go to opposite poles. That is why a heterozygote Aa produces about half A and half a gametes, not Aa gametes as a rule.",
         ["blend into a medium allele in every generation", "stay together on the same gamete always", "are destroyed at fertilization"]),
        ("A true-breeding purple pea (PP) crossed to true-breeding white (pp) yields F1 that are all purple. Purple is:",
         "dominant; white is recessive",
         "The F1 are Pp. Dominance means the heterozygote looks like the P parent. Recessive white appears again in F2 when pp reconstitutes.",
         ["incompletely dominant in this description", "codominant with white in the F1", "not genetic"]),
        ("Mendel’s independent assortment applies when:",
         "two genes are on different chromosomes (or far apart on one)",
         "Metaphase I orientations of different homolog pairs are independent. Linked genes on one chromosome violate the 9:3:3:1 expectation.",
         ["two genes are the same gene", "all genes in humans are on one chromosome", "mitosis shuffles homologs"]),
        ("A 3:1 phenotypic ratio in an F2 monohybrid cross is evidence of:",
         "segregation of one gene with complete dominance",
         "Genotypes 1 PP : 2 Pp : 1 pp, but P_ looks the same, so phenotypes 3:1. If the ratio is 1:2:1 of appearances, think incomplete dominance.",
         ["two genes on different chromosomes only", "only cytoplasmic inheritance", "a 9:3:3:1 dihybrid"]),
        ("A testcross of a dominant-phenotype individual uses a:",
         "homozygous recessive tester, so the offspring ratio reveals the unknown genotype",
         "If the unknown is PP, all offspring show dominant. If Pp, half recessive. The tester contributes only recessive alleles, so it cannot mask the unknown gametes.",
         ["homozygous dominant tester", "another unknown dominant", "a triploid"]),
        ("Probability of two independent events both happening is the:",
         "product of their individual probabilities",
         "Two coins both heads: $\\frac{1}{2}\\times\\frac{1}{2}=\\frac{1}{4}$. Two heterozygous parents both passing a: $\\frac{1}{2}\\times\\frac{1}{2}=\\frac{1}{4}$ for aa.",
         ["sum of the probabilities always", "difference of the probabilities", "product plus one"]),
        ("Probability of either of two mutually exclusive genotypes (PP or Pp) is the:",
         "sum of their probabilities",
         "From Aa × Aa: P(PP)=1/4, P(Pp)=1/2, P(dominant phenotype)=3/4. Add when outcomes cannot both be true for one offspring.",
         ["product only", "1 minus the product in every case including independent ‘and’ events", "always 1/2"]),
        ("AaBb × AaBb, unlinked, complete dominance: the fraction of offspring that are A_B_ (both dominant phenotypes) is:",
         "9/16",
         "Each gene gives 3/4 dominant phenotype. Independent: $\\frac{3}{4}\\times\\frac{3}{4}=\\frac{9}{16}$. The 9:3:3:1 is this product rule in a table.",
         ["3/4", "1/16", "1/2"]),
        ("From Aa × Aa, the chance of three children all being aa is:",
         "1/64",
         "Each child is an independent fertilization: $(1/4)^3=1/64$. Do not multiply by 3; that would be a different question (expected count).",
         ["3/4", "1/12", "1/4"]),
        ("A Punnett square is a map of:",
         "random combination of parental gametes",
         "Rows and columns are gametes (products of meiosis). Boxes are zygotes. The square does not create linkage or change Mendel’s laws; it displays them.",
         ["mitotic anaphase in skin cells", "a cladogram of peas", "Hardy–Weinberg for a whole species only"]),
        ("Linked genes tend to be inherited together because they:",
         "sit on the same chromosome and only recombine if a crossover happens between them",
         "Distance in map units ≈ recombination frequency × 100. Close genes: few recombinants. Far genes: RF approaches 50%, looking unlinked.",
         ["are always on different chromosomes", "cannot mutate", "are both mitochondrial"]),
        ("In a testcross of a dihybrid with genes in coupling (AB/ab × ab/ab), parentals look like AB and ab; recombinants look like:",
         "Ab and aB",
         "Crossovers between the loci swap alleles to produce the other two haplotypes. RF = (recombinants)/total.",
         ["only AABB", "only abab as a new class", "mitochondrial types"]),
        ("If 18 + 22 recombinant offspring appear among 200 progeny, RF is:",
         "0.20 (20 map units)",
         "$(18+22)/200=0.20$. One map unit is 1% recombination. Do not count parentals in the numerator.",
         ["0.80", "40 map units because 18+22=40 without dividing", "0.50 exactly always for any two genes"]),
        ("A recombination frequency of 50% between two genes usually means:",
         "they are unlinked — different chromosomes or very far apart",
         "Independent assortment also gives 50% recombinant-looking types. Mapping cannot resolve genes that far apart as a single interval without intermediate markers.",
         ["they are 0 map units apart", "they are the same gene", "meiosis failed"]),
        ("Crossing over occurs in prophase I. That is why linkage maps are built from:",
         "meiotic products (gametes or testcross offspring), not from mitosis of skin cells",
         "Somatic crossing over is rare and not how classical maps were made. The biology of Unit 4 is the mechanism under Unit 5’s numbers.",
         ["binary fission", "transcription rates", "Hardy–Weinberg p²"]),
        ("In a pedigree, two unaffected parents have an affected child. The trait is most likely:",
         "recessive (parents are heterozygous carriers)",
         "Dominant traits do not usually skip from two unaffected parents unless a new mutation. Recessive traits hide in heterozygotes. Confirm with more of the pedigree.",
         ["Y-linked if the child is a daughter", "always mitochondrial", "dominant with 100% penetrance and no mutation"]),
        ("An X-linked recessive trait (like many forms of hemophilia) appears more in:",
         "males, who are hemizygous for X genes",
         "A son gets his X from his mother. A carrier mother (XᴴXʰ) has a 1/2 chance to pass the allele to each son. Fathers pass their X to daughters, not to sons.",
         ["females only, because they have two X’s that both must show the trait every time", "everyone equally without regard to sex chromosomes", "only grandparents"]),
        ("A Y-linked trait is passed:",
         "from father to all sons and to no daughters",
         "Daughters do not receive a Y. If a pedigree shows father–daughter transmission, it is not Y-linked.",
         ["from mother to all children", "only through daughters", "to 1/4 of grandchildren regardless of sex"]),
        ("Mitochondrial DNA is inherited:",
         "from the mother (egg cytoplasm) in animals",
         "Sperm contributes almost no cytoplasm. A pedigree of a mitochondrial disease shows transmission from affected mothers to all children, and no transmission from affected fathers.",
         ["from the father only", "equally from both parents’ nuclei", "on the Y chromosome"]),
        ("Incomplete penetrance means:",
         "some individuals with the genotype do not show the phenotype",
         "The pedigree then looks ‘messy’ compared with Mendel’s peas. Environment and other genes (epistasis, modifiers) are often why.",
         ["the allele is not DNA", "Punnett squares cannot be drawn for peas", "dominance is the same as penetrance"]),
        ("A human male is XY. His gametes that determine chromosomal sex of offspring carry:",
         "either X or Y (roughly half and half)",
         "Mothers contribute X to every egg. The sperm’s sex chromosome decides XX vs XY. Nondisjunction can produce XO, XXY, etc. (Unit 4).",
         ["only X", "only Y", "both X and Y in every sperm"]),
        ("X-inactivation (Barr body) in XX mammals means:",
         "one X is silenced at random in each cell, making females mosaics for heterozygous X genes",
         "Calico cats are the mascot. Dosage compensation also explains why extra X chromosomes are more tolerable than extra autosomes.",
         ["both X chromosomes are deleted", "males inactivate their Y in every tissue", "mitochondria inactivate nuclear genes"]),
        ("A translocation moves a piece of one chromosome to another. If it disrupts a gene or creates a fusion protein, the phenotype can change even if:",
         "the person still has a balanced amount of DNA overall",
         "Structure (where a gene sits, what it fuses to) changes function. Karyotypes can see large translocations; they miss SNPs.",
         ["DNA amount must always be aneuploid", "translocations are RNA-only events", "Punnett squares forbid chromosomal change"]),
        ("Nondisjunction in meiosis can produce a gamete with two sex chromosomes. Fertilization can then yield:",
         "XXY, XO, or similar aneuploidies depending on the partner gamete",
         "Track the sex chromosomes like any homolog pair. This is Unit 4 arithmetic living in a heredity unit.",
         ["only 2n=46 guaranteed", "polyploidy of all autosomes necessarily", "a change from DNA to protein in the karyotype"]),
        ("A gene on an autosome vs on X: the Punnett difference is:",
         "sons get their single X from mom; autosomal genes come from both parents equally in both sexes",
         "That is why X-linked ratios are sex-specific. Write the sex chromosomes into the square when the stem says X-linked.",
         ["autosomal genes skip fathers always", "X-linked genes cannot appear in females", "there is no difference in transmission"]),
        ("Hydrangea flower color changing with soil pH is:",
         "the same genotype producing different phenotypes in different environments",
         "Phenotype = genotype + environment + noise. The DNA did not mutate when the soil changed. AP wants that split.",
         ["a change in the plant’s DNA sequence caused by pH", "complete dominance becoming incomplete in every gene", "mitochondrial inheritance of pH"]),
        ("Siamese cat dark points on cold ears exist because:",
         "a temperature-sensitive enzyme makes pigment only in cooler tissues",
         "The genotype is the same in every skin cell. The environment (temperature) gates the enzyme. Structure–function plus environment.",
         ["different genes in the ears vs the torso", "X-inactivation of an autosomal gene", "the cat is a chimera of two species"]),
        ("Norm of reaction means:",
         "the set of phenotypes one genotype can show across environments",
         "Height vs nutrition is a classic human example. ‘The gene for height’ is incomplete language; many genes plus environment.",
         ["a Punnett square with four fixed environments", "Hardy–Weinberg p² as a phenotype", "a cladogram"]),
        ("Identical twins with different weights illustrate:",
         "environment (and maybe epigenetics) acting on the same DNA sequence",
         "Monozygotic twins start with essentially the same genotype. Divergence is powerful evidence against genetic determinism of that trait.",
         ["that twins have different nuclear genomes by definition", "Mendel’s law failing for all genes", "Y-linkage of weight"]),
        ("Phenotypic plasticity is adaptive when:",
         "one genotype can match different habitats without mutation",
         "A plant that grows sun leaves vs shade leaves from one genome can occupy a patchy forest. Plasticity is a strategy; it is not Lamarckian ‘need creates genes.’",
         ["DNA sequence changes every time the environment changes, as the definition of plasticity", "selection cannot act on plastic traits", "plasticity is only for animals with brains"]),
        ("Aa × aa, complete dominance: expected phenotypic ratio is:",
         "1 dominant : 1 recessive",
         "This is a testcross of a heterozygote. Gametes from Aa are 1/2 A and 1/2 a; the aa parent adds only a.",
         ["3:1", "9:3:3:1", "all dominant"]),
        ("Incomplete dominance of red RR × white rr gives pink Rr. F2 phenotypic ratio is:",
         "1 red : 2 pink : 1 white",
         "Heterozygote is visibly different, so the genotypic 1:2:1 is also the phenotypic ratio. Do not force 3:1 onto incomplete dominance.",
         ["3 red : 1 white", "all pink", "9:7"]),
        ("ABO blood types: Iᴬ and Iᴮ are codominant; i is recessive. A parent Iᴬi × Iᴮi can have a type O child with probability:",
         "1/4",
         "The O child must be ii: $\\frac{1}{2}\\times\\frac{1}{2}=\\frac{1}{4}$. They can also produce AB, A, and B. Four blood types from two heterozygotes.",
         ["0 because O is dominant", "1/2", "1"]),
        ("Chi-square for a 3:1 expectation with 80 purple and 20 white: $\\chi^2=(80-75)^2/75+(20-25)^2/25$. That equals:",
         "1.33",
         "$(5)^2/75 + (-5)^2/25 = 25/75 + 25/25 = 0.333+1=1.333$. df=1, critical 3.84, so the data fit 3:1 at the usual 0.05 level.",
         ["5", "25", "0"]),
        ("Epistasis: a second gene must be working for pigment to show. A 9:3:4 or 9:7 ratio often means:",
         "one gene hides or is required for another’s phenotype",
         "A dihybrid still segregates 9:3:3:1 genotypically, but phenotypes collapse. Ratios that are not 9:3:3:1 are a clue to pathway logic.",
         ["the genes are the same locus", "mitosis failed", "Hardy–Weinberg p+q≠1"]),
        ("A map: A—10—B—20—C. Expected RF between A and C if no double-crossover correction is:",
         "30%",
         "Add the intervals: 10+20=30 map units ≈ 30% recombination for small distances. Double crossovers make the observed A–C RF a bit less than 30%.",
         ["10%", "200%", "50% exactly because 10+20>50"]),
        ("A daughter is color-blind (X-linked recessive). Her father:",
         "must be color-blind, because she got one X from him and it must carry the allele",
         "She is XᵇXᵇ, so father contributed Xᵇ (and he expresses it). Mother contributed the other Xᵇ. Sons get X from mom only.",
         ["must have normal color vision", "passed a Y that carries the color-vision gene", "cannot be related"]),
        ("A mitochondrial pedigree: affected fathers have no affected children; affected mothers have all children at risk. That pattern is:",
         "cytoplasmic (maternal) inheritance, not Mendelian nuclear",
         "Do not force 3:1 onto mitochondria. The organelle’s DNA rides in the egg.",
         ["Y-linked", "autosomal dominant with complete father-to-son transmission", "X-linked recessive that skips mothers"]),
        ("Polygenic inheritance (many loci + environment) tends to produce:",
         "a continuous distribution (a bell-shaped histogram of height, for example)",
         "Each locus adds a small increment. The more loci, the smoother the curve. Environment smears it further. This is not one Punnett square of 3:1.",
         ["only two discrete pea-like classes always", "a 9:3:3:1 in humans for height", "no heritability"]),
        ("A chi-square test rejects a 9:3:3:1 model. One biological reason is:",
         "the genes are linked, so parental classes are over-represented",
         "Another reason is epistasis. The statistics tell you the model failed; biology tells you why. AP wants both layers on hard items.",
         ["Punnett squares cannot be used for two genes even if unlinked", "chi-square requires pH", "independent assortment always holds"]),
        ("Hemizygous means:",
         "only one copy is present (males for X genes), so a single recessive allele is expressed",
         "That is why X-linked recessives are not ‘hidden’ in males the way they are in XX heterozygotes.",
         ["having four copies of every autosome", "being diploid for mitochondria", "lacking a phenotype"]),
        ("A carrier screen: both parents are heterozygous for the same recessive disease (q² rare). Chance two carriers have an affected child is:",
         "1/4 for each pregnancy, independently",
         "Mendel still applies at one locus. Population frequency of carriers is a Unit 7 (2pq) question; this item is just the Punnett.",
         ["1 because they are carriers", "0 because the allele is rare", "2pq"]),
        ("Barr bodies in a 47,XXY male: how many?",
         "1",
         "n(X)−1 Barr bodies. XXY has one inactivation, like XX females. XO has zero. This links Units 4 and 5.",
         ["0", "2", "23"]),
        ("If two genes show 8% recombination, they are:",
         "linked, about 8 map units apart",
         "RF=0.08 ≠ 0.50, so not assorting independently. They could still be on a chromosome that also carries distant genes that look unlinked.",
         ["unlinked on two autosomes necessarily", "the same nucleotide", "mitochondrial and nuclear"]),
        ("Why do we testcross rather than crossing two unknown double heterozygotes to measure RF?",
         "the tester’s gametes are all recessive, so offspring phenotypes directly display the heterozygote’s gamete types",
         "A heterozygote × heterozygote hides haplotypes behind dominance. Mapping wants to see gametes.",
         ["testcrosses prevent crossing over", "RF cannot be measured in eukaryotes", "Punnett squares forbid testers"]),
        ("An environmentally induced phenotype that mimics a mutant (a phenocopy) is important because:",
         "you cannot read genotype from phenotype without more information",
         "Pedigrees assume phenotype tracks genotype. Phenocopies and incomplete penetrance are the fine print.",
         ["environment cannot affect phenotype by definition", "phenocopies change the DNA sequence to match the mutant", "Mendel’s peas had no environment"]),
        ("AP Stretch: AaBbCc, all unlinked, all needed dominant for a pathway (A_B_C_). Fraction of offspring from a self-cross that work is:",
         "27/64",
         "$(3/4)^3=27/64$. Each locus contributes an independent 3/4. This is the product rule on three genes — an FRQ favorite.",
         ["3/4", "9/16", "1/64"]),
        ("AP Stretch: χ² = 5.0, df = 1, critical value 3.84 at p=0.05. You should:",
         "reject the 3:1 (or other 1-df) model; the deviation is unlikely by chance alone",
         "χ² larger than critical → reject. Then propose linkage, mis-scoring, or a different genetic model. Do not ‘adjust the observations’ as a method.",
         ["accept the model because 5 > 3.84 means a better fit", "increase df until it fits", "conclude the data are not biological"]),
        ("AP Stretch: A three-point testcross: double-crossover classes are the rarest and tell you:",
         "which gene is in the middle (the one that ‘flipped’ relative to parentals)",
         "Compare a double-crossover haplotype to a parental: the single gene that differs in position is the middle locus. Then add the two small intervals.",
         ["that all three genes are unlinked", "the mitochondrial map", "that RF is always 50%"]),
        ("AP Stretch: A woman with an X-linked recessive son, but she has no family history, could be:",
         "a heterozygous carrier (maybe new mutation in her or her parent) — you cannot assume 2/3 without extra population assumptions, but carrier is still the main Mendelian explanation",
         "The AP-safe claim: the son got Xᵇ from mom, so mom has at least that allele in the germline. Germline mosaicism and new mutation are allowed nuances.",
         ["the son got the allele on the Y from dad", "the allele skipped the X and sat on an autosome in the son only by definition of X-linked", "fathers pass X-linked alleles to sons"]),
        ("AP Stretch: LOD scores aside, why does RF underestimate true crossover number for distant genes?",
         "double crossovers restore parental haplotype and are invisible as recombinants",
         "Observed RF = single COs minus the hidden doubles (plus higher orders). Mapping functions exist because of this. Close genes: negligible doubles.",
         ["crossing over happens only in mitosis for distant genes", "RF cannot exceed 1% by definition", "parentals are not scored"]),
        ("AP Stretch: Allele $D$ is autosomal, dominant, and male-limited (no phenotype in XX) with 80% penetrance in XY heterozygotes. An affected man ($Dd$) and an unaffected woman ($dd$) ask: what is the chance their next child is a son who shows the trait?",
         "0.20",
         "Three independent filters: P(child is XY)=$1/2$; P(inherits $D$)=$1/2$; P(shows the trait | XY and $Dd$)=$0.80$. Product: $0.5\\times0.5\\times0.80=0.20$. A daughter cannot show a male-limited phenotype even if she is $Dd$. This is not a one-step $1/2\\times$penetrance item.",
         ["0.80", "0.40", "0.50"]),
        ("AP Stretch: Two loci 6 cM apart. In 1000 meiosis, expected recombinant gametes ≈ 60. If you see 40, a reasonable next hypothesis is:",
         "interference (one crossover reduced the chance of another) or chance, testable with more data / a χ² on RF",
         "Interference is biological: crossovers are not independent along a chromosome. AP Stretch wants the mechanism, not a shrug.",
         ["the genes must be on different chromosomes if RF < map prediction", "meiosis I was skipped", "map units cannot be less than 50"]),
        ("AP Stretch: A plant self-incompatibility locus with many alleles is a case where:",
         "phenotype (pollen rejection) depends on matching alleles between pollen and pistil — not a simple 3:1",
         "Genetics can be Mendelian at the locus and still look non-Mendelian in a greenhouse because the environment of the pistil is another genotype. Heredity meets ecology of mating.",
         ["the plant has no meiosis", "all alleles are cytoplasmic", "Punnett squares require 16 boxes for one locus"]),
        ("AP Stretch: Why is a 2:1 live-born ratio a clue to an embryonic lethal allele (heterozygote × heterozygote)?",
         "the homozygous class dies, so 1:2:1 genotypes become 2 live heterozygotes : 1 wild-type homozygote",
         "Yellow mice and Manx cats are famous. Count the missing class. Chi-square against 3:1 vs 2:1 distinguishes.",
         ["lethal alleles always raise the recessive class to 3/4", "2:1 means independent assortment of two genes", "lethality converts the gene to RNA"]),
    ])


def build_unit5():
    title = "AP Biology Unit 5: Heredity"
    description = (
        "Mendelian ratios, Punnett probability, linkage maps, pedigrees, chromosomal inheritance, "
        "and environment shaping phenotype — with squares, maps, and consistent arithmetic."
    )

    c1 = concept_block(
        "1. Mendelian genetics",
        [
            "A gene is a stretch of DNA that influences a trait. Alleles are versions of that gene. A diploid cell has two alleles of each autosomal gene — one on each homolog.",
            "Genotype is the allele pair (PP, Pp, pp). Phenotype is what you see. Dominant alleles show their phenotype in the heterozygote; recessive alleles show only when both copies are recessive.",
            "Mendel’s segregation: the two alleles separate into different gametes. That is meiosis I in molecular clothing. Fertilization restores two alleles at random.",
            "Independent assortment: alleles of different genes (on different chromosomes) mix independently. A dihybrid AaBb makes four gamete types in equal numbers if the loci are unlinked: AB, Ab, aB, ab.",
            "True-breeding means homozygous. Mendel crossed true-breeding opposites, got uniform F1 heterozygotes, then F2 ratios (3:1 or 9:3:3:1) that revealed the hidden math.",
            "Incomplete dominance makes the heterozygote intermediate (red × white → pink). Codominance makes both alleles show (AB blood). Those are still Mendelian segregation — the phenotype key changed, not meiosis.",
        ],
        "Probability, maps, and Hardy–Weinberg all reuse segregation. If 3:1 is a blur, Unit 7’s 2pq will be a blur too.",
        "Write alleles as letters, circle the heterozygote, and ask: does it look like the dominant parent (complete), in between (incomplete), or like both (codominance)?",
        lesson_figure(
            punnett_svg("A", "a", "A", "a"),
            "Aa × Aa Punnett square",
            "Boxes: AA, Aa, Aa, aa. Phenotypes 3:1 if A is completely dominant; genotypes still 1:2:1.",
        )
        + solved(1, "True-breeding tall TT × dwarf tt. What are F1 genotypes and phenotypes if tall is dominant?",
                 ["All F1 are Tt.",
                  "All look tall.",
                  "The dwarf phenotype is hidden, not destroyed; it can return in F2."],
                 "all Tt, all tall", "", "Easy")
        + solved(2, "Tt × Tt. Give genotypic and phenotypic ratios (complete dominance).",
                 ["Gametes T or t from each parent.",
                  "Genotypes: 1 TT : 2 Tt : 1 tt.",
                  "Phenotypes: 3 tall : 1 dwarf."],
                 "1:2:1 genotypes; 3:1 phenotypes", "", "Medium")
        + solved(3, "Why does a 1:2:1 phenotypic ratio suggest incomplete dominance rather than complete dominance?",
                 ["Complete dominance collapses TT and Tt into one look, making 3:1.",
                  "If the heterozygote is visibly different, the three genotypes stay three phenotypes.",
                  "Segregation still happened; the dominance rule changed."],
                 "the heterozygote is its own phenotype, revealing 1:2:1", "", "Hard"),
        ("Blending away the alleles",
         "F1 looking intermediate is not blending inheritance if F2 recovers parentals. Mendel’s point: alleles stay discrete. Pink flowers still carry R and r."),
        ("Separate genotype math from appearance",
         "Always write 1:2:1 first, then apply the dominance rule to get the phenotype ratio. Skipping that step is how 3:1 gets glued onto pink flowers."),
        [
            "I can state segregation and independent assortment in meiosis language.",
            "I can compute 3:1 and 9:3:3:1 when the assumptions hold.",
            "I can tell complete, incomplete, and codominance apart.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Probability and Punnett",
        [
            "A Punnett square is a table of gametes combining at random. It does not cause genetics; it displays the sample space of fertilization.",
            "The product rule: P(A and B) = P(A)P(B) if the events are independent. Two unlinked genes, or two children, usually qualify.",
            "The sum rule: P(A or B) = P(A)+P(B) if A and B cannot both happen in the same trial (mutually exclusive genotypes of one child).",
            "A testcross (dominant phenotype × recessive) is the cleanest probability tool: offspring ratios mirror the unknown parent’s gametes.",
            "For three unlinked genes, do not draw a 64-box square on an AP clock. Use $(1/2)^n$ or $(3/4)^n$ with the product rule.",
            "Chi-square asks whether a deviation from 3:1 or 9:3:3:1 is just luck. $\\chi^2=\\sum (O-E)^2/E$. Degrees of freedom = classes − 1. If χ² exceeds the critical value, reject that genetic model and look for linkage or epistasis.",
        ],
        "Hard FRQs are probability in a paragraph. The square is training wheels; the product rule is the bicycle.",
        "Underline AND vs OR in the sentence. AND → multiply. OR (exclusive) → add. Then check independence.",
        lesson_figure(
            punnett_svg("A", "a", "a", "a"),
            "Testcross Aa × aa",
            "Offspring 1 Aa : 1 aa. Phenotypes 1:1. The tester’s column is all a, so the square reveals the heterozygote’s gametes.",
        )
        + solved(4, "Aa × Aa. Probability the first child is aa AND the second is aa?",
                 ["Each fertilization is independent.",
                  "P(aa)=1/4 each time.",
                  "$(1/4)\\times(1/4)=1/16$."],
                 "1/16", "", "Easy")
        + solved(5, "AaBb × AaBb, unlinked. Probability of an aabb child?",
                 ["P(aa)=1/4, P(bb)=1/4, independent.",
                  "Product: $1/16$.",
                  "That is the double-recessive corner of 9:3:3:1."],
                 "1/16", "", "Medium")
        + solved(6, "80 purple : 20 white vs 3:1. Compute χ² (E=75 and 25) and interpret at critical 3.84, df=1.",
                 ["$(80-75)^2/75=25/75=0.333$.",
                  "$(20-25)^2/25=25/25=1$.",
                  "$\\chi^2=1.33<3.84$, so you do not reject 3:1; luck can explain this scatter."],
                 "χ²≈1.33; fail to reject 3:1", "", "Hard"),
        ("Adding when the problem said AND",
         "‘Both children recessive’ is a product. Adding 1/4+1/4=1/2 is the probability a specific child is recessive or… no — it is a different event. Read the conjunction.",),
        ("Write E = (fraction)×n before χ²",
         "If n=100 and 3:1, E=75 and 25. Using 80 and 20 as E is circular. Observed vs expected must be different lists."),
        [
            "I can use the product and sum rules on independent fertilizations.",
            "I can read a Punnett square as a sample space of gametes.",
            "I can compute a simple χ² and compare it to a critical value.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Linked genes and recombination",
        [
            "Genes on the same chromosome are physically linked. They travel together in meiosis unless a crossover happens between them.",
            "A dihybrid in coupling (cis) has AB on one homolog and ab on the other, written AB/ab. Repulsion (trans) is Ab/aB. Parentals match those haplotypes; recombinants are the other pair.",
            "Recombination frequency RF = recombinants / total. One map unit (centiMorgan) is 1% recombination. Close genes: small RF. RF cannot exceed 50% in a simple two-point measure.",
            "Crossing over in prophase I is the mechanism. Double crossovers can look parental, so large distances are underestimated by raw RF.",
            "A three-point testcross finds gene order: the rarest class is double crossovers, and the gene that switched relative to parentals is in the middle.",
            "If RF ≈ 50%, the genes behave as unlinked — different chromosomes, or so far apart that a crossover is almost guaranteed. Independent assortment and ‘far linkage’ look the same in a two-point cross.",
        ],
        "Unit 4’s chiasmata are why Unit 5 has maps. Chromosomal inheritance (next) is what happens when whole chromosomes, not just crossovers, misbehave.",
        "Always identify parentals first (most common classes in a testcross). Everything else is recombinant math.",
        lesson_figure(
            (
                '<svg viewBox="0 0 320 120" width="100%" style="max-width:320px" role="img">'
                '<line x1="20" y1="40" x2="300" y2="40" stroke="#1d4ed8" stroke-width="8"/>'
                '<line x1="20" y1="80" x2="300" y2="80" stroke="#b91c1c" stroke-width="8"/>'
                '<circle cx="80" cy="40" r="8" fill="#fde68a"/><text x="74" y="28" font-size="12">A</text>'
                '<circle cx="80" cy="80" r="8" fill="#fde68a"/><text x="74" y="104" font-size="12">a</text>'
                '<circle cx="240" cy="40" r="8" fill="#bbf7d0"/><text x="234" y="28" font-size="12">B</text>'
                '<circle cx="240" cy="80" r="8" fill="#bbf7d0"/><text x="234" y="104" font-size="12">b</text>'
                '<path d="M160 40 L160 80" stroke="#0f172a" stroke-width="2" stroke-dasharray="4 3"/>'
                '<text x="168" y="68" font-size="11">crossover between</text>'
                "</svg>"
            ),
            "Two loci on one chromosome pair",
            "A crossover between A and B produces recombinant chromatids Ab and aB.",
        )
        + solved(7, "Testcross data: 90 AB, 88 ab, 11 Ab, 11 aB. What is RF?",
                 ["Recombinants = 11+11=22.",
                  "Total = 200.",
                  "RF=22/200=0.11 → 11 map units."],
                 "0.11 (11 cM)", "", "Easy")
        + solved(8, "Why are the AB and ab classes larger here?",
                 ["They match the parental haplotypes on the dihybrid’s chromosomes.",
                  "No crossover is needed to make them.",
                  "Ab and aB require a crossover between the genes, which is rarer if the genes are close."],
                 "they are parentals (coupling AB/ab)", "", "Medium")
        + solved(9, "Genes A–B = 10 cM, B–C = 20 cM, order A-B-C. Why might observed RF(A–C) be less than 30%?",
                 ["Single crossovers in either interval make A–C recombinants (about 30%).",
                  "A double crossover (one in each interval) swaps B but returns A and C to parental combination.",
                  "Those doubles are not counted as A–C recombinants, so observed RF underestimates the true crossover number."],
                 "double crossovers hide as parentals", "", "Hard"),
        ("Treating 18 recombinant flies as 18% without dividing by the total",
         "RF is a fraction. 18 recombinants among 200 is 9%, not 18%. Always divide by the whole count of offspring."),
        ("Star the two biggest classes",
         "Those are parentals and tell you how the alleles were arranged (cis vs trans). Mapping without that step is guessing."),
        [
            "I can compute RF and convert it to map units.",
            "I can identify parental vs recombinant classes in a testcross.",
            "I can explain why RF maxes out near 50% and why doubles hide.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Pedigrees",
        [
            "A pedigree is a family tree of a trait. Circles are females, squares are males, shading means affected. A horizontal line is a mating; a vertical line drops to children.",
            "Autosomal recessive: affected children can have two unaffected (carrier) parents; the trait can skip generations; roughly equal sexes. Cystic fibrosis pattern.",
            "Autosomal dominant: every affected child has an affected parent (unless new mutation); no skip in a fully penetrant pedigree; equal sexes. Achondroplasia pattern (with the caveat of lethality of the homozygote sometimes).",
            "X-linked recessive: more affected males; no father-to-son transmission of the X trait; an affected male’s daughters are at least carriers. Hemophilia pattern.",
            "Mitochondrial: all children of an affected mother at risk; children of an affected father not at risk through that father. Draw the cytoplasm, not the nucleus.",
            "Real pedigrees include incomplete penetrance and variable expressivity. Do not force a pea-perfect story if the data show skipped dominant phenotypes — say so.",
        ],
        "Counseling-style AP items are pedigree items. Chromosomal sex-linkage is the next concept; pedigrees are how it is diagnosed on paper.",
        "Eliminate modes: if father-to-son transmission exists, it is not X-linked recessive. If two unaffecteds had an affected child, it is not a fully penetrant dominant.",
        lesson_figure(
            _pedigree_svg(),
            "A pedigree in which unaffected parents have an affected son",
            "That pattern screams ‘recessive hiding in heterozygotes’ until proven otherwise.",
        )
        + solved(10, "Two unaffecteds have an affected daughter. Why is X-linked recessive unlikely if the father is unaffected?",
                 ["An X-linked recessive daughter must be homozygous, so she got a mutant X from dad.",
                  "Dad would then be hemizygous mutant and should be affected.",
                  "An unaffected father blocks that simple X-recessive explanation for an affected daughter."],
                 "affected X-recessive daughter requires an affected father", "", "Easy")
        + solved(11, "A trait goes from an affected mother to all her children and never from an affected father to his children. Best mode?",
                 ["Nuclear Mendelian modes usually allow father-to-child transmission.",
                  "Egg cytoplasm carries mitochondria; sperm does not (to a first approximation).",
                  "This is maternal cytoplasmic inheritance."],
                 "mitochondrial / maternal cytoplasmic", "", "Medium")
        + solved(12, "An autosomal dominant with 60% penetrance: probability a heterozygous affected person’s child with a normal (aa) mate shows the trait?",
                 ["P(inherit D)=1/2.",
                  "P(show | inherit)=0.60.",
                  "P(show)=$0.5\\times0.6=0.30$."],
                 "0.30", "", "Hard"),
        ("Diagnosing dominance because ‘lots of people are shaded’",
         "A common recessive in a small family can look busy. Use transmission rules (skipping, father-to-son, who can be a carrier), not shading density."),
        ("Try to break each mode with one arrow",
         "Find a transmission that a mode forbids. One forbidden arrow kills that hypothesis. What remains is your answer."),
        [
            "I can read standard pedigree symbols.",
            "I can distinguish autosomal recessive, autosomal dominant, X-linked, and mitochondrial patterns.",
            "I can fold incomplete penetrance into a probability.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Chromosomal inheritance",
        [
            "Genes are on chromosomes, so they inherit as chromosomes do. That is the chromosomal theory (Sutton, Boveri, Morgan). Mendel’s factors are loci on homologs.",
            "Sex linkage is chromosomal inheritance of the X or Y. In humans, XX is typically female, XY male. Sons get X from mother and Y from father.",
            "Hemizygous males express whatever allele is on their single X. That is why X-linked recessives are not masked in sons.",
            "X-inactivation randomly silences one X in each XX cell (Barr body). Heterozygous females can be mosaics (calico cats). Extra X chromosomes are inactivated too, which is why sex-chromosome aneuploidy can be milder than autosome aneuploidy.",
            "Chromosomal mutations: deletion, duplication, inversion, translocation. They can break genes or fuse them (chronic myelogenous leukemia’s BCR-ABL is a translocation story). Aneuploidy is the wrong count (Unit 4 nondisjunction).",
            "When you solve an X-linked Punnett, write the sex chromosomes every time: XᴬXᵃ × XᴬY, not just Aa × A. The Y is not a second X.",
        ],
        "Pedigrees plus karyotypes plus Punnett squares become one toolkit. Unit 6 will put the actual DNA on those chromosomes.",
        "If the stem says color blindness, hemophilia, or Duchenne, draw X and Y before you compute.",
        lesson_figure(
            punnett_svg("Xᵃ", "Y", "Xᴬ", "Xᵃ"),
            "X-linked recessive: carrier mother × affected father (example layout)",
            "Daughters get the father’s X; sons get the mother’s X. That asymmetry is the whole topic.",
        )
        + solved(13, "Carrier mother XᴴXʰ × normal father XᴴY. Probability of a color-blind son among sons? Among all children?",
                 ["Sons get mom’s X: 1/2 Xʰ, so 1/2 of sons are color-blind.",
                  "Half of children are sons, so $(1/2)\\times(1/2)=1/4$ of all children are color-blind sons.",
                  "Daughters all get dad’s Xᴴ, so none of the daughters are color-blind in this cross."],
                 "1/2 of sons; 1/4 of all children are color-blind sons", "", "Easy")
        + solved(14, "Why is father-to-son transmission of an X-linked allele impossible?",
                 ["A son’s X comes from his mother.",
                  "The father contributes Y to a son.",
                  "If you see father-to-son, look at autosomes or Y-linkage, not X."],
                 "sons get Y from dad, not X", "", "Medium")
        + solved(15, "A woman is color-blind. What must be true of her father, and what is her genotype?",
                 ["She needs two mutant X copies: XᵇXᵇ.",
                  "Father contributed one Xᵇ and is hemizygous, so he is color-blind.",
                  "Mother contributed the other Xᵇ (affected or carrier)."],
                 "father is color-blind; daughter XᵇXᵇ", "", "Hard"),
        ("Using autosomal Punnett squares for X-linked stems",
         "If you treat the father as AA or Aa, you have already missed the sex-chromosome mechanism. The letters must sit on X and Y."),
        ("Track the X like a package with a return address",
         "Label each X with mom or dad. Sons: mom’s package. Daughters: one from each. This cartoon prevents 3:1 answers on hemophilia."),
        [
            "I can explain hemizygosity and X-linked transmission.",
            "I can use Barr bodies as dosage compensation.",
            "I can connect translocations and aneuploidy to phenotype.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Environmental effects on phenotype",
        [
            "Phenotype is not a printout of genotype. Temperature, pH, nutrition, light, and other genes all modify what a genome produces.",
            "A norm of reaction is the palette of phenotypes one genotype can show across environments. Human height vs childhood nutrition is a continuous example.",
            "Some effects are dramatic switches: Siamese cat pigment enzymes that work only in the cold; hydrangea color vs soil pH. The DNA sequence in the dark ear and the pale torso can be the same.",
            "Multifactorial traits (heart disease, height, skin color) are polygenic plus environment. Histograms look bell-shaped, not 3:1.",
            "Phenotypic plasticity can be adaptive: one genome, many looks, each matching a microhabitat. That is not a mutation each time the weather changes.",
            "AP will try to trick you into ‘the environment changed the DNA.’ Gene expression can change (epigenetics, induction); the nucleotide sequence usually did not. Unit 6 is where those expression mechanisms live.",
        ],
        "Natural selection (Unit 7) sees phenotypes. If environment hides or exaggerates a genotype, selection’s target shifts. Heredity is incomplete without this caveat.",
        "Split every trait question into sequence vs expression vs environment. Only the first is a mutation in the DNA letters.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", sample_curve(lambda x: 8 + 0.9 * x, 0, 10)),
                    ("#059669", sample_curve(lambda x: 5 + 0.5 * x, 0, 10)),
                ],
                xlim=(0, 10), ylim=(0, 20), xlab="nutrition", ylab="height",
                points=[(8, 15.2, "genotype A"), (8, 9.0, "genotype B")],
            ),
            "Two genotypes, many heights",
            "Each line is a norm of reaction. At the same nutrition, A is taller than B, but both rise with food.",
        )
        + solved(16, "Hydrangeas of one cultivar are blue in acidic soil and pink in basic soil. Did the genotype mutate?",
                 ["The plants can be clones or the same cultivar (same alleles at the color-relevant genes).",
                  "Soil pH changes pigment chemistry / aluminum availability.",
                  "Phenotype changed; DNA sequence of the cultivar did not have to."],
                 "no; environment altered the phenotype", "", "Easy")
        + solved(17, "Why are identical twins a useful design for spotting environmental effects?",
                 ["They start with essentially the same nuclear genotype.",
                  "Differences that appear later (weight, some diseases) implicate environment, chance, or epigenetic drift.",
                  "Fraternal twins share environment more than random kids but only half their alleles, so the comparison is a classic geneticist’s tool."],
                 "same DNA, so differences point off-sequence", "", "Medium")
        + solved(18, "A temperature-sensitive mutation lives at 22 °C and dies at 37 °C. Interpret in structure–function language.",
                 ["The protein fold is marginally stable.",
                  "Heat supplies enough energy to unfold the mutant protein (or to inactivate an enzyme) but not the wild-type.",
                  "The genotype is constant; the environment crosses a biophysical threshold. That is why ‘permissive vs restrictive temperature’ exists in genetics labs."],
                 "environment hits a fragile protein fold", "", "Hard"),
        ("Writing ‘the gene turned into a different gene because of soil’",
         "Induction and epigenetics change expression. Mutation changes sequence. AP wants the correct layer. Soil pH is not a mutagen in the hydrangea story."),
        ("Always name the environmental variable",
         "Temperature, pH, diet, light — pick the one in the stem. Then say whether it changed folding, pigment chemistry, or growth resources. Vague ‘environment matters’ is weak."),
        [
            "I can define phenotype as genotype plus environment.",
            "I can explain norms of reaction and plasticity with examples.",
            "I can avoid claiming that the environment rewrote the DNA when only expression or chemistry changed.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Mendelian segregation, assortment, and dominance types",
            "Punnett probability, product/sum rules, and χ²",
            "Linkage, RF, and chromosome maps",
            "Pedigree modes of inheritance",
            "X-linkage, Barr bodies, and chromosomal mutations",
            "Environment, plasticity, and multifactorial traits",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Gene Expression and Regulation
# ===========================================================================

def _u6_questions():
    return _qs([
        ("DNA replication is semiconservative, meaning each daughter helix has:",
         "one old strand and one new strand",
         "Meselson–Stahl showed this with ¹⁵N labeling. Each template directs a complementary new strand by base pairing. Conservative replication (old helix stays together) was ruled out.",
         ["two new strands with the old helix discarded intact as one model that won", "four strands in a triple helix", "RNA only"]),
        ("DNA polymerase adds nucleotides to a:",
         "3′–OH, so chains grow 5′→3′",
         "Nucleoside triphosphates join at the 3′ end. That is why the two sides of a fork are leading (continuous) vs lagging (Okazaki fragments).",
         ["5′ phosphate as the only growth end", "the middle of a base", "a peptide bond"]),
        ("Helicase, primase, and ligase: the matching jobs are:",
         "unwind helix; lay RNA primer; seal nicks between Okazaki fragments",
         "DNA polymerase cannot start a chain de novo, so primase (an RNA polymerase) starts it. Ligase makes the last phosphodiester after RNA primers are replaced with DNA.",
         ["ligase unwinds; helicase glues; primase is a ribosome", "all three transcribe mRNA", "helicase translates proteins"]),
        ("Proofreading by DNA polymerase uses:",
         "3′→5′ exonuclease activity to remove a mismatched nucleotide",
         "The same enzyme that polymerizes can back up. Remaining errors are caught by mismatch repair. Mutation rate is low but not zero — Unit 7 needs those leftovers.",
         ["ribosomes rejecting tRNAs in the nucleus", "Rubisco", "crossing over in G1"]),
        ("Telomerase is needed on eukaryotic linear chromosomes because:",
         "the lagging strand cannot finish the last RNA primer’s gap, so ends would shorten",
         "Telomerase adds telomere repeats using an RNA template (a reverse transcriptase). Most somatic cells lack it; stem cells and many cancers have it.",
         ["circular bacterial chromosomes always need telomerase", "telomerase transcribes rRNA only", "Okazaki fragments exist only at telomeres"]),
        ("Transcription copies DNA into RNA using:",
         "RNA polymerase reading the template strand 3′→5′ and building RNA 5′→3′",
         "The coding (nontemplate) strand matches the RNA sequence with T/U swapped. Promoters (TATA-like elements) decide where to start. No primer is required, unlike DNA polymerase.",
         ["ribosomes reading DNA directly", "DNA ligase making mRNA", "tRNA as the template for DNA"]),
        ("Eukaryotic pre-mRNA processing includes:",
         "5′ cap, 3′ poly-A tail, and splicing out introns",
         "The cap and tail protect the message and help export/translation. Spliceosomes (snRNAs + proteins) join exons. Alternative splicing can make more than one protein from one gene.",
         ["adding Okazaki fragments to mRNA", "removing all exons as the default", "translation before capping in the cytosol as the only path in eukaryotes"]),
        ("A mutation in a splice site can:",
         "keep an intron in or skip an exon, wrecking the protein reading frame",
         "The DNA of the exon may be perfect, but the mature mRNA is wrong. That is why ‘silent’ thinking about exons-only fails.",
         ["only change telomeres", "convert the gene into a carbohydrate", "prevent DNA replication uniquely and nothing else"]),
        ("The template strand for a gene is 3′-TAC GGA-5′. The mRNA (no processing) is:",
         "5′-AUG CCU-3′",
         "RNA pairs A-U and C-G with the template. Template 3′-TAC GGA-5′ → RNA 5′-AUG CCU-3′. The coding strand would have been 5′-ATG GGA-3′.",
         ["5′-TAC GGA-3′", "3′-AUG CCU-5′ as the only correct 5′ start", "5′-ATG GGA-3′ (DNA T kept in RNA)"]),
        ("Polyadenylation happens after:",
         "the RNA is cleaved near the 3′ end; then A’s are added without a DNA template",
         "The poly-A tail is not encoded as a long T stretch in the usual way. It is added by poly-A polymerase. Length affects mRNA lifetime.",
         ["ribosomes adding A’s to proteins", "DNA polymerase adding TTTT telomeres as mRNA", "splicing adding A’s inside introns only"]),
        ("A codon is three mRNA bases. Translation starts at:",
         "AUG (methionine in eukaryotes) in the correct reading frame",
         "The ribosome (rRNA + protein) matches each codon to a tRNA anticodon. Stop codons (UAA, UAG, UGA) bind release factor, not an amino-acid tRNA.",
         ["the TATA box in the cytosol", "any UUU as a required start in all genes", "the centromere"]),
        ("tRNA is an adapter because:",
         "one end has an anticodon; the other carries the matching amino acid (charged by aminoacyl-tRNA synthetase)",
         "The genetic code’s accuracy is the synthetase’s accuracy. Wobble lets some tRNAs read more than one codon for the same amino acid.",
         ["tRNA is a ribosome subunit made of only protein", "tRNA transcribes DNA", "anticodons bind amino acids directly with no RNA"]),
        ("If mRNA is 5′-AUG-UUU-UGA-3′, the peptide is:",
         "Met–Phe, then stop (two amino acids)",
         "AUG = Met, UUU = Phe, UGA = stop. Do not add an amino acid for the stop. Reading frame is in triplets from the start.",
         ["Met–Phe–Trp", "three amino acids including a stop residue", "Phe–Met only, reading 3′→5′"]),
        ("Prokaryotic transcription and translation can couple because:",
         "there is no nucleus; ribosomes can bind mRNA while it is still being made",
         "Eukaryotes separate the processes in space and time (processing in the nucleus first). That is a structure–function difference from Unit 2.",
         ["bacteria have bigger nuclei", "eukaryotes lack ribosomes", "tRNA exists only in plants"]),
        ("A frameshift (+1 insertion) after the start codon usually:",
         "garbles every amino acid downstream and often hits a premature stop",
         "Triplet grouping is unforgiving. A 3-base insertion may add one amino acid and be milder. AP wants that distinction.",
         ["change only the first codon and then self-correct", "affect only DNA replication", "convert protein into DNA"]),
        ("The lac operon is off when lactose is absent because:",
         "the repressor protein binds the operator and blocks RNA polymerase",
         "An operon is a cluster of genes transcribed as one mRNA, common in bacteria. Lactose (allolactose) binds the repressor, so it lets go — induction.",
         ["CAP binds the operator in high glucose as the only off switch", "the operator is a eukaryotic intron", "ribosomes cannot exist in E. coli"]),
        ("Even with lactose present, lac transcription is low if glucose is high because:",
         "cAMP is low, so CAP does not activate the promoter (catabolite repression)",
         "Full expression needs two ‘yes’ signals: lactose (repressor off) AND low glucose (cAMP–CAP on). That is energy strategy at the DNA.",
         ["glucose binds the lac repressor more tightly than lactose", "high glucose destroys the lacZ gene", "operons require mitochondria"]),
        ("A repressor is negative control; CAP is positive control. Positive control means:",
         "an activator must bind for high transcription",
         "Negative = a repressor can shut the gene. Many bacterial genes use both knobs. Do not call CAP a repressor.",
         ["the gene is on chromosomes in the nucleus only", "positive means the mutation is beneficial", "activators always bind operators to block polymerase"]),
        ("trp operon is repressible: tryptophan high →:",
         "corepressor tryptophan enables the repressor to bind and shut biosynthesis",
         "You do not build amino acids you already have. Compare to lac (inducible catabolic operon). Anabolic vs catabolic logic.",
         ["trp genes turn on to make even more tryptophan as the only response", "the operator is spliced out", "CAP replaces tryptophan"]),
        ("A mutation that inactivates the lac repressor (I⁻) causes:",
         "constitutive lac expression (on even without lactose), unless other control still limits it",
         "No working repressor → operator rarely blocked. CAP still modulates level with glucose, but the classic I⁻ phenotype is ‘always on’ relative to lactose.",
         ["the operon can never turn on", "DNA replication stops", "eukaryotic splicing of lacZ"]),
        ("Eukaryotic genes are not usually in operons. Coordinated expression uses:",
         "shared transcription-factor binding sites (enhancers) on separate genes",
         "One hormone receptor can turn on a battery of genes that all have the same enhancer motif. Spatial separation is solved with proteins, not one mRNA.",
         ["one promoter transcribing 20 genes as a single bacterial-style mRNA in humans as the rule", "the Golgi copying DNA", "crossing over of mRNAs"]),
        ("Chromatin can silence a gene when it is:",
         "tightly packed (heterochromatin, often with extra methylation) so polymerase and TFs cannot access the promoter",
         "Histone acetylation generally loosens chromatin (on). DNA methylation at CpG often represses. Epigenetics is heritable through mitosis without changing the base sequence.",
         ["completely unpackaged DNA that cannot be found", "methylation of RNA polymerase’s active site only in bacteria", "Okazaki packing"]),
        ("An enhancer can work far from the promoter because:",
         "DNA loops so bound activators touch the promoter machinery (Mediator)",
         "Distance on the sequence is not distance in 3-D. This is why ‘the gene is only the coding sequence’ is too small a definition.",
         ["enhancers are tRNAs", "ribosomes loop DNA", "enhancers are found only on plasmids in humans"]),
        ("miRNAs and siRNAs regulate after transcription by:",
         "base-pairing with mRNA to block translation or trigger mRNA cutting (RNAi)",
         "The cell can turn a gene off without changing the DNA of that gene. That is expression control, not mutation.",
         ["building Okazaki fragments on mRNA", "replacing exons with telomeres", "activating CAP in the nucleus"]),
        ("Alternative splicing of one pre-mRNA can:",
         "produce protein isoforms with different exons, so one gene → several polypeptides",
         "Antibody class switching is a different DNA-level story; alternative splicing is RNA-level. Both increase diversity without more genes.",
         ["change the organism’s chromosome number", "replace transcription", "occur only in bacteria with operons"]),
        ("A restriction enzyme cuts DNA at a specific palindromic sequence, often leaving:",
         "sticky (overhanging) or blunt ends that can be ligated to matching DNA",
         "Recombinant plasmids are cut with the same enzyme as the insert so ends match. Ligase seals. That is cloning, not mitosis.",
         ["random cuts every nucleotide", "peptide bonds in proteins", "RNA primers only"]),
        ("PCR amplifies a DNA segment by cycling:",
         "denature (heat), anneal primers, extend with a heat-stable polymerase",
         "Each cycle roughly doubles the target. Primers choose which fragment. No cells required. Invented to replace slow cloning for many tasks.",
         ["transcription then translation in a thermocycler as the PCR definition", "restriction digestion without primers", "gel electrophoresis inside the polymerase"]),
        ("On an agarose gel, DNA moves toward the positive electrode because it is:",
         "negatively charged on its phosphates; small fragments run farther",
         "The gel is a sieve. A ladder of known sizes lets you read unknown sizes. Supercoiled plasmids behave differently from linear cuts — a lab nuance AP sometimes mentions.",
         ["positively charged; large fragments run farther always", "uncharged; movement is by osmosis", "attracted to RNA only"]),
        ("cDNA is DNA made from mRNA with reverse transcriptase. It is useful because:",
         "it lacks introns, so a bacterial cell can express a eukaryotic coding sequence",
         "Mature mRNA already spliced. cDNA libraries represent expressed genes of that tissue. Genomic DNA still has introns.",
         ["cDNA is RNA", "cDNA contains only promoters from the mitochondrion", "bacteria require human introns to splice"]),
        ("CRISPR-Cas9 is a programmable nuclease: a guide RNA targets Cas9 to a matching DNA sequence to:",
         "cut that DNA, after which repair can knock out or edit the gene",
         "The biology is bacterial adaptive immunity reused as a tool. Specificity is RNA–DNA pairing, the same pairing logic as the rest of this unit.",
         ["translate the guide RNA into Cas9 protein as its only step", "cut RNA polymerase as the definition of CRISPR", "replace gel electrophoresis"]),
        ("Meselson–Stahl: after one generation in ¹⁴N, a single hybrid band means:",
         "each helix is one heavy old strand + one light new strand (semiconservative)",
         "Conservative replication would have kept a heavy–heavy band plus a light–light band. Dispersive would also look hybrid at first, but later generations distinguished it. AP may stop at the one-generation killer of conservative.",
         ["DNA became RNA", "no replication occurred", "all DNA stayed heavy–heavy"]),
        ("Why are RNA primers required on the lagging strand more often than on the leading strand?",
         "each Okazaki fragment needs a new start; the leading strand needs one start per fork",
         "Same chemistry (polymerase needs a 3′-OH), different geometry of the antiparallel fork.",
         ["leading-strand polymerase can start de novo in cells", "primase only works at telomeres", "Okazaki fragments are proteins"]),
        ("A nonsense mutation introduces a stop codon. The protein is usually:",
         "truncated (short), often nonfunctional and sometimes destroyed by NMD",
         "Missense changes one amino acid. Silent changes a codon but not the amino acid (wobble/degeneracy). Frameshift scrambles. Learn the four words as a set.",
         ["longer by three amino acids always", "converted into tRNA", "unaffected because stop is ignored in eukaryotes"]),
        ("The genetic code is degenerate, meaning:",
         "multiple codons can specify the same amino acid",
         "That is why some DNA changes are silent. It is not ‘degenerate’ as an insult; it is redundancy that buffers mutation.",
         ["each codon codes three amino acids", "one tRNA carries all 20 amino acids", "there is no start codon"]),
        ("LacIˢ super-repressor that cannot bind lactose causes:",
         "the operon to stay off even when lactose is present (unless the operator is mutant)",
         "The repressor is stuck in the operator-binding shape. This is a classic partial-diploid genetics problem: Iˢ is dominant to I⁺ for repression.",
         ["constitutive expression", "loss of the Z gene from the chromosome", "CAP becoming a repressor"]),
        ("A eukaryotic gene with an enhancer 50 kb away is still the same gene’s control region because:",
         "chromosome looping brings the enhancer-bound activators to that promoter, not to every promoter",
         "Insulators/boundaries help keep enhancers from the wrong genes. Specificity is 3-D plus protein partners.",
         ["enhancers work by becoming mRNA", "50 kb away means it must control a different chromosome only", "promoters cannot bind TFs"]),
        ("Methylation patterns can be copied after replication by maintenance methyltransferases. That is epigenetic inheritance through:",
         "mitosis (and sometimes meiosis), without changing the base sequence of the gene",
         "The information is in the modification pattern, not in A vs G. Environment can influence those marks (Unit 5’s plasticity meeting Unit 6).",
         ["changing every C to T in the gene", "Okazaki ligation", "Hardy–Weinberg"]),
        ("A Northern blot (or RNA-seq) shows mRNA amount. A Western blot shows protein. If mRNA is high but protein is low, regulation may be:",
         "translational block or rapid protein degradation (post-transcriptional / post-translational)",
         "AP wants you to locate the step. Transcriptional control would have lowered the mRNA too.",
         ["only promoter mutation", "DNA replication failure", "the gene being mitochondrial by definition"]),
        ("Taq polymerase is used in PCR because:",
         "it survives the 95 °C denaturation step that would ruin a typical mesophile polymerase",
         "A thermophile enzyme’s structure (Unit 3 optima) is why PCR is practical. Biology of hot springs, tool of molecular genetics.",
         ["it transcribes RNA at 95 °C as PCR’s definition", "it ligates sticky ends", "it is a restriction enzyme"]),
        ("A plasmid cloning vector needs an origin of replication and usually:",
         "a selectable marker (antibiotic resistance) and a cloning site in a reporter (like lacZ)",
         "You force bacteria to keep the plasmid (antibiotic) and you see which colonies took the insert (blue-white screening). Without selection, plasmids are lost.",
         ["a centromere and telomeres as in human artificial chromosomes for every E. coli plasmid", "introns required for bacterial splicing", "mitochondrial DNA only"]),
        ("Sticky ends from EcoRI on vector and insert anneal because:",
         "the overhangs are complementary single-stranded DNA",
         "Hydrogen bonding holds them; ligase makes covalent backbone bonds. Same base-pairing as the rest of life.",
         ["the ends are lipids", "ribosomes join DNA", "EcoRI adds amino acids"]),
        ("If you run PCR products and see a band at the expected size plus a primer-dimer at the bottom, the dimer is:",
         "tiny primer–primer products that ran farther because they are small",
         "Gel reading: distance ↔ size. Extra small bands are often artifacts, not extra genes.",
         ["genomic DNA stuck in the well as a dimer by definition", "protein", "the largest possible amplicon"]),
        ("A knockout mouse using CRISPR to break both alleles of a gene tests:",
         "loss-of-function: what phenotype appears when that protein is gone",
         "That is the geneticist’s gold standard for ‘what does this gene do,’ with the caveat of compensation and off-target cuts.",
         ["gain-of-function of an oncogene necessarily", "Hardy–Weinberg equilibrium of the cage", "operon induction in the mouse gut only"]),
        ("Why does a silent mutation in a splice-site-adjacent exon sometimes still cause disease?",
         "it can destroy an exonic splicing enhancer, so the exon is skipped",
         "‘Silent’ is about the codon table, not about splicing codes. Sequence can mean more than amino acids.",
         ["silent mutations always change the amino acid", "exons cannot affect splicing", "tRNA ignores exons"]),
        ("In prokaryotes, the Shine–Dalgarno sequence helps the ribosome:",
         "find the start AUG on the mRNA",
         "Eukaryotes use the 5′ cap and scanning instead (usually). Initiation differences are a regulation point (IRES, uORFs) on hard items.",
         ["splice introns", "add the poly-A tail", "unwind DNA ahead of helicase"]),
        ("Catabolite repression saves energy by:",
         "not fully inducing lac (and similar operons) when a better sugar (glucose) is already present",
         "Fitness again: do not spend ATP and amino acids building lactose machines you do not need. Unit 3’s strategy, Unit 6’s mechanism.",
         ["destroying glucose genes when lactose appears", "splicing out lacZ", "methylating the operator with histone H1 in E. coli as the standard story"]),
        ("AP Stretch: A mutant DNA polymerase lacks proofreading but mismatch repair is intact. Mutation rate will:",
         "rise, because more mismatches leave the fork for MMR to catch, and MMR is not perfect",
         "Layers of fidelity: base pairing, proofreading, MMR. Removing a layer raises the residual error rate. Cancer mutator phenotypes hit these layers.",
         ["fall to zero because MMR is better than proofreading in every case", "be unchanged because ligase proofreads", "rise only in RNA genes"]),
        ("AP Stretch: An intron mutation creates a new AG splice acceptor. The likely protein effect is:",
         "inclusion of extra amino acids or a frameshift, depending on the inserted length mod 3",
         "Cryptic splice sites are a real disease mechanism. Count nucleotides in the extra bit: multiple of 3 vs not.",
         ["no effect because introns are never in DNA", "the promoter moving to the Golgi", "telomerase splicing the intron"]),
        ("AP Stretch: Partial diploid I⁺ Oᶜ Z⁻ / I⁻ O⁺ Z⁺. Predict β-galactosidase without lactose vs with lactose (ignore CAP).",
         "off without lactose (repressor from I⁺ can act in trans on both operators except Oᶜ is cis-acting — here Z⁺ is with O⁺, so repressed until lactose); on with lactose",
         "Oᶜ is cis-acting (only the Z on that DNA). I product is trans-acting. Z⁺ sits on the O⁺ chromosome, so I⁺ repressor (from either I) can turn it off until inducer. I⁻ on the other chromosome does not wreck I⁺. This is the AP operon chess problem.",
         ["always on because of I⁻", "always off because of Z⁻ on one copy, which poisons the cell’s only enzyme", "no transcription because diploids cannot have operons"]),
        ("AP Stretch: You want to express human insulin in E. coli. Why start from cDNA rather than the genomic insulin gene?",
         "E. coli cannot splice out human introns; cDNA is the already-spliced coding sequence",
         "You still need a bacterial promoter and often a fusion/secretion trick. The intron problem is the first AP-level blocker.",
         ["cDNA contains the human promoter that E. coli prefers", "genomic DNA is RNA", "bacteria require human histones to transcribe"]),
        ("AP Stretch: A miRNA matches an mRNA imperfectly in animals, usually causing:",
         "translational repression and/or mRNA destabilization rather than a perfect siRNA-style cut",
         "Perfect complementarity (more typical of siRNA) leads to cleavage. Imperfect matches still regulate — that is why one miRNA has many targets. Networks, not one gene.",
         ["activation of CAP", "DNA ligation of the mRNA into the genome as the usual outcome", "conversion of mRNA into tRNA"]),
        ("AP Stretch: ChIP-seq shows a transcription factor bound 80 kb from a gene that still depends on that TF. The mechanistic link is:",
         "a chromatin loop (and often cohesin) pairing that site with the promoter, tested nowadays by Hi-C",
         "Distance in kb is not an argument against regulation. The old AP enhancer story plus modern 3-D genome.",
         ["the TF must have been a restriction enzyme cutting at 80 kb", "80 kb away means the TF is irrelevant", "ribosomes bind enhancers to transcribe"]),
        ("AP Stretch: PCR contamination control: a negative control with no template should show:",
         "no band; a band means primer contamination or leftover amplicon in reagents",
         "Experimental design (Unit 8) applied to a molecular protocol. Controls are not optional because PCR is exponential — one molecule becomes a lie you can see on a gel.",
         ["a stronger band than the sample as proof of enzyme quality", "smeared genomic DNA always", "protein"]),
        ("AP Stretch: A eukaryotic activator is fused to a bacterial repressor’s DNA-binding domain (domain swap). If transcription of a reporter rises, you showed:",
         "activation is modular — the activation domain can work when aimed at a new DNA site",
         "Classic modular-domain logic (Ptashne-style). Structure (two domains) → function (bind DNA vs recruit machinery).",
         ["bacteria have nuclei", "repressors cannot bind DNA", "the reporter was translated without mRNA"]),
        ("AP Stretch: Why does a mutation in a tRNA anticodon (suppressor tRNA) sometimes restore function to a gene with a stop mutation?",
         "the tRNA now inserts an amino acid at that stop codon, completing a (mutant) protein",
         "Suppression is a second-site rescue. Fitness cost: some real stops may also be read through. AP Stretch loves two-locus molecular rescue.",
         ["the stop codon is removed from the DNA by the tRNA as a restriction enzyme", "ribosomes ignore all stops in the cell forever with no cost", "the tRNA becomes mRNA"]),
    ])


def build_unit6():
    title = "AP Biology Unit 6: Gene Expression and Regulation"
    description = (
        "Replication, transcription, translation, bacterial and eukaryotic regulation, "
        "and biotechnology tools — with fork, operon, and pairing diagrams."
    )

    c1 = concept_block(
        "1. DNA replication",
        [
            "Before a cell divides, it must copy its DNA. Replication is semiconservative: each new double helix keeps one parental strand as a template for a new complementary strand.",
            "Base pairing is the copying rule. A opposite T, G opposite C. Hydrogen bonds (Unit 1) make the rule accurate enough to start; enzymes make it accurate enough for a genome.",
            "DNA polymerase can add nucleotides only to a 3′–OH, so synthesis is always 5′→3′. Because strands are antiparallel, one side of the fork (leading) is continuous and the other (lagging) is made as Okazaki fragments.",
            "Helicase unwinds. Single-strand binding proteins keep strands apart. Primase lays a short RNA primer because DNA polymerase cannot start a chain from nothing. Ligase seals the last nick after primers are replaced with DNA.",
            "Proofreading (3′→5′ exo) plus mismatch repair keep the error rate tiny. The leftover mutations are the raw material of Unit 7.",
            "Linear eukaryotic chromosomes have an end-replication problem: the last lagging primer leaves a gap. Telomerase, in cells that have it, extends telomeres so chromosomes do not shrink every cycle.",
        ],
        "Meiosis, cancer, PCR, and mutation all assume this geometry. If 5′→3′ is shaky, every later tool in this unit will feel like trivia.",
        "At a fork, draw arrows only 5′→3′. The lagging strand will look backward relative to fork movement — that discomfort is the lesson.",
        lesson_figure(
            _fork_svg(),
            "A replication fork",
            "Green: leading strand, one continuous 5′→3′ arrow. Orange: Okazaki pieces on the lagging strand.",
        )
        + solved(1, "Why does the lagging strand need many primers while the leading strand needs one per fork?",
                 ["Polymerase only grows 5′→3′.",
                  "As the fork opens, the lagging template exposes new 5′ ends that require a fresh 3′-OH start.",
                  "The leading template stays in the correct orientation for continuous growth."],
                 "each Okazaki fragment needs its own 3′-OH start", "", "Easy")
        + solved(2, "Meselson–Stahl grew ¹⁵N DNA then switched to ¹⁴N. After one generation there was one intermediate-density band. Which model died?",
                 ["Conservative replication would keep a heavy parental helix and make a fully light new helix — two bands.",
                  "One hybrid band matches one old strand + one new strand.",
                  "Semiconservative replication survived that first generation test."],
                 "conservative replication is incompatible with one hybrid band", "", "Medium")
        + solved(3, "A cell lacks ligase. What DNA feature accumulates, and which strand is hit harder?",
                 ["Nicks remain between Okazaki fragments after primers are processed.",
                  "The lagging strand is a chain of fragments; the leading strand has far fewer joints.",
                  "The chromosome can break at those nicks — lethal if unrepaired."],
                 "nicked lagging-strand DNA", "", "Hard"),
        ("Drawing both new strands growing toward the 5′ end of the new chain",
         "If your arrows point the wrong way, Okazaki fragments will appear on the wrong side. Always label 5′ and 3′ on the templates first."),
        ("Template first, then the new 5′→3′ arrow",
         "Students start with the new strand and invent 3′→5′ synthesis. The enzyme does not do that in cells. Fight the drawing, not the chemistry."),
        [
            "I can explain semiconservative replication and 5′→3′ synthesis.",
            "I can assign helicase, primase, polymerase, and ligase a job.",
            "I can describe leading vs lagging strands and telomeres.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Transcription and RNA processing",
        [
            "Transcription is DNA → RNA. RNA polymerase binds a promoter, unwinds a short stretch, and builds RNA 5′→3′ complementary to the template strand. Uracil replaces thymine.",
            "The coding strand has the same sequence as the RNA (T/U). When a question gives ‘the nontemplate strand,’ write the RNA by copying and swapping T for U.",
            "In bacteria, the mRNA can be used at once. In eukaryotes, the primary transcript (pre-mRNA) is processed in the nucleus: a 5′ cap, a poly-A tail, and splicing to remove introns.",
            "Splicing is not junk removal only. Alternative splicing chooses different exon combinations so one gene can encode several protein variants — a reason humans have more proteins than a naive gene count suggests.",
            "The cap and tail are tickets for export and translation and they slow degradation. Short-lived mRNAs are often short-tailed or decapped on purpose (regulation).",
            "A promoter mutation can silence a gene that has a perfect coding sequence. A splice-site mutation can ruin a protein whose exons look healthy. Location of the mutation matters as much as the letter that changed.",
        ],
        "Translation only sees mature mRNA. If you skip processing, eukaryotic gene-expression FRQs fall apart.",
        "Convert every DNA sequence to RNA with pairing, then ask: is this still pre-mRNA, or already spliced?",
        lesson_figure(
            _transcription_pair_svg(),
            "DNA template pairs with RNA (A·U)",
            "G still pairs with C; A in DNA templates U in RNA. T on DNA still pairs A on RNA.",
        )
        + solved(4, "Coding strand 5′-ATG CCC TAA-3′. What is the mRNA (unspliced, same segment)?",
                 ["Coding strand matches RNA except T→U.",
                  "mRNA 5′-AUG CCC UAA-3′.",
                  "UAA is a stop codon later in translation."],
                 "5′-AUG CCC UAA-3′", "", "Easy")
        + solved(5, "List three eukaryotic processing steps and one job for each.",
                 ["5′ cap: export, ribosome recognition, stability.",
                  "Splicing: remove introns, join exons (and maybe choose isoforms).",
                  "Poly-A tail: stability, export, efficient translation."],
                 "cap, splice, tail — stability/export/isoforms", "", "Medium")
        + solved(6, "A G-to-A change in an intron 2 bp from the intron–exon junction causes disease, but the exon sequence is unchanged. Why can the protein still fail?",
                 ["Splice sites are partly inside introns.",
                  "The spliceosome may miss the real junction and keep intron RNA or skip the exon.",
                  "The reading frame of the mature mRNA changes even though the exon DNA ‘looks fine’ in a coding-only view."],
                 "splice-site failure alters mature mRNA", "", "Hard"),
        ("Transcribing both DNA strands of one gene as mRNA in the same direction",
         "One gene has one template strand. The other strand is coding. Bidirectional transcription of two different genes is a different story."),
        ("Write T→U on the coding strand rather than pairing twice",
         "If they give the template, pair it. If they give the coding strand, copy with T→U. Mixing those recipes inverts the sequence."),
        [
            "I can distinguish template vs coding strands and write mRNA.",
            "I can describe capping, tailing, and splicing.",
            "I can predict the effect of a splice-site mutation.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Translation",
        [
            "Translation is mRNA → protein. The genetic code maps each three-base codon to an amino acid (or to stop). It is nearly universal, which is why a human gene can be expressed in bacteria if you solve the intron problem.",
            "Initiation in eukaryotes: the small ribosomal subunit, with initiator tRNA-Met, usually binds the cap and scans to the first AUG. Prokaryotes use a Shine–Dalgarno sequence near the start.",
            "Elongation: the ribosome has A, P, and E sites. A charged tRNA with the right anticodon enters A; a peptide bond forms; the ribosome translocates. rRNA, not a protein, is the peptidyl transferase — a ribozyme.",
            "Termination: a stop codon recruits release factor. The polypeptide leaves and folds (Unit 1 tertiary structure). Chaperones often help.",
            "The code is degenerate: several codons per amino acid. Silent mutations exploit that. A frameshift (+1 or −1) does not.",
            "Coupled transcription-translation in bacteria is why operons can make one polycistronic mRNA that yields several proteins in a row. Eukaryotes usually translate one cistron per mRNA.",
        ],
        "Missense, nonsense, and frameshift language shows up on every AP paper. Translation is where those words become amino acids.",
        "Split the mRNA into triplets from the start codon before you touch a codon table. A one-base slip is a frameshift in your work, not in the cell.",
        lesson_figure(
            (
                '<svg viewBox="0 0 340 130" width="100%" style="max-width:340px" role="img">'
                '<rect x="20" y="40" width="70" height="40" fill="#dbeafe" stroke="#1e3a8a"/>'
                '<text x="55" y="64" text-anchor="middle" font-size="12">AUG</text>'
                '<rect x="100" y="40" width="70" height="40" fill="#dbeafe" stroke="#1e3a8a"/>'
                '<text x="135" y="64" text-anchor="middle" font-size="12">UUU</text>'
                '<rect x="180" y="40" width="70" height="40" fill="#fecaca" stroke="#b91c1c"/>'
                '<text x="215" y="64" text-anchor="middle" font-size="12">UGA</text>'
                '<text x="55" y="100" text-anchor="middle" font-size="11">Met</text>'
                '<text x="135" y="100" text-anchor="middle" font-size="11">Phe</text>'
                '<text x="215" y="100" text-anchor="middle" font-size="11">stop</text>'
                "</svg>"
            ),
            "Reading frame in triplets",
            "AUG starts Met. UUU is Phe. UGA stops — no amino acid for the stop codon.",
        )
        + solved(7, "mRNA 5′-AUG GGA UAA-3′. Amino-acid sequence?",
                 ["AUG = Met (start).",
                  "GGA = Gly.",
                  "UAA = stop, so the peptide is Met–Gly."],
                 "Met–Gly", "", "Easy")
        + solved(8, "A mutation changes UAC (Tyr) to UAA. Name the mutation class and the protein effect.",
                 ["UAA is stop, so this is a nonsense mutation.",
                  "Translation ends early; the protein is truncated.",
                  "Function is usually lost unless the stop is very near the true end."],
                 "nonsense; truncated polypeptide", "", "Medium")
        + solved(9, "An insertion of one base right after AUG. Why is this usually worse than a substitution of one base?",
                 ["Substitution changes at most one codon (missense or silent or nonsense).",
                  "A +1 insertion shifts every downstream triplet.",
                  "The protein is random after that point and often hits a premature stop — a frameshift."],
                 "frameshift scrambles the rest of the chain", "", "Hard"),
        ("Adding an amino acid for the stop codon",
         "Stop is a release-factor binding site, not a 21st amino acid. Met–Phe–Stop is not a tripeptide."),
        ("Frame from AUG, not from the first letter they printed",
         "If the sequence includes 5′ UTR bases before AUG, those are not translated. Find the start, then triplet-count."),
        [
            "I can translate a short mRNA using start and stop.",
            "I can classify silent, missense, nonsense, and frameshift mutations.",
            "I can describe tRNA as an adapter and the ribosome as the catalyst.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Gene regulation in prokaryotes",
        [
            "Bacteria live in boom-and-bust chemistry. They cannot afford to transcribe every gene all the time. Regulation is mostly at transcription initiation — the cheapest step to shut.",
            "An operon is a promoter + operator + a set of genes on one mRNA. The lac operon encodes lactose-use enzymes. The trp operon encodes tryptophan-building enzymes.",
            "Lac is inducible and catabolic. No lactose: repressor binds operator, polymerase is blocked. Lactose present: allolactose takes the repressor off. That is negative control relieved by inducer.",
            "Glucose still matters. Low glucose raises cAMP; cAMP–CAP binds near the promoter and helps polymerase (positive control). High glucose: little CAP help. Full lac expression is lactose yes AND glucose no.",
            "Trp is repressible and anabolic. High tryptophan: trp is a corepressor that lets the repressor bind. Why build an amino acid you are swimming in?",
            "Mutations taught the logic: I⁻ constitutive, Oᶜ cis-constitutive, Iˢ super-repressor. The repressor protein can act on both copies (trans); the operator only controls the genes on its own DNA (cis).",
        ],
        "This is the model AP uses to test ‘how does a cell match gene expression to environment?’ Eukaryotes use more parts, same idea.",
        "For lac, write two checkboxes: repressor off? CAP on? High expression needs both checks.",
        lesson_figure(
            _operon_svg(),
            "The lac operon layout",
            "P = promoter, O = operator (repressor’s parking spot), ZYA = enzyme genes on one mRNA.",
        )
        + solved(10, "No lactose, glucose present. Is lac on or off, and which protein is on the operator?",
                 ["No lactose → repressor is free to bind O.",
                  "Polymerase is blocked.",
                  "CAP is also inactive (glucose high), but the repressor alone is enough to keep the operon off."],
                 "off; lac repressor on the operator", "", "Easy")
        + solved(11, "Lactose present, glucose absent. Why is expression highest?",
                 ["Inducer removes repressor (operator clear).",
                  "Low glucose → cAMP–CAP activates the promoter.",
                  "Both negative control is lifted and positive control is on."],
                 "repressor off and CAP on", "", "Medium")
        + solved(12, "Explain cis vs trans with Oᶜ Z⁺ / O⁺ Z⁻.",
                 ["Oᶜ only unlocks the Z gene on its own DNA, so Z⁺ is constitutively expressed from that molecule.",
                  "The Z⁻ gene cannot make functional enzyme no matter how open its operator is.",
                  "Operators do not float over to the other chromosome; repressors (proteins) can."],
                 "Oᶜ is cis to Z⁺; enzyme is made constitutively from that copy", "", "Hard"),
        ("Thinking lactose turns genes on by mutating them",
         "The DNA sequence of ZYA does not change when lactose arrives. A protein changes shape and leaves the operator. That is regulation, not evolution (yet)."),
        ("Two checkboxes for lac",
         "Lactose? Glucose? Draw them on the FRQ. Missing CAP is the usual half-answer that loses a point."),
        [
            "I can define operon, operator, repressor, and inducer.",
            "I can explain lac’s dual control by lactose and glucose.",
            "I can contrast inducible lac with repressible trp.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Eukaryotic regulation",
        [
            "Eukaryotic DNA is wrapped on nucleosomes. Tight packing (heterochromatin) hides promoters. Loose packing (euchromatin), often with histone acetylation, lets transcription factors in.",
            "DNA methylation (usually CpG) tends to silence. These marks can be copied after replication, so two daughter cells can ‘remember’ to be liver vs neuron without changing sequence — epigenetic memory through mitosis.",
            "General transcription factors plus RNA polymerase sit at the promoter. Specific transcription factors bind enhancers, which may be far away, and loop to the promoter via Mediator. Combinations of TFs give cell-type specificity.",
            "After transcription, eukaryotes still regulate: alternative splicing, mRNA export, miRNA silencing, and protein degradation (ubiquitin–proteasome). A gene can be ‘on’ as RNA and still not make a stable protein.",
            "Coordinated genes share enhancer motifs, not a bacterial operon mRNA. One steroid receptor can therefore turn on a suite of genes.",
            "Development is regulation in time: morphogen gradients set TF combinations, which set more TFs (a cascade, Unit 4-style) until a cell’s fate is locked by chromatin as well as by ongoing signals.",
        ],
        "Cancer, development, and cloning ethics items all reduce to ‘which layer of expression broke?’ Sequence vs chromatin vs splicing vs miRNA.",
        "Name the layer: chromatin, enhancer, promoter, splicing, mRNA stability, translation, protein life. Then pick the molecule that acts there.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 1 + 10 / (1 + math.exp(-0.8 * (x - 6))), 0, 12))],
                xlim=(0, 12), ylim=(0, 12), xlab="activator concentration", ylab="transcription",
                points=[(6, 6.0, "cooperative switch")],
            ),
            "A steep transcriptional response to an activator",
            "Cooperative binding at enhancers can make a switch-like on/off, useful in development.",
        )
        + solved(13, "Why does histone acetylation often increase transcription?",
                 ["Acetyl groups neutralize positive charges on histone tails.",
                  "DNA (negative) is held less tightly, chromatin opens.",
                  "TFs and polymerase can occupy the promoter."],
                 "looser chromatin, better access", "", "Easy")
        + solved(14, "A miRNA complementary to an mRNA’s 3′ UTR is added. Predict mRNA/protein.",
                 ["The miRNA–RISC complex binds the mRNA.",
                  "Translation drops and/or the mRNA is destabilized.",
                  "Protein falls; the gene’s DNA is unchanged."],
                 "less protein (and often less mRNA); DNA unchanged", "", "Medium")
        + solved(15, "Two cell types have the same genome. Why does only muscle transcribe myosin?",
                 ["Muscle has a set of TFs (and open myosin enhancers) that other cells lack.",
                  "Other cells may pack the locus as heterochromatin or lack the activator combination.",
                  "Same sequence, different regulatory state — the definition of differentiation."],
                 "cell-specific TFs/chromatin at the myosin locus", "", "Hard"),
        ("Claiming eukaryotes have operons as the main coordination tool",
         "A few exist as exceptions, but the AP default is: separate genes, shared TF motifs, chromatin. Do not paste lac onto a human chromosome without comment."),
        ("Layer the answer",
         "If mRNA is present but protein is not, do not blame the promoter. Move downstream: translation or degradation. Match the data to the layer."),
        [
            "I can connect chromatin marks to on/off transcription.",
            "I can explain enhancers, looping, and cell-type TFs.",
            "I can place miRNA and alternative splicing on the expression timeline.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Biotechnology tools",
        [
            "Biotechnology uses enzymes we already met, aimed by human-chosen sequences. Restriction enzymes cut at palindromes. Ligase pastes. Reverse transcriptase makes cDNA from mRNA. Heat-stable polymerase runs PCR.",
            "PCR: 95 °C separates strands, cooler temperatures anneal primers, ~72 °C extends. n cycles can theoretically give 2ⁿ copies of the flanked region. Primers are the specificity.",
            "Gel electrophoresis sorts DNA by size in an electric field. Phosphates make DNA negative, so it runs to the anode. Small pieces thread the gel faster. A ladder is the ruler.",
            "Plasmids are extra-chromosomal circles in bacteria. As vectors they need an origin, a selectable marker, and a place to paste insert DNA. Transformation puts the plasmid into a cell.",
            "cDNA clones skip introns, so bacteria can make a eukaryotic protein. Insulin was the famous medical product. Expression still needs a prokaryotic promoter in front of that cDNA.",
            "CRISPR-Cas9 is a nuclease steered by a guide RNA. A cut can knock a gene out (error-prone repair) or, with a template, edit a base. Off-target cuts are the practical risk. Pairing specificity is the same idea as the rest of this unit.",
        ],
        "AP asks you to choose a tool for a job: amplify, cut, separate, clone, edit, or measure expression. The tools are not a separate science — they are replication and restriction in a tube.",
        "Match the verb: amplify → PCR; separate by size → gel; copy mRNA to DNA → reverse transcriptase; cut at a sequence → restriction enzyme; edit a gene → CRISPR (or older homologous recombination).",
        lesson_figure(
            xy_graph(
                curves=[("#0f172a", [(1, 2), (2, 4), (3, 8), (4, 16), (5, 32)])],
                xlim=(0, 6), ylim=(0, 36), xlab="PCR cycle", ylab="copies (ideal)",
                points=[(5, 32, "2^5=32")],
            ),
            "Ideal PCR doubling",
            "Each cycle copies the target again. Real PCR plateaus when primers or polymerase saturate, but the principle is exponential.",
        )
        + solved(16, "You have a tiny crime-scene DNA sample and need millions of copies of one locus. Tool?",
                 ["The amount is too small to clone by cutting and seeing on a gel first.",
                  "PCR amplifies a primer-defined region exponentially.",
                  "Then you can gel-check or sequence the product."],
                 "PCR", "", "Easy")
        + solved(17, "A gel shows bands at 200 bp and 800 bp. Which ran farther, and why does DNA move at all?",
                 ["The 200 bp fragment is smaller so it ran farther toward the positive electrode.",
                  "DNA’s phosphate backbone is negative.",
                  "The gel matrix sieves by size."],
                 "200 bp farther; DNA is negative", "", "Medium")
        + solved(18, "Design the shortest path to make human insulin in E. coli from a human pancreas mRNA pool.",
                 ["Isolate mRNA, reverse-transcribe to cDNA (no introns).",
                  "Clone the insulin cDNA into a plasmid with a bacterial promoter and selectable marker.",
                  "Transform E. coli, select, induce expression, purify the peptide.",
                  "Genomic DNA would have failed at splicing."],
                 "cDNA → expression plasmid → transform bacteria", "", "Hard"),
        ("Thinking a gel sorts by charge sign only, ignoring size",
         "All ordinary DNA fragments are negative. Size is why they separate. Proteins on SDS-PAGE are a different lab story (also sieving, after SDS makes them negative)."),
        ("Name the enzyme that does the chemistry",
         "PCR without naming a polymerase, cloning without ligase, cDNA without reverse transcriptase — those answers feel hollow to a grader. Put the protein in the sentence."),
        [
            "I can outline PCR cycles and why Taq is used.",
            "I can read a DNA gel (charge and size).",
            "I can justify cDNA for eukaryotic genes in bacteria and state what CRISPR cuts.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Semiconservative 5′→3′ replication and the fork",
            "Transcription, cap/tail/splice",
            "Translation, the code, and mutation classes",
            "lac/trp operon logic in bacteria",
            "Chromatin, enhancers, and eukaryotic layers of control",
            "PCR, gels, plasmids, cDNA, and CRISPR",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Natural Selection
# ===========================================================================

def _u7_questions():
    return _qs([
        ("Natural selection requires variation that is:",
         "heritable and that causes differences in survival or reproduction",
         "Darwin’s logic: more are born than can last; individuals differ; some differences are inherited; those that help leave more offspring become common. Without heritability, the next generation does not keep the trait.",
         ["acquired in one lifetime and never encoded in DNA, as Lamarck’s complete theory", "always caused by the organism’s need creating new genes on purpose", "only the result of genetic drift in infinite populations"]),
        ("A fossil series showing horses’ teeth changing over time is evidence of:",
         "descent with modification (the pattern), which selection can explain as a process",
         "Evidence includes fossils, biogeography, homology, vestigial structures, and DNA. Selection is one mechanism; drift, mutation, and migration also change populations.",
         ["individuals stretching their teeth and passing stretched teeth as the only mechanism", "a cladogram of operons", "Hardy–Weinberg being true in that fossil bed"]),
        ("Homologous structures (a bat wing and a human arm) indicate:",
         "shared ancestry; the bones were modified for different jobs",
         "Analogy (insect wing vs bird wing) is similar function without the same underlying bones — often convergent evolution. AP wants homology vs analogy straight.",
         ["that bats are insects", "no common ancestor possible", "identical DNA sequences in all genes always"]),
        ("Artificial selection (dog breeds, crops) is evidence that:",
         "heritable variation can be sorted to change a population’s mean trait",
         "Humans play the role of the environment’s filter. Darwin used this as an analogy for nature’s filter. It does not prove nature has a breeder; it shows the genetic raw material exists.",
         ["species cannot change", "only acquired traits matter", "mutation does not occur in crops"]),
        ("Fitness in evolutionary biology means:",
         "relative reproductive success, not gym strength",
         "A sterile champion bodybuilder has fitness zero. A small camouflaged moth that leaves more offspring is fitter. Unit 3 used the same word for energy strategies; here it is reproductive.",
         ["maximum ATP in mitochondria as the definition", "being the largest animal in the clade always", "having the most mutations"]),
        ("Hardy–Weinberg equilibrium is a null model: allele frequencies stay put if:",
         "no mutation, no migration, no selection, random mating, and a very large population (no drift)",
         "If a real population fails HW, at least one assumption is false. HW is not a claim that nature is always still; it is a baseline.",
         ["selection is strong and the population is size 2", "mutation rate is 100% per generation", "mating is only among identical phenotypes by force"]),
        ("If q² = 0.09 for a recessive phenotype, q is 0.3 and the heterozygote frequency 2pq is:",
         "0.42",
         "p = 1−0.3 = 0.7. 2pq = 2(0.7)(0.3) = 0.42. That is the carrier frequency under HW.",
         ["0.09", "0.3", "0.7"]),
        ("A population of 100 has 36 recessive homozygotes. If HW holds, p² (dominant homozygotes) is:",
         "0.16",
         "q²=0.36, q=0.6, p=0.4, p²=0.16. About 16 AA and 48 Aa in 100 people.",
         ["0.36", "0.6", "0.48 as p²"]),
        ("Genetic drift is strongest in:",
         "small populations, where random sampling error swings allele frequencies",
         "Founder effects and bottlenecks are drift stories. Drift is not ‘selection without a reason’; it is uncorrelated with fitness. Alleles can be lost even if they are slightly beneficial.",
         ["infinite populations", "only in Hardy–Weinberg populations of infinite size", "only when mutation is zero and selection is infinite"]),
        ("A bottleneck that kills at random (a flood) mainly causes:",
         "drift: the survivors’ alleles are a random sample, diversity usually falls",
         "If the flood killed by genotype (slow runners), that would be selection. Mechanism depends on whether survival correlated with heritable traits.",
         ["only mutation creating every lost allele immediately", "Hardy–Weinberg restoration in one generation always", "speciation in a single night necessarily"]),
        ("The biological species concept says species are:",
         "groups that can interbreed and produce viable, fertile offspring (and are reproductively isolated from others)",
         "It works poorly for fossils, asexuals, and many plants. Morphological and phylogenetic species concepts exist for those cases. AP still tests BSC first.",
         ["any two organisms that look identical", "populations that share one mutation", "only organisms in the same habitat"]),
        ("Allopatric speciation begins with:",
         "a geographic barrier that stops gene flow, then divergence by selection/drift/mutation",
         "When the barrier later falls, they may no longer interbreed (reproductive isolation). The barrier did not itself mutate the DNA; it allowed independent evolution.",
         ["instant chromosome doubling as the only allopatric path", "speciation in the same lake with no barrier as the definition of allopatry", "humans choosing breeds"]),
        ("A prezygotic barrier is one that:",
         "prevents fertilization (timing, courtship, sperm-egg incompatibility, habitat)",
         "Postzygotic: hybrid inviability, sterility (mules), breakdown. Pre vs post is about whether a zygote forms.",
         ["kills hybrids after they form as the meaning of prezygotic", "is a fossil gap", "is genetic drift by definition"]),
        ("Sympatric speciation can occur via:",
         "polyploidy in plants, or habitat/mate-choice shifts without a mountain range",
         "Polyploid offspring may be instantly reproductively isolated from the diploid parent population. That is a fast, well-documented plant path.",
         ["only continents splitting", "HW equilibrium", "telomerase"]),
        ("Gene flow between two diverging populations tends to:",
         "homogenize allele frequencies and slow speciation",
         "Isolation (no gene flow) is why allopatry works. A hybrid zone with lots of gene flow can collapse a split.",
         ["always speed speciation", "create telomeres", "stop mutation"]),
        ("A shared derived character (synapomorphy) is useful on a cladogram because it:",
         "marks a clade: the ancestor where the trait arose and all descendants",
         "Shared ancestral traits (all vertebrates have DNA) do not resolve who is closer to whom. Outgroups tell you which state is derived.",
         ["is present in all life and therefore splits every node", "is an analog from convergence as the preferred character", "must be a fossil"]),
        ("On a cladogram, the closest relatives of species A are:",
         "the species that share the most recent common node with A",
         "Do not count how far right the labels sit on a poorly drawn tree. Rotate branches — sister relationships stay the same. That rotation invariance is the point of trees.",
         ["whichever name is printed closest in font size", "the outgroup always", "the species with the longest drawn branch necessarily"]),
        ("Convergent evolution produces analogous traits that can:",
         "mislead a tree if you treat them as homologies",
         "Cacti and euphorbs both look succulent but are not sister groups. Use many characters, especially DNA, to outvote convergence.",
         ["prove the two lineages share a recent node for that analog", "be the definition of a synapomorphy", "stop selection"]),
        ("A molecular clock assumes:",
         "roughly constant mutation accumulation, so more DNA differences ≈ more time since split",
         "It must be calibrated with fossils. Rate varies by gene and lineage — a limitation AP expects you to mention on hard items.",
         ["all mutations are selected identically", "drift does not occur", "species cannot split"]),
        ("Parsimony in phylogenetics prefers:",
         "the tree that requires the fewest evolutionary changes (all else equal)",
         "It is a method, not a law of nature. Convergent traits can still trick a parsimony tree. More data help.",
         ["the tree with the most changes", "random trees", "only fossil trees"]),
        ("A mass extinction is followed by:",
         "empty niches and often adaptive radiation of survivors",
         "Mammals after non-avian dinosaurs is the mascot. Background extinction is the normal trickle. Mass extinctions are rare but reset the board.",
         ["immediate return to the same species list", "the end of mutation", "Hardy–Weinberg on a global scale forcing p=q"]),
        ("Why does high genetic diversity help a species survive environmental change?",
         "some alleles may already be useful in the new conditions (standing variation)",
         "Selection can only sort existing heritable variation (plus new mutation, which is slow). A bottleneck that strips diversity is a future extinction risk.",
         ["diversity means no selection can ever occur", "all alleles are equally fit in all environments", "mutation stops in diverse populations"]),
        ("Invasive species often succeed because:",
         "they escape coevolved predators/pathogens and hit naive communities",
         "That is an ecological mechanism with evolutionary consequences (extinction of natives, hybridization). Unit 8 will add the community math.",
         ["they cannot evolve", "they always have fewer chromosomes", "HW forbids them"]),
        ("Antibiotic resistance spreads because:",
         "resistant bacteria leave more offspring when the drug is present (selection)",
         "The drug does not ‘create’ the mutation as a directed response; it filters. Plasmids can then move resistance by gene flow (horizontal transfer).",
         ["antibiotics mutate DNA toward resistance as Lamarck would predict in every cell", "eukaryotes cannot have resistance genes", "drift is the only process in huge bacterial populations under drug"]),
        ("Heterozygote advantage (sickle cell vs malaria) maintains:",
         "both alleles in the population because Aa has highest fitness in malaria zones",
         "HW frequencies then reflect selection, not the null. q is not simply √(disease frequency) if selection is this strong — but AP often still uses the √ shortcut unless they specify otherwise.",
         ["only aa as the fittest in malaria zones", "loss of A necessarily", "no phenotype differences"]),
        ("The RNA-world hypothesis suggests early life used RNA because RNA can:",
         "store information and catalyze reactions (ribozymes), including peptide-bond help today",
         "DNA is a better stable archive; proteins are better diverse catalysts. RNA sits in between — a plausible stepping stone. Membranes (protobionts) solved concentration.",
         ["RNA cannot catalyze anything, unlike DNA", "proteins came first because they store genomes", "lipids encode genes in the RNA world by definition"]),
        ("Miller–Urey-type experiments showed:",
         "organic monomers can form from inorganic gases plus energy under plausible early-Earth conditions",
         "They do not show a cell popping out. Abiotic synthesis is step one: monomers, then polymers, then packaging, then heredity. AP wants the limited claim.",
         ["that modern bacteria formed in the flask", "that oxygen-rich air is required for monomers", "that mitochondria formed first"]),
        ("A protobiont / vesicle helps origin-of-life scenarios because it:",
         "compartmentalizes molecules so reactions and genomes stay together",
         "Unit 2’s membranes, deep in time. Without a bag, your RNA and metabolites diffuse away.",
         ["creates a nucleus immediately", "is a fossil dinosaur", "stops all chemistry"]),
        ("Why is oxygenic photosynthesis a turning point in Earth’s history?",
         "O₂ accumulated, enabling aerobic respiration’s high ATP yield and an ozone shield",
         "It also caused a mass extinction of anaerobes (the oxygen catastrophe). Energetics (Unit 3) plus extinction (this unit) in one event.",
         ["O₂ poisoned all life forever", "photosynthesis removed all carbon from Earth", "aerobic respiration predates water-splitting in all models as a requirement"]),
        ("Horizontal gene transfer in early (and modern) microbes complicates trees because:",
         "genes can jump across lineages, so one tree may not fit every gene",
         "The ‘web of life’ idea. Still, a core tree of cells exists; HGT is extra edges. AP: know that HGT is real and that it blurs species boundaries in bacteria.",
         ["bacteria never exchange DNA", "only animals have HGT as the main origin of mitochondria", "cladograms cannot use DNA"]),
        ("A population of beetles has heritable color. Birds eat conspicuous beetles. After 20 years, cryptic color is common. This is:",
         "directional selection on a heritable trait",
         "Phenotype distribution shifted toward one extreme. Stabilizing would favor the mean; disruptive would favor both extremes.",
         ["Lamarckian stretching of pigment glands as the mechanism that rewrote DNA on purpose", "drift in an infinite population with no deaths", "a founder event with no predation"]),
        ("Vestigial hind-limb bones in whales support:",
         "descent from terrestrial tetrapod ancestors",
         "The structure remains after the function faded. Homology plus fossils (Ambulocetus and friends) make the case stronger than either alone.",
         ["that whales are fish", "that selection cannot reduce unused structures", "independent origin of all bones"]),
        ("Sexual selection can produce traits that look bad for survival (huge tails) because:",
         "they raise mating success enough to offset survival costs",
         "Fitness is genes in the next generation, including via mates. Natural and sexual selection can pull opposite ways.",
         ["survival is the only component of fitness", "tails cannot be heritable", "HW requires long tails"]),
        ("If p = 0.8 today and 0.5 fifty generations later with no known selection, a likely cause in a small island is:",
         "genetic drift",
         "Large shifts with no fitness correlation in small N is drift. Migration could also do it if immigrants differed. Mutation is too weak to move p that far that fast.",
         ["a change in the genetic code", "Hardy–Weinberg forcing p to 0.5", "telomere shortening of the allele"]),
        ("Reproductive isolation is the key step in speciation under the BSC because:",
         "without it, gene flow keeps the two groups as one allele pool",
         "Divergence in looks is not enough if they still mix. Many bird cryptic species look similar but do not mate.",
         ["isolation means they live on different continents by definition only", "BSC requires fossils", "isolation is the same as mutation"]),
        ("A hybrid zone that produces sterile offspring is a:",
         "postzygotic barrier reinforcing two species",
         "Selection may then favor stronger prezygotic isolation (reinforcement) so individuals do not waste gametes on sterile hybrids.",
         ["prezygotic courtship", "HW equilibrium", "an operon"]),
        ("Outgroup of (lizard, snake, bird) if you are studying amniote reptiles+birds might be a:",
         "frog (an amphibian that split earlier)",
         "The outgroup polarizes characters: whatever the frog and only some ingroup share may be ancestral. Pick a relative that is close but outside the clade of interest.",
         ["a more derived bird", "the same snake twice", "a bacterium as the only legal outgroup for amniotes"]),
        ("Two DNA sequences differ at 12 silent sites. A related pair differ at 4. If the clock holds, the first pair:",
         "split about three times as long ago",
         "12/4=3. Silent sites are often closer to neutral, so they clock better than selected amino-acid changes. Still a rough tool.",
         ["are the same species necessarily", "split 12+4=16 times more recently", "cannot be compared"]),
        ("Adaptive radiation is:",
         "many species arising quickly from one ancestor as they occupy different niches",
         "Hawaiian honeycreepers, Darwin’s finches, post-extinction mammals. Opportunity + isolation + selection.",
         ["one species staying unchanged", "extinction of all but one niche", "HW on islands forbidding new species"]),
        ("Why is ‘need’ not a mechanism of evolution?",
         "mutation is random with respect to need; selection filters afterward",
         "Bacteria did not invent resistance because they wished it. Variants existed or arose; the antibiotic made them common. This is the anti-Lamarck sentence AP wants.",
         ["organisms can rewrite any gene by effort", "selection creates specific mutations on demand in the textbook model", "drift is directed by need"]),
        ("Inbreeding increases homozygosity. That can expose:",
         "recessive deleterious alleles, lowering mean fitness (inbreeding depression)",
         "Genotype frequencies leave HW (more p² and q², less 2pq) even if allele frequencies p and q stay the same. Mating system ≠ selection, but it changes how selection sees recessives.",
         ["heterozygote frequency rising above 2pq", "mutation stopping", "species becoming outgroups"]),
        ("A founder population of 8 lizards colonizes an island. Allele B is lost. The best label is:",
         "founder-effect drift",
         "Small sample from the mainland gene pool. Later selection might act on what remains, but the loss itself can be luck.",
         ["directional selection for losing B with evidence only of N=8", "gene flow from a huge source the same year", "a molecular clock calibration"]),
        ("Clade = monophyletic group =:",
         "an ancestor and all of its descendants",
         "Paraphyletic (reptiles excluding birds) leaves some descendants out. Polyphyletic glues analogous look-alikes. AP tree-thinking is this vocabulary.",
         ["any two species that look alike", "an ancestor minus its descendants", "a habitat"]),
        ("Endosymbiosis as origin of mitochondria is both Unit 2 evidence and Unit 7 history because:",
         "a once-free bacterium became a permanent mutualist — a speciation-like merger of lineages",
         "The tree of eukaryotes has a fusion event, not only splits. HGT and endosymbiosis are extra arrows on the tree of life.",
         ["mitochondria form by budding from the nucleus in the origin story", "chloroplasts predate all cells", "endosymbiosis is a type of Hardy–Weinberg"]),
        ("Stabilizing selection on birth weight favors:",
         "intermediate phenotypes; extremes (too small/too large) have lower survival",
         "The mean may stay put while variance falls. Directional would move the mean. Read the graph’s arrows, not the vocabulary flashcard only.",
         ["both extremes over the mean", "only the largest babies in every century as stabilizing", "random loss of the mean"]),
        ("If a population is in HW at a locus, the frequency of heterozygotes is maximized when:",
         "p = q = 0.5, giving 2pq = 0.5",
         "2p(1−p) peaks at p=0.5. Rare alleles hide mostly in heterozygotes (2pq >> q² when q is small).",
         ["p=1", "q=0", "p=0.9, 2pq=0.9"]),
        ("AP Stretch: A gene has two alleles. Observed: 600 AA, 300 Aa, 100 aa. Expected HW from p=(2×600+300)/2000=0.75 would be 562.5, 375, 62.5. Excess AA and aa means:",
         "possible assortative mating, a Wahlund effect (hidden structure), or selection against heterozygotes — not HW",
         "χ² would be large. Biology: heterozygote deficit. Do not invent new p without saying you are using allele counts from the data; the point is the genotype mismatch.",
         ["perfect HW because 600+300+100=1000", "q²=0.1 proving equilibrium", "mutation from A to a in one generation creating 100 aa from nothing else"]),
        ("AP Stretch: Speciation with ongoing gene flow (e.g., hawthorn vs apple maggot flies) can still occur if:",
         "divergent selection + mate choice tied to habitat are stronger than mixing",
         "Sympatric/ecological speciation is controversial in animals but this is the AP-friendly case: the host plant is both habitat and mate-meeting place, reducing gene flow without a mountain.",
         ["gene flow is 100% and selection is zero", "HW holds at all loci including those for host choice", "a geographic ocean appears inside one tree"]),
        ("AP Stretch: A DNA tree and a morphological tree disagree at one node. The scientific move is:",
         "ask whether convergence, HGT, incomplete lineage sorting, or mis-scored characters is to blame — then add data",
         "Disagreement is a hypothesis generator, not a reason to discard trees. AP science-practice: methods have assumptions.",
         ["always throw out DNA because fossils cannot lie", "always throw out morphology because DNA cannot converge", "conclude species do not exist"]),
        ("AP Stretch: After a bottleneck, deleterious recessives may increase in frequency because:",
         "drift can raise q, and inbreeding in the small N exposes aa to selection later",
         "Conservation genetics: loss of diversity is not only ‘less pretty variation’; it is a fitness time bomb. Connect drift to inbreeding depression.",
         ["bottlenecks remove all recessives by definition", "selection cannot act after a flood", "HW immediately restores 2pq to 0.5"]),
        ("AP Stretch: Why can a molecular clock of a synonymous site run faster than of a nonsynonymous site in the same gene?",
         "silent changes are closer to neutral, so they accumulate at something like the mutation rate; amino-acid changes are often removed by purifying selection",
         "dN/dS < 1 is purifying; >1 can be positive selection. That ratio is an AP-adjacent way to detect selection on a gene.",
         ["amino acids mutate more often because ribosomes create DNA", "silent sites cannot mutate", "selection favors all amino-acid changes"]),
        ("AP Stretch: An outgroup has state 0, and two ingroup sisters have state 1. The parsimonious claim is:",
         "1 arose once on the branch leading to those sisters (a synapomorphy)",
         "If 1 also appears on a distant branch, you suspect convergence or reversal. Character mapping is tree thinking with a pencil.",
         ["state 1 is ancestral because the outgroup ‘should have been 1’", "the outgroup evolved from the ingroup", "nodes cannot have states"]),
        ("AP Stretch: Oxygenic cyanobacteria vs later aerobic eukaryotes: the delay exists because:",
         "O₂ first oxidized sinks (iron) before accumulating in air, and aerobic respiration’s complexes evolved in that new world",
         "Earth history is chemistry plus evolution. Banded iron formations are the geological receipt. Do not compress 2 billion years into ‘photosynthesis then animals the next day.’",
         ["animals photosynthesized first", "O₂ appeared after dinosaurs", "mitochondria produced the first O₂"]),
        ("AP Stretch: Frequency-dependent selection (rare morph advantage) can maintain polymorphism because:",
         "as an allele becomes common, its fitness falls (predators form a search image), so neither allele fixes easily",
         "This is selection, not HW, actively holding diversity. Scale-eating fish and some immune genes (plus heterozygote advantage) are the textbook cluster.",
         ["rare alleles always have fitness zero", "common alleles cannot be seen by predators by definition", "drift is frequency-dependent in infinite populations"]),
        ("AP Stretch: Why does the BSC fail for asexual bdelloid rotifers, and what do we use instead?",
         "they do not interbreed, so ‘potential to mate’ is empty; we use phylogenetic/morphological clusters and ecology",
         "Species concepts are tools with domains of applicability — a science-practice answer, not a gotcha that species are fake.",
         ["asexuals cannot evolve", "BSC works if we pretend they mate", "rotifers are not alive"]),
    ])


def build_unit7():
    title = "AP Biology Unit 7: Natural Selection"
    description = (
        "Darwin’s mechanism and evidence, Hardy–Weinberg math, speciation, cladograms, "
        "extinction/diversity, and origins of life — with trees and frequency calculations."
    )

    c1 = concept_block(
        "1. Darwin and evidence",
        [
            "Natural selection is a process, not a need. Individuals in a species vary. Some of that variation is heritable. More are born than the environment can support. Those whose heritable traits help them survive and reproduce leave more of those traits in the next generation.",
            "Fitness is relative reproductive success. It is not strength, speed, or ATP except insofar as those raise offspring number in that environment.",
            "Evidence of descent with modification is separate from the mechanism. Fossils show change through time. Biogeography shows related species on nearby islands. Homology (including DNA) shows shared ancestry. Vestigial structures are leftovers.",
            "Homology is similarity due to ancestry (forelimb bones). Analogy is similarity due to convergent function (wings of insects and birds). Trees must not treat analogies as shared derived traits.",
            "Artificial selection proves that sorting heritable variation can move a population far from its starting mean. Nature’s ‘breeder’ is the filter of survival and mating, not a person with a goal.",
            "Mutation supplies new alleles at random with respect to need. Selection, drift, and migration then change their frequencies. Lamarckian ‘need creates the useful gene’ is the idea AP wants you to reject.",
        ],
        "Every later Unit 7 calculation assumes this causal chain. If you skip heritability, you are describing the wrong process.",
        "Write four clauses: variation, heritability, differential reproduction, change in the population. If a choice skips one, it is not natural selection.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#94a3b8", sample_curve(lambda x: 18 * math.exp(-((x - 8) ** 2) / 10), 0, 16)),
                    ("#b91c1c", sample_curve(lambda x: 18 * math.exp(-((x - 11) ** 2) / 10), 0, 16)),
                ],
                xlim=(0, 16), ylim=(0, 20), xlab="beak depth", ylab="count",
                points=[(8, 18, "before"), (11, 18, "after drought")],
            ),
            "Directional selection on a heritable beak trait",
            "The distribution’s mean moved. Individuals did not stretch their beaks and pass stretched beaks; some beak genotypes reproduced more.",
        )
        + solved(1, "Cheetahs that run faster catch more gazelles and raise more cubs. The cubs tend to be fast. Name the process and the missing word if speed were not genetic.",
                 ["This is natural selection on speed.",
                  "The trait must be heritable.",
                  "If speed were only training, cubs would not systematically inherit it, and the population mean would not evolve."],
                 "natural selection; heritability is required", "", "Easy")
        + solved(2, "Why is a bat wing homologous to a human arm but analogous to an insect wing?",
                 ["Bat and human share a common tetrapod ancestor with the same bone layout; the job changed.",
                  "Insect wings are not modified tetrapod forelimbs; they evolved separately for flight.",
                  "Same function, different origin → analogy / convergence."],
                 "shared bones = homology; insect wing = analogy", "", "Medium")
        + solved(3, "Antibiotics are added; resistant bacteria become common. Why is ‘the antibiotic created the resistance gene in each cell that needed it’ the wrong story?",
                 ["Resistance alleles arise by mutation or gene transfer, not by the cell’s wish.",
                  "The drug kills sensitive cells, so resistant ones leave more offspring.",
                  "The population’s allele frequency changed by selection on pre-existing (or horizontally acquired) variation."],
                 "filter, not instruction; mutation is not directed by need", "", "Hard"),
        ("Equating evolution with natural selection only",
         "Evolution is a change in a population’s genetic makeup. Drift, mutation, and migration also count. Selection is the non-random part that produces adaptation."),
        ("Check heritability in the stem",
         "If the stem never says the trait is genetic, do not leap to evolution. Acquired muscle from a gym is not an allele."),
        [
            "I can state Darwin’s requirements for natural selection.",
            "I can separate homology from analogy and list evidence of descent.",
            "I can reject need-driven mutation as a mechanism.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Hardy–Weinberg",
        [
            "A population’s gene pool is all the alleles at a locus. p is the frequency of allele A; q of allele a; $p+q=1$ for two alleles.",
            "If mating is random and no other forces act, genotype frequencies are $p^2$ (AA), $2pq$ (Aa), $q^2$ (aa). That is Hardy–Weinberg equilibrium — a null model, like ‘no friction’ in physics.",
            "The five assumptions: no mutation, no migration (gene flow), no selection, random mating, infinite (or huge) population so drift is negligible. Real populations break at least one; the model still lets us measure how far they break it.",
            "From a recessive phenotype frequency you can estimate $q=\\sqrt{q^2}$ only if you assume HW. Carriers are then $2pq$, usually much larger than $q^2$ when the disease is rare.",
            "Drift is sampling error. It is fast when N is small. Bottlenecks and founder events are drift with a storyline. They reduce diversity and can fix harmful alleles by luck.",
            "Selection, nonrandom mating, and migration move populations off HW in predictable directions (fewer heterozygotes, more of one homozygote, etc.). Chi-square can test observed vs $p^2:2pq:q^2$.",
        ],
        "Speciation and conservation genetics both start from ‘what is p doing?’ If you cannot compute 2pq, you cannot talk about carriers or hidden variation.",
        "First get p and q from allele counts if possible. Only then square them. Do not treat phenotype percents as p.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda p: 2 * p * (1 - p), 0, 1))],
                xlim=(0, 1), ylim=(0, 0.6), xlab="p", ylab="2pq",
                points=[(0.5, 0.5, "max het=0.5")],
            ),
            "Heterozygote frequency vs p under HW",
            "2pq peaks at 0.5 when p=q=0.5. Rare alleles hide in heterozygotes.",
        )
        + solved(4, "1% of a HW population shows a recessive trait. What is q, and what fraction are carriers?",
                 ["$q^2=0.01$ so $q=0.1$.",
                  "$p=0.9$.",
                  "$2pq=2(0.9)(0.1)=0.18$ — 18% carriers."],
                 "q=0.1; carriers 18%", "", "Easy")
        + solved(5, "Among 200 alleles in 100 diploids you count 120 A. Find p, q, and expected Aa under HW.",
                 ["p=120/200=0.6, q=0.4.",
                  "Expected Aa = 2pq × 100 = 2(0.6)(0.4)×100 = 48.",
                  "Expected AA=36, aa=16."],
                 "p=0.6, q=0.4, ~48 heterozygotes", "", "Medium")
        + solved(6, "A flood randomly kills 90% of a population. Name the process and a likely effect on diversity.",
                 ["Survival was luck, not a heritable trait — genetic drift (bottleneck).",
                  "The gene pool is a small sample; some alleles are lost.",
                  "Heterozygosity typically falls; later inbreeding can expose recessives."],
                 "bottleneck drift; diversity down", "", "Hard"),
        ("Using 1% affected as p=0.01",
         "1% recessive phenotype is q², not q and not p. Take the square root first. This single slip wrecks every carrier item."),
        ("Write the five assumptions, then circle which one broke",
         "If they describe cousins marrying, it is nonrandom mating. If N=12, it is drift. If a pesticide, it is selection. Name the broken assumption."),
        [
            "I can use $p+q=1$ and $p^2+2pq+q^2=1$.",
            "I can estimate carrier frequency from a recessive phenotype under HW.",
            "I can explain drift, bottlenecks, and why HW is a null model.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Speciation",
        [
            "Speciation is the splitting of one lineage into two that no longer share a fully mixed gene pool. Under the biological species concept, they do not make viable, fertile offspring together.",
            "Gene flow is the enemy of speciation: migrants remix alleles. Allopatric speciation starts when a geographic barrier (river, canyon, glacier) stops that flow. Each side then drifts and adapts on its own.",
            "If the barrier vanishes and the two groups cannot or will not interbreed, speciation has occurred. Prezygotic barriers stop fertilization; postzygotic barriers make hybrids fail after fertilization.",
            "Sympatric speciation happens without a mountain: polyploidy in plants is the cleanest case. Habitat choice or mate choice can also reduce gene flow inside one lake or one forest.",
            "Hybrid zones form where incomplete barriers meet. If hybrids are unfit, selection may reinforce prezygotic isolation. If hybrids are fine, the split may collapse.",
            "Species concepts disagree at the edges (asexuals, fossils, ring species). That is not a failure of evolution; it is biology being bushy rather than a filing cabinet.",
        ],
        "Phylogeny next will draw the splits. Speciation is the process that creates the nodes.",
        "Ask: did gene flow stop, and by what barrier (place, time, behavior, chromosomes, hybrid death)?",
        lesson_figure(
            (
                '<svg viewBox="0 0 320 140" width="100%" style="max-width:320px" role="img">'
                '<rect x="20" y="20" width="120" height="100" fill="#dbeafe" stroke="#1e3a8a"/>'
                '<rect x="180" y="20" width="120" height="100" fill="#dcfce7" stroke="#166534"/>'
                '<text x="80" y="70" text-anchor="middle" font-size="12">pop A</text>'
                '<text x="240" y="70" text-anchor="middle" font-size="12">pop B</text>'
                '<line x1="140" y1="20" x2="180" y2="20" stroke="#b91c1c" stroke-width="6"/>'
                '<line x1="140" y1="120" x2="180" y2="120" stroke="#b91c1c" stroke-width="6"/>'
                '<text x="160" y="16" text-anchor="middle" font-size="11" fill="#b91c1c">barrier</text>'
                "</svg>"
            ),
            "Allopatry: a barrier splits one gene pool into two",
            "No gene flow. Mutation, selection, and drift can now send A and B down different paths.",
        )
        + solved(7, "A canyon splits squirrels. After 10,000 years they meet and do not mate. What happened, and what kind of barrier is ‘will not mate’?",
                 ["Allopatric divergence while gene flow was zero.",
                  "Failure to mate is prezygotic isolation.",
                  "They now behave as biological species if hybrids also are not produced."],
                 "allopatric speciation; prezygotic (behavioral) isolation", "", "Easy")
        + solved(8, "A mule is a sterile horse–donkey hybrid. Pre- or postzygotic, and why are horse and donkey still called two species?",
                 ["A zygote formed, so the barrier is postzygotic (hybrid sterility).",
                  "Gene pools stay separate because mules do not contribute offspring.",
                  "BSC still classifies them as two species."],
                 "postzygotic sterility; gene pools remain separate", "", "Medium")
        + solved(9, "How can polyploidy create a new plant species in one generation?",
                 ["A 2n gamete + 2n gamete (or genome doubling) can make a 4n plant.",
                  "Back-crossing to 2n parents yields odd ploidy and usually sterile hybrids.",
                  "Instant reproductive isolation — sympatric speciation with a chromosomal mechanism."],
                 "even polyploid instantly isolated from diploid parents", "", "Hard"),
        ("Requiring a mountain for every speciation",
         "Allopatry is common, not exclusive. Polyploidy and ecological speciation are on the AP list. ‘No river, therefore no species’ is false."),
        ("Classify the barrier as pre or post first",
         "Did a zygote form? No → pre. Yes, but the offspring fails → post. Then name the subtype (temporal, mechanical, sterility…)."),
        [
            "I can state the biological species concept and its limits.",
            "I can contrast allopatric vs sympatric paths.",
            "I can sort prezygotic vs postzygotic barriers.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Phylogeny and cladograms",
        [
            "A phylogeny is a hypothesis of branching descent. A cladogram is a tree of clades. A clade (monophyletic group) is an ancestor plus all descendants.",
            "We build trees from shared derived characters — traits that arose once on a branch and were inherited. Ancestral traits shared by everyone in the study group do not tell us the inner branching.",
            "An outgroup is a relative just outside the group of interest. It tells us which character state is likely ancestral. Frogs outgroup amniotes; lancelets outgroup vertebrates.",
            "Branch rotation does not change sister relationships. Reading a tree as a ladder with ‘higher’ species on the right is a mistake. The only information is who shares a more recent node.",
            "Convergence and reversals create homoplasy, which can fool parsimony. DNA sequences give many characters; we still watch for HGT and incomplete lineage sorting on hard items.",
            "Molecular clocks convert mutation counts into time, calibrated with fossils. They are approximate. Different genes tick at different rates because selection vs neutrality differs.",
        ],
        "Unit 8’s biodiversity and this unit’s extinctions are events on these trees. If you misread sisters, you misread who went extinct together.",
        "Find the node, then list everyone downstream of it. That list is the clade. Ignore left-right order.",
        lesson_figure(
            _cladogram_svg(),
            "A cladogram with an outgroup",
            "A and B share a node the outgroup does not. The blue mark is a shared derived trait of A+B.",
        )
        + solved(10, "Tree: (outgroup, (shark, (frog, (lizard, (bird, mammal))))). Are birds closer to lizards or to mammals on this hypothesis?",
                 ["On this parenthetical tree, bird and mammal share a node that lizard does not.",
                  "Therefore birds are closer to mammals than to lizards on this hypothesis.",
                  "If the tree had been (lizard, bird) as sisters, the answer would flip. Read the parentheses, not the English names’ vibe."],
                 "closer to mammals on this tree (they share a more recent node)",
                 "Real textbooks often place birds with crocodilians, not mammals — the skill is reading THIS tree.", "Easy")
        + solved(11, "Why is ‘has a backbone’ a poor character to split a shark vs a frog vs a human?",
                 ["All three are vertebrates; the backbone is ancestral for the ingroup.",
                  "A shared ancestral trait does not tell you which two are sisters.",
                  "You need a derived trait (amniotic egg, hair, jaws of a certain type, a DNA synapomorphy)."],
                 "it is shared ancestral, not derived, for these taxa", "", "Medium")
        + solved(12, "Two cactus-like plants on different continents share spines and succulent stems but DNA puts them far apart. Interpret.",
                 ["The look-alikes are convergent (analogous) adaptations to dry habitats.",
                  "Using those traits as homologies would group them wrongly.",
                  "DNA (and flowers, if they differ in family-level traits) outvotes the desert costume."],
                 "convergence; do not treat the succulent look as a synapomorphy", "", "Hard"),
        ("Reading trees as rankings with humans as the goal",
         "Evolution has no predetermined ladder. Every living tip has been evolving for the same time since the root. ‘Higher’ is not a tree measurement."),
        ("Circle the node, shade the descendants",
         "If the shaded set matches the clade in the question, you read it right. If a species inside the shade is left out of your answer, you broke monophyly."),
        [
            "I can define clade, outgroup, and shared derived character.",
            "I can identify sister groups despite branch rotation.",
            "I can explain how convergence misleads morphological trees.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Extinction and diversity",
        [
            "Extinction is the permanent loss of a lineage. Background extinction is the normal trickle. Mass extinctions (five famous ones, plus a possible human-driven sixth) remove a large fraction of species in a geologically short interval.",
            "Causes include climate shifts, volcanism, impacts, anoxia, and now habitat destruction, overharvest, invasives, and rapid climate change. The common theme is that the environment moves faster than adaptation and migration can track.",
            "Diversity rebounds after mass extinction, often by adaptive radiation of survivors into empty niches. That rebound takes millions of years — not a semester.",
            "Genetic diversity within a species is a buffer. No variation, no selection response. Bottlenecked species (cheetahs, some island birds) are extinction-prone for this reason as well as for small N drift.",
            "Invasive species and introduced pathogens can cause extinctions because native species did not coevolve with those enemies. Hawaiian birds vs avian malaria is a brutal example.",
            "Humans are now a global selective agent: trophy hunting, fisheries (smaller fish maturing earlier), antibiotic and pesticide resistance. Unit 7 is not only about finches.",
        ],
        "Unit 8 will put numbers on populations and climate. This concept is the evolutionary frame: lost branches do not return.",
        "Separate within-species diversity (alleles) from species diversity (tips on the tree). Conservation needs both.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", [(0, 80), (2, 78), (3, 20), (5, 22), (8, 40), (12, 70)])],
                xlim=(0, 12), ylim=(0, 90), xlab="time (arbitrary)", ylab="species diversity",
                points=[(3, 20, "mass extinction")],
            ),
            "Diversity crash and slow rebound",
            "A mass extinction is a cliff. Adaptive radiation is a long climb, not an instant reset.",
        )
        + solved(13, "Why does a bottleneck raise later extinction risk even if N recovers?",
                 ["Alleles lost in the bottleneck do not automatically return.",
                  "Low diversity means fewer raw materials for selection if the environment changes again.",
                  "Small-N inbreeding can also fix deleterious recessives."],
                 "lost genetic diversity; weaker future adaptive potential", "", "Easy")
        + solved(14, "After the end-Cretaceous impact, mammals radiated. Connect empty niches to speciation.",
                 ["Dinosaur extinction freed resources and habitats.",
                  "Surviving mammals that differed in diet/habitat had less competition.",
                  "Selection plus isolation produced many new species — adaptive radiation."],
                 "vacated niches + selection/isolation → radiation", "", "Medium")
        + solved(15, "Fisheries that keep only large fish select for what life-history change, and why is that evolution?",
                 ["Heritable tendency to mature smaller/younger becomes fitter because large late-maturers are killed first.",
                  "The catch is a selective filter, like Darwin’s birds.",
                  "The population’s mean size at maturity can fall within decades — evolution, not just fewer old fish this year."],
                 "selection for smaller, earlier maturation", "", "Hard"),
        ("Thinking extinct species can re-evolve identically once the climate returns",
         "You cannot replay the same mutations and the same coevolving partners. Dolphins look shark-ish (convergence) but they are not Mesozoic ichthyosaurs returned. Lost clades stay lost."),
        ("Name the filter",
         "Impact winter, antibiotic, gill net, invasive snake — put the selective or random killer in the sentence. ‘Extinction happened’ is not an explanation."),
        [
            "I can contrast background and mass extinction.",
            "I can explain adaptive radiation after a crash.",
            "I can connect genetic diversity and human harvest to extinction risk.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Origins of life",
        [
            "Life today needs a genome, metabolism, and a membrane. Origins research asks how those pieces could arise without a prior cell. It is hypothesis-driven; there is no single surviving witness.",
            "Abiotic synthesis: energy (lightning, UV, vents) plus simple gases can make amino acids, bases, and sugars (Miller–Urey and later variants). The early atmosphere’s exact mix is debated; the point is that organics are not magic.",
            "Polymers: clay surfaces, drying lagoons, or vent minerals can concentrate monomers and favor linkage. RNA can both store sequence and catalyze (ribozymes) — the RNA-world idea. Today’s ribosome still uses rRNA to make peptide bonds, a smoking gun.",
            "Packaging: fatty-acid vesicles spontaneously form bilayers (Unit 1 hydrophobic effect) and can grow and split. A genome inside a bag is a proto-cell: selection can now act on a unit that keeps its molecules together.",
            "The last universal common ancestor (LUCA) was already cellular, with DNA, proteins, and membranes. The origin story is older than LUCA. Later, oxygenic photosynthesis changed the planet and made aerobic respiration’s ATP bonanza possible.",
            "Endosymbiosis (mitochondria, chloroplasts) and horizontal gene transfer mean the tree of life has mergers and gene jumps, especially among microbes. Origins did not produce a perfectly tidy ladder.",
        ],
        "This concept stitches Units 1–3 (chemistry, membranes, energetics) to evolution. AP essays often want a numbered sequence: monomers → polymers → RNA catalysis → membranes → selection.",
        "Keep claims modest: experiments show organic molecules can form, not that a bacterium assembled in a flask.",
        lesson_figure(
            (
                '<svg viewBox="0 0 340 130" width="100%" style="max-width:340px" role="img">'
                '<rect x="10" y="40" width="70" height="50" rx="8" fill="#fef3c7" stroke="#b45309"/>'
                '<text x="45" y="70" text-anchor="middle" font-size="11">monomers</text>'
                '<text x="95" y="70" font-size="16">→</text>'
                '<rect x="115" y="40" width="70" height="50" rx="8" fill="#dbeafe" stroke="#1e3a8a"/>'
                '<text x="150" y="70" text-anchor="middle" font-size="11">RNA</text>'
                '<text x="200" y="70" font-size="16">→</text>'
                '<ellipse cx="255" cy="65" rx="40" ry="30" fill="#dcfce7" stroke="#166534"/>'
                '<text x="255" y="70" text-anchor="middle" font-size="11">vesicle</text>'
                '<text x="170" y="115" text-anchor="middle" font-size="12">then selection on protocells</text>'
                "</svg>"
            ),
            "A minimal origins sequence",
            "Monomers, then informational/catalytic polymers, then a membrane so selection has a unit.",
        )
        + solved(16, "Name two jobs RNA can do that make it a candidate for an early genome-plus-enzyme.",
                 ["Sequence of bases stores information (like DNA).",
                  "Some RNAs catalyze reactions, including peptide-bond formation in the ribosome.",
                  "A two-in-one molecule reduces the ‘which came first’ problem."],
                 "information + catalysis (ribozymes)", "", "Easy")
        + solved(17, "Why is a membrane a turning point for Darwinian evolution at the origin of life?",
                 ["Without a compartment, useful molecules diffuse away from the reactions that made them.",
                  "A vesicle keeps genome and metabolites together as a unit.",
                  "Selection can then favor vesicles that grow and divide more — true inheritance of a package."],
                 "compartmentalization creates a selectable individual", "", "Medium")
        + solved(18, "Miller–Urey made amino acids. What did it not show, and why does that still matter?",
                 ["It did not produce a living cell, a genome, or Darwinian replication.",
                  "It showed a plausible abiotic source of monomers, removing one ‘impossible ingredient’ objection.",
                  "Later steps (polymers, RNA world, membranes) remain active research — AP wants the limited, accurate claim."],
                 "monomers yes; cells no — still a key first step", "", "Hard"),
        ("Jumping from amino acids in a flask to ‘life was created in 1953’",
         "That overclaim is easy to mock and loses AP points. State the result: organic monomers under inferred early-Earth energy inputs."),
        ("Number the steps on the FRQ",
         "1 monomers, 2 polymers/RNA, 3 vesicles, 4 heredity+selection, 5 LUCA much later. Graders like a sequence more than a name-drop of Miller."),
        [
            "I can outline abiotic monomers, RNA world, and membranes.",
            "I can limit Miller–Urey to what it actually showed.",
            "I can connect oxygenic photosynthesis to later aerobic life.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Natural selection’s requirements and evidence of descent",
            "Hardy–Weinberg math, drift, and broken assumptions",
            "Speciation, gene flow, and reproductive barriers",
            "Cladograms, clades, and tree reading",
            "Extinction, diversity, and human as a selective agent",
            "Chemical origins of life and the RNA-world idea",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Ecology
# ===========================================================================

def _u8_questions():
    return _qs([
        ("A trophic level is a feeding step. Producers are:",
         "autotrophs that convert inorganic carbon into organic carbon (usually by photosynthesis)",
         "They are the base of almost every food web’s energy. Net primary productivity (NPP) is GPP minus the producers’ own respiration — the energy actually available to herbivores.",
         ["only carnivores", "decomposers that eat only meat", "the top of the energy pyramid by definition"]),
        ("About 10% of energy is transferred up each trophic step because:",
         "most energy is lost as heat, unused biomass, and consumer respiration",
         "The 10% rule is a rough average, not a law. It is why food chains are short and why a pyramid of energy never inverts (unlike some pyramids of numbers).",
         ["predators create energy", "energy is destroyed at each step in violation of physics", "herbivores get 90% of GPP as a rule"]),
        ("NPP is highest, among typical biomes, in:",
         "tropical rainforest (warm, wet, long growing season)",
         "Open ocean has huge area but low NPP per m². Algal beds and reefs are productive per area. AP graphs of NPP vs precipitation/temperature are this idea.",
         ["desert", "open ocean per square meter as the single highest", "tundra"]),
        ("A pyramid of energy cannot invert because:",
         "energy transfers are inefficient; less energy is available at each higher level",
         "A pyramid of numbers can invert (one tree, many insects). Biomass can invert in some aquatic systems with fast phytoplankton turnover. Energy over a time interval cannot.",
         ["numbers cannot invert either", "top carnivores photosynthesize", "heat is a form of NPP"]),
        ("Decomposers matter because they:",
         "recycle chemical nutrients (N, P, C) back to producers; they do not recycle energy",
         "Energy flows through and leaves as heat. Atoms cycle. Mixing those two sentences is an AP classic miss.",
         ["return used energy to the sun", "create new energy for producers", "stop the carbon cycle"]),
        ("Exponential growth $dN/dt=rN$ occurs when:",
         "resources are not limiting, so the per-capita rate r stays constant",
         "The curve is J-shaped. r is births minus deaths per individual. Doubling time shrinks as N grows — that is the danger of human or invasive outbreaks early on.",
         ["the population is at K", "r is always negative", "N cannot change"]),
        ("Logistic growth $dN/dt=rN(K-N)/K$ adds:",
         "carrying capacity K, so growth slows as N approaches K",
         "When N=K, dN/dt=0. When N is small, (K−N)/K≈1 and it looks exponential. Real populations overshoot, oscillate, or get knocked down by weather.",
         ["a second exponential term that never slows", "K as the extinction threshold", "r becoming infinite at K"]),
        ("Density-dependent limits include:",
         "competition, disease, predation that intensify as N rises",
         "Density-independent: storms, fire, many abiotic shocks that hit regardless of N (though a larger N still loses more individuals). AP wants examples, not just the phrase.",
         ["only hurricanes", "only meteor impacts", "factors that never change with N, by definition of dependent"]),
        ("r-selected species vs K-selected: r-selected tend to:",
         "reproduce early with many small offspring and little parental care (weeds, many insects)",
         "K-selected: fewer offspring, more care, live near carrying capacity (elephants, many trees). These are ends of a spectrum, not moral grades.",
         ["always be large mammals", "never grow exponentially even when invading", "have K=1 by definition"]),
        ("A population of 500 has r=0.1 in exponential growth. Instantaneous dN/dt is:",
         "50 individuals per time unit",
         "$0.1\\times500=50$. After a short interval N is larger, so the next increment is larger. That is the J-curve.",
         ["0.1", "5000", "0"]),
        ("Competitive exclusion says two species with identical niches:",
         "cannot stably coexist; one will win the resource",
         "Coexistence often requires niche partitioning (different prey sizes, times, root depths). Character displacement is evolution of those differences where species overlap.",
         ["must fuse into one species", "always form a mutualism", "have the same carrying capacity as a sum always"]),
        ("A keystone species has an effect:",
         "out of proportion to its biomass (often a predator that protects diversity)",
         "Pisaster sea stars and wolves in some systems: remove them, and a competitive dominant (mussels, elk) takes over, diversity falls. Not the same as the most common species (that may be a foundation species).",
         ["equal to its biomass always", "only if it is a producer", "that is always negative"]),
        ("Mutualism vs commensalism vs parasitism: the signs of the interaction are:",
         "+/+, +/0, and +/− respectively",
         "Mycorrhizae are mutualism. Barnacles on a whale can be commensal. Tapeworms are parasites. Predation is also +/− but ends in death of prey, not a long infection.",
         ["all three are +/+", "parasitism is −/−", "mutualism is +/−"]),
        ("Invasive species often lack:",
         "the predators, parasites, and competitors they coevolved with at home",
         "Enemy release plus a vacant or underused niche explains many explosions. They can then compete with or eat natives (Unit 7 extinctions).",
         ["all photosynthesis", "any r at all", "the ability to mutate"]),
        ("Aposematic coloration is a:",
         "warning signal that the prey is toxic or dangerous, which predators learn",
         "Mimicry then evolves: Batesian (harmless fakes the warning) vs Müllerian (two nasty species share a look). Community evolution of signals.",
         ["camouflage that hides the prey as the definition of aposematic", "a producer strategy only", "commensalism with plants"]),
        ("Species richness is the count of species; evenness is how equal their abundances are. A community of 5 equally common species is:",
         "more even (and usually more diverse by Simpson/Shannon) than 5 species where one is 99%",
         "Conservation cares about both. A monoculture plantation can have the same richness as a meadow if you only count species lists from a lazy sample — evenness exposes the fake.",
         ["less diverse by every index", "identical in diversity to the 99% case because richness matches", "not a community"]),
        ("A foundation species (kelp, coral, trees) structures the habitat. Unlike a keystone predator it is often:",
         "abundant and physically creating the niche space others use",
         "Both are ‘important,’ but the mechanism differs: biomass architecture vs disproportionate interaction strength. AP may give a scenario and ask which label fits.",
         ["rare and eating the competitive dominant as the foundation definition", "always microbial", "density-independent weather"]),
        ("Island biogeography: richness rises with island size and falls with:",
         "distance from the mainland (harder immigration)",
         "Equilibrium of immigration vs extinction. Habitat fragments on land behave like islands. That is why corridors and larger reserves matter.",
         ["distance making immigration easier", "size making extinction more likely always", "K of the ocean"]),
        ("Simpson diversity is higher when:",
         "more species are present and individuals are spread among them, not piled on one",
         "You do not need the formula memorized if you can reason: two even species > one species; ten even > two even. FRQs often give a table and ask which plot is more diverse.",
         ["one species has all the individuals", "richness is 1", "evenness is zero"]),
        ("Why might a more diverse community resist invasion or disease better?",
         "niche complementarity and a lower chance the invader finds a wide-open resource, plus dilution of hosts",
         "This is a hypothesis with evidence in many systems, not a guarantee. Still the AP-level ‘diversity–stability’ story.",
         ["diversity lowers NPP to zero", "keystones cannot exist in diverse systems", "HW forbids invasion"]),
        ("Eutrophication is:",
         "nutrient overload (N, P) causing algal blooms, then decomposition that strips oxygen",
         "Dead zones in the Gulf of Mexico are this cascade. The fertilizer did not ‘poison fish’ directly; oxygen collapse did. Cause-and-effect chain required.",
         ["ozone thinning by CFCs as the definition of eutrophication", "a type of mutualism", "logistic K increasing forever"]),
        ("Burning fossil fuels raises atmospheric CO₂, which:",
         "traps outgoing infrared (greenhouse) and also acidifies oceans as CO₂ dissolves",
         "Two independent problems from one gas: climate forcing and $CO_2+H_2O\\rightleftharpoons H_2CO_3$. Coral calcification suffers. AP loves the chemistry link to Unit 1.",
         ["cools the planet by blocking all sunlight", "raises ocean pH", "stops the carbon cycle"]),
        ("A keystone predator is removed and mussels carpet the rock, algae and snails decline. The lost service was:",
         "predation that prevented competitive exclusion by mussels",
         "Diversity was maintained by consumption of the dominant competitor. That is Paine’s result in sentence form.",
         ["mussels photosynthesizing for the star", "the predator’s NPP", "eutrophication of the intertidal"]),
        ("Habitat fragmentation raises extinction risk because:",
         "smaller patches support smaller N (more drift/inbreeding) and less immigration (island biogeography)",
         "Edge effects (drier, more predators) add insult. Corridors are a design response.",
         ["fragments increase K for all species", "distance to mainland falls to zero", "r becomes infinite"]),
        ("An introduced pathogen on an island bird that never evolved with it is a:",
         "novel biotic disruption, often density-independent at first if transmission is virulent enough to crash N",
         "Hawaiian honeycreepers vs avian malaria is the case study. Evolution (Unit 7) and ecology meet.",
         ["mutualism", "an increase in NPP of the birds", "Hardy–Weinberg restoration"]),
        ("The independent variable is what you manipulate; the dependent variable is what you measure. In ‘fertilizer dose vs plant biomass,’ IV and DV are:",
         "dose; biomass",
         "Constants: light, water, pot size, species. Replication: many pots per dose. Control: zero fertilizer. This template transfers to any ecology experiment.",
         ["biomass; dose", "the greenhouse as IV", "pH of the galaxy"]),
        ("A control group is:",
         "the baseline treatment without the factor you are testing, used for comparison",
         "Without it you cannot say the factor caused the change. A negative PCR control (Unit 6) is the same logic in a tube.",
         ["the group you like most", "a second independent variable you change at the same time on purpose without a design", "n=1 always"]),
        ("Replication (many individuals or plots per treatment) is needed because:",
         "biological noise is large; one plant cannot represent the treatment",
         "You then can estimate variability and avoid being fooled by a single freak plot. n=1 is an anecdote, not an experiment.",
         ["replication means copying DNA in the field", "one plot is always enough if you care", "K cannot be measured with replicates"]),
        ("A valid experiment changes one hypothesized factor at a time (or uses a factorial design on purpose). Confounding means:",
         "two factors change together so you cannot tell which caused the DV shift",
         "If the high-fertilizer pots also sat in the sun, light is confounded with fertilizer. Randomize location.",
         ["the control worked", "NPP is zero", "you used too many replicates"]),
        ("Error bars that overlap a lot between treatments suggest:",
         "the difference may not be distinguishable from noise (need a proper test; do not overclaim)",
         "AP graph-reading: non-overlap is a hint of a real difference, not a proof, but huge overlap is a reason for caution. Sample size matters.",
         ["the means are infinitely different", "the experiment had no DV", "error bars measure NPP only"]),
        ("GPP minus autotrophic respiration equals:",
         "NPP — the carbon actually available to the rest of the food web",
         "If a graph shows GPP and respiration, subtract. If respiration of producers rises with temperature faster than GPP, NPP can fall even if GPP looks fine — a climate item.",
         ["only secondary production", "K of the herbivores by definition", "10% of GPP always exactly"]),
        ("Secondary production is:",
         "the biomass heterotrophs add from eating others",
         "Efficiency is low (the 10% idea). Ectotherms often convert more of their food to biomass than endotherms because they spend less on heat (Unit 3 fitness).",
         ["GPP of plants", "the sun’s photons", "carrying capacity of space"]),
        ("A food web is more realistic than a chain because:",
         "species eat at multiple levels and have multiple prey; energy paths branch and reconnect",
         "Omnivory blurs trophic numbers. Still, energy ultimately traces to producers (or to chemoautotrophs in vents).",
         ["chains allow more species than webs", "webs violate energy flow", "producers eat carnivores as the usual base"]),
        ("If N=900 and K=1000, logistic growth is slow because:",
         "$(K-N)/K=0.1$, so only 10% of rN remains",
         "The remaining ‘room’ is small. Crowding, resource shortage, and waste are the biology under that algebra.",
         ["the population is in exponential takeoff", "K was exceeded so r is larger", "dN/dt equals rN still"]),
        ("Overshoot of K followed by a crash can happen when:",
         "reproduction responds late (time lag) or the resource is overconsumed",
         "Lynx–hare oscillations are a coupled predator–prey lag story. Logistic is a smooth ideal, not a promise.",
         ["r=0 and N=0", "K is infinite", "density dependence is instantaneous and perfect always"]),
        ("Niche partitioning of Anolis lizards (different perch heights) allows:",
         "coexistence by reducing interspecific competition for the same insects in the same place",
         "The fundamental niche is the full range they could use; the realized niche is the slice they actually occupy with competitors present.",
         ["identical niches to persist against competitive exclusion", "mutualism with the insects only", "K to become infinite"]),
        ("A parasite that castrates its host but keeps it alive is still +/− because:",
         "the parasite gains fitness; the host’s reproduction (fitness) falls",
         "Fitness, not ‘death this week,’ is the ecological currency. Unit 7’s word again.",
         ["the interaction is +/+ if the host lives a long time", "castration is commensal", "parasites are producers"]),
        ("Batesian mimicry requires:",
         "a palatable mimic, a noxious model, and predators that learn to avoid the model’s look",
         "If mimics become too common, the signal is unreliable and protection collapses (frequency dependence — Unit 7).",
         ["both species being equally toxic as the Batesian definition", "no predators", "the mimic being a producer"]),
        ("A biodiversity hotspot is typically:",
         "high endemic richness plus high threat — a conservation-priority patch",
         "Endemic means found nowhere else. Losing a hotspot loses unique branches of the tree (Unit 7), not just local N.",
         ["a parking lot with one grass", "the open ocean gyre with the lowest NPP", "an ice sheet"]),
        ("Ocean acidification harms calcifiers because:",
         "more CO₂ lowers pH and [CO₃²⁻], making shells/skeletons harder to build",
         "Unit 1 buffers meet Unit 8 climate. The chemistry is not optional decoration.",
         ["pH rises, helping all shells", "CO₂ is unused in oceans", "calcifiers photosynthesize CO₂ away in all cases as animals"]),
        ("CFCs vs CO₂: CFCs famously:",
         "destroy stratospheric ozone (more UV), a different problem than CO₂’s greenhouse/acidification",
         "Do not mash every atmospheric issue into one blob. Ozone hole ≠ greenhouse effect, even if some gases play in both arenas.",
         ["are the main cause of ocean dead zones", "raise NPP of deserts necessarily", "are a type of keystone predator"]),
        ("An El Niño year reducing upwelling off Peru crashes:",
         "nutrients → phytoplankton → fish, a bottom-up productivity shock",
         "Bottom-up vs top-down (keystone predator) are two ways to move a food web. Name which end you shoved.",
         ["only the top predator independently of nutrients", "mutualism between tuna and phytoplankton as the first crash", "K of the desert"]),
        ("Mark-recapture: 40 marked, later 100 captured of which 10 marked. N̂ ≈",
         "400",
         "$N/40 = 100/10$ so $N=400$. Assumptions: marks do not fall off, no huge births/deaths, random mixing. AP may ask which assumption broke.",
         ["40", "100", "10"]),
        ("A mesocosm experiment is useful because:",
         "you can manipulate one factor in a still-somewhat-natural community, with replication",
         "Tradeoff: more realism than a test tube, less control than a growth chamber. Match the tool to the question.",
         ["it requires n=1 by definition", "you cannot have a control", "IV and DV swap"]),
        ("Null hypothesis for ‘fertilizer raises biomass’ is usually:",
         "fertilizer has no effect on mean biomass (any difference is noise)",
         "You then use a statistical test. AP experimental design: state null, predict under the alternative, name constants, show a control.",
         ["fertilizer definitely works", "plants are not alive", "K is fertilizer"]),
        ("Random assignment of pots to sun/shade vs fertilizer treatments prevents:",
         "a systematic confound between treatment and location",
         "Randomize, replicate, control. The three-word lab religion. Blocking (all treatments in each greenhouse bench) is even better.",
         ["photosynthesis", "the need for a DV", "NPP from existing"]),
        ("AP Stretch: A lake’s GPP is 5000 g C/m²/yr, autotrophic respiration 3000, herbivores eat 400 of NPP and respire 350. NPP and herbivore production are:",
         "NPP=2000; herbivore net production=50",
         "NPP=GPP−R_auto=2000. Herbivore production = ingested − feces − respiration; here they gave eat 400 and respire 350, implying 50 if egestion is already netted or ignored. State the 2000 clearly; the 50 follows if 400 is assimilated. If 400 is ingested with unstated feces, AP usually treats the given pair as the subtraction they want.",
         ["NPP=5000; herbivores=400", "NPP=3000; herbivores=750", "NPP=2000; herbivores=400"]),
        ("AP Stretch: Two islands, same size; A is 10 km offshore, B is 100 km. Equilibrium richness should be higher on A because:",
         "immigration rate is higher, so the immigration–extinction balance sits at more species",
         "Extinction rates similar if area (hence K per species) is similar. Distance is the immigration knob. Fragments far from source habitat are the mainland version.",
         ["extinction is higher on A", "K is infinite on B", "distance increases gene flow from the mainland to B more than A"]),
        ("AP Stretch: A logistic model with a time lag produces oscillations around K when:",
         "the delay is long enough that N overshoots before reproduction slows",
         "This is why smooth logistic curves on worksheets are not the only possible $dN/dt$. Delayed density dependence is a real AP-adjacent idea.",
         ["r=0", "K=N always with no lag", "time lags remove density dependence"]),
        ("AP Stretch: Removing a cleaner-fish mutualist from a reef decreases client-fish health and can cascade. The interaction was +/+, but the community effect is:",
         "loss of a mutualist can look keystone-like if many species depended on the service",
         "Labels (mutualism, keystone) can overlap in function. Argue from the interaction network, not from a single vocabulary word.",
         ["mutualists cannot be important because they are +/+", "the reef’s NPP must rise", "parasitism begins automatically"]),
        ("AP Stretch: CO₂ fertilization might raise GPP, but warming raises respiration and drought closes stomata. Net NPP in a forest might fall because:",
         "the losses (R, water stress) can outweigh extra photosynthesis — a systems, not single-factor, prediction",
         "AP climate items punish single-knob thinking. Draw GPP and R as two arrows.",
         ["NPP must rise if CO₂ rises, by definition of GPP", "stomata closed means Calvin still has unlimited CO₂ in air without entering the leaf", "respiration is independent of temperature"]),
        ("AP Stretch: You test whether a predator is keystone: cages with/without predator, measure richness. A good design also:",
         "replicates cages, randomizes locations, and includes a cage-control for cage artifacts (mesh without excluding the predator, if possible)",
         "Cage effects (light, flow) are classic confounds. Experimental design is the concept; sea stars are the story.",
         ["uses n=1 cage because keystones are unique", "changes temperature at the same time only in predator cages", "has no measured DV"]),
        ("AP Stretch: A 99% CI for mean biomass of fertilized vs control overlap. The most responsible claim is:",
         "the data do not show a clear mean difference at that confidence level; do not announce a huge effect",
         "Overlapping intervals are not a formal test, but AP graph literacy wants humility. Increase n or use a proper t-test/ANOVA in a real lab.",
         ["the fertilizer is proven stronger than gravity", "overlap means the IV was biomass", "you should drop the control"]),
        ("AP Stretch: Bottom-up vs top-down in the same kelp forest: more nutrients raise kelp, more otters raise kelp by eating urchins. If both happen, an experiment must:",
         "factorially (or separately) manipulate nutrients and otters, or you cannot assign the kelp increase to one cause",
         "Confounded productivity and predation are how arguments in ecology last decades. Design is how you end them.",
         ["measure only NPP of otters", "assume keystones override nutrients always, so skip controls", "use a food chain of length 1"]),
        ("AP Stretch: Dead-zone oxygen sag is worst after the bloom crashes because:",
         "decomposers respire the dead algae, consuming O₂ faster than it resupplies",
         "The fish kill is delayed relative to the green water. Sequence: nutrients → bloom → death → BOD spike → hypoxia. Skip a step, lose the FRQ.",
         ["algae produce extra O₂ after they die", "hypoxia is caused by extra photosynthesis at night only in the bloom’s peak without decomposition", "N and P directly bind hemoglobin in fish as the first step"]),
    ])


def build_unit8():
    title = "AP Biology Unit 8: Ecology"
    description = (
        "Energy flow, population math, communities, biodiversity, climate disruptions, "
        "and experimental design — with pyramids, logistic curves, and consistent NPP arithmetic."
    )

    c1 = concept_block(
        "1. Energy flow and trophic levels",
        [
            "An ecosystem is a community plus its abiotic stage (light, water, nutrients, climate). Energy flows through it; chemical elements cycle within it. Those two sentences organize the whole unit.",
            "Producers (autotrophs) capture inorganic carbon. Gross primary productivity (GPP) is total photosynthesis. Net primary productivity (NPP) is GPP minus the producers’ own respiration — the leftover organic carbon that can feed everyone else.",
            "A trophic level is a feeding step: producers, primary consumers (herbivores), secondary consumers, and so on. Omnivores sit on more than one step, so real systems are webs, not neat chains.",
            "At each transfer, most energy is lost as heat (the second law), as feces, and as the consumer’s own respiration. A rough classroom figure is 10% passed on. That is why there are few top predators and why human meat diets need more land than plant diets for the same calories.",
            "Pyramids of energy, measured over a time interval, cannot invert. Pyramids of numbers or biomass sometimes can (one oak tree, thousands of insects; phytoplankton eaten so fast their standing biomass is small).",
            "Decomposers (fungi, bacteria, detritivores) unlock N, P, and C from dead matter so producers can reuse atoms. They do not send energy backward to the sun. Nutrients cycle; energy does not.",
        ],
        "Climate and food-web FRQs both start from NPP. If you mix energy with nutrients, the dead-zone story and the greenhouse story will blur.",
        "For every arrow in a web, ask: is this energy (one-way, leaky) or an atom (can return)? Then name the trophic step.",
        lesson_figure(
            _pyramid_svg(),
            "An energy pyramid with a 10% transfer",
            "If producers capture 1000 units, herbivores might get ~100 and carnivores ~10. Heat and respiration steal the rest.",
        )
        + solved(1, "A field has GPP = 8000 g C/m²/yr and producer respiration = 5000. What is NPP, and who can eat it?",
                 ["NPP = 8000 − 5000 = 3000 g C/m²/yr.",
                  "That 3000 is the organic carbon left after plants pay their own ATP bill.",
                  "Herbivores, omnivores, and decomposers draw from it (not from GPP in full)."],
                 "NPP = 3000; available to consumers/decomposers", "", "Easy")
        + solved(2, "Why might a biomass pyramid in the ocean invert while an energy pyramid does not?",
                 ["Phytoplankton are eaten almost as fast as they grow, so standing biomass is small.",
                  "Zooplankton biomass can look larger at a snapshot.",
                  "Over a year, more energy still passed through the phytoplankton; the energy pyramid stays right-side up."],
                 "snapshot biomass ≠ yearly energy flow", "", "Medium")
        + solved(3, "Humans can eat tuna or eat anchovies (or grain). Using ~10% transfer, why is eating lower on the web more energy-efficient?",
                 ["Each extra trophic step keeps only a slice of the energy below.",
                  "Tuna sit higher than anchovies; grain sits at the producer level.",
                  "The same NPP supports more human calories if we skip steps — a Unit 3 efficiency idea at ecosystem scale."],
                 "fewer transfers → more of NPP in the human plate", "", "Hard"),
        ("Recycling energy in the nutrient cycle diagram",
         "Carbon atoms return as CO₂; the energy that was in the C–H bonds was already bled off as heat. Draw two diagrams if you have to: a cycle for C and a one-way river for energy."),
        ("Subtract respiration to get NPP before feeding the web",
         "If they give GPP and you send it all to cows, you double-counted the plants’ own metabolism. Write NPP = GPP − R in the margin every time."),
        [
            "I can define GPP vs NPP and trophic levels.",
            "I can explain ~10% transfer and why energy pyramids do not invert.",
            "I can contrast energy flow with nutrient cycling.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Population growth",
        [
            "A population is individuals of one species in one place. N is its size. B and D (births and deaths) plus immigration and emigration change N.",
            "Exponential growth: $dN/dt = rN$. r is the per-capita increase. When resources are unlimited, N doubles on a regular schedule and the graph is a J. Humans did this after medicine and fossil fuels; bacteria do this in fresh broth.",
            "Logistic growth: $dN/dt = rN(K-N)/K$. K is carrying capacity — the N the environment can support. Growth is fastest at K/2 and slows to zero at K. The graph is an S (sigmoid).",
            "Density-dependent factors get stronger as N rises: disease, competition, waste, many predators. Density-independent factors (frost, fire, storms) hit whether N is 10 or 10,000, though totals differ.",
            "Life-history strategies: r-selected species (many cheap offspring, early reproduction) vs K-selected (few expensive offspring, more care). Invasives often behave r-selected in a new range.",
            "Real data overshoot K, crash, or cycle (hares and lynx). Time lags in reproduction make the logistic equation too tidy. Still, r and K are the language of AP graphs.",
        ],
        "Community ecology sits on these curves: predators can lower prey K or r; competition lowers each species’ realized K.",
        "Read the axes: is N vs t a J or an S? Then name whether they told you K. Compute dN/dt with the matching equation.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#94a3b8", sample_curve(lambda t: 4 * math.exp(0.35 * t), 0, 10)),
                    ("#4f46e5", sample_curve(lambda t: 80 / (1 + math.exp(-0.7 * (t - 6))), 0, 14)),
                ],
                xlim=(0, 14), ylim=(0, 90), xlab="time", ylab="N",
                dashes=[("h", 80, "K")],
                points=[(10, 4 * math.exp(3.5), "")],
            ),
            "Exponential (gray) vs logistic (blue) approaching K",
            "The S-curve bends as N nears carrying capacity. The J-curve does not know K.",
        )
        + solved(4, "N=200, r=0.2, exponential. What is dN/dt?",
                 ["$dN/dt=rN=0.2\\times200=40$.",
                  "About 40 extra individuals per time unit right now.",
                  "As N grows, that derivative grows too — the J."],
                 "40 per time unit", "", "Easy")
        + solved(5, "N=150, K=200, r=0.2, logistic. Compute dN/dt.",
                 ["$(K-N)/K=(50)/200=0.25$.",
                  "$dN/dt=0.2\\times150\\times0.25=7.5$.",
                  "Much slower than the exponential 30 you would have gotten ignoring K."],
                 "7.5 per time unit", "", "Medium")
        + solved(6, "A storm kills 40% of a dense population and 40% of a sparse one. Density-dependent or not, and why can totals still differ?",
                 ["The same percent regardless of N is the signature of a density-independent abiotic shock.",
                  "40% of 10,000 is still more deaths than 40% of 100.",
                  "Dependence is about the rate’s relationship to N, not about zero deaths in small populations."],
                 "density-independent percent; totals still scale with N", "", "Hard"),
        ("Calling K the number born",
         "K is a ceiling set by resources and interactions, not a birth count. N can be below, at, or briefly above K."),
        ("Write the equation before the story",
         "If they give K, you are in logistic land. If they say ‘unlimited broth,’ exponential. Mixing the formulas is the algebra error that looks like a biology error."),
        [
            "I can compute exponential and logistic $dN/dt$.",
            "I can interpret K and the S vs J shapes.",
            "I can sort density-dependent vs independent examples.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Community interactions",
        [
            "A community is populations of different species that interact. The interaction table is small: competition −/−, predation/herbivory/parasitism +/−, mutualism +/+, commensalism +/0.",
            "Competitive exclusion: two species cannot share the exact same limiting niche forever. Coexistence usually means partitioning — different times, prey, root depths, or microhabitats. Character displacement is the evolutionary echo of that pressure.",
            "Predators can raise diversity by eating the competitive dominant (keystone predation). Herbivores shape plant communities the same way. Parasites can regulate host N and even alter host behavior.",
            "Mutualisms (mycorrhizae, pollination, cleaner fish) are not charity; each side’s fitness rises. Break the pair and both can suffer, sometimes with cascades.",
            "Invasives often arrive without their enemies. They can outcompete natives or eat them in a naive community. That is ecology plus Unit 7’s missing coevolution.",
            "Food-web diagrams hide interaction strength. A rare sea star can matter more than a common sponge. Ask ‘what happens if we remove it?’ — the keystone test.",
        ],
        "Biodiversity and disruption concepts are this table under stress. Experimental design will try to measure these arrows.",
        "Put + and − on every pair in the stem. Then name the interaction. Then predict N of each species if one is removed.",
        lesson_figure(
            (
                '<svg viewBox="0 0 320 140" width="100%" style="max-width:320px" role="img">'
                '<circle cx="70" cy="70" r="28" fill="#bbf7d0" stroke="#166534"/>'
                '<text x="70" y="74" text-anchor="middle" font-size="11">algae</text>'
                '<circle cx="160" cy="70" r="28" fill="#fde68a" stroke="#92400e"/>'
                '<text x="160" y="74" text-anchor="middle" font-size="11">mussel</text>'
                '<circle cx="250" cy="70" r="28" fill="#fecaca" stroke="#b91c1c"/>'
                '<text x="250" y="74" text-anchor="middle" font-size="11">star</text>'
                '<text x="115" y="40" font-size="12">−/−</text>'
                '<text x="200" y="40" font-size="12">+/−</text>'
                '<text x="160" y="125" text-anchor="middle" font-size="11">star eats mussel; mussel outcompetes algae</text>'
                "</svg>"
            ),
            "A three-species interaction sketch",
            "The star’s +/− on mussels can protect algae by preventing competitive exclusion — keystone logic.",
        )
        + solved(7, "Two barnacle species: one is shaded out of the high intertidal by desiccation, the other is eaten/crowded lower down. Name the two limits.",
                 ["The upper border is often abiotic (drying) — not competition.",
                  "The lower border is often biotic (competition or predation).",
                  "Connell’s barnacles: realized niche is smaller than fundamental niche because of the neighbor."],
                 "abiotic upper limit; biotic lower limit", "", "Easy")
        + solved(8, "Remove Pisaster, mussels take the rock, diversity drops. Why is the star a keystone, not merely a predator?",
                 ["Its biomass is not huge, but its effect on richness is huge.",
                  "It eats the dominant competitor, so inferior competitors persist.",
                  "A predator that ate rare species instead might lower diversity — same +/− sign, opposite community result."],
                 "disproportionate effect via eating the dominant competitor", "", "Medium")
        + solved(9, "Mycorrhizal fungi get sugar; plants get P and water. Drought intensifies the plant’s need. Predict the interaction’s importance, and why it is still +/+.",
                 ["Both partners’ fitness still rises relative to living without the other (definition of mutualism).",
                  "The plant may send more carbon when P is limiting — regulation of a +/+ deal.",
                  "If a fungus cheats, selection may punish it; mutualism is evolutionarily stable only when cheaters are limited."],
                 "more critical in drought; still mutualism if both gain fitness", "", "Hard"),
        ("Calling every important species a keystone",
         "Trees can be foundation species because of sheer structure and biomass. Keystone is about outsized effect per biomass, often via consumption. Use the definition, not the vibe."),
        ("Sign table, then removal prediction",
         "If A is −/− with B, removing A should help B. If A is a keystone predator on B and B excludes C, removing A hurts C. Chain the signs."),
        [
            "I can label competition, predation, mutualism, and commensalism with +/−/0.",
            "I can explain competitive exclusion and niche partitioning.",
            "I can define keystone vs foundation species with an example.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Biodiversity",
        [
            "Biodiversity is variety at three stacked levels: genetic (alleles in a population), species (richness and evenness in a community), and ecosystem (habitats on a landscape). Losing any layer has a different cost (Unit 7 already covered genetic loss).",
            "Richness is a head count of species. Evenness asks whether they are equally common. A forest of 99% one tree and 1% of four others is species-rich on a list and poor in evenness.",
            "Simpson and Shannon indices combine richness and evenness. You can reason without memorizing formulas: more species and more even → higher diversity.",
            "Island biogeography: large islands and near islands hold more species at equilibrium because extinction is lower (large) and immigration is higher (near). Habitat fragments are islands in a sea of farm or city.",
            "Endemics exist only in one place. Hotspots combine endemism with threat. Conservation triage uses that map because those branches of the tree of life have nowhere else to live.",
            "Diversity can stabilize some ecosystem functions (productivity, invasion resistance) via complementary niches — a hypothesis with a lot of field support and some exceptions. Do not overclaim, but do not ignore it.",
        ],
        "Climate disruption next will subtract species. This concept is what is being subtracted and why the subtraction is hard to reverse.",
        "When given a table of abundances, compute richness first, then squint at evenness, then pick which plot is more diverse.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", sample_curve(lambda a: 5 + 12 * (1 - math.exp(-0.15 * a)), 1, 40))],
                xlim=(0, 40), ylim=(0, 20), xlab="island area", ylab="richness",
                points=[(5, 8.3, "small"), (30, 16.2, "large")],
            ),
            "Species–area: richness rises with island (or patch) size",
            "Larger area → more habitats and higher K per species → lower extinction. The curve bends (not a line through the origin).",
        )
        + solved(10, "Plot A: 4 species, 25 each. Plot B: 4 species, 97,1,1,1. Same richness. Which is more even/diverse and why?",
                 ["Richness is 4 in both.",
                  "A is perfectly even; B is almost a monoculture.",
                  "Any standard diversity index ranks A higher."],
                 "plot A; evenness is higher", "", "Easy")
        + solved(11, "Two equal-sized islands; one is closer to the mainland. Predict richness and name the theory.",
                 ["Closer island: higher immigration, similar extinction if area matches.",
                  "Equilibrium richness is higher on the near island.",
                  "MacArthur–Wilson island biogeography."],
                 "near island richer; island biogeography", "", "Medium")
        + solved(12, "A park is cut into 10 tiny pieces with no corridors. Why does richness fall even if total acreage is unchanged?",
                 ["Each piece has smaller N → more local extinction (drift, inbreeding, stochasticity).",
                  "Immigration among pieces drops (they are now far ‘islands’).",
                  "Edge habitat increases, hurting interior specialists. Area is not the only variable — configuration matters."],
                 "fragmentation raises extinction and lowers immigration; edges expand", "", "Hard"),
        ("Equating richness with diversity in every sentence",
         "A list of 20 species that includes 19 vagrants seen once is not a diverse functioning community. Mention evenness when the abundances are given."),
        ("Treat fragments as islands",
         "Distance to source habitat, area, and corridors map onto immigration and extinction. That translation turns a conservation news story into an AP mechanism."),
        [
            "I can distinguish richness, evenness, and genetic/ecosystem diversity.",
            "I can apply island biogeography to real islands and to fragments.",
            "I can explain endemism and hotspots as conservation logic.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Disruptions and climate",
        [
            "Communities are not still. Disturbance (fire, storm, flood, disease) resets patches. Intermediate disturbance can raise richness by stopping competitive dominants from monopolizing (the intermediate-disturbance idea).",
            "Human disruptions are faster and more global: habitat loss, overharvest, invasives, nutrient runoff, and greenhouse gases. They stack.",
            "Eutrophication: extra N and P → algal bloom → algae die → decomposers respire → hypoxia → fish kill. The fertilizer’s harm is a chain, not a toxin cartoon.",
            "Climate: CO₂ and other greenhouse gases trap infrared. Warming shifts ranges, phenology (when flowers open vs when bees emerge), and extremes (drought, fire, marine heat waves). Mismatched timing is an interaction disruption.",
            "The same CO₂ acidifies oceans: more carbonic acid, lower pH, harder calcification for corals, pteropods, and shellfish. Unit 1 chemistry on a planetary beaker.",
            "Ozone depletion (CFCs) is a separate stratospheric UV problem. Do not dump it into the greenhouse bin. Accurate mechanism names are how you earn the climate FRQ.",
        ],
        "Experimental design last will try to test these mechanisms. You cannot design the test if the chain (nutrients → bloom → BOD → hypoxia) is fuzzy.",
        "For each disruption, write a three-step causal chain and say whether it is bottom-up, top-down, abiotic, or chemical.",
        lesson_figure(
            xy_graph(
                curves=[("#0ea5e9", sample_curve(lambda y: 280 + 2.2 * (y ** 1.4), 0, 10))],
                xlim=(0, 10), ylim=(250, 450), xlab="decades (schematic)", ylab="CO₂ ppm",
                points=[(0, 280, "preindustrial"), (10, 420, "now")],
            ),
            "Rising atmospheric CO₂ (schematic)",
            "The curve is not a flat line at the origin. More CO₂ means more greenhouse forcing and more ocean acidification.",
        )
        + solved(13, "A dead zone forms in summer off a river mouth that drains farms. Outline the chain from fertilizer to fish.",
                 ["N and P enter the river and then the sea.",
                  "Phytoplankton bloom, then die.",
                  "Decomposers consume O₂; hypoxia kills or drives out fish.",
                  "The first cause is nutrients; the lethal mechanism is low oxygen."],
                 "eutrophication cascade to hypoxia", "", "Easy")
        + solved(14, "Why does ocean acidification follow from rising atmospheric CO₂?",
                 ["CO₂ dissolves: $CO_2+H_2O\\rightleftharpoons H_2CO_3\\rightleftharpoons H^++HCO_3^-$.",
                  "[H⁺] up → pH down.",
                  "Carbonate availability for shells drops; calcifiers struggle."],
                 "dissolved CO₂ makes carbonic acid; pH falls; calcification suffers", "", "Medium")
        + solved(15, "Bees emerge earlier than flowers after a warm spring (or vice versa). Name the disruption type and the fitness cost.",
                 ["Phenological mismatch — climate shifted the timing of two interacting species differently.",
                  "The mutualism (+/+) fails in that year: bees lack food, plants lack pollination.",
                  "It is an interaction disruption caused by an abiotic trend, not a new predator."],
                 "phenology mismatch; both sides lose fitness that season", "", "Hard"),
        ("Blaming ‘pollution’ without a mechanism",
         "Say nutrient-driven hypoxia, or CO₂-driven warming, or CFC-driven ozone loss. The word pollution is a bucket. AP pays for the chain inside the bucket."),
        ("Two CO₂ problems, two sentences",
         "Greenhouse (infrared, climate) is not the same as ocean pH. Write both when the stem is atmospheric CO₂. One sentence each is enough and complete."),
        [
            "I can sequence eutrophication to a dead zone.",
            "I can connect CO₂ to climate and to ocean pH separately.",
            "I can describe phenological mismatch and fragmentation as disruptions.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Experimental design in ecology",
        [
            "Ecology experiments ask whether a factor causes a change in a population or community. The independent variable (IV) is the factor you set. The dependent variable (DV) is what you measure (N, biomass, richness, O₂).",
            "A control is the baseline without the treatment (or with a sham). Without it, you have a story, not a contrast. Cage-controls, solvent-controls, and unfertilized plots exist because every method has side effects.",
            "Constants (controlled variables) are everything else you keep the same: species, starting N, light, water, season. If two things change, you have a confound and cannot name the cause.",
            "Replication means many independent plots, tanks, or individuals per treatment. n=1 cannot tell difference from luck. Randomize which plot gets which treatment so location is not confounded with IV.",
            "A null hypothesis usually says the IV has no effect. You collect data that could falsify it. Error bars and overlap are a first look; they are not a full t-test, but AP graphs expect cautious reading.",
            "Field experiments trade realism for control. Lab mesocosms reverse that. Match the design to the question: you cannot learn keystone effects in a test tube of one species, and you cannot isolate a hormone in a whole ocean without a gradient or experiment.",
        ],
        "This is AP Science Practice in an ecology costume. The same template graded your enzyme labs in Unit 3 and PCR controls in Unit 6.",
        "Before you write a procedure: IV, DV, control, constants, n, randomize. If any box is empty, the design is not done.",
        lesson_figure(
            (
                '<svg viewBox="0 0 340 140" width="100%" style="max-width:340px" role="img">'
                '<rect x="15" y="30" width="90" height="70" fill="#e2e8f0" stroke="#0f172a"/>'
                '<text x="60" y="70" text-anchor="middle" font-size="11">control</text>'
                '<rect x="125" y="30" width="90" height="70" fill="#bbf7d0" stroke="#166534"/>'
                '<text x="170" y="70" text-anchor="middle" font-size="11">low N</text>'
                '<rect x="235" y="30" width="90" height="70" fill="#86efac" stroke="#166534"/>'
                '<text x="280" y="70" text-anchor="middle" font-size="11">high N</text>'
                '<text x="170" y="125" text-anchor="middle" font-size="12">same light, water, species; n&gt;1 each</text>'
                "</svg>"
            ),
            "Three fertilizer treatments with a true control",
            "Only N dose changes. Everything else is held still. Each box is a set of replicate pots, not one pot.",
        )
        + solved(16, "Claim: ‘sunlight makes plants grow.’ Design the IV, DV, control, and two constants.",
                 ["IV: light level (or hours of light).",
                  "DV: biomass or height after a set time.",
                  "Control: dark or ambient-low light, depending on the claim.",
                  "Constants: water, soil, species, temperature, pot size; replicate many plants per light level."],
                 "IV=light; DV=growth; control=low/no extra light; hold water/soil/species", "", "Easy")
        + solved(17, "Predator-exclusion cages raise mussel cover, but the mesh also cuts flow. What confound is that, and what extra treatment helps?",
                 ["The cage changed two things: no predator AND altered water flow/light.",
                  "A partial cage (roof without sides, or mesh that still allows the predator) tests the artifact.",
                  "If partial cages match open plots, the predator removal, not the mesh climate, caused the mussel boom."],
                 "cage artifact confound; add a cage-control", "", "Medium")
        + solved(18, "Fertilized and control means differ, but 95% error bars overlap a lot and n=3. What do you conclude, and what would you change?",
                 ["You cannot confidently claim a treatment effect; overlap plus tiny n means noise could explain the gap.",
                  "Increase replication, keep the same constants, maybe block by bench.",
                  "Do not drop the control to ‘make the effect look bigger.’ That is not design; that is theater."],
                 "insufficient evidence; raise n, keep controls", "", "Hard"),
        ("Changing two IVs and calling it a controlled experiment",
         "Fertilizer plus extra water plus a sunnier window is three IVs. Either hold two still or use a factorial design that plans the combination. Accidental combination is a confound."),
        ("Fill the six-box template on the FRQ",
         "IV, DV, control, constants, replication, randomization. Graders award those boxes even when the biology story is short. Empty boxes lose easy points."),
        [
            "I can identify IV, DV, control, and constants in an ecology experiment.",
            "I can explain why replication and randomization beat n=1 stories.",
            "I can spot confounds (including cage artifacts) and overlapping error bars.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "NPP, trophic transfer, and nutrient cycling vs energy flow",
            "Exponential vs logistic growth and density dependence",
            "Community interaction signs, keystones, and niches",
            "Richness, evenness, islands, and hotspots",
            "Eutrophication, climate, acidification, and mismatch",
            "IV/DV, controls, replication, and confounds",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Chemistry of Life', ['Water and hydrogen bonding', 'Elements of life and CHNOPS', 'Carbohydrates and lipids', 'Proteins and nucleic acids', 'Structure meets function', 'pH and buffers']), ('Cell Structure and Function', ['Prokaryote vs eukaryote', 'Organelles and compartmentalization', 'Membrane structure', 'Passive transport', 'Active transport', 'Tonicity and water potential']), ('Cellular Energetics', ['Enzyme structure and specificity', 'Environmental effects on enzymes', 'Cellular respiration', 'Photosynthesis', 'Fitness and energy strategies', 'Coupled reactions and ATP']), ('Cell Communication and Cell Cycle', ['Signal transduction', 'Feedback and cell response', 'Mitosis', 'Cell cycle regulation', 'Meiosis', 'Nondisjunction and variation']), ('Heredity', ['Mendelian genetics', 'Probability and Punnett', 'Linked genes and recombination', 'Pedigrees', 'Chromosomal inheritance', 'Environmental effects on phenotype']), ('Gene Expression and Regulation', ['DNA replication', 'Transcription and RNA processing', 'Translation', 'Gene regulation in prokaryotes', 'Eukaryotic regulation', 'Biotechnology tools']), ('Natural Selection', ['Darwin and evidence', 'Hardy-Weinberg', 'Speciation', 'Phylogeny and cladograms', 'Extinction and diversity', 'Origins of life']), ('Ecology', ['Energy flow and trophic levels', 'Population growth', 'Community interactions', 'Biodiversity', 'Disruptions and climate', 'Experimental design in ecology'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>AP Biology Complete</h1>"
        f"<p><strong>For:</strong> <strong>AP Biology</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )



