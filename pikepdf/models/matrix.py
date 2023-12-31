# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""PDF content matrix support."""

from __future__ import annotations

from math import cos, pi, sin


class PdfMatrix:
    """Support class for PDF content stream matrices.

    PDF content stream matrices are 3x3 matrices summarized by a shorthand
    ``(a, b, c, d, e, f)`` which correspond to the first two column vectors.
    The final column vector is always ``(0, 0, 1)`` since this is using
    `homogenous coordinates <https://en.wikipedia.org/wiki/Homogeneous_coordinates>`_.

    PDF uses row vectors.  That is, ``vr @ A'`` gives the effect of transforming
    a row vector ``vr=(x, y, 1)`` by the matrix ``A'``.  Most textbook
    treatments use ``A @ vc`` where the column vector ``vc=(x, y, 1)'``.

    (``@`` is the Python matrix multiplication operator.)

    Addition and other operations are not implemented because they're not that
    meaningful in a PDF context (they can be defined and are mathematically
    meaningful in general).

    PdfMatrix objects are immutable. All transformations on them produce a new
    matrix.
    """

    def __init__(self, *args):
        """Initialize a PdfMatrix."""
        # fmt: off
        if not args:
            self.values = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        elif len(args) == 6:
            a, b, c, d, e, f = map(float, args)
            self.values = ((a, b, 0),
                           (c, d, 0),
                           (e, f, 1))
        elif isinstance(args[0], PdfMatrix):
            self.values = args[0].values
        elif len(args[0]) == 6:
            a, b, c, d, e, f = map(float, args[0])
            self.values = ((a, b, 0),
                           (c, d, 0),
                           (e, f, 1))
        elif len(args[0]) == 3 and len(args[0][0]) == 3:
            self.values = (tuple(args[0][0]),
                           tuple(args[0][1]),
                           tuple(args[0][2]))
        else:
            raise ValueError('invalid arguments: ' + repr(args))
        # fmt: on

    @staticmethod
    def identity():
        """Return an identity matrix."""
        return PdfMatrix()

    def __matmul__(self, other):
        """Multiply this matrix by another matrix.

        Can be used to concatenate transformations.
        """
        a = self.values
        b = other.values
        return PdfMatrix(
            [
                [sum(float(i) * float(j) for i, j in zip(row, col)) for col in zip(*b)]
                for row in a
            ]
        )

    def scaled(self, x, y):
        """Concatenate a scaling matrix to this matrix."""
        return self @ PdfMatrix((x, 0, 0, y, 0, 0))

    def rotated(self, angle_degrees_ccw):
        """Concatenate a rotation matrix to this matrix."""
        angle = angle_degrees_ccw / 180.0 * pi
        c, s = cos(angle), sin(angle)
        return self @ PdfMatrix((c, s, -s, c, 0, 0))

    def translated(self, x, y):
        """Translate this matrix."""
        return self @ PdfMatrix((1, 0, 0, 1, x, y))

    @property
    def shorthand(self):
        """Return the 6-tuple (a,b,c,d,e,f) that describes this matrix."""
        return (self.a, self.b, self.c, self.d, self.e, self.f)

    @property
    def a(self):
        """Return matrix this value."""
        return self.values[0][0]

    @property
    def b(self):
        """Return matrix this value."""
        return self.values[0][1]

    @property
    def c(self):
        """Return matrix this value."""
        return self.values[1][0]

    @property
    def d(self):
        """Return matrix this value."""
        return self.values[1][1]

    @property
    def e(self):
        """Return matrix this value.

        Typically corresponds to translation on the x-axis.
        """
        return self.values[2][0]

    @property
    def f(self):
        """Return matrix this value.

        Typically corresponds to translation on the y-axis.
        """
        return self.values[2][1]

    def __eq__(self, other):
        if isinstance(other, PdfMatrix):
            return self.shorthand == other.shorthand
        return False

    def encode(self):
        """Encode this matrix in binary suitable for including in a PDF."""
        return '{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}'.format(
            self.a, self.b, self.c, self.d, self.e, self.f
        ).encode()

    def __repr__(self):
        return f"pikepdf.PdfMatrix({repr(self.values)})"
