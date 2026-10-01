# engine.py

from encoding import encode_state
from rotation import R1_normalize, R2_align, R3_response
from projection import project_role
from intensity import map_intensities

def run_rpo(raw, agency_view, subject_view, rho, memory):
    # 1. R1
    normalized = R1_normalize(raw)

    # 2. R2
    aligned = R2_align(agency_view, subject_view)

    # 3. R3
    response_exponents = R3_response(aligned)

    # 4. Projection
    projected = project_role(response_exponents, rho)

    # 5. Intensities
    intensities = map_intensities(projected)

    # 6. Memory update
    sigma = encode_state(normalized)
    memory.update(sigma, projected)

    return intensities, memory
