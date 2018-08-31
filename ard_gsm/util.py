#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cPickle as pickle
import gzip
import os

import numpy as np


def pickle_dump(path, obj, compress=False):
    if compress:
        with gzip.open(path, 'wb') as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(path, 'wb') as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(path, compressed=False):
    if compressed:
        with gzip.open(path, 'rb') as f:
            return pickle.load(f)
    else:
        with open(path, 'rb') as f:
            return pickle.load(f)


def iter_sub_dirs(root):
    for item in os.listdir(root):
        item = os.path.join(root, item)
        if os.path.isdir(item):
            yield item


def read_xyz_file(path, with_energy=False):
    with open(path) as f:
        contents = [line.strip() for line in f]

    xyzs = []
    i = 0
    while i < len(contents):
        if not contents[i]:  # Empty line
            break
        else:
            natoms = int(contents[i])
            xyz = contents[(i+2):(i+2+natoms)]
            symbols, coords = [], []
            for line in xyz:
                data = line.split()
                symbols.append(data[0])
                coords.append([float(c) for c in data[1:]])
            if with_energy:
                energy = float(contents[i+1])
                xyzs.append((symbols, np.array(coords), energy))
            else:
                xyzs.append((symbols, np.array(coords)))
            i += natoms + 2

    return xyzs


def get_dist_vecs(coords):
    """
    Calculate and return the distance vectors between all combinations
    of points given an array of Cartesian coordinates. The vectors are
    returned as a 3D tensor in which each vector can be accessed as
    d = tensor[:, point_idx1, point_idx2], where d is the vector that
    points from point1 to point2.
    """
    coords = coords.reshape(np.size(coords) // 3, 3)
    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]
    dx = x[..., np.newaxis] - x[np.newaxis, ...]
    dy = y[..., np.newaxis] - y[np.newaxis, ...]
    dz = z[..., np.newaxis] - z[np.newaxis, ...]
    return -np.array([dx, dy, dz])
