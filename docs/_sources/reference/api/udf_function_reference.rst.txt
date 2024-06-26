.. _udf_function_reference:

User Defined Functions (UDF)
============================

.. function:: X + Y

  Returns the sum of layers X and Y.

.. function:: X - Y

  Returns the difference between layers X and Y.

.. function:: X * Y

  Returns the product of layers X and Y.

.. function:: X / Y

  Returns the quotient of layers X and Y.

.. function:: X ? Y : Z

  This is a pixel-wise if-then-else construction. For each pixel, the value is Y if X is true, otherwise Z.

.. function:: math:abs(X)

  Returns the absolute value of layer X.

.. function:: math:acos(X)

  Calculates the inverse cosine (arc cosine) over layer X. The returned angle is in the range :math:`[0, \pi]`.

.. function math:addExact(X, Y)

.. function:: math:asin(X)

  Inverse sine (arc sine) function. The return value is in the range :math:`[-\pi/2, \pi/2]`.

.. function:: math:atan(X)

  Inverse tangent (arc tan) function. The return value is in the range :math:`[-\pi/2, \pi/2]`.

.. function:: math:atan2(X, Y)

.. function:: math:cbrt(X)

  Returns the cube root of X.

.. function:: math:ceil(X)

  Rounds each pixel up to the nearest larger integer.

.. function:: math:copySign(X, Y)

.. function:: math:cos(X)

  Cosine of X.

.. function:: math:cosh(X)

  Hyperbolic cosine of X.

.. function:: math:decrementExact(X)

.. function:: math:exp(X)

  Exponential function.

.. function:: math:expm1(X)

  Returns :math:`e^X - 1`.

.. function:: math:floorDiv(X, Y)

.. function:: math:floorMod(X, Y)

.. function:: math:getExponent(X)

.. function:: math:hypot(X, Y)

  Calculates :math:`\sqrt{X^2 + Y^2}`.

The complete list is based on `java.lang.Math <https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html>`_.
