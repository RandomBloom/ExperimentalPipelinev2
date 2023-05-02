from constants import SECONDS_PER_DAY, MICROMOL_PER_MOL, LITRES_PER_M3, ELECTRONS_PER_OXYGEN


def olc_to_flc(olc_slopes, olc_chl_a, flc_chl_a):
    """

    Args:
        olc_slopes (np.array): array of O2 production rates in mumol L-1 s-1
        olc_chl_a (float): Chl a levels for OLC measurement in mug L-1
        flc_chl_a (float): Chl a levels for FLC measurement in mug L-1
    """

    ratio = flc_chl_a/olc_chl_a
    new_rates = ratio * ELECTRONS_PER_OXYGEN * olc_slopes * SECONDS_PER_DAY * LITRES_PER_M3/MICROMOL_PER_MOL # mol electrons m-3 d-1


def flc_to_JVPII(Fqm_p, E, Fm, Fo, Ka):
    """
    Args:
        Fqm_p (np.array): efficiency (Fq'/Fm')
        E (np.array): light levels (PFD)
        Fm (float): maximal fluorescence
        Fo (float): baseline fluorescence
        Ka

    """
    aLHII = (Fm * Fo)/(Fm - Fo) * Ka * 10**(-6)
    rP_to_JVPII = aLHII * 60 * 60 * 24 * 10**(-6)
    jvpii = Fqm_p * E * rP_to_JVPII
    return jvpii
