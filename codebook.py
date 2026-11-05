"""Versioned, human-authorized definitions; never classify records at runtime."""
from configuration import ROOT

CODEBOOK_VERSION = '1.1'
CODEBOOK_PATH = ROOT / 'data/prepared/mechanism-codebook.md'
MECHANISMS = ['Repair/moving', 'Entering/exiting', 'Belt contact', 'Struck by equipment', 'Fall', 'Non-use equipment/cord-related falls', 'Unknown/Unclassified']
APPROVED_TEXT = 'Version: 1.1\n\n| injury_mechanism | definition | overlap_rule |\n|---|---|---|\n| `Repair/moving` | Injury while lifting, folding, assembling, cleaning, or servicing an unmounted treadmill. | Takes precedence over `Struck by equipment` or `Fall` if the patient was not using the treadmill for exercise. |\n| `Entering/exiting` | Slip, trip, or loss of balance while mounting, stepping onto, or stepping off the treadmill. | Takes precedence over general `Fall` when the narrative specifies getting on or off. |\n| `Belt contact` | Friction burn, pinch, entrapment, or direct pull from the moving belt (or belt sudden stop/surge) as the initiating event. | Takes precedence over `Fall` when belt contact/slip initiated the fall; if a general fall merely lands on the belt, code as `Fall`. |\n| `Struck by equipment` | Hit by a falling, folding, or tipping treadmill frame/console, or thrown into part of the machine without a preceding fall. | Excludes impacts that occur solely as the landing of a `Fall` or during `Repair/moving`. |\n| `Fall` | Loss of balance, trip, dizziness, or fall on/from the treadmill while using it for exercise or as a supporting surface, without a more specific initiating mechanism above. Surface use includes standing/being on an unpowered treadmill; motor operation is not required. | Keep falls on/from a supporting treadmill surface here even when power state is unstated. Excludes an explicitly non-use trip over equipment/cord or landing against equipment. Mounting/dismounting, moving/servicing and initiating moving-belt events retain precedence. |\n| `Non-use equipment/cord-related falls` | A physical injury from a trip over treadmill equipment or its attached cord, or a fall into/against the equipment, when the narrative establishes activity outside treadmill exercise, supporting-surface use, mounting/dismounting, or moving/servicing. | Includes an unrelated initiating trip followed by injury-producing treadmill contact; do not attribute the initiating hazard to the treadmill. A preceding fall excludes Struck by equipment. Do not infer non-use, power state, or cord initiation merely because the narrative omits them. If use context needed to distinguish categories is genuinely unresolved, hold the mapping for review. |\n| `Unknown/Unclassified` | Reviewed treadmill-involved visit where the narrative lacks sufficient detail to determine how the injury occurred. | Reserved for reviewed unclear narratives; never used to bypass unfinished candidate review. |\n'


def approved_text():
    return APPROVED_TEXT


def read_codebook(path=CODEBOOK_PATH):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('Version: ' + CODEBOOK_VERSION + '\n'):
        raise ValueError('Expected approved mechanism codebook version ' + CODEBOOK_VERSION)
    if text != APPROVED_TEXT:
        raise ValueError('Codebook definitions differ from the approved version ' + CODEBOOK_VERSION)
    return text
