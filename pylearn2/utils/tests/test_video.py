"""Tests for pylearn2.utils.video"""
import numpy
from pylearn2.utils.video import FrameLookup, spatiotemporal_cubes


__author__ = "David Warde-Farley"
__copyright__ = "Copyright 2011, David Warde-Farley / Universite de Montreal"
__license__ = "BSD"
__maintainer__ = "David Warde-Farley"
__email__ = "wardefar@iro"


# TODO: write a test for get_video_dims, raising SkipTest
# if pyffmpeg can't be imported


def test_frame_lookup():
    input_data = [('foo', 15), ('bar', 19), ('baz', 26)]
    lookup = FrameLookup(input_data)
    assert len(lookup) == (15 + 19 + 26)
    assert lookup[15] == ('bar', 19, 0)
    assert lookup[14] == ('foo', 15, 14)
    assert lookup[15 + 19 + 4] == ('baz', 26, 4)


def test_spatiotemporal_cubes():
    def check_patch_coverage(files):
        rng = numpy.random.RandomState(1)  # left unchanged since is an argument
        inputs = [(fname, array.shape) for fname, array in files.iteritems()]
        shape = (5, 7, 7)
        for fname, index in spatiotemporal_cubes(inputs, shape, 50000, rng):
            cube = files[fname][index]
            if len(files[fname].shape) == 3:
                assert cube.shape == shape
            else:
                assert cube.shape[:3] == shape[:3]
            cube[...] = True
        for fname, array in files.iteritems():
            assert array.all()

    files = {
        'file1': numpy.zeros((10, 30, 21), dtype=bool),
        'file2': numpy.zeros((15, 25, 28), dtype=bool),
        'file3': numpy.zeros((7, 18, 22), dtype=bool),
    }
    check_patch_coverage(files)

    # Check that stuff still works with an extra color channel dimension.
    files = {
        'file1': numpy.zeros((10, 30, 21, 3), dtype=bool),
        'file2': numpy.zeros((15, 25, 28, 3), dtype=bool),
        'file3': numpy.zeros((7, 18, 22, 3), dtype=bool),
    }
    check_patch_coverage(files)
