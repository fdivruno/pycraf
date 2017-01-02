#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, unicode_literals, division, print_function
    )

from functools import partial, lru_cache
# import numpy as np
import pyproj


__all__ = [
    'utm_to_wgs84', 'wgs84_to_utm', 'utm_to_wgs84_32N',
    'etrs89_to_wgs84', 'wgs84_to_etrs89',
    ]


@lru_cache(maxsize=16, typed=True)
def _create_proj(sys1, sys2, zone=None, south=False):
    '''
    Helper function to create and cache pyproj.Proj instances.
    '''

    if sys1 == 'UTM' and sys2 == 'WGS84':

        _proj_str = (
            '+proj=utm +ellps=WGS84 +datum=WGS84 +units=m +no_defs '
            '+zone={:d}'.format(zone)
            )
        if south:
            _proj_str += '+south'

    elif sys1 == 'ETRS89' and sys2 == 'WGS84':

        _proj_str = (
            '+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 '
            '+ellps=GRS80 +units=m +no_defs'
            )

    return pyproj.Proj(_proj_str)


def utm_to_wgs84(ulon, ulat, zone, south=False):
    '''
    Convert UTM coordinates to GPS/WGS84.

    Parameters
    ----------
    ulon, ulat - UTM longitude and latitude
    zone - UTM zone (e.g., 32 for Effelsberg, with south == False)
    south - set to True if on southern hemisphere

    Returns
    -------
    glon, glat - GPS/WGS84 longitude and latitude

    Notes
    -----
    Uses
        +proj=utm +zone=xx +ellps=WGS84 +datum=WGS84 +units=m +no_defs [+south]
    for pyproj setup.
    '''

    _proj = _create_proj('UTM', 'WGS84', zone, south)

    return _proj(ulon, ulat, inverse=True)


def wgs84_to_utm(glon, glat, zone, south=False):
    '''
    Convert GPS/WGS84 coordinates to UTM.

    Parameters
    ----------
    glon, glat - GPS/WGS84 longitude and latitude
    zone - UTM zone (e.g., 32 for Effelsberg)

    Returns
    -------
    ulon, ulat - UTM longitude and latitude

    Notes
    -----
    Uses
        +proj=utm +zone=xx +ellps=WGS84 +datum=WGS84 +units=m +no_defs [+south]
    for pyproj setup.
    '''

    _proj = _create_proj('UTM', 'WGS84', zone, south)

    return _proj(glon, glat, inverse=False)


# This is for Western Germany (Effelsberg)
utm_to_wgs84_32N = partial(utm_to_wgs84, zone=32, south=False)
wgs84_to_utm_32N = partial(wgs84_to_utm, zone=32, south=False)


def etrs89_to_wgs84(elon, elat):
    '''
    Convert ETSR89 coordinates to GPS/WGS84.

    ETRS89 is the European Terrestrial Reference System.
    (Using a Lambert Equal Area projection.)

    Parameters
    ----------
    elon, elat - ETRS89 longitude and latitude

    Returns
    -------
    glon, glat - GPS/WGS84 longitude and latitude

    Notes
    -----
    Uses
        +proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000
        +ellps=GRS80 +units=m +no_defs
    for pyproj setup.
    '''

    _proj = _create_proj('ETRS89', 'WGS84')

    return _proj(elon, elat, inverse=True)


def wgs84_to_etrs89(glon, glat):
    '''
    Convert GPS/WGS84 coordinates to ETSR89.

    ETRS89 is the European Terrestrial Reference System.
    (Using a Lambert Equal Area projection.)

    Parameters
    ----------
    glon, glat - GPS/WGS84 longitude and latitude

    Returns
    -------
    elon, elat - ETRS89 longitude and latitude

    Notes
    -----
    Uses
        +proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000
        +ellps=GRS80 +units=m +no_defs
    for pyproj setup.
    '''

    _proj = _create_proj('ETRS89', 'WGS84')

    return _proj(glon, glat, inverse=False)


if __name__ == '__main__':
    print('This not a standalone python program! Use as module.')