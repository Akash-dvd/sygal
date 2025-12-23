# Required for tests
# import sys
# sys.path.append('/app/solver')

from Sygal.initial import *



# Test cases for substitution
test_cases_subs = [
  # (expression, substitution_pair, expected_result)
  # Format: ((expr, (old, new)), result)
  ((((a1<(a2^a3))^(b1<(b2^b3)))^(a1<(b1^b2^a3))^a3, (a1<(b1^b2^a3), b1)), ((a1<(a2^a3))^a3^(b1<(b2^b3)))^b1),
]

def test_subs():
  """Test substitution in GExpr."""
  # Substitution is a method call, not a transformation function
  # So we'll test it directly
  temp1 = ((a1<(a2^a3))^(b1<(b2^b3)))^(a1<(b1^b2^a3))^a3
  ts1 = a1<(b1^b2^a3)
  ts2 = b1
  temp11 = temp1.subs((ts1,ts2))
  expected = ((a1<(a2^a3))^a3^(b1<(b2^b3)))^b1
  assert temp11 == expected