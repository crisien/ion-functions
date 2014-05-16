#!/usr/bin/env python
"""
@package ion_functions.data.fdc_functions
@file ion_functions/data/fdc_functions.py
@author Craig Risien and Russell Desiderio
@brief Module containing FDC related data-calculations.
"""

import numpy as np


def fdc_fdchp_grv(lat):
    """
    Description:

        Calculates gravity (acceleration due to earth's gravitational field)
        as a function of latitude. This code is straight from the FDCHP DPS.

    Implemented by:

        2014-05-15: Russell Desiderio. Initial Code

    Usage:

        g = fdc_fdchp_grv(lat)

            where

        g = acceleration due to earth's gravitational field [m/s/s]
        lat = latitude of instrument in decimal degrees.

    References:

        OOI (2014). Data Product Specification for FDCHP Data Products. Document
            Control Number 1341-00280. https://alfresco.oceanobservatories.org/
            (See: Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00280_Data_Product_Spec_FDCHP_OOI.pdf)
    """
    # constants from the DPS
    gamma = 9.7803267715     # equatorial value for 'g'
    c1 = 0.0052790414
    c2 = 0.0000232718
    c3 = 0.0000001262
    c4 = 0.0000000007

    x = np.sin(np.radians(lat))
    xsq = x * x

    g = gamma * (1.0 + xsq * (c1 + xsq * (c2 + xsq * (c3 + xsq * c4))))
    return g


def fdc_fdchp_update(ang_rates, angles, n_rec):
    """
    Description:

        This function is drevied from the EDDYCORR toolbox.
        It computes the angular update matrix as described in
        Edson et al. (1998) and Thwaites (1995) page 50.

    Implemented by:

        2014-05-15: Craig Risien. Initial Code

    Usage:

        values = fdc_fdchp_update(ang_rates, angles, n_rec)

            where

        values = output matrix of values
        ang_rates = (3xN) array of angular rates.
        angles = (3xN) array of Euler angles phi,theta,psi.
        n_rec = number of records. If the FDCHP is sampling at
                10Hz for 20 min, n_rec should equal 12000.

    References:

        OOI (2014). Data Product Specification for FDCHP Data Products. Document
            Control Number 1341-00280. https://alfresco.oceanobservatories.org/
            (See: Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00280_Data_Product_Spec_FDCHP_OOI.pdf)
    """

    p = ang_rates[0, 0:n_rec]
    t = ang_rates[1, 0:n_rec]
    ps = ang_rates[2, 0:n_rec]

    up = angles[0, 0:n_rec]
    vp = angles[1, 0:n_rec]
    wp = angles[2, 0:n_rec]

    u = up + vp * np.sin(p) * np.tan(t) + wp * np.cos(p) * np.tan(t)
    v = 0 + vp * np.cos(p) - wp * np.sin(p)
    w = 0 + vp * np.sin(p) / np.cos(t) + wp * np.cos(p) / np.cos(t)

    values = np.vstack((u, v, w))
    return values


def fdc_fdchp_trans(ang_rates, angles, n_rec, iflag=True):
    """
    Description:

        ?

    Implemented by:

        2014-05-15: Craig Risien. Initial Code

    Usage:

        values = fdc_fdchp_trans(ang_rates, angles, n_rec, iflag=True)

            where

        values = output matrix of values
        ang_rates = (3xN) array of angular rates.
        angles = (3xN) array of Euler angles phi,theta,psi.
        iflag = True
        n_rec = number of records. If the FDCHP is sampling at
                10Hz for 20 min, n_rec should equal 12000.

    References:

        OOI (2014). Data Product Specification for FDCHP Data Products. Document
            Control Number 1341-00280. https://alfresco.oceanobservatories.org/
            (See: Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00280_Data_Product_Spec_FDCHP_OOI.pdf)
    """

    p = ang_rates[0, 0:n_rec]
    t = ang_rates[1, 0:n_rec]
    ps = ang_rates[2, 0:n_rec]

    up = angles[0, 0:n_rec]
    vp = angles[1, 0:n_rec]
    wp = angles[2, 0:n_rec]

    if iflag:
        u = (up * np.cos(t) * np.cos(ps) + vp * (np.sin(p) * np.sin(t) *
             np.cos(ps) - np.cos(p) * np.sin(ps)) + wp * (np.cos(p) *
             np.sin(t) * np.cos(ps) + np.sin(p) * np.sin(ps)))
        v = (up * np.cos(t) * np.sin(ps) + vp * (np.sin(p) * np.sin(t) *
             np.sin(ps) + np.cos(p) * np.cos(ps)) + wp * (np.cos(p) *
             np.sin(t) * np.sin(ps) - np.sin(p) * np.cos(ps)))
        w = (up * (-np.sin(t)) + vp * (np.cos(t) * np.sin(p)) + wp *
             (np.cos(t) * np.cos(p)))
    else:
        u = (up * np.cos(t) * np.cos(ps) + vp * np.cos(t) * np.sin(ps) -
             wp * np.sin(t))
        v = (up * (np.sin(p) * np.sin(t) * np.cos(ps) - np.cos(p) *
             np.sin(ps)) + vp * (np.sin(p) * np.sin(t) * np.sin(ps) +
             np.cos(p) * np.cos(ps)) + wp * (np.cos(t) * np.sin(p)))
        w = (up * (np.cos(p) * np.sin(t) * np.cos(ps) + np.sin(p) *
             np.sin(ps)) + vp * (np.cos(p) * np.sin(t) * np.sin(ps) -
             np.sin(p) * np.cos(ps)) + wp * (np.cos(t) * np.cos(p)))

    values = np.vstack((u, v, w))
    return values
