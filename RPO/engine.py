from .encoding import encode_state
from .rotation import R1_normalize, R2_align, R3_response
from .projection import project_role
from .intensity import map_intensities
from .memory import PairedMemory

def run_rpo(raw: dict[str, float],
            agency_view: dict[str, float],
            subject_view: dict[str, float],
            rho: float,
            memory: PairedMemory):
    normalized = R1_normalize(raw)
    aligned = R2_align(agency_view, subject_view)
    response_exponents = R3_response(aligned)
    projected = project_role(response_exponents, rho)
    intensities = map_intensities(projected)
    sigma = encode_state(normalized)
    memory.update(sigma, projected)
    return intensities
