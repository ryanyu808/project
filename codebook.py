"""Versioned, human-authorized definitions; never classify records at runtime."""
from configuration import ROOT

CODEBOOK_VERSION = '1.2'
CODEBOOK_PATH = ROOT / 'data/prepared/mechanism-codebook.md'
MECHANISMS = ['Repair/moving', 'Entering/exiting', 'Belt contact', 'Struck by equipment', 'Fall', 'Equipment/cord obstacle or landing falls', 'Unknown/Unclassified']
APPROVED_TEXT = 'Version: 1.2\n\n| injury_mechanism | definition | overlap_rule |\n|---|---|---|\n| `Repair/moving` | Injury while lifting, folding, assembling, cleaning, or servicing an unmounted treadmill. | Takes precedence over `Struck by equipment` or `Fall` if the patient was not using the treadmill for exercise. |\n| `Entering/exiting` | Slip, trip, or loss of balance while mounting, stepping onto, or stepping off the treadmill. | Takes precedence over general `Fall` when the narrative specifies getting on or off. |\n| `Belt contact` | Friction burn, pinch, entrapment, or direct pull from the moving belt (or belt sudden stop/surge) as the initiating event. | Takes precedence over `Fall` when belt contact/slip initiated the fall; if a general fall merely lands on the belt, code as `Fall`. |\n| `Struck by equipment` | Hit by a falling, folding, or tipping treadmill frame/console, or thrown into part of the machine without a preceding fall. | Excludes impacts that occur solely as the landing of a `Fall` or during `Repair/moving`. |\n| `Fall` | Loss of balance, trip, dizziness, or fall on/from the treadmill while using it for exercise or as a supporting surface, without a more specific initiating mechanism above. Surface use includes standing/being on an unpowered treadmill; motor operation is not required. | Keep falls on/from the supporting treadmill surface here, including during operation and unpowered surface use. If only a fall on/from the treadmill is reported, retain this general category without inferring motor operation. A general fall merely landing on the belt stays Fall. Specific moving/servicing, mounting/dismounting and initiating moving-belt events retain precedence. |\n| `Equipment/cord obstacle or landing falls` | A physical injury from a fall in which treadmill equipment or its attached cord is a documented obstacle or an object encountered on landing, rather than the supporting surface from which the patient falls. Classification describes the equipment relationship; actual exercise use and motor state may be unknown. | Do not infer non-use, motor operation, exercise activity, cord initiation, or equipment causation of the initial loss of balance. Includes an external trip followed by injury-producing treadmill contact. Falls during documented operation/on/from a supporting treadmill surface remain Fall unless a more specific initiating mechanism applies. A preceding fall excludes Struck by equipment; handling and mounting rules retain precedence. |\n| `Unknown/Unclassified` | Reviewed treadmill-involved visit where the narrative lacks sufficient detail to determine how the injury occurred. | Reserved for reviewed unclear narratives; never used to bypass unfinished candidate review. |\n'


def approved_text():
    return APPROVED_TEXT


def read_codebook(path=CODEBOOK_PATH):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('Version: ' + CODEBOOK_VERSION + '\n'):
        raise ValueError('Expected approved mechanism codebook version ' + CODEBOOK_VERSION)
    if text != APPROVED_TEXT:
        raise ValueError('Codebook definitions differ from the approved version ' + CODEBOOK_VERSION)
    return text
